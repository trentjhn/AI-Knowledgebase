---
name: http-client-hygiene
description: Checklist for writing HTTP client code that queries authenticated APIs — prevents API keys from leaking through exception messages, logs, and traceback output paths. Invoke whenever you write or modify code that calls `requests.get/post` against a third-party API, especially one that accepts the key as a URL query parameter.
origin: parking-lead-gen-agent incident (2026-04-18) — Google Places and Hunter.io keys were leaking through `requests.HTTPError.__str__()` because requests embeds the full URL (with `?key=...`) in the exception message.
---

# HTTP Client Secret Hygiene

The single most reliable way to leak an API key is to catch an exception from `requests` and log it verbatim. The key shows up in three places you don't expect: the exception's `__str__()`, the `__cause__` chain, and the uncaught-exception traceback printer. This skill is a checklist that closes all three paths.

## When to Activate

- Writing new code that calls a third-party API with `requests.get` / `requests.post`
- The API accepts credentials as a URL query parameter (Hunter, Google Maps/Places, SendGrid v2, many legacy REST APIs)
- Adding error-handling / retry logic around an existing HTTP client
- Reviewing a PR that touches `except requests.*` or logs HTTP failures
- Before shipping any project that makes authenticated HTTP calls

## The Threat Model in One Paragraph

`requests` stores the full request URL on every exception it raises. `raise_for_status()` formats the default `HTTPError` message as `"404 Client Error: Not Found for url: https://api.example.com/v1/endpoint?api_key=sk-REAL-KEY"`. `ConnectionError` and `Timeout` both stringify with the URL embedded in a `urllib3` message. When your code does `except requests.HTTPError as e: logger.warning(f"... {e}")` or lets the exception propagate unhandled, that formatted string — key and all — lands in your logs, your crash reports, your stderr, and anywhere else Python's default traceback printer reaches. Query-parameter auth is the bug magnifier: header auth (`Authorization: Bearer ...`) doesn't round-trip through exception stringification the same way.

## The Four-Point Checklist

Run through this for **every** HTTP client call that touches a secret. If your answer to any question is "I don't know," assume the worst and add the defense.

### 1. Never interpolate the exception object into a log message

```python
# WRONG — `{e}` calls str(e) which includes the full URL with ?api_key=...
except requests.ConnectionError as e:
    logger.warning(f"Hunter connection error for {domain}: {e}")

# RIGHT — log only the exception class name, and only the sanitized context
# you explicitly collected. Never `{e}` or `repr(e)` on a requests exception.
except requests.ConnectionError:
    logger.warning(f"Hunter connection error for {domain}")
except Exception as e:
    logger.warning(
        f"Hunter request failed for {domain} ({type(e).__name__})"
    )
```

This is the most common leak and the easiest fix. Audit every `except requests.*` block in your codebase. Any `{e}`, `{err}`, `{exc}`, `repr(e)`, or `str(e)` inside a log message is a potential leak.

### 2. Re-raise `HTTPError` with a scrubbed message, and use `from None`

When you need the exception to propagate (e.g., the API returned 401 and you want the run to halt), do NOT let `requests`' default message escape. Build a new `HTTPError` with a sanitized message and use `raise ... from None` to suppress `__cause__`.

```python
# WRONG — `raise_for_status()` propagates the stock message including the URL.
# Even `except requests.HTTPError: raise` keeps `__cause__`, which Python's
# traceback printer walks and prints str(cause) for — leaking the URL.
r.raise_for_status()

# RIGHT — catch, inspect status, re-raise scrubbed, suppress cause.
try:
    r.raise_for_status()
except requests.HTTPError as e:
    status = getattr(getattr(e, "response", None), "status_code", None)
    if status == 401:
        raise requests.HTTPError(
            f"Hunter 401 Unauthorized for {domain}"
        ) from None  # `from None` suppresses __cause__ printing
    if status in (429, 402):
        raise HunterExhausted(f"Hunter returned {status}") from None
    # Other statuses: log sanitized and return a soft failure.
    logger.warning(f"Hunter HTTP {status} for {domain}")
    return None
```

**Why `from None`, not `from e`:** `from e` preserves the cause chain for debugging, but Python's default uncaught-exception handler walks `__cause__` and prints `str(cause)` — which includes the leaky URL. In production, `from None` is the correct default unless you have a separate mechanism to scrub cause output.

### 3. Prefer header auth over query-param auth when the API supports it

```python
# Query-param auth — the key lives in the URL and leaks through every
# exception stringification path.
requests.get(
    "https://api.hunter.io/v2/domain-search",
    params={"domain": domain, "api_key": key},  # leaky
)

# Header auth — the key is in r.headers, not the URL, and won't appear in
# urllib3's `Max retries exceeded with url: ...` format string.
requests.get(
    "https://api.example.com/v1/endpoint",
    params={"domain": domain},
    headers={"Authorization": f"Bearer {key}"},  # safe
)
```

Not all APIs support header auth — Hunter.io, Google Maps legacy endpoints, and many small SaaS APIs still require the key as `?api_key=` or `?key=`. When you have a choice, choose headers. When you don't, tighten defenses #1 and #2.

### 4. Write a regression test that asserts the secret does not appear

A test that mocks a leaky exception and asserts the secret is absent from both the log capture and the raised exception's `str()` is the only way to prove the defense still works after a refactor. This test is cheap to write and catches the single most likely regression.

```python
def test_hunter_connection_error_does_not_leak_api_key(caplog):
    """ConnectionError str includes the full URL with `api_key=...`.
    The warning log must not echo it verbatim — key must not hit disk."""
    secret_key = "HUNTER_SECRET_abc123_DO_NOT_LEAK"
    leaky_exc = requests.ConnectionError(
        "HTTPSConnectionPool(host='api.hunter.io', port=443): "
        "Max retries exceeded with url: "
        f"/v2/domain-search?domain=biz.com&api_key={secret_key} "
        "(Caused by NameResolutionError(...))"
    )
    with patch("src.enricher.requests.get", side_effect=leaky_exc):
        with caplog.at_level("WARNING", logger="src.enricher"):
            lookup_email_hunter("biz.com", hunter_api_key=secret_key)
    full_log = "\n".join(r.message for r in caplog.records)
    assert secret_key not in full_log

def test_hunter_401_raises_sanitized_httperror_without_url():
    """The raised HTTPError must not include the query-param key, and must
    have __cause__ == None so the traceback printer has nothing to walk."""
    secret_key = "HUNTER_SECRET_key_401_path"
    fake_resp = MagicMock()
    fake_resp.status_code = 401
    fake_resp.raise_for_status.side_effect = requests.HTTPError(
        "401 Client Error: Unauthorized for url: "
        f"https://api.hunter.io/v2/domain-search?domain=biz.com&api_key={secret_key}",
        response=fake_resp,
    )
    with patch("src.enricher.requests.get", return_value=fake_resp):
        with pytest.raises(requests.HTTPError) as excinfo:
            lookup_email_hunter("biz.com", hunter_api_key=secret_key)
    assert secret_key not in str(excinfo.value)
    assert excinfo.value.__cause__ is None
```

## Canonical Safe HTTP Client Skeleton

```python
import logging
import requests

logger = logging.getLogger(__name__)


class ExternalAPIError(Exception):
    """Caller-visible failure from the external API. Never carries the URL."""


def call_authenticated_api(domain: str, api_key: str) -> dict | None:
    if not api_key or not domain:
        return None
    try:
        r = requests.get(
            "https://api.example.com/v1/endpoint",
            params={"domain": domain, "api_key": api_key},
            timeout=10,
        )
        r.raise_for_status()
    except requests.HTTPError as e:
        # Inspect response status without stringifying the exception.
        resp = getattr(e, "response", None)
        status = getattr(resp, "status_code", None)
        if status == 401:
            raise ExternalAPIError(
                f"API 401 Unauthorized for {domain}"
            ) from None
        if status in (429, 402):
            logger.warning(
                f"API {status} for {domain}: back off or disable for this run"
            )
            raise ExternalAPIError(f"API {status} for {domain}") from None
        logger.warning(f"API HTTP {status} for {domain}")
        return None
    except requests.Timeout:
        logger.warning(f"API timeout for {domain}")
        return None
    except requests.ConnectionError:
        # DO NOT include {e}: ConnectionError.__str__() embeds the URL
        # including ?api_key=<real key> — leaks the secret to logs.
        logger.warning(f"API connection error for {domain}")
        return None
    except Exception as e:
        # Exotic requests exceptions (InvalidURL, TooManyRedirects) also
        # stringify with the URL+query. Log only the exception class.
        logger.warning(
            f"API request failed for {domain} ({type(e).__name__})"
        )
        return None
    try:
        return r.json()
    except ValueError as e:
        logger.warning(f"API response parse failed for {domain} ({type(e).__name__})")
        return None
```

## Audit an Existing Codebase

```bash
# Any `{e}` or `{err}` inside an except block that catches a requests exception:
grep -rn --include="*.py" -E "except requests\..*:" .
grep -rn --include="*.py" -E "\{(e|err|exc|exception)\}" .

# Any `from e` inside a requests-related except block — candidate for `from None`:
grep -rn --include="*.py" -E "raise .* from e$" .

# Bare raise_for_status() not wrapped in a try — the stock message escapes:
grep -rn --include="*.py" "raise_for_status" .

# Query-param auth patterns — candidates for header-auth migration:
grep -rn --include="*.py" -E "params=.*(api_key|api-key|apikey|access_token|key)" .
```

Any hit on lines 1-3 above needs review against the checklist.

## Why This Is a Skill, Not Just a Rule

A one-line rule ("don't log exception objects from requests") is necessary but insufficient. The failure mode has four escape hatches (`{e}`, `from e`, `raise_for_status()`, bare `raise`), two library-level root causes (the URL is in the exception because `requests` puts it there, and Python walks `__cause__` by default), and one runtime path most engineers don't think about (the uncaught-exception traceback printer). You need the checklist, the scrubbed skeleton, the regression test pattern, and the audit commands to close all of them. Invoking this skill pulls all four into context at once.

## Related

- `LEARNING/PRODUCTION/ai-security/ai-security.md` — "HTTP Client Secret Hygiene" section (same content, reference depth)
- OWASP LLM Top 10 — LLM02 (Sensitive Information Disclosure) covers the broader class
- CLAUDE.md rule "API keys in `.env` only" — this skill is the enforcement mechanism for that rule

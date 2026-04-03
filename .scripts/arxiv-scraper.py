#!/usr/bin/env python3
"""
ArXiv Weekly Digest Generator for AI Knowledge Base

Queries ArXiv API for papers from the past week, uses Claude to score
relevance to KB topics (Prompt Engineering, Context Engineering, Reasoning LLMs,
Agentic Engineering, Skills, Evaluation, Fine-tuning, AI Security, Alignment & Safety),
and outputs a ranked digest markdown file.
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict
import os
import sys
import time
import re
import anthropic

# Consolidated ArXiv query mapping
TOPIC_QUERIES = {
    "Prompt Engineering": [
        '("prompt engineering" OR "in-context learning" OR "few-shot learning")',
    ],
    "Context Engineering": [
        '("retrieval augmented generation" OR "RAG" OR "context window")',
    ],
    "Reasoning LLMs": [
        '("chain of thought" OR "reasoning")',
    ],
    "Agentic Engineering": [
        '("agent" OR "tool use" OR "multi-agent") AND ("language model" OR "LLM")',
    ],
    "Skills": [
        '("instruction tuning" OR "task-specific")',
    ],
    "Evaluation": [
        '("evaluation" OR "benchmark") AND ("language model" OR "LLM")',
    ],
    "Fine-tuning": [
        '("fine-tuning" OR "LoRA" OR "RLHF" OR "DPO" OR "preference learning")',
    ],
    "AI Security": [
        '("adversarial" OR "jailbreak" OR "robustness") AND ("language model" OR "LLM")',
    ],
    "Alignment & Safety": [
        '("alignment" OR "safety" OR "value alignment")',
    ],
}

ARXIV_CATEGORIES = "(cat:cs.AI OR cat:cs.CL OR cat:stat.ML)"
ARXIV_API = "http://export.arxiv.org/api/query?"


def get_date_range() -> tuple:
    """Get past 7 days for ArXiv query."""
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    from_date = week_ago.strftime("%Y%m%d0000")
    to_date = today.strftime("%Y%m%d2359")
    return from_date, to_date, today


def build_query(topic_query: str, from_date: str, to_date: str) -> str:
    """Build a full ArXiv query with category, date range, and topic filters."""
    return f'{ARXIV_CATEGORIES} AND submittedDate:[{from_date} TO {to_date}] AND ({topic_query})'


def fetch_papers(query: str, max_results: int = 5) -> list:
    """Fetch papers from ArXiv API with rate limit handling."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(ARXIV_API, params=params, timeout=15)
            response.raise_for_status()
            return parse_arxiv_response(response.text)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = (2 ** attempt) * 5
                print(f"  Rate limited. Waiting {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                return []
        except requests.RequestException:
            return []

    return []


def parse_arxiv_response(xml_response: str) -> list:
    """Parse ArXiv API XML response."""
    papers = []
    entry_pattern = r'<entry>(.*?)</entry>'
    entries = re.findall(entry_pattern, xml_response, re.DOTALL)

    for entry in entries:
        try:
            id_match = re.search(r'<id>http://arxiv\.org/abs/([\d.v]+)</id>', entry)
            title_match = re.search(r'<title>(.*?)</title>', entry)
            summary_match = re.search(r'<summary>(.*?)</summary>', entry)
            updated_match = re.search(r'<updated>([\d-]+)', entry)

            if not (id_match and title_match and summary_match):
                continue

            arxiv_id = id_match.group(1)
            title = title_match.group(1).strip()
            summary = summary_match.group(1).strip().replace('\n', ' ')
            published = updated_match.group(1) if updated_match else ""

            papers.append({
                "id": arxiv_id,
                "title": title,
                "summary": summary[:300],
                "published": published,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
            })
        except Exception:
            pass

    return papers


def score_papers_with_claude(papers_dict: dict) -> dict:
    """Score paper relevance to KB topics using Claude API.

    Returns dict mapping paper_id -> (score: float 0-1, matching_topics: list)
    Note: normalizes IDs by stripping version numbers (v1, v2, etc.)
    """
    if not papers_dict:
        return {}

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Build prompt with papers (use base ID without version for consistency with Claude output)
    paper_list = "\n\n".join([
        f"Paper {i+1}: {pid.split('v')[0]}\nTitle: {paper['title']}\nAbstract: {paper['summary']}"
        for i, (pid, paper) in enumerate(papers_dict.items())
    ])

    prompt = f"""You are evaluating ArXiv papers for a distilled, practitioner-depth AI Knowledge Base. The KB is NOT comprehensive—it synthesizes and distills. High-signal papers are those that would directly inform KB content updates or reveal gaps.

The KB covers these 9 topics:
1. Prompt Engineering - prompting techniques, few-shot learning, output control
2. Context Engineering - RAG, context windows, context management patterns
3. Reasoning LLMs - chain of thought, planning, reasoning systems
4. Agentic Engineering - agents, tool use, multi-agent systems, orchestration
5. Skills - instruction tuning, task-specific specialization
6. Evaluation - benchmarking, evaluation methodology, metrics
7. Fine-tuning - LoRA, RLHF, DPO, preference learning
8. AI Security - adversarial robustness, jailbreaks, safety
9. Alignment & Safety - alignment, safety, constitutional AI

SCORING CRITERIA (0.0-1.0):

Score 0.8+ if the paper:
- Reveals a NEW MECHANISM or PATTERN not yet in the KB (e.g., novel architectural insight, unexpected failure mode, counterintuitive finding)
- DEEPLY explores 1-2 KB topics (not surface coverage of many)
- Explicitly analyzes WHY something works or WHY it breaks (mechanism > "we got +2% accuracy")
- Includes failure modes, anti-patterns, or limitations that practitioners need to know
- Presents a reusable pattern, not a domain-specific application (e.g., "novel RAG filtering" > "medical AI using RAG")
- Is dense enough to distill into KB content (clear concepts, not incremental tweaks)

Score 0.5-0.8 if the paper:
- Is solid engineering work but somewhat derivative (confirms existing patterns, not new)
- Covers practical techniques but shallow across multiple topics
- Lacks explicit failure mode analysis
- Is domain-specific but technique could transfer

Score <0.5 if the paper:
- Is pure theory with limited practical implementation details
- Narrowly domain-specific with low transfer value
- Overlaps heavily with existing KB content without new insight
- Is incremental (small gains, no new understanding)

IMPORTANT: Return ONLY a JSON object with this structure (no markdown, no explanation):
{{
  "2402.12345": {{"score": 0.85, "topics": ["Prompt Engineering", "Reasoning LLMs"]}},
  "2403.54321": {{"score": 0.45, "topics": []}},
  ...
}}

Papers to evaluate:

{paper_list}"""

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse JSON response (strip markdown code fences if present)
        response_text = response.content[0].text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()

        scores = json.loads(response_text)

        return scores
    except json.JSONDecodeError as e:
        print(f"Failed to parse Claude response as JSON: {e}", file=sys.stderr)
        print(f"Response was: {response_text}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Claude API error: {e}", file=sys.stderr)
        return {}


def deduplicate_papers(topics_papers: dict) -> tuple:
    """Deduplicate papers across topics."""
    seen = {}
    topic_map = defaultdict(set)

    for topic, papers in topics_papers.items():
        for paper in papers:
            paper_id = paper["id"]
            if paper_id not in seen:
                seen[paper_id] = paper
            topic_map[paper_id].add(topic)

    return seen, topic_map


def format_digest(papers_dict: dict, topic_map: dict, claude_scores: dict, today: datetime, total_before_filter: int, relevance_threshold: float = 0.7) -> str:
    """Format papers as markdown digest (each paper displayed once, sorted by relevance)."""
    lines = [
        f"# ArXiv Digest — {today.strftime('%B %d, %Y')}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*",
        f"*Date Range: Past 7 days*",
        f"*Filtered by: Claude relevance scoring (threshold {relevance_threshold}+)*",
        "",
    ]

    # Filter papers by relevance threshold (using base ID for lookup in claude_scores)
    filtered_papers = {
        pid: paper for pid, paper in papers_dict.items()
        if claude_scores.get(pid.split('v')[0], {}).get("score", 0) >= relevance_threshold
    }

    if not filtered_papers:
        lines.append(f"No papers above relevance threshold ({relevance_threshold}) found this week.")
        return "\n".join(lines)

    filtered_count = len(filtered_papers)
    lines.append(f"**KB-Relevant Papers: {filtered_count} (filtered from {total_before_filter})**")
    lines.append("")

    # Sort by Claude relevance score (descending)
    papers_sorted = sorted(
        filtered_papers.items(),
        key=lambda item: claude_scores.get(item[0].split('v')[0], {}).get("score", 0),
        reverse=True
    )

    for i, (paper_id, paper) in enumerate(papers_sorted, 1):
        arxiv_topics = ", ".join(sorted(topic_map[paper_id]))
        base_id = paper_id.split('v')[0]
        kb_topics = claude_scores.get(base_id, {}).get("topics", [])
        kb_topics_str = ", ".join(kb_topics) if kb_topics else "General"

        lines.append(f"{i}. **{paper['title']}**")
        lines.append(f"   - **Published:** {paper['published']}")
        lines.append(f"   - **KB Topics:** {kb_topics_str}")
        lines.append(f"   - **Abstract:** {paper['summary']}...")
        lines.append(f"   - **Link:** [{paper['id']}]({paper['url']})")
        lines.append(f"   - **ArXiv Topics:** {arxiv_topics}")
        lines.append("")

    return "\n".join(lines)


def main():
    """Main workflow."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "raw", "arxiv-papers")
    os.makedirs(output_dir, exist_ok=True)

    from_date, to_date, today = get_date_range()
    print(f"Querying ArXiv for papers from {from_date[:8]} to {to_date[:8]}...", file=sys.stderr)

    # Fetch papers
    all_topics_papers = {}
    total_queries = sum(len(queries) for queries in TOPIC_QUERIES.values())
    completed = 0

    for topic, queries in TOPIC_QUERIES.items():
        all_topics_papers[topic] = []
        for query in queries:
            completed += 1
            print(f"  [{completed}/{total_queries}] {topic}...", file=sys.stderr)

            full_query = build_query(query, from_date, to_date)
            papers = fetch_papers(full_query, max_results=20)
            all_topics_papers[topic].extend(papers)

            if completed < total_queries:
                time.sleep(2)

    # Deduplicate
    unique_papers, topic_mapping = deduplicate_papers(all_topics_papers)
    total_before_filter = len(unique_papers)
    print(f"Found {total_before_filter} unique papers. Scoring relevance with Claude...", file=sys.stderr)

    # Score papers with Claude
    claude_scores = score_papers_with_claude(unique_papers)

    if not claude_scores:
        print("Claude scoring failed. Exiting.", file=sys.stderr)
        return None

    print(f"Scored {len(claude_scores)} papers. Generating digest...", file=sys.stderr)

    # Generate digest (threshold 0.8 for high-signal practical engineering patterns)
    digest = format_digest(unique_papers, topic_mapping, claude_scores, today, total_before_filter, relevance_threshold=0.8)

    # Write to file
    filename = f"{today.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(digest)

    print(f"Digest written to {filepath}", file=sys.stderr)

    return filepath


if __name__ == "__main__":
    main()

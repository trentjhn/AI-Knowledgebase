import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

SAMPLE_DIGEST = """# ArXiv Digest — April 17, 2026
*Generated: 2026-04-17 09:24 UTC*

**KB-Relevant Papers: 2 (filtered from 50)**

1. **Think Anywhere in Code Generation**
   - **Published:** 2026-03-31
   - **KB Topics:** Reasoning LLMs
   - **Abstract:** The paper introduces Think-Anywhere...
   - **Link:** [2603.29957v1](https://arxiv.org/abs/2603.29957v1)
   - **ArXiv Topics:** cs.SE

2. **Context Over Content**
   - **Published:** 2026-04-16
   - **KB Topics:** Evaluation, AI Security
   - **Abstract:** The LLM-as-a-judge paradigm...
   - **Link:** [2604.15224v1](https://arxiv.org/abs/2604.15224v1)
   - **ArXiv Topics:** Alignment & Safety
"""

def test_parse_digest_count():
    from arxiv_deep_dive import parse_digest
    papers = parse_digest(SAMPLE_DIGEST)
    assert len(papers) == 2

def test_parse_digest_fields():
    from arxiv_deep_dive import parse_digest
    papers = parse_digest(SAMPLE_DIGEST)
    assert papers[0]['id'] == '2603.29957v1'
    assert papers[0]['title'] == 'Think Anywhere in Code Generation'
    assert papers[0]['abstract'] == 'The paper introduces Think-Anywhere...'
    assert papers[0]['kb_topics'] == ['Reasoning LLMs']

def test_parse_digest_second_paper():
    from arxiv_deep_dive import parse_digest
    papers = parse_digest(SAMPLE_DIGEST)
    assert papers[1]['id'] == '2604.15224v1'
    assert 'Evaluation' in papers[1]['kb_topics']
    assert 'AI Security' in papers[1]['kb_topics']

def test_parse_digest_skips_malformed_entry():
    from arxiv_deep_dive import parse_digest
    malformed = """# ArXiv Digest
**KB-Relevant Papers: 2**

1. **Broken Paper**
   - **Published:** 2026-04-01
   - **KB Topics:** Evaluation
   - **Abstract:** Missing the link field.

2. **Good Paper**
   - **Published:** 2026-04-02
   - **KB Topics:** Reasoning LLMs
   - **Abstract:** Has all fields.
   - **Link:** [9999.0000v1](https://arxiv.org/abs/9999.0000v1)
"""
    papers = parse_digest(malformed)
    assert len(papers) == 1
    assert papers[0]['id'] == '9999.0000v1'
    assert papers[0]['title'] == 'Good Paper'


SAMPLE_HTML = """
<html><body>
<section id="S1"><h2>1 Introduction</h2><p>This paper presents a novel approach.</p></section>
<section id="S2"><h2>2 Method</h2><p>We use GRPO with alpha=0.1.</p></section>
<section id="S3"><h2>3 Experiments</h2><p>Results on LeetCode: 69.4%.</p></section>
<section id="S4"><h2>4 Ablation</h2><p>Without cold start: 47.9%.</p></section>
<section id="S5"><h2>5 Conclusion</h2><p>Think-Anywhere achieves SOTA.</p></section>
</body></html>
"""


def test_extract_sections_finds_method():
    from arxiv_deep_dive import extract_sections
    result = extract_sections(SAMPLE_HTML)
    assert 'GRPO' in result


def test_extract_sections_finds_results():
    from arxiv_deep_dive import extract_sections
    result = extract_sections(SAMPLE_HTML)
    assert '69.4%' in result


def test_extract_sections_finds_ablation():
    from arxiv_deep_dive import extract_sections
    result = extract_sections(SAMPLE_HTML)
    assert '47.9%' in result

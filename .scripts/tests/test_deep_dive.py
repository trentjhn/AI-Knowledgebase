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

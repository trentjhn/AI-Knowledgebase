#!/usr/bin/env python3
"""
ArXiv Weekly Digest Generator for AI Knowledge Base

Queries ArXiv API for papers matching KB topics, deduplicates across topics,
and outputs a weekly digest markdown file.
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import quote
import os
import sys
import time

# ArXiv query mapping: topic -> list of search queries
TOPIC_QUERIES = {
    "Prompt Engineering": [
        '"prompt engineering"',
        '"in-context learning"',
        '"few-shot learning"',
    ],
    "Context Engineering": [
        '"retrieval augmented generation"',
        '"RAG"',
        '"context window"',
    ],
    "Reasoning LLMs": [
        '"chain of thought"',
        '"reasoning"',
    ],
    "Agentic Engineering": [
        '"agent" AND ("language model" OR "LLM")',
        '"tool use"',
        '"multi-agent"',
    ],
    "Skills": [
        '"instruction tuning"',
        '"task-specific"',
    ],
    "Evaluation": [
        '"evaluation" AND ("LLM" OR "language model")',
        '"benchmark"',
    ],
    "Fine-tuning": [
        '"fine-tuning"',
        '"LoRA"',
        '"RLHF"',
        '"DPO"',
        '"preference learning"',
    ],
    "AI Security": [
        '"adversarial" AND ("LLM" OR "language model")',
        '"jailbreak"',
        '"robustness"',
    ],
    "Alignment & Safety": [
        '"alignment"',
        '"safety"',
        '"value alignment"',
    ],
}

# Category filter
ARXIV_CATEGORIES = "(cat:cs.AI OR cat:cs.CL OR cat:stat.ML)"
LLM_FILTER = '("language model" OR "LLM" OR "neural network")'

ARXIV_API = "http://export.arxiv.org/api/query?"


def build_query(topic_query: str) -> str:
    """Build a full ArXiv query with filters."""
    # Wrap topic query if it's not already
    if not topic_query.startswith('(') and not topic_query.startswith('"'):
        topic_query = f'"{topic_query}"'

    # Combine: category + topic query (LLM filter removed to avoid no-results)
    return f"{ARXIV_CATEGORIES} AND ({topic_query})"


def fetch_papers(query: str, max_results: int = 10) -> list:
    """Fetch papers from ArXiv API with rate limit handling."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    # Retry logic with exponential backoff
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(ARXIV_API, params=params, timeout=20)
            response.raise_for_status()
            return parse_arxiv_response(response.text)
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) * 3  # 3s, 6s, 12s
                print(f"  Rate limited. Waiting {wait_time}s before retry...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                print(f"HTTP Error {response.status_code}: {e}", file=sys.stderr)
                return []
        except requests.RequestException as e:
            print(f"Error fetching from ArXiv: {e}", file=sys.stderr)
            return []

        # Polite delay between requests (ArXiv courtesy)
        time.sleep(2)

    print(f"Failed after {max_retries} retries", file=sys.stderr)
    return []


def parse_arxiv_response(xml_response: str) -> list:
    """Parse ArXiv API XML response and extract paper info."""
    papers = []

    # Simple XML parsing (avoid external XML library dependency)
    import re

    # Extract entries using regex
    entry_pattern = r'<entry>(.*?)</entry>'
    entries = re.findall(entry_pattern, xml_response, re.DOTALL)

    for entry in entries:
        try:
            # Extract fields
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
                "summary": summary[:300],  # Truncate to 300 chars
                "published": published,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
            })
        except Exception as e:
            print(f"Error parsing entry: {e}", file=sys.stderr)
            continue

    return papers


def deduplicate_papers(topics_papers: dict) -> tuple:
    """
    Deduplicate papers across topics.
    Returns: (deduplicated_papers, topic_mapping)
    """
    seen = {}  # arxiv_id -> paper
    topic_map = defaultdict(set)  # arxiv_id -> set of topics

    for topic, papers in topics_papers.items():
        for paper in papers:
            paper_id = paper["id"]
            if paper_id not in seen:
                seen[paper_id] = paper
            topic_map[paper_id].add(topic)

    return seen, topic_map


def get_date_info() -> tuple:
    """Get current date info for filename and header."""
    today = datetime.now()
    return today


def format_digest(papers_dict: dict, topic_map: dict) -> str:
    """Format papers as markdown digest."""
    today = get_date_info()

    # Group papers by topic
    topic_papers = defaultdict(list)
    for paper_id, paper in papers_dict.items():
        topics = topic_map[paper_id]
        for topic in topics:
            topic_papers[topic].append(paper)

    # Sort topics
    topics = sorted(topic_papers.keys())

    # Build markdown
    lines = [
        f"# ArXiv Digest — {today.strftime('%B %d, %Y')}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
    ]

    if not topics:
        lines.append("No papers found this week.")
        return "\n".join(lines)

    for topic in topics:
        papers = topic_papers[topic]
        lines.append(f"## {topic} [{len(papers)} paper{'s' if len(papers) != 1 else ''}]")
        lines.append("")

        for i, paper in enumerate(papers, 1):
            tags = ", ".join(sorted(topic_map[paper["id"]]))
            lines.append(f"{i}. **{paper['title']}**")
            lines.append(f"   - **Published:** {paper['published']}")
            lines.append(f"   - **Abstract:** {paper['summary']}...")
            lines.append(f"   - **Link:** [{paper['id']}]({paper['url']})")
            lines.append(f"   - **Tags:** {tags}")
            lines.append("")

    return "\n".join(lines)


def main():
    """Main workflow."""
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "..", "raw", "arxiv-papers")
    os.makedirs(output_dir, exist_ok=True)

    # Fetch papers for each topic
    all_topics_papers = {}
    total_queries = sum(len(queries) for queries in TOPIC_QUERIES.values())
    completed = 0

    print(f"Fetching papers from {total_queries} queries...", file=sys.stderr)

    for topic, queries in TOPIC_QUERIES.items():
        all_topics_papers[topic] = []
        for query in queries:
            completed += 1
            print(f"  [{completed}/{total_queries}] {topic}: {query[:50]}...", file=sys.stderr)

            full_query = build_query(query)
            papers = fetch_papers(full_query, max_results=5)
            all_topics_papers[topic].extend(papers)

            # Polite delay between queries (ArXiv courtesy: ~1-2 requests per second max)
            if completed < total_queries:
                time.sleep(2)

    # Deduplicate
    unique_papers, topic_mapping = deduplicate_papers(all_topics_papers)
    print(f"Found {len(unique_papers)} unique papers", file=sys.stderr)

    # Generate digest
    digest = format_digest(unique_papers, topic_mapping)

    # Write to file
    today = get_date_info()
    filename = f"{today.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(digest)

    print(f"Digest written to {filepath}", file=sys.stderr)
    print(f"Total papers: {len(unique_papers)}", file=sys.stderr)

    return filepath


if __name__ == "__main__":
    main()

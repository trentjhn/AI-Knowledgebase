#!/usr/bin/env python3
"""
ArXiv Weekly Digest Generator for AI Knowledge Base

Queries ArXiv API for papers from last 7 days, deduplicates across topics,
and outputs a weekly digest markdown file.
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict
import os
import sys
import time
import re

# Consolidated ArXiv query mapping: topic -> list of search queries
# Reduced from 26 to 9 queries by combining similar topics
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

# Category filter
ARXIV_CATEGORIES = "(cat:cs.AI OR cat:cs.CL OR cat:stat.ML)"
ARXIV_API = "http://export.arxiv.org/api/query?"


def get_date_range() -> tuple:
    """Get 7-day date range for ArXiv query."""
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    # ArXiv uses YYYYMMDDHHMM format for submittedDate
    from_date = week_ago.strftime("%Y%m%d0000")
    to_date = today.strftime("%Y%m%d2359")
    return from_date, to_date, today


def build_query(topic_query: str, from_date: str, to_date: str) -> str:
    """Build a full ArXiv query with category, date range, and topic filters."""
    # Combine: category + date range + topic query
    return f'{ARXIV_CATEGORIES} AND submittedDate:[{from_date} TO {to_date}] AND ({topic_query})'


def fetch_papers(query: str, max_results: int = 3) -> list:
    """Fetch papers from ArXiv API with rate limit handling."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    # Retry logic with exponential backoff
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(ARXIV_API, params=params, timeout=15)
            response.raise_for_status()
            return parse_arxiv_response(response.text)
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) * 5
                print(f"  Rate limited. Waiting {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                print(f"HTTP Error {response.status_code}", file=sys.stderr)
                return []
        except requests.RequestException as e:
            print(f"Error: timeout/connection issue", file=sys.stderr)
            return []

    return []


def parse_arxiv_response(xml_response: str) -> list:
    """Parse ArXiv API XML response and extract paper info."""
    papers = []

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
                "summary": summary[:300],
                "published": published,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
            })
        except Exception as e:
            pass

    return papers


def deduplicate_papers(topics_papers: dict) -> tuple:
    """Deduplicate papers across topics."""
    seen = {}  # arxiv_id -> paper
    topic_map = defaultdict(set)  # arxiv_id -> set of topics

    for topic, papers in topics_papers.items():
        for paper in papers:
            paper_id = paper["id"]
            if paper_id not in seen:
                seen[paper_id] = paper
            topic_map[paper_id].add(topic)

    return seen, topic_map


def format_digest(papers_dict: dict, topic_map: dict, today: datetime) -> str:
    """Format papers as markdown digest."""
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

    total_papers = len(papers_dict)
    lines.append(f"**Total: {total_papers} papers**")
    lines.append("")

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
            lines.append(f"   - **Topics:** {tags}")
            lines.append("")

    return "\n".join(lines)


def main():
    """Main workflow."""
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "..", "raw", "arxiv-papers")
    os.makedirs(output_dir, exist_ok=True)

    from_date, to_date, today = get_date_range()

    # Fetch papers for each topic
    all_topics_papers = {}
    total_queries = sum(len(queries) for queries in TOPIC_QUERIES.values())
    completed = 0

    print(f"Fetching papers from {total_queries} queries (last 7 days)...", file=sys.stderr)

    for topic, queries in TOPIC_QUERIES.items():
        all_topics_papers[topic] = []
        for query in queries:
            completed += 1
            print(f"  [{completed}/{total_queries}] {topic}...", file=sys.stderr)

            full_query = build_query(query, from_date, to_date)
            papers = fetch_papers(full_query, max_results=3)
            all_topics_papers[topic].extend(papers)

            # Polite delay between queries
            if completed < total_queries:
                time.sleep(2)

    # Deduplicate
    unique_papers, topic_mapping = deduplicate_papers(all_topics_papers)
    print(f"Found {len(unique_papers)} unique papers", file=sys.stderr)

    # Generate digest
    digest = format_digest(unique_papers, topic_mapping, today)

    # Write to file
    filename = f"{today.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(digest)

    print(f"Digest written to {filepath}", file=sys.stderr)
    print(f"Total papers: {len(unique_papers)}", file=sys.stderr)

    return filepath


if __name__ == "__main__":
    main()

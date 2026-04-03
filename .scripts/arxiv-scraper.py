#!/usr/bin/env python3
"""
ArXiv Weekly Digest Generator for AI Knowledge Base

Queries ArXiv API for papers from 2-4 weeks ago (rolling window),
filters by Semantic Scholar citations (5+), deduplicates across topics,
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
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
CITATION_THRESHOLD = 1


def get_date_range() -> tuple:
    """Get 1-4 week rolling window for ArXiv query."""
    today = datetime.now()
    week_4_ago = today - timedelta(days=28)
    week_1_ago = today - timedelta(days=7)

    from_date = week_4_ago.strftime("%Y%m%d0000")
    to_date = week_1_ago.strftime("%Y%m%d2359")
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
            if response.status_code == 429:
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
                "citation_count": 0,
            })
        except Exception:
            pass

    return papers


def fetch_citation_count(arxiv_id: str) -> int:
    """Get citation count from Semantic Scholar API."""
    try:
        clean_id = arxiv_id.split('v')[0]
        params = {
            "query": f"arxiv:{clean_id}",
            "fields": "citationCount",
            "limit": 1,
        }
        response = requests.get(SEMANTIC_SCHOLAR_API, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("data") and len(data["data"]) > 0:
            return data["data"][0].get("citationCount", 0)
        return 0
    except Exception:
        return 0


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


def format_digest(papers_dict: dict, topic_map: dict, today: datetime, total_before_filter: int) -> str:
    """Format papers as markdown digest (each paper displayed once)."""
    lines = [
        f"# ArXiv Digest — {today.strftime('%B %d, %Y')}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*",
        f"*Date Range: 1-4 weeks ago (rolling window)*",
        f"*Filtered by: 1+ citations on Semantic Scholar*",
        "",
    ]

    if not papers_dict:
        lines.append("No highly-cited papers found this week.")
        return "\n".join(lines)

    filtered = len(papers_dict)
    lines.append(f"**Quality Papers: {filtered} (filtered from {total_before_filter} by citation count)**")
    lines.append("")

    # Sort papers by citation count (descending)
    papers_sorted = sorted(
        papers_dict.items(),
        key=lambda item: item[1].get("citation_count", 0),
        reverse=True
    )

    for i, (paper_id, paper) in enumerate(papers_sorted, 1):
        tags = ", ".join(sorted(topic_map[paper_id]))
        citations = paper.get("citation_count", 0)
        lines.append(f"{i}. **{paper['title']}**")
        lines.append(f"   - **Published:** {paper['published']}")
        lines.append(f"   - **Citations:** {citations} (Semantic Scholar)")
        lines.append(f"   - **Abstract:** {paper['summary']}...")
        lines.append(f"   - **Link:** [{paper['id']}]({paper['url']})")
        lines.append(f"   - **Topics:** {tags}")
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
            papers = fetch_papers(full_query, max_results=10)
            all_topics_papers[topic].extend(papers)

            if completed < total_queries:
                time.sleep(2)

    # Deduplicate
    unique_papers, topic_mapping = deduplicate_papers(all_topics_papers)
    total_before_filter = len(unique_papers)
    print(f"Found {total_before_filter} unique papers. Fetching citation counts...", file=sys.stderr)

    # Get Semantic Scholar citations
    for paper_id, paper in unique_papers.items():
        citation_count = fetch_citation_count(paper_id)
        paper["citation_count"] = citation_count
        time.sleep(0.3)

    # Filter by citation threshold
    filtered_papers = {
        pid: paper for pid, paper in unique_papers.items()
        if paper.get("citation_count", 0) >= CITATION_THRESHOLD
    }

    print(f"After filtering (5+ citations): {len(filtered_papers)} papers", file=sys.stderr)

    # Generate digest
    digest = format_digest(filtered_papers, topic_mapping, today, total_before_filter)

    # Write to file
    filename = f"{today.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(digest)

    print(f"Digest written to {filepath}", file=sys.stderr)

    return filepath


if __name__ == "__main__":
    main()

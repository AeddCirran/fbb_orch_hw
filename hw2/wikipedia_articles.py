#!/usr/bin/env python3

import argparse
import json
import time
import sys
from collections import deque
from urllib.parse import urljoin, unquote

import requests
from bs4 import BeautifulSoup

USER_AGENT = "WikiCrawler (Educational project; labanovvlad3125@gmail.com)"
HEADERS = {"User-Agent": USER_AGENT}
BASE_URL = "https://en.wikipedia.org"


def extract_wiki_links(html, base_url, max_links):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", id="mw-content-text")
    if not content:
        content = soup  # fallback

    links = []
    for a_tag in content.find_all("a", href=True):
        href = a_tag["href"]
        if not href.startswith("/wiki/") or ":" in href:
            continue
        if "#" in href:
            href = href.split("#")[0]
            if not href:
                continue

        full_url = urljoin(base_url, href)
        title = unquote(full_url.split("/wiki/")[-1].split("#")[0])
        if title not in [t for t, _ in links]:
            links.append((title, full_url))
            if len(links) >= max_links:
                break

    return links


def crawl(start_url, max_depth, max_links):
    start_title = unquote(start_url.split("/wiki/")[-1].split("#")[0])
    visited = set()
    visited.add(start_title)
    edges = []
    frontier = deque()
    frontier.append((start_title, start_url, 0))

    while frontier:
        title, url, depth = frontier.popleft()
        if depth >= max_depth:
            pass

        print(f"Fetching (depth {depth}): {title}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                print(f"  Skipping {title} (HTTP {resp.status_code})")
                continue
        except Exception as e:
            print(f"  Error fetching {title}: {e}")
            continue

        discovered = extract_wiki_links(resp.text, url, max_links)
        print(f"  Found {len(discovered)} links")

        for dst_title, dst_url in discovered:
            edges.append([title, dst_title])

            if dst_title not in visited and depth + 1 <= max_depth:
                visited.add(dst_title)
                frontier.append((dst_title, dst_url, depth + 1))

        time.sleep(0.1)

    nodes = set()
    for src, dst in edges:
        nodes.add(src)
        nodes.add(dst)
    nodes.add(start_title)

    graph = {
        "nodes": sorted(list(nodes)),
        "edges": edges,
    }
    return graph, start_title


def main():
    parser = argparse.ArgumentParser(description="Wiki crawler")
    parser.add_argument("--url", required=True, help="Starting URL")
    parser.add_argument("--depth", type=int, required=True, help="Max depth")
    parser.add_argument(
        "--max-links",
        type=int,
        default=100,
        help="Max num of links per page",
    )
    args = parser.parse_args()

    graph, start_title = crawl(args.url, args.depth, args.max_links)

    output_file = f"{start_title}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    print(f"Graph saved to {output_file}")
    print(f"Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")


if __name__ == "__main__":
    main()

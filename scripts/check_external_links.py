#!/usr/bin/env python3
"""Check external Markdown links without treating access controls as dead links."""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https://[^\s)>]+")
REACHABLE_BUT_GATED = {401, 403, 405, 418, 429}
DEFINITELY_DEAD = {404, 410}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "qa" not in path.parts
    )


def collect_urls() -> list[str]:
    urls: set[str] = set()
    for path in markdown_files():
        urls.update(URL_RE.findall(path.read_text(encoding="utf-8")))
    return sorted(urls)


def check(url: str, timeout: float) -> tuple[str, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 FDE-Knowledge-Base-Link-Checker/1.0",
            "Range": "bytes=0-2047",
        },
        method="GET",
    )
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            code = response.getcode()
            return ("ok", str(code), url)
    except urllib.error.HTTPError as error:
        if error.code in REACHABLE_BUT_GATED:
            return ("gated", str(error.code), url)
        if error.code in DEFINITELY_DEAD:
            return ("dead", str(error.code), url)
        return ("unverified", str(error.code), url)
    except Exception as error:  # Network failures need a human retry, not a traceback.
        detail = getattr(error, "reason", None)
        label = str(detail or type(error).__name__).replace("\n", " ")[:80]
        return ("unverified", label, url)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查知识库中的公开链接")
    parser.add_argument("--timeout", type=float, default=12.0, help="每个链接的超时秒数")
    parser.add_argument("--workers", type=int, default=8, help="并发请求数量")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="把网络原因造成的未核验链接也视为失败",
    )
    args = parser.parse_args()

    urls = collect_urls()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda url: check(url, args.timeout), urls))

    labels = ("ok", "gated", "unverified", "dead")
    counts = {label: sum(result[0] == label for result in results) for label in labels}
    print(
        f"Checked {len(results)} URLs: {counts['ok']} ok, "
        f"{counts['gated']} access-controlled, {counts['unverified']} unverified, "
        f"{counts['dead']} dead"
    )
    for label, detail, url in results:
        if label != "ok":
            print(f"{label.upper():10} {detail:80} {url}")
    if counts["dead"]:
        return 1
    if args.strict and counts["unverified"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

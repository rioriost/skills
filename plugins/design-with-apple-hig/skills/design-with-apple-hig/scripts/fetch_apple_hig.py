#!/usr/bin/env python3
"""Fetch one current Apple HIG topic from Apple's official DocC JSON endpoint."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


HIG_PREFIX = "https://developer.apple.com/design/human-interface-guidelines/"
DOCC_PREFIX = "https://developer.apple.com/tutorials/data/design/human-interface-guidelines/"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class AppleOnlyRedirect(urllib.request.HTTPRedirectHandler):
    """Keep this official-source reader on the original trusted origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != "https" or parsed.netloc != "developer.apple.com":
            raise ValueError("Refusing redirect outside https://developer.apple.com")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def parse_slug(value: str) -> str:
    value = value.strip()
    if "://" not in value:
        slug = value.strip("/").lower()
    else:
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme != "https" or parsed.netloc != "developer.apple.com":
            raise ValueError("URL must use https://developer.apple.com")
        prefix = "/design/human-interface-guidelines/"
        if not parsed.path.startswith(prefix):
            raise ValueError("URL must be an Apple Human Interface Guidelines topic")
        slug = parsed.path[len(prefix) :].strip("/").lower()
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("topic must be a single lowercase Apple HIG slug")
    return slug


def fetch_json(url: str, timeout: float) -> dict[str, Any]:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a finite positive number")
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "design-with-apple-hig/2.0 (+official-source-reader)",
        },
    )
    opener = urllib.request.build_opener(AppleOnlyRedirect())
    with opener.open(request, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"Apple returned HTTP {response.status}")
        data = json.load(response)
        if not isinstance(data, dict):
            raise ValueError("Apple DocC response must be a JSON object")
        return data


def inline_text(node: Any, references: dict[str, Any], warnings: set[str]) -> str:
    if node is None:
        return ""
    if isinstance(node, list):
        return "".join(inline_text(item, references, warnings) for item in node)
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        warnings.add("Malformed inline content; inspect the official page")
        return ""
    if isinstance(node.get("text"), str):
        return node["text"]
    if node.get("type") == "reference":
        title = node.get("overridingTitle")
        if isinstance(title, str):
            return title
        ref = references.get(node.get("identifier", ""), {})
        if isinstance(ref, dict) and isinstance(ref.get("title"), str):
            return ref["title"]
        warnings.add("Unresolved inline reference; inspect the official page")
        return ""
    if node.get("type") not in {None, "strong", "emphasis", "codeVoice", "paragraph"}:
        warnings.add(f"Unsupported inline type: {node.get('type')}")
    for key in ("inlineContent", "content"):
        if key in node:
            return inline_text(node[key], references, warnings)
    return ""


def render_blocks(
    blocks: Any, references: dict[str, Any], out: list[str], warnings: set[str]
) -> None:
    if not isinstance(blocks, list):
        warnings.add("Malformed block collection; inspect the official page")
        return
    for block in blocks:
        if not isinstance(block, dict):
            warnings.add("Malformed block; inspect the official page")
            continue
        kind = block.get("type")
        if kind == "heading":
            level = min(max(int(block.get("level", 2)), 1), 6)
            text = str(block.get("text", "")).strip()
            if text:
                out.append(f"{'#' * level} {text}")
        elif kind in ("paragraph", "small"):
            text = inline_text(block.get("inlineContent", []), references, warnings).strip()
            if text:
                out.append(text)
        elif kind in ("unorderedList", "orderedList"):
            ordered = kind == "orderedList"
            for index, item in enumerate(block.get("items", []), start=1):
                rendered_item: list[str] = []
                render_blocks(item.get("content", []), references, rendered_item, warnings)
                if rendered_item:
                    marker = f"{index}." if ordered else "-"
                    indent = " " * (len(marker) + 1)
                    text = "\n\n".join(rendered_item).replace("\n", "\n" + indent)
                    out.append(f"{marker} {text}")
        elif kind == "codeListing":
            code = block.get("code", [])
            if isinstance(code, list):
                out.append("```\n" + "\n".join(str(line) for line in code) + "\n```")
        elif kind == "table":
            warnings.add("Table rendered as text rows; verify header/span relationships on the official page")
            for row in block.get("rows", []):
                cells = []
                for cell in row:
                    rendered_cell: list[str] = []
                    render_blocks(cell, references, rendered_cell, warnings)
                    cells.append(" / ".join(rendered_cell).replace("|", "\\|"))
                if any(cells):
                    out.append(" | ".join(cells))
        elif kind == "row":
            for column in block.get("columns", []):
                render_blocks(column.get("content", []), references, out, warnings)
        elif kind == "tabNavigator":
            for tab in block.get("tabs", []):
                out.append(f"### {tab.get('title', 'Untitled tab')}")
                render_blocks(tab.get("content", []), references, out, warnings)
        elif kind == "links":
            continue
        else:
            if kind not in (None, "aside"):
                warnings.add(f"Unsupported block type: {kind}")
            if kind == "aside":
                out.append(f"### {block.get('name', 'Note')}")
            nested = block.get("content")
            if isinstance(nested, list):
                render_blocks(nested, references, out, warnings)


def build_result(slug: str, data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Apple DocC response must be a JSON object")
    metadata = data.get("metadata", {}) if isinstance(data.get("metadata"), dict) else {}
    if not isinstance(metadata.get("title"), str) or not metadata["title"].strip():
        raise ValueError("Apple DocC response is missing a topic title")
    sections = data.get("primaryContentSections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("Apple DocC response is missing primary content")
    custom = metadata.get("customMetadata", {}) if isinstance(metadata.get("customMetadata"), dict) else {}
    references = data.get("references", {}) if isinstance(data.get("references"), dict) else {}
    rendered: list[str] = []
    warnings: set[str] = set()
    render_blocks(sections, references, rendered, warnings)
    if not rendered:
        raise ValueError("No readable primary content; inspect the official page")
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {
        "title": metadata.get("title", slug),
        "slug": slug,
        "source_url": HIG_PREFIX + slug,
        "docc_url": DOCC_PREFIX + slug + ".json",
        "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "extraction_warnings": sorted(warnings),
        "extraction_note": "Text extraction only; inspect media and complex layout on the official page. Retrieval time is not a publication or OS release date.",
        "supported_platforms": custom.get("supported-platforms"),
        "alert_date": custom.get("alert-date"),
        "alert_text": custom.get("alert-text"),
        "available_locales": metadata.get("availableLocales") or metadata.get("availableLanguages"),
        "content": "\n\n".join(rendered).strip(),
    }


def compare_metadata(result: dict[str, Any], baseline: Any) -> dict[str, Any]:
    if not isinstance(baseline, dict) or baseline.get("source_url") != result["source_url"]:
        raise ValueError("Baseline must be metadata for the same HIG source_url")
    previous = baseline.get("source_sha256")
    if previous is not None and (
        not isinstance(previous, str) or not re.fullmatch(r"[a-f0-9]{64}", previous)
    ):
        raise ValueError("Baseline source_sha256 must be a lowercase SHA-256 digest")
    status = "unknown" if previous is None else (
        "unchanged" if previous == result["source_sha256"] else "changed"
    )
    return {"status": status, "baseline_retrieved_at_utc": baseline.get("retrieved_at_utc")}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read one current Apple HIG topic from Apple's official DocC JSON."
    )
    parser.add_argument("topic", help="HIG slug or canonical Apple HIG topic URL")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--compare-metadata", type=Path, help="Compare with previous JSON metadata for this topic (does not overwrite it)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        slug = parse_slug(args.topic)
        data = fetch_json(DOCC_PREFIX + slug + ".json", args.timeout)
        result = build_result(slug, data)
        if args.compare_metadata:
            baseline = json.loads(args.compare_metadata.read_text(encoding="utf-8"))
            result["comparison"] = compare_metadata(result, baseline)
    except (ValueError, OSError, RuntimeError, TypeError, KeyError, AttributeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.metadata_only:
        result = {key: value for key, value in result.items() if key != "content"}

    if args.format == "json" or args.metadata_only:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"# {result['title']}")
        print(f"\n- Source: {result['source_url']}")
        print(f"- Retrieved: {result['retrieved_at_utc']}")
        print(f"- Source SHA-256: {result['source_sha256']}")
        print(f"- Extraction: {result['extraction_note']}")
        for warning in result["extraction_warnings"]:
            print(f"- Warning: {warning}")
        if "comparison" in result:
            print(f"- Baseline comparison: {result['comparison']['status']}")
        if result.get("supported_platforms"):
            print(f"- Platforms: {result['supported_platforms']}")
        if result.get("alert_date") or result.get("alert_text"):
            print(f"- Update: {result.get('alert_date') or 'unspecified'} — {result.get('alert_text') or ''}")
        if result.get("content"):
            print("\n" + result["content"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

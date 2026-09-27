#!/usr/bin/env python3
"""Check vendored provenance and standalone URL-import packaging, offline."""

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/design-with-apple-hig'
SKILL = PLUGIN / 'skills/design-with-apple-hig'


def main():
    source = json.loads((PLUGIN / 'SOURCE.json').read_text())
    for name, expected in source['sha256'].items():
        actual = hashlib.sha256((SKILL / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Vendored source differs from recorded revision: {name}')

    portable = ROOT / 'zed/design-with-apple-hig/SKILL.md'
    text = portable.read_text()
    header = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not header:
        raise ValueError('Missing standalone skill frontmatter')
    fields = dict(line.split(': ', 1) for line in header[1].splitlines())
    if fields.get('name') != portable.parent.name or not fields.get('description'):
        raise ValueError('Standalone skill identity/description is invalid')
    if len(fields['description']) > 1024 or len(text.splitlines()) >= 500:
        raise ValueError('Standalone skill exceeds Zed recommended size limits')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        parsed = urlsplit(target)
        if target.startswith('#'):
            continue
        if parsed.scheme != 'https' or not parsed.netloc:
            raise ValueError(f'URL-only import has an unavailable relative resource: {target}')
    if 'scripts/' in text or 'references/' in text:
        raise ValueError('Standalone edition assumes an adjacent resource directory')
    for copyright_line in ('Copyright (c) 2026 Sunwood AI Labs', 'Copyright (c) 2026 Rio Fujita'):
        if copyright_line not in text:
            raise ValueError('Standalone MIT attribution is missing')
    if (PLUGIN / 'LICENSE').read_bytes() != (SKILL / 'LICENSE').read_bytes():
        raise ValueError('Upstream license was not preserved')

    market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
    entries = [p for p in market['plugins'] if p['name'] == 'design-with-apple-hig']
    if len(entries) != 1 or entries[0]['source']['path'] != './plugins/design-with-apple-hig':
        raise ValueError('Marketplace does not resolve exactly one HIG plugin')
    manifest = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
    if manifest['name'] != 'design-with-apple-hig' or manifest['skills'] != './skills/':
        raise ValueError('Plugin entrypoint does not resolve the complete skill')
    print(f'Apple HIG package valid: {len(source["sha256"])} preserved source files; '
          f'{len(text.splitlines())}-line standalone import with no local dependencies')


if __name__ == '__main__':
    main()

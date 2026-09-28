#!/usr/bin/env python3
"""Validate the repository's single-file Zed editions without running examples."""

import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate(path):
    text = path.read_text(encoding='utf-8')
    header = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not header:
        raise ValueError(f'{path}: missing frontmatter')
    # These editions deliberately use simple one-line, unquoted YAML fields.
    fields = {}
    for line in header[1].splitlines():
        key, separator, value = line.partition(': ')
        if not separator or key in fields:
            raise ValueError(f'{path}: malformed or duplicate metadata')
        fields[key] = value
    name = fields.get('name', '')
    if (not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)
            or len(name) > 64 or name != path.parent.name):
        raise ValueError(f'{path}: invalid skill name')
    if not 0 < len(fields.get('description', '')) <= 1024:
        raise ValueError(f'{path}: invalid description length')
    if len(text.splitlines()) >= 500:
        raise ValueError(f'{path}: standalone edition exceeds size budget')
    targets = re.findall(r'\]\(([^)]+)\)', text)
    targets += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', text, re.M)
    for target in targets:
        parsed = urlsplit(target)
        if not target.startswith('#') and (parsed.scheme != 'https' or not parsed.netloc):
            raise ValueError(f'{path}: unavailable imported resource: {target}')
    if 'scripts/' in text or 'references/' in text:
        raise ValueError(f'{path}: adjacent resource dependency needs review')
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8').strip()
    # HIG carries additional upstream attribution between the title and grant.
    for paragraph in license_text.split('\n\n'):
        if paragraph not in text:
            raise ValueError(f'{path}: incomplete embedded MIT notice')
    fences = re.findall(r'^```([^\n]*)\n(.*?)^```\s*$', text, re.M | re.S)
    if len(re.findall(r'^```', text, re.M)) != 2 * len(fences):
        raise ValueError(f'{path}: unbalanced code fences')
    for language, example in fences:
        if language in ('sh', 'bash'):
            subprocess.run(['/bin/bash', '-n'], input=example, text=True, check=True)
    print(f'{path.relative_to(ROOT)}: valid ({len(text.splitlines())} lines)')


if __name__ == '__main__':
    paths = sorted((ROOT / 'zed').glob('*/SKILL.md'))
    if not paths:
        raise SystemExit('No standalone skills found')
    for path in paths:
        validate(path)

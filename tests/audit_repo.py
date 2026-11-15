"""Audit distributable text: privacy patterns, local Markdown links, JSON/SVG validity, required files."""
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
patterns = [r'192' + r'\.168', r'10' + r'\.[0-9]+\.', 'duck' + 'dns', 'ts' + r'\.net', '/s' + 'rv/', '/ho' + 'me/',
            'mine' + 'craft', 'AI' + 'HUB', 'rpi-' + 'k3s']
fail, count = [], 0
for p in ROOT.rglob('*'):
    rel = p.relative_to(ROOT)
    if not p.is_file() or any(x in ('__pycache__', '.git') for x in rel.parts):
        continue
    if p.suffix in ('.png', '.gif', '.jpg'):
        continue
    if p.suffix == '.svg':
        ET.parse(p)
    if p.suffix == '.json':
        json.loads(p.read_text(encoding='utf-8'))
    text = p.read_text(encoding='utf-8')
    count += 1
    for pattern in patterns:
        if re.search(pattern, text, re.I):
            fail.append(f'{rel}: privacy rule {pattern}')
    if p.suffix == '.md':
        for href in re.findall(r'\]\(([^)]+)\)', text):
            if ':' in href or href.startswith('#'):
                continue
            if not (p.parent / href.split('#')[0].split('?')[0]).exists():
                fail.append(f'{rel}: missing link {href}')
for name in ['README.md', 'README.es.md', 'CONTRIBUTORS.md', 'LICENSE', 'NOTICE.md', 'SECURITY.md', 'CHANGELOG.md', 'docs/index.html', 'docs/.nojekyll',
             'docs/data/timing-model.json', 'src/estimate.py', 'src/cuts.py', 'skill/ai-video-edit-and-shorts/SKILL.md']:
    if not (ROOT / name).is_file():
        fail.append(f'missing {name}')
if fail:
    print('\n'.join(fail))
    sys.exit(1)
print(f'OK: {count} text files, JSON/SVG parsing, local Markdown links, privacy patterns and required files')

# -*- coding: utf-8 -*-
"""Validate the book extraction and deployment"""

import urllib.request, json, sys

BASE = 'http://localhost:8081'

try:
    r = urllib.request.urlopen(f'{BASE}/book/data.json')
    data = json.loads(r.read().decode('utf-8'))
    print(f'1. data.json: {data["total_articles"]} articles, {data["total_images"]} images')
except Exception as e:
    print(f'1. FAIL: {e}')
    sys.exit(1)

article_ids = [a['id'] for a in data['articles']]
print(f'2. Article IDs: {article_ids}')

all_ok = True
for aid in article_ids:
    try:
        r2 = urllib.request.urlopen(f'{BASE}/book/{aid}.json')
        adata = json.loads(r2.read().decode('utf-8'))
        blocks = adata.get('blocks', [])
        img_count = sum(1 for b in blocks if b['type'] == 'image')
        txt_count = sum(1 for b in blocks if b['type'] == 'text')
        print(f'   {aid}: {len(blocks)} blocks ({txt_count} text, {img_count} images)')
    except Exception as e:
        print(f'   {aid}: FAIL - {e}')
        all_ok = False

try:
    r3 = urllib.request.urlopen(f'{BASE}/toc.html')
    toc_html = r3.read().decode('utf-8')
    assert 'toc.js' in toc_html
    print('3. toc.html OK')
except Exception as e:
    print(f'3. FAIL: {e}')
    all_ok = False

try:
    r4 = urllib.request.urlopen(f'{BASE}/reader.html')
    reader_html = r4.read().decode('utf-8')
    assert 'book.css' in reader_html
    assert 'reader.js' in reader_html
    print('4. reader.html OK (includes book.css + reader.js)')
except Exception as e:
    print(f'4. FAIL: {e}')
    all_ok = False

# Check one image
try:
    r5 = urllib.request.urlopen(f'{BASE}/book/images/01-taiwan_001.jpeg')
    assert r5.status == 200
    print('5. Images accessible (01-taiwan_001.jpeg OK)')
except Exception as e:
    print(f'5. FAIL: {e}')
    all_ok = False

if all_ok:
    print('\n=== ALL CHECKS PASSED ===')
else:
    print('\n=== SOME CHECKS FAILED ===')
    sys.exit(1)

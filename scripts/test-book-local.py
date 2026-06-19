# -*- coding: utf-8 -*-
"""Comprehensive test of book reader"""
import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'http://localhost:8081'

def test(path, desc):
    try:
        r = urllib.request.urlopen(f'{BASE}{path}')
        if r.status == 200:
            print(f'  OK {desc}')
            return r.read()
        else:
            print(f'  FAIL {desc}: status {r.status}')
            return None
    except Exception as e:
        print(f'  FAIL {desc}: {e}')
        return None

# Test core files
test('/toc.html', 'toc.html')
test('/reader.html', 'reader.html')
r = test('/book/data.json', 'book/data.json')

if r:
    data = json.loads(r.decode('utf-8'))
    print(f'\n  Articles in master: {data["total_articles"]}')
    
    for art in data['articles']:
        aid = art['id']
        if aid in ('cover', 'toc'): continue
        r2 = test(f'/book/{aid}.json', f'book/{aid}.json')
        if r2:
            adata = json.loads(r2.decode('utf-8'))
            blocks = adata.get('blocks', [])
            n_text = sum(1 for b in blocks if b['type'] == 'text')
            n_img = sum(1 for b in blocks if b['type'] == 'image')
            if n_text > 0:
              first = blocks[0]['content'][:40].replace('\n',' ')
            else:
              first = '(no text blocks)'
            print(f'       {aid}: {len(blocks)} blocks ({n_text} text, {n_img} images)')
            print(f'       first: {first}...')

# Test image access
r3 = test('/book/images/01-taiwan_001.jpeg', 'first image')
if r3:
    print(f'       image size: {len(r3)} bytes')

# Test EN version
r4 = test('/book/en-00-preface.json', 'en-00-preface.json')
if r4:
    en_data = json.loads(r4.decode('utf-8'))
    print(f'       EN blocks: {len(en_data["blocks"])}')
    print(f'       first: {en_data["blocks"][0]["content"][:60]}...')

print('\n=== DONE ===')

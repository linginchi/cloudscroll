"""Verify paragraph merge quality."""
import json, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(root, 'dist', 'book', 'data.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

for art in data['articles']:
    aid = art['id']
    if aid in ('cover', 'toc', '00-preface'):
        continue
    art_path = os.path.join(root, 'dist', 'book', f'{aid}.json')
    with open(art_path, 'r', encoding='utf-8') as f:
        article = json.load(f)
    text_blocks = [b for b in article['blocks'] if b['type'] == 'text']
    print(f'\n=== {aid} ({len(text_blocks)} text blocks) ===')
    for tb in text_blocks:
        print(f'  [{len(tb["content"])}c] {tb["content"][:80]}')

"""Verify translations and subtitle fixes."""
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Check 01-taiwan subtitle
with open(os.path.join(root, 'dist', 'book', '01-taiwan.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
print('01-taiwan subtitle:', d['subtitle'])
print('01-taiwan en_subtitle:', d.get('en_subtitle', ''))

# Check 05-vietnam subtitle
with open(os.path.join(root, 'dist', 'book', '05-vietnam.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
print('05-vietnam subtitle:', d['subtitle'])
print('05-vietnam en_subtitle:', d.get('en_subtitle', ''))

# Check block counts match for all en-*.json files
for aid in ['01-taiwan', '02-philippines', '03-kuala-lumpur', '04-penang',
            '05-vietnam', '06-korea', '07-new-zealand', '08-usa', '09-macau', '10-kinmen']:
    with open(os.path.join(root, 'dist', 'book', f'{aid}.json'), 'r', encoding='utf-8') as f:
        zh = json.load(f)
    with open(os.path.join(root, 'dist', 'book', f'en-{aid}.json'), 'r', encoding='utf-8') as f:
        en = json.load(f)
    
    zh_texts = len([b for b in zh['blocks'] if b['type'] == 'text'])
    en_texts = len([b for b in en['blocks'] if b['type'] == 'text'])
    match = 'OK' if zh_texts == en_texts else 'MISMATCH'
    print(f'{match}: {aid} ZH={zh_texts} EN={en_texts} text blocks')

# Show sample EN content
print('\n--- en-05-vietnam sample ---')
with open(os.path.join(root, 'dist', 'book', 'en-05-vietnam.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
for b in d['blocks'][:4]:
    if b['type'] == 'text':
        print(f'  [{len(b["content"])}c] {b["content"][:120]}')

print('\n--- en-01-taiwan sample ---')
with open(os.path.join(root, 'dist', 'book', 'en-01-taiwan.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
for b in d['blocks'][:4]:
    if b['type'] == 'text':
        print(f'  [{len(b["content"])}c] {b["content"][:120]}')

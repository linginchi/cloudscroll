import json, re, os

root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dist', 'book')

# Check en-00-preface.json for Chinese residuals
with open(os.path.join(root, 'en-00-preface.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Title: {data['en']}")
has_chinese = False
for i, b in enumerate(data['blocks']):
    if b['type'] == 'text':
        truncated = b['content'][:80]
        cn = '⚠ CN' if re.search(r'[\u4e00-\u9fff]', b['content']) else '  EN'
        print(f"  [{i}] {cn} {truncated}")
        if re.search(r'[\u4e00-\u9fff]', b['content']):
            has_chinese = True

print(f"\nResult: {'⚠ STILL HAS CHINESE' if has_chinese else '✓ ALL ENGLISH'}")

# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document
book_dir = os.path.join(os.getcwd(), 'book')
files = [f for f in os.listdir(book_dir) if f.endswith('.docx') and not f.startswith('~$')]
files.sort()
print(f"找到 {len(files)} 篇 docx 档案\n")
total_chars = 0; total_imgs = 0; all_r = []
for fname in files:
    path = os.path.join(book_dir, fname)
    doc = Document(path)
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    all_text = '\n'.join(paras)
    cjk = sum(1 for c in all_text if '\u4e00' <= c <= '\u9fff')
    imgs = len(doc.inline_shapes)
    total_chars += cjk; total_imgs += imgs
    title = paras[0][:60] if paras else '(空)'
    sub = len([p for p in paras if len(p) <= 20])
    summary = all_text[:150].replace('\n',' ')
    print(f"  [{fname}]")
    print(f"    标题: {title}")
    print(f"    字数: {cjk}  图片: {imgs}  段落: {len(paras)}  小标(~): {sub}")
    print(f"    摘要: {summary}\n")
    all_r.append({'f':fname,'c':cjk,'i':imgs})
print("="*60)
print(f"总计: {len(all_r)} 篇, 总字数 {total_chars:,}, 总图片 {total_imgs}")
if all_r:
    cs = [r['c'] for r in all_r]
    print(f"最短: {min(cs):,} / 最长: {max(cs):,} / 平均: {total_chars//len(all_r):,}")
    print(f"\n{'档案':<40s}{'字数':<8s}{'图片'}")
    for r in all_r:
        n = r['f'].replace('.docx','')[:38]
        print(f"{n:<40s}{r['c']:<8d}{r['i']}")

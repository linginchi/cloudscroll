# -*- coding: utf-8 -*-
"""
scripts/extract-book.py

Extract text + images from all 13 docx files in book/
Output structured JSON + images to assets/images/book/ and dist/book/

Usage: python scripts/extract-book.py
       python scripts/extract-book.py --output-dir dist  (default)
"""

import os, sys, json, shutil, re, zipfile, tempfile
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from lxml import etree

# Ensure UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, 'book')
ASSETS_IMG_DIR = os.path.join(ROOT, 'assets', 'images', 'book')
DIST_DIR = os.path.join(ROOT, 'dist')
DIST_BOOK_DIR = os.path.join(DIST_DIR, 'book')
DIST_IMG_DIR = os.path.join(DIST_BOOK_DIR, 'images')

nsmap = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}

TOC_MAP = {
    '台湾': '01-taiwan',              # 台湾屢遊散記
    '菲岛': '02-philippines',         # 菲岛情怀 (simplified)
    '菲島': '02-philippines',         # traditional variant
    '霧鎖雲頂': '03-kuala-lumpur',
    '檳島親遊': '04-penang',
    '麗星': '05-vietnam',            # 麗星驰碧浪 / 麗星馳碧浪
    '長今': '06-korea',              # 長今尋縱 / 長今尋蹤
    '新西蘭': '07-new-zealand',
    '勝景怡人': '08-usa',
    '澳門': '09-macau',              # 屢次澳門遊蹤紀
    '浯洲': '10-kinmen',
}

# Known list of chapter/epigraph texts that should NOT be treated as article titles
CHAPTER_HEADERS = {
    '第一輯 向世界出發',
    '第二輯 神州大地之行',
    'Part I: To the World',
    'Part II: Journeys Across China',
}

def extract_images_from_docx(docx_path, output_dir, article_id):
    """Extract images from docx zip and return a map of rId -> filename"""
    img_map = {}
    os.makedirs(output_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            # List all files in the zip
            all_files = z.namelist()

            # Find image files (in word/media/ typically)
            img_files = [f for f in all_files if f.startswith('word/media/')]

            for i, img_path in enumerate(sorted(img_files)):
                ext = os.path.splitext(img_path)[1].lower()
                if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'):
                    ext = '.jpg'  # fallback
                out_name = f'{article_id}_{i+1:03d}{ext}'
                out_path = os.path.join(output_dir, out_name)

                with z.open(img_path) as src, open(out_path, 'wb') as dst:
                    dst.write(src.read())

                # Map the internal path to our filename
                img_map[img_path] = out_name

                # Also try to map rId
                # The relationship between rId and media path is in word/_rels/document.xml.rels
                rels_path = 'word/_rels/document.xml.rels'
                if rels_path in all_files:
                    with z.open(rels_path) as f:
                        rels_xml = f.read()
                    rels_root = etree.fromstring(rels_xml)
                    for rel in rels_root:
                        target = rel.get('Target', '')
                        target_full = f'word/{target}' if not target.startswith('word/') else target
                        if target_full == img_path:
                            rid = rel.get('Id')
                            if rid:
                                img_map[rid] = out_name

    except Exception as e:
        print(f'  Warning: zip extraction failed for images: {e}')

    return img_map


def find_images_in_paragraph(para, img_map, seen_embeds=None):
    """Find unique image rIds/blip embeds in a paragraph's XML"""
    if seen_embeds is None:
        seen_embeds = set()
    results = []
    para_element = para._element

    blips = para_element.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
    for blip in blips:
        embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if embed and embed in img_map and embed not in seen_embeds:
            seen_embeds.add(embed)
            results.append(img_map[embed])

    return results


def extract_article(docx_path, output_dir):
    """Extract one docx file into structured content"""
    fname = os.path.basename(docx_path)
    name_stem = os.path.splitext(fname)[0]

    # Determine article ID
    article_id = None
    for key, aid in TOC_MAP.items():
        if key in name_stem:
            article_id = aid
            break

    if article_id is None:
        if '自序' in name_stem:
            article_id = '00-preface'
        elif '目錄' in name_stem:
            article_id = 'toc'
        elif '封面' in name_stem:
            article_id = 'cover'
        else:
            article_id = f'zz-{name_stem[:8]}'

    print(f'\n=== {fname} → {article_id} ===')

    doc = Document(docx_path)

    # Extract images first
    img_dir = os.path.join(output_dir, 'images')
    img_map = extract_images_from_docx(docx_path, img_dir, article_id)
    print(f'  Images extracted: {len(img_map)} files')

    # Build structured content
    blocks = []  # list of {type: 'text'|'image', content: str|list}
    seen_embeds = set()

    for para in doc.paragraphs:
        text = para.text.strip()

        # Check for images in this paragraph (deduped)
        para_imgs = find_images_in_paragraph(para, img_map, seen_embeds)

        for img_name in para_imgs:
            blocks.append({
                'type': 'image',
                'src': f'images/{img_name}',
            })

        if text:
            blocks.append({
                'type': 'text',
                'content': text,
            })

    # ---- Merge broken paragraphs ----
    # Consecutive text blocks that got split across paragraphs in the DOCX
    # (because the author pressed Enter mid-sentence) are re-joined.
    # Key indicator: prev paragraph ends with a bare CJK character (no punctuation).
    CJK_CONTINUATION_PUNCT = set('。！？，、；：」』》）—…～··""''』】')

    def is_title_like(text):
        """Heuristic: skip merging for paragraphs that look like titles/headings."""
        t = text.strip()
        if not t:
            return True
        if '【' in t:          # subtitle markers like 【金門遊】
            return True
        if len(t) < 8:          # very short lines
            return True
        if t in CHAPTER_HEADERS:
            return True
        return False

    merged = []
    i = 0
    while i < len(blocks):
        if blocks[i]['type'] != 'text' or i == len(blocks) - 1:
            merged.append(blocks[i])
            i += 1
            continue

        cur = blocks[i]['content']
        nxt = blocks[i + 1]

        if nxt['type'] == 'text':
            nxt_text = nxt['content']
            should_merge = False

            # Never merge the very first text block — it's the title line
            first_text_idx = next(
                (idx for idx, b in enumerate(blocks) if b['type'] == 'text'), None
            )

            if cur and not is_title_like(cur) and i != first_text_idx:
                # Ends with a bare character (no punctuation) → definitely broken
                if cur[-1] not in CJK_CONTINUATION_PUNCT and not cur[-1].isspace():
                    should_merge = True

            if should_merge:
                blocks[i]['content'] = cur + nxt_text
                blocks.pop(i + 1)
                continue

        merged.append(blocks[i])
        i += 1

    blocks = merged

    # If no images found via XML, try inline_shapes fallback
    if not seen_embeds and doc.inline_shapes:
        print(f'  Warning: inline_shapes={len(doc.inline_shapes)} but no XML images found')

    # Determine title - skip chapter/section headers
    title = ''
    subtitle = ''
    author = '林樺'

    text_blocks = [b['content'] for b in blocks if b['type'] == 'text']
    # Find the first paragraph that looks like a real article title (not a chapter header)
    for tb in text_blocks:
        if tb.strip() in CHAPTER_HEADERS:
            continue
        # Skip empty-looking lines
        lines = [l.strip() for l in tb.split('\n') if l.strip()]
        for line in lines:
            if line in CHAPTER_HEADERS:
                continue
            if '【' in line:
                # Extract title from 【xxx】title format
                parts = line.split('】')
                title = parts[-1].strip() if len(parts) > 1 else line.strip()
            else:
                title = line[:60]
            break
        if title:
            break

    # Try to find a subtitle
    found_title = False
    for tb in text_blocks:
        content = tb.strip()
        if not found_title:
            if title in content or (title and title[:20] in content):
                found_title = True
            continue
        if content and content not in CHAPTER_HEADERS and len(content) < 40 and title not in content:
            subtitle = content
            break

    # Count stats
    cjk_count = sum(1 for b in blocks if b['type'] == 'text' for c in b['content'] if '\u4e00' <= c <= '\u9fff')
    img_total = sum(1 for b in blocks if b['type'] == 'image')

    article = {
        'id': article_id,
        'file': fname,
        'zh': title,
        'en': '',
        'subtitle': subtitle,
        'author': author,
        'blocks': blocks,
        'stats': {
            'chars': cjk_count,
            'unique_images': img_total,
            'paragraphs': len(text_blocks),
        }
    }

    # Save per-article JSON
    article_path = os.path.join(output_dir, f'{article_id}.json')
    with open(article_path, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)

    print(f'  Saved: {article_path} ({cjk_count} chars, {img_total} images)')

    return article


def build_master_index(articles):
    """Build the master book/data.json from extracted articles"""
    # Sort: cover, toc, preface, then numbered articles
    order = {
        'cover': 0,
        'toc': 1,
        '00-preface': 2,
    }
    for aid, idx in TOC_MAP.items():
        order[TOC_MAP[aid]] = 10 + list(TOC_MAP.values()).index(TOC_MAP[aid])

    sorted_articles = sorted(articles, key=lambda a: order.get(a['id'], 99))

    # Chapter grouping - all travel articles go into 第一輯
    chapter1_ids = set(v for k, v in TOC_MAP.items())

    # Filter: only include articles that belong to the chapter
    chapter1_articles = [a for a in sorted_articles if a['id'] in chapter1_ids]

    chapters = [
        {
            'zh': '第一輯 向世界出發',
            'en': 'Part I: To the World',
            'articles': [{
                'id': a['id'],
                'zh': a['zh'],
                'en': a.get('en', ''),
                'subtitle': a.get('subtitle', ''),
                'file': a['file'],
                'stats': a['stats'],
            } for a in chapter1_articles]
        },
    ]

    master = {
        'title': '我的人生旅行',
        'title_en': 'A Life Unfolded in Miles',
        'author': '林樺',
        'author_en': 'Lin Hua',
        'total_articles': len(articles),
        'total_chars': sum(a['stats']['chars'] for a in articles),
        'total_images': sum(a['stats']['unique_images'] for a in articles),
        'chapters': chapters,
        'articles': [{
            'id': a['id'],
            'zh': a['zh'],
            'en': a.get('en', ''),
            'subtitle': a.get('subtitle', ''),
            'file': a['file'],
            'stats': a['stats'],
        } for a in sorted_articles],
    }

    return master


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='dist')
    args = parser.parse_args()

    output_base = os.path.join(ROOT, args.output_dir, 'book')
    os.makedirs(output_base, exist_ok=True)
    img_out = os.path.join(output_base, 'images')
    os.makedirs(img_out, exist_ok=True)

    # Also copy to assets/images/book/ for source control
    os.makedirs(ASSETS_IMG_DIR, exist_ok=True)

    docx_files = sorted([
        os.path.join(BOOK_DIR, f) for f in os.listdir(BOOK_DIR)
        if f.endswith('.docx') and not f.startswith('~$')
    ])

    print(f'Found {len(docx_files)} docx files')
    print(f'Output: {output_base}')

    all_articles = []
    for docx_path in docx_files:
        article = extract_article(docx_path, output_base)
        all_articles.append(article)

        # Also copy images to assets/ for version control
        article_img_dir = os.path.join(ASSETS_IMG_DIR, article['id'])
        os.makedirs(article_img_dir, exist_ok=True)
        src_img_dir = os.path.join(output_base, 'images')
        if os.path.exists(src_img_dir):
            for f in os.listdir(src_img_dir):
                if f.startswith(article['id']):
                    src = os.path.join(src_img_dir, f)
                    dst = os.path.join(article_img_dir, f)
                    try:
                        shutil.copy2(src, dst)
                    except:
                        pass

    # Build master index
    master = build_master_index(all_articles)
    master_path = os.path.join(output_base, 'data.json')
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    print(f'\n{"="*60}')
    print(f'Master index: {master_path}')
    print(f'Total articles: {master["total_articles"]}')
    print(f'Total chars: {master["total_chars"]:,}')
    print(f'Total images: {master["total_images"]}')
    print(f'Done.')


if __name__ == '__main__':
    main()

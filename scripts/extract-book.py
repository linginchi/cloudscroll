# -*- coding: utf-8 -*-
"""
scripts/extract-book.py

Extract text + images from all docx files across all 3 volumes.
Output structured JSON + images to assets/images/book/ and dist/book/

Usage: python scripts/extract-book.py
       python scripts/extract-book.py --output-dir dist  (default)
"""

import os, sys, json, shutil, re, zipfile, tempfile
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# Watermark configuration
WATERMARK_TEXT = '雲箋文舍'
WATERMARK_FONT_PATH = 'C:/Windows/Fonts/STKAITI.TTF'
WATERMARK_OPACITY = 0x50  # alpha channel: 0x00=transparent, 0xFF=opaque, ~31% opacity
WATERMARK_MARGIN_RATIO = 0.04  # distance from right/bottom edge as fraction of image dimension

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, 'book')
V2_BOOK_DIR = os.path.join(BOOK_DIR, '我的人生旅行第二輯')
V3_BOOK_DIR = os.path.join(BOOK_DIR, '我的人生旅行第三輯')
V4_BOOK_DIR = os.path.join(BOOK_DIR, '我的人生旅行第四輯')
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


def _apply_watermark(img_bytes, ext):
    """Add a semi-transparent 「雲箋文舍」 watermark to the bottom-right corner."""
    try:
        from io import BytesIO
        img = Image.open(BytesIO(img_bytes))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        w, h = img.size
        font_size = max(int(w * 0.085), 18)
        try:
            font = ImageFont.truetype(WATERMARK_FONT_PATH, font_size)
        except Exception:
            font = ImageFont.load_default()
        bbox = font.getbbox(WATERMARK_TEXT)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        margin_x = max(int(w * WATERMARK_MARGIN_RATIO), 8)
        margin_y = max(int(h * WATERMARK_MARGIN_RATIO), 8)
        x = w - tw - margin_x
        y = h - th - margin_y
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.text((x, y), WATERMARK_TEXT, font=font,
                   fill=(255, 255, 255, WATERMARK_OPACITY))
        result = Image.alpha_composite(img, overlay)
        out = BytesIO()
        fmt = 'PNG' if ext == '.png' else 'JPEG'
        if fmt == 'JPEG':
            result = result.convert('RGB')
        result.save(out, format=fmt, quality=88)
        return out.getvalue()
    except Exception as e:
        print(f'    Watermark warning: {e}')
        return img_bytes


TOC_MAP = {
    '台湾': '01-taiwan',
    '菲岛': '02-philippines',
    '菲島': '02-philippines',
    '霧鎖雲頂': '03-kuala-lumpur',
    '檳島親遊': '04-penang',
    '麗星': '05-vietnam',
    '長今': '06-korea',
    '新西蘭': '07-new-zealand',
    '勝景怡人': '08-usa',
    '澳門': '09-macau',
    '浯洲': '10-kinmen',
}

V2_TOC_MAP = {
    '京城勝跡': 'v2-01',
    '東滬': 'v2-02',
    '蘇城': 'v2-03',
    '杭郡': 'v2-04',
    '津門': 'v2-05',
    '三亞': 'v2-06',
    '遼寧三城': 'v2-07',
    '北國雙城': 'v2-08',
    '冰城': 'v2-09',
    '珠水': 'v2-10',
    '鵬城': 'v2-11',
    '中山行旅': 'v2-12',
    '珠海': 'v2-13',
    '鷺島': 'v2-14',
    '杏壇': 'v2-15',
    '南平': 'v2-16',
    '福師大': 'v2-17',
    '韶山': 'v2-18',
    '桂林山水行': 'v2-19',
    '商都': 'v2-20',
    '河洛夢': 'v2-21',
    '雲水謠': 'v2-22',
    '溫情': 'v2-23',
    '晋水': 'v2-24',
}

V2_ARTICLES = [
    {'id': 'v2-01', 'zh': '屢次京城勝跡記', 'en': 'Chronicles of the Capital'},
    {'id': 'v2-02', 'zh': '東滬行遊雜筆', 'en': 'Sketches of Shanghai'},
    {'id': 'v2-03', 'zh': '蘇城名山名鎮遊記', 'en': 'Suzhou: Hills and Towns'},
    {'id': 'v2-04', 'zh': '遊覽杭郡千古勝', 'en': 'Hangzhou: A Thousand Years of Splendour'},
    {'id': 'v2-05', 'zh': '津門故里遊覽隨筆', 'en': 'Tianjin: The Portal of the North'},
    {'id': 'v2-06', 'zh': '三亞山海遊覽小記', 'en': 'Sanya: Between the Mountains and the Sea'},
    {'id': 'v2-07', 'zh': '遼寧三城紀行', 'en': 'Three Cities of Liaoning'},
    {'id': 'v2-08', 'zh': '北國雙城札記', 'en': 'Twin Cities of the North'},
    {'id': 'v2-09', 'zh': '閒寫冰城遊思', 'en': 'Reflections on the Ice City'},
    {'id': 'v2-10', 'zh': '一江珠水 萬里花城', 'en': 'City of the Pearl River'},
    {'id': 'v2-11', 'zh': '鵬城遊歷雜記', 'en': 'Notes on Shenzhen'},
    {'id': 'v2-12', 'zh': '中山行旅錄', 'en': 'A Journey to Zhongshan'},
    {'id': 'v2-13', 'zh': '海隅珠海札記', 'en': 'Zhuhai by the Sea'},
    {'id': 'v2-14', 'zh': '尋味廈門  鷺島遊錄', 'en': 'In Search of Amoy'},
    {'id': 'v2-15', 'zh': '杏壇戀廈門', 'en': 'Cherishing Xiamen'},
    {'id': 'v2-16', 'zh': '南平探親閒遊  武夷山水留蹤', 'en': 'Nanping and Wuyi Mountain'},
    {'id': 'v2-17', 'zh': '福師大訪學行', 'en': 'A Visit to Fujian Normal University'},
    {'id': 'v2-18', 'zh': '山水藏靈秀  韶山仰偉人', 'en': 'Zhangjiajie and Shaoshan'},
    {'id': 'v2-19', 'zh': '桂林山水行記', 'en': 'A Journey to Guilin'},
    {'id': 'v2-20', 'zh': '商都覽勝  古廟謁忠', 'en': 'Zhengzhou and Weihui'},
    {'id': 'v2-21', 'zh': '一場河洛夢  半部商丘史', 'en': 'Luoyang and Shangqiu'},
    {'id': 'v2-22', 'zh': '一方雲水謠  萬座土樓情', 'en': 'Tulou and Yunshuiyao'},
    {'id': 'v2-23', 'zh': '一城風物  滿懷溫情', 'en': 'The Charms of Zhangzhou'},
    {'id': 'v2-24', 'zh': '晋水涵千古  泉城載萬疆', 'en': 'The Eternal City of Quanzhou'},
]

V3_TOC_MAP = {
    '鶴髮': 'v3-01',
    '髮松姿': 'v3-01',
    '新加坡國立': 'v3-02',
    '再覽獅城': 'v3-03',
    '星耀樟宜': 'v3-04',
    '奇花': 'v3-05',
    '文化路': 'v3-06',
    '桃城': 'v3-07',
    '經典景點之一': 'v3-08',
    '经典景点之一': 'v3-08',
    '經典景點之二': 'v3-09',
    '经典景点之二': 'v3-09',
    '布袋港': 'v3-10',
    '映月橋': 'v3-11',
    '月影潭心': 'v3-12',
    '彌陀': 'v3-13',
    '除夕': 'v3-14',
    '元旦': 'v3-15',
    '嘉義大學': 'v3-16',
    '义大學': 'v3-16',
    '湖美': 'v3-17',
    '鎮天宮': 'v3-18',
    '紫雲寺': 'v3-19',
}

V3_ARTICLES = [
    {'id': 'v3-01', 'zh': '鶴髮松姿遊獅城', 'en': 'Silver Hair, Lingering Grace in the Lion City'},
    {'id': 'v3-02', 'zh': '新加坡國立大學參觀隨筆', 'en': 'A Visit to the National University of Singapore'},
    {'id': 'v3-03', 'zh': '再覽獅城華埠風光', 'en': 'Revisiting the Sights of Singapore Chinatown'},
    {'id': 'v3-04', 'zh': '獅城星耀樟宜漫記', 'en': 'Jewel Changi: A Leisurely Note'},
    {'id': 'v3-05', 'zh': '飽賞獅城奇花嘉木', 'en': 'Admiring the Flora of Singapore'},
    {'id': 'v3-06', 'zh': '嘉義文化路夜市夜韻遊記', 'en': 'A Night at Chiayi Culture Road Night Market'},
    {'id': 'v3-07', 'zh': '桃城影塔  射日風情', 'en': 'Shadow Tower of Peach City, Under the Sun'},
    {'id': 'v3-08', 'zh': '漫遊嘉義經典景點之一', 'en': 'Classic Sights of Chiayi, Part One'},
    {'id': 'v3-09', 'zh': '漫遊嘉義經典景點之二', 'en': 'Classic Sights of Chiayi, Part Two'},
    {'id': 'v3-10', 'zh': '探索布袋港的風情', 'en': 'Exploring the Charm of Budai Harbour'},
    {'id': 'v3-11', 'zh': '暮遊爾陀映月橋', 'en': 'An Evening Stroll by the Moonlit Bridge'},
    {'id': 'v3-12', 'zh': '暮遊月影潭心', 'en': 'Moon Shadows on the Lake at Dusk'},
    {'id': 'v3-13', 'zh': '閒逛嘉義彌陀夜市', 'en': 'A Leisurely Walk Through Chiayi Mituo Night Market'},
    {'id': 'v3-14', 'zh': '難忘的2023年除夕夜', 'en': 'An Unforgettable New Year\'s Eve, 2023'},
    {'id': 'v3-15', 'zh': '嘉義元旦夜賞漫遊', 'en': 'A New Year\'s Day Ramble in Chiayi'},
    {'id': 'v3-16', 'zh': '國立嘉義大學參觀紀行', 'en': 'A Visit to National Chiayi University'},
    {'id': 'v3-17', 'zh': '萬人逛湖美商展賞嘉義夜市風情', 'en': 'Ten Thousand at the Lakeview Fair: Chiayi Night Market'},
    {'id': 'v3-18', 'zh': '暢遊鎮天宮  瞻仰桃園盟', 'en': 'Zhentian Temple and the Oath of the Peach Garden'},
    {'id': 'v3-19', 'zh': '半天岩紫雲寺遊半天', 'en': 'Half a Day at Ziyun Temple, Bantianyan'},
]

V4_TOC_MAP = {
    '五星校友': 'v4-01',
    '慶回歸': 'v4-02',
    '殫見洽聞': 'v4-03',
    '殫見': 'v4-03',
    '禪城': 'v4-04',
    '開元古刹': 'v4-05',
    '開元': 'v4-05',
    '觀天眼': 'v4-06',
    '天眼': 'v4-06',
    '守歲': 'v4-07',
}

V4_ARTICLES = [
    {'id': 'v4-01', 'zh': '五校友鵬城歡聚遊', 'en': 'Alumni Reunion in Pengcheng'},
    {'id': 'v4-02', 'zh': '慶回歸、敘鄉情、敬老獎學盛會', 'en': 'A Gala of Homecoming and Honour'},
    {'id': 'v4-03', 'zh': '殫見洽聞 通達古今', 'en': 'Erudition: Bridging Past and Present'},
    {'id': 'v4-04', 'zh': '遊禪城鳳城隨筆', 'en': 'Sketches of Chancheng and Fengcheng'},
    {'id': 'v4-05', 'zh': '重遊開元古刹 再悟泉郡千年', 'en': 'Revisiting Kaiyuan Temple, Quanzhou'},
    {'id': 'v4-06', 'zh': '閒步觀天眼 蘩樓品清茶', 'en': 'A Stroll by the Tianyan, Tea at Fanlou'},
    {'id': 'v4-07', 'zh': '鵬城守歲 萬象歡筵', 'en': 'New Year\'s Eve Gala in Shenzhen'},
]

CHAPTER_HEADERS = {
    '第一輯 向世界出發',
    '第二輯 神州大地之行',
    '第三輯 中外覽勝錄',
    '第四輯 旅遊天地',
    'Part I: To the World',
    'Part II: Journeys Across China',
    'Part III: Sights at Home and Abroad',
    'Part IV: Traveller\'s Paradise',
}


def _build_rotation_map(zip_file):
    """Parse word/document.xml to build a map of rId -> (cw_degrees, flip_h, flip_v)."""
    rot_map = {}
    try:
        if 'word/document.xml' not in zip_file.namelist():
            return rot_map
        doc_xml = zip_file.read('word/document.xml')
        root = etree.fromstring(doc_xml)

        A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

        for xfrm in root.findall(f'.//{{{A_NS}}}xfrm'):
            rot = xfrm.get('rot')
            flip_h = xfrm.get('flipH')
            flip_v = xfrm.get('flipV')
            if not rot and not flip_h and not flip_v:
                continue

            # Walk up to the pic:pic element (xfrm → spPr → pic)
            sp_pr = xfrm.getparent()
            if sp_pr is None:
                continue
            pic = sp_pr.getparent()
            if pic is None:
                continue

            blip = pic.find(f'.//{{{A_NS}}}blip')
            if blip is None:
                continue
            embed = blip.get(f'{{{R_NS}}}embed')
            if not embed:
                continue

            deg = int(rot) / 60000 if rot else 0
            rot_map[embed] = (deg, flip_h == '1', flip_v == '1')
    except Exception:
        pass
    return rot_map


def _apply_image_transforms(img_bytes, ext, rotation_deg, flip_h, flip_v):
    """Apply rotation (clockwise) + flips to raw image bytes, return new bytes."""
    from io import BytesIO
    img = Image.open(BytesIO(img_bytes))

    if flip_h:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_v:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    if rotation_deg != 0:
        # OOXML stores clockwise rotation; PIL rotates counter-clockwise — negate
        img = img.rotate(-rotation_deg, expand=True, resample=Image.LANCZOS)

    out = BytesIO()
    fmt = 'PNG' if ext == '.png' else 'JPEG'
    if fmt == 'JPEG' and img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.save(out, format=fmt, quality=90)
    return out.getvalue()


def extract_images_from_docx(docx_path, output_dir, article_id):
    img_map = {}
    os.makedirs(output_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            all_files = z.namelist()
            img_files = [f for f in all_files if f.startswith('word/media/')]

            # Build rotation map from document.xml (rId → (deg, flipH, flipV))
            rot_map = _build_rotation_map(z)

            # Build rId → media-path map from rels
            rid_to_media = {}
            rels_path = 'word/_rels/document.xml.rels'
            if rels_path in all_files:
                with z.open(rels_path) as f:
                    rels_root = etree.fromstring(f.read())
                for rel in rels_root:
                    rid = rel.get('Id')
                    target = rel.get('Target', '')
                    target_full = f'word/{target}' if not target.startswith('word/') else target
                    if rid and target_full in img_files:
                        rid_to_media[rid] = target_full

            for i, img_path in enumerate(sorted(img_files)):
                ext = os.path.splitext(img_path)[1].lower()
                if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'):
                    ext = '.jpg'
                out_name = f'{article_id}_{i+1:03d}{ext}'
                out_path = os.path.join(output_dir, out_name)

                with z.open(img_path) as src:
                    img_data = src.read()

                # Look up rotation/flip for this image via its rId(s)
                rotation_deg = 0
                flip_h = False
                flip_v = False
                for rid, mp in rid_to_media.items():
                    if mp == img_path and rid in rot_map:
                        rotation_deg, flip_h, flip_v = rot_map[rid]
                        break

                # Apply rotation/flip BEFORE watermark
                if rotation_deg != 0 or flip_h or flip_v:
                    img_data = _apply_image_transforms(img_data, ext, rotation_deg, flip_h, flip_v)

                # Apply watermark
                watermarked = _apply_watermark(img_data, ext)
                with open(out_path, 'wb') as dst:
                    dst.write(watermarked)

                img_map[img_path] = out_name

                # Map rIds to output filename
                for rid in rid_to_media:
                    if rid_to_media[rid] == img_path:
                        img_map[rid] = out_name

    except Exception as e:
        print(f'  Warning: zip extraction failed for images: {e}')

    return img_map


def find_images_in_paragraph(para, img_map, seen_embeds=None):
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


def extract_article(docx_path, output_dir, toc_map=None):
    if toc_map is None:
        toc_map = TOC_MAP

    fname = os.path.basename(docx_path)
    name_stem = os.path.splitext(fname)[0]

    article_id = None
    for key, aid in toc_map.items():
        if key in name_stem:
            article_id = aid
            break

    if article_id is None:
        if '自序' in name_stem:
            article_id = '00-preface'
        elif '目錄' in name_stem and '第二輯' not in name_stem and '第三輯' not in name_stem:
            article_id = 'toc'
        elif '封面' in name_stem:
            article_id = 'cover'
        else:
            article_id = f'zz-{name_stem[:8]}'

    print(f'\n=== {fname} → {article_id} ===')

    doc = Document(docx_path)

    img_dir = os.path.join(output_dir, 'images')
    img_map = extract_images_from_docx(docx_path, img_dir, article_id)
    print(f'  Images extracted: {len(img_map)} files')

    blocks = []
    seen_embeds = set()

    for para in doc.paragraphs:
        text = para.text.strip()

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

    CJK_CONTINUATION_PUNCT = set('。！？，、；：」』》）—…～··""''』】')

    def is_title_like(text):
        t = text.strip()
        if not t:
            return True
        if '【' in t:
            return True
        if len(t) < 8:
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

            first_text_idx = next(
                (idx for idx, b in enumerate(blocks) if b['type'] == 'text'), None
            )

            if cur and not is_title_like(cur) and i != first_text_idx:
                if cur[-1] not in CJK_CONTINUATION_PUNCT and not cur[-1].isspace():
                    should_merge = True

            if should_merge:
                blocks[i]['content'] = cur + nxt_text
                blocks.pop(i + 1)
                continue

        merged.append(blocks[i])
        i += 1

    blocks = merged

    if not seen_embeds and doc.inline_shapes:
        print(f'  Warning: inline_shapes={len(doc.inline_shapes)} but no XML images found')

    title = ''
    subtitle = ''
    author = '林樺'

    text_blocks = [b['content'] for b in blocks if b['type'] == 'text']
    for tb in text_blocks:
        if tb.strip() in CHAPTER_HEADERS:
            continue
        lines = [l.strip() for l in tb.split('\n') if l.strip()]
        for line in lines:
            if line in CHAPTER_HEADERS:
                continue
            if '【' in line:
                parts = line.split('】')
                title = parts[-1].strip() if len(parts) > 1 else line.strip()
            else:
                title = line[:60]
            break
        if title:
            break

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

    cjk_count = sum(1 for b in blocks if b['type'] == 'text' for c in b['content'] if '\u4e00' <= c <= '\u9fff')
    img_total = sum(1 for b in blocks if b['type'] == 'image')

    # Clean 《》 from title
    title = title.replace('《', '').replace('》', '')

    # Fix: 自序 "餘生於" → "余生於"
    if article_id == '00-preface':
        for block in blocks:
            if block['type'] == 'text' and '餘生於' in block['content']:
                block['content'] = block['content'].replace('餘生於', '余生於')

    # Clean 《》 from title blocks in content (preserve body text citations)
    for block in blocks:
        if block['type'] != 'text':
            continue
        content = block['content']
        if article_id == 'toc':
            # TOC: every line references an article title, clean all
            block['content'] = content.replace('《', '').replace('》', '')
        elif title and title in content.replace('《', '').replace('》', ''):
            # Block contains the article title (after stripping 《》), clean 《》 from it
            block['content'] = content.replace('《', '').replace('》', '')

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

    article_path = os.path.join(output_dir, f'{article_id}.json')
    with open(article_path, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)

    print(f'  Saved: {article_path} ({cjk_count} chars, {img_total} images)')

    return article


def build_master_index(articles_v1, articles_v2, articles_v3, articles_v4):
    """Build the master book/data.json from all four volumes"""
    v1_order = {
        'cover': 0,
        'toc': 1,
        '00-preface': 2,
    }
    for aid, idx in TOC_MAP.items():
        v1_order[TOC_MAP[aid]] = 10 + list(TOC_MAP.values()).index(TOC_MAP[aid])

    sorted_v1 = sorted(articles_v1, key=lambda a: v1_order.get(a['id'], 99))

    v2_order = {}
    for i, meta in enumerate(V2_ARTICLES):
        v2_order[meta['id']] = 100 + i

    sorted_v2 = sorted(
        [a for a in articles_v2 if a['id'] in v2_order],
        key=lambda a: v2_order.get(a['id'], 999)
    )

    v3_order = {}
    for i, meta in enumerate(V3_ARTICLES):
        v3_order[meta['id']] = 200 + i

    sorted_v3 = sorted(
        [a for a in articles_v3 if a['id'] in v3_order],
        key=lambda a: v3_order.get(a['id'], 999)
    )

    v4_order = {}
    for i, meta in enumerate(V4_ARTICLES):
        v4_order[meta['id']] = 300 + i

    sorted_v4 = sorted(
        [a for a in articles_v4 if a['id'] in v4_order],
        key=lambda a: v4_order.get(a['id'], 999)
    )

    ch1_ids = set(v for k, v in TOC_MAP.items())
    ch1_articles = [a for a in sorted_v1 if a['id'] in ch1_ids]

    ch2_ids = set(a['id'] for a in V2_ARTICLES)
    ch2_articles = [a for a in sorted_v2 if a['id'] in ch2_ids]

    ch3_ids = set(a['id'] for a in V3_ARTICLES)
    ch3_articles = [a for a in sorted_v3 if a['id'] in ch3_ids]

    ch4_ids = set(a['id'] for a in V4_ARTICLES)
    ch4_articles = [a for a in sorted_v4 if a['id'] in ch4_ids]

    def art_info(a):
        return {
            'id': a['id'],
            'zh': a['zh'],
            'en': a.get('en', ''),
            'subtitle': a.get('subtitle', ''),
            'file': a['file'],
            'stats': a['stats'],
        }

    chapters = [
        {
            'zh': '第一輯 向世界出發',
            'en': 'Part I: To the World',
            'articles': [art_info(a) for a in ch1_articles],
        },
        {
            'zh': '第二輯 神州大地之行',
            'en': 'Part II: Journeys Across China',
            'articles': [art_info(a) for a in ch2_articles],
        },
        {
            'zh': '第三輯 中外覽勝錄',
            'en': 'Part III: Sights at Home and Abroad',
            'articles': [art_info(a) for a in ch3_articles],
        },
        {
            'zh': '第四輯 旅遊天地',
            'en': 'Part IV: Traveller\'s Paradise',
            'articles': [art_info(a) for a in ch4_articles],
        },
    ]

    all_articles = sorted_v1 + sorted_v2 + sorted_v3 + sorted_v4

    master = {
        'title': '我的人生旅行',
        'title_en': 'A Life Unfolded in Miles',
        'author': '林樺',
        'author_en': 'Lin Hua',
        'total_articles': len(all_articles),
        'total_chars': sum(a['stats']['chars'] for a in all_articles),
        'total_images': sum(a['stats']['unique_images'] for a in all_articles),
        'chapters': chapters,
        'articles': [art_info(a) for a in all_articles],
    }

    return master


def process_volume_files(docx_files, output_base, toc_map):
    """Process a list of docx files, return list of articles"""
    articles = []
    for docx_path in docx_files:
        article = extract_article(docx_path, output_base, toc_map=toc_map)
        articles.append(article)

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
    return articles


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='dist')
    args = parser.parse_args()

    output_base = os.path.join(ROOT, args.output_dir, 'book')
    os.makedirs(output_base, exist_ok=True)
    img_out = os.path.join(output_base, 'images')
    os.makedirs(img_out, exist_ok=True)

    os.makedirs(ASSETS_IMG_DIR, exist_ok=True)

    # ── Volume 1 ──
    v1_files = sorted([
        os.path.join(BOOK_DIR, f) for f in os.listdir(BOOK_DIR)
        if f.endswith('.docx') and not f.startswith('~$') and not os.path.isdir(os.path.join(BOOK_DIR, f))
    ])
    print(f'\n{"="*60}')
    print(f'Volume 1: {len(v1_files)} docx files in book/')
    print(f'{"="*60}')
    articles_v1 = process_volume_files(v1_files, output_base, TOC_MAP)

    # ── Volume 2 ──
    articles_v2 = []
    if os.path.isdir(V2_BOOK_DIR):
        v2_files = sorted([
            os.path.join(V2_BOOK_DIR, f) for f in os.listdir(V2_BOOK_DIR)
            if f.endswith('.docx') and not f.startswith('~$') and '目錄' not in f
        ])
        print(f'\n{"="*60}')
        print(f'Volume 2: {len(v2_files)} docx files in 我的人生旅行第二輯/')
        print(f'{"="*60}')
        articles_v2 = process_volume_files(v2_files, output_base, V2_TOC_MAP)
    else:
        print(f'Volume 2 directory not found: {V2_BOOK_DIR}')

    # ── Volume 3 ──
    articles_v3 = []
    if os.path.isdir(V3_BOOK_DIR):
        v3_files = sorted([
            os.path.join(V3_BOOK_DIR, f) for f in os.listdir(V3_BOOK_DIR)
            if f.endswith('.docx') and not f.startswith('~$') and '目錄' not in f and '目录' not in f
        ])
        print(f'\n{"="*60}')
        print(f'Volume 3: {len(v3_files)} docx files in 我的人生旅行第三輯/')
        print(f'{"="*60}')
        articles_v3 = process_volume_files(v3_files, output_base, V3_TOC_MAP)
    else:
        print(f'Volume 3 directory not found: {V3_BOOK_DIR}')

    # ── Volume 4 ──
    articles_v4 = []
    if os.path.isdir(V4_BOOK_DIR):
        v4_files = sorted([
            os.path.join(V4_BOOK_DIR, f) for f in os.listdir(V4_BOOK_DIR)
            if f.endswith('.docx') and not f.startswith('~$') and '目錄' not in f and '目录' not in f
        ])
        print(f'\n{"="*60}')
        print(f'Volume 4: {len(v4_files)} docx files in 我的人生旅行第四輯/')
        print(f'{"="*60}')
        articles_v4 = process_volume_files(v4_files, output_base, V4_TOC_MAP)
    else:
        print(f'Volume 4 directory not found: {V4_BOOK_DIR}')

    # ── Build master index ──
    master = build_master_index(articles_v1, articles_v2, articles_v3, articles_v4)
    master_path = os.path.join(output_base, 'data.json')
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    print(f'\n{"="*60}')
    print(f'Master index: {master_path}')
    print(f'Total articles: {master["total_articles"]}')
    print(f'Total chars: {master["total_chars"]:,}')
    print(f'Total images: {master["total_images"]}')
    print(f'Chapters: {len(master["chapters"])}')
    for ch in master['chapters']:
        print(f'  {ch["zh"]} — {len(ch["articles"])} articles')
    print(f'Done.')


if __name__ == '__main__':
    main()

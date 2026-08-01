# -*- coding: utf-8 -*-
"""
Extract 《雲心文集》 articles in exact TOC order.

Source: book/雲心文集/
Output: src/yunxin/*.json + src/yunxin/data.json

Order MUST follow 《雲心文集目錄》. Do not reorder by filename.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from docx import Document

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / 'book' / '雲心文集'
OUT_DIR = ROOT / 'src' / 'yunxin'

# Exact TOC order. file = exact filename under book/雲心文集/
# title = display title (正文名 when it differs from 目錄名)
ARTICLES = [
    {
        'id': '00-preface',
        'section': 'preface',
        'section_title': '自序',
        'num': '00',
        'title': '我的人生路',  # 目錄：自序《我的人生路》
        'file': '《雲心文集》自序.docx',
    },
    # 第一輯 詩
    {
        'id': '01-return-alma-mater',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '01',
        'title': '重返母校感懷',  # 正文名（目錄寫「重遊」）
        'file': '《重返母校感懷》.docx',
    },
    {
        'id': '02-mao-statue',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '02',
        'title': '毛澤東銅像',
        'file': '毛澤東銅像.docx',
    },
    {
        'id': '03-guilin-trip',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '03',
        'title': '桂林之遊有感',
        'file': '桂林之遊有感.docx',
    },
    {
        'id': '04-sentosa',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '04',
        'title': '重遊故地聖陶沙',
        'file': '《重遊故地聖陶沙》詩一首.docx',
    },
    {
        'id': '05-yangzheng',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '05',
        'title': '養正中學同窗聚會感言',
        'file': '養正中學同窗聚會感言.docx',
    },
    {
        'id': '06-pengcheng',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '06',
        'title': '耆年校友共遊鵬城感懷',
        'file': '耆年校友共遊鵬城感懷.docx',
    },
    {
        'id': '07-two-poems',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '07',
        'title': '詩二首',
        'file': '詩二首.docx',
    },
    {
        'id': '08-cishan',
        'section': 'poetry',
        'section_title': '第一輯  詩',
        'num': '08',
        'title': '遊香港慈山寺有感',
        'file': '《遊香港慈山寺有感》 .docx',
    },
    # 第二輯 詩詞
    {
        'id': '09-guilin-landscape',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '01',
        'title': '七律·桂林山水甲天下',
        'file': '桂林山水甲天下(1).docx',
    },
    {
        'id': '10-jiangshan',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '02',
        'title': '七絕·江山如畫',
        'file': '《七絕·江山如畫》(1).docx',
    },
    {
        'id': '11-bigan',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '03',
        'title': '七律·瞻仰比干陵墓',
        'file': '七 律 •瞻比干陵墓(1).docx',
    },
    {
        'id': '12-bao-zheng',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '04',
        'title': '七律·咏包拯',
        'file': '七律·咏包拯(1).docx',
    },
    {
        'id': '13-jiageng',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '05',
        'title': '七律·華僑領袖嘉庚頌',
        'file': '七律·華僑領袖嘉庚頌(1).docx',
    },
    {
        'id': '14-xiamen-garden',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '06',
        'title': '七律·咏海上花園廈門',
        'file': '《七律·詠海上花園廈門》(1).docx',
    },
    {
        'id': '15-qingpingle-filin',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '07',
        'title': '清平樂·慶菲律賓錦馬林氏聯鄉會六十華誕',
        'file': '清平樂•慶菲律賓錦馬林氏聯鄉會六十華誕(1).docx',
    },
    {
        'id': '16-caisangzi',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '08',
        'title': '采桑子·香江故宮',
        'file': '采桑子•香江故宮.docx',
    },
    {
        'id': '17-hk-palace',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '09',
        'title': '七律·遊香港故宮博物館',
        'file': '七律˙遊香港故宮博物館(1).docx',
    },
    {
        'id': '18-gelian-23',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '10',
        'title': '七律·慶葛聯會二十三華誕',
        'file': '七律•慶葛聯會二十三華誕(1).docx',
    },
    {
        'id': '19-qingpingle-council',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '11',
        'title': '清平樂·理事會共襄盛舉',
        'file': '清平乐•理事會共襄盛舉(1).docx',
    },
    {
        'id': '20-liantan-30',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '12',
        'title': '七律·慶蓮潭同鄉會三十華誕',
        'file': '七律•慶蓮潭同鄉會三十華誕(1).docx',
    },
    {
        'id': '21-huanxisha',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '13',
        'title': '浣溪沙·咏瑰麗的鷺島',
        'file': '浣溪沙•咏瑰麗的鷺島(1).docx',
    },
    {
        'id': '22-loyal-minister',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '14',
        'title': '七律·亘古忠臣',
        'file': '七律·亘古忠臣  (1).docx',
    },
    {
        'id': '23-mantingfang',
        'section': 'ci',
        'section_title': '第二輯  詩詞',
        'num': '15',
        'title': '滿庭芳·葛聯會廿六華誕',
        'file': '滿庭芳•葛聯會廿六華誕  詞牌.docx',
    },
    # 第三輯 散文
    {
        'id': '24-weihui',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '01',
        'title': '謁祖衛輝紀忠魂',
        'file': '謁祖衛輝紀忠魂.docx',
    },
    {
        'id': '25-jiageng-qingming',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '02',
        'title': '清明懷念嘉庚先生',
        'file': '清明懷念嘉庚先生.docx',
    },
    {
        'id': '26-yuanding',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '03',
        'title': '樂為園丁哺芬芳',
        'file': '樂為園丁哺芬芳 .docx',
    },
    {
        'id': '27-gelian-zuzi',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '04',
        'title': '葛州聯誼會足志',
        'file': '葛州聯誼會足志.docx',
    },
    {
        'id': '28-gezhou',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '05',
        'title': '我的家鄉葛州',
        'file': '我的家鄉葛州 - .docx',
    },
    {
        'id': '29-zhongxiao',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '06',
        'title': '忠孝續文脈',
        'file': '忠孝續文脈.docx',
    },
    {
        'id': '30-guishan',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '07',
        'title': '飽覽天下桂山秋',
        'file': '飽覽天下桂山秋.docx',
    },
    {
        'id': '31-feidao',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '08',
        'title': '遠赴菲島敘鄉誼',
        'file': '遠赴菲島敘鄉誼.docx',
    },
    {
        'id': '32-chunming',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '09',
        'title': '光輝年華 輝粲春茗',
        'file': '光輝年華 輝粲春茗 .docx',
    },
    {
        'id': '33-yangquyun',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '10',
        'title': '緬懷革命先驅楊衢雲',
        'file': '緬懷革命先驅楊衢雲.docx',
    },
    {
        'id': '34-xiangjiang-haojiang',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '11',
        'title': '香江濠江萬水情',
        'file': '香江濠江萬水情.docx',
    },
    {
        'id': '35-tang-shuangxiang',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '12',
        'title': '湯公肇黌 一脈雙庠',
        'file': '湯公肇黌  一脈雙庠.docx',
    },
    {
        'id': '36-yi-tang',
        'section': 'prose',
        'section_title': '第三輯  散文',
        'num': '13',
        'title': '憶湯校長',
        'file': '憶湯校長.docx',
    },
    # 第四輯 雜記
    {
        'id': '37-xiyang-huanghun',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '01',
        'title': '夕陽與黃昏',
        'file': '夕阳与黄昏.docx',
    },
    {
        'id': '38-rensheng-zheli',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '02',
        'title': '人生哲理',
        'file': '人生哲理.docx',
    },
    {
        'id': '39-rensheng-ganwu',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '03',
        'title': '人生感悟勵志錄',
        'file': '人生感悟勵志錄.docx',
    },
    {
        'id': '40-neikeng-zonghui',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '04',
        'title': '代香港內坑鎮聯鄉總會題辭賀內坑鎮僑聯會僑史館開館誌慶',
        'file': '代内坑总会、蓮潭及葛州鄉会撰赠题辞.docx',
    },
    {
        'id': '41-liantan-neikeng',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '05',
        'title': '代蓮潭同鄉會題辭賀內坑鎮僑聯會僑史館開館誌慶',
        'file': '代内坑总会、蓮潭及葛州鄉会撰赠题辞.docx',
    },
    {
        'id': '42-gezhou-neikeng',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '06',
        'title': '代葛州聯誼會題辭賀內坑鎮僑聯會僑史館開館誌慶',
        'file': '代内坑总会、蓮潭及葛州鄉会撰赠题辞.docx',
    },
    {
        'id': '43-bamin-yang',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '07',
        'title': '代香港八閩楊氏宗親聯合會撰贈賀全球楊氏祭祖盛會',
        'file': '代八閩楊氏宗親會、杨衢衢云纪念协会、蓮潭鄉会撰贈賀楊氏祭祖盛會圓滿成功 - 複製.docx',
    },
    {
        'id': '44-yangquyun-assoc',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '08',
        'title': '代香港楊衢雲紀念協會撰贈賀全球楊氏祭祖盛會',
        'file': '代八閩楊氏宗親會、杨衢衢云纪念协会、蓮潭鄉会撰贈賀楊氏祭祖盛會圓滿成功 - 複製.docx',
    },
    {
        'id': '45-liantan-yang',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '09',
        'title': '代蓮潭同鄉會撰贈賀全球楊氏祭祖盛會',
        'file': '代八閩楊氏宗親會、杨衢衢云纪念协会、蓮潭鄉会撰贈賀楊氏祭祖盛會圓滿成功 - 複製.docx',
    },
    {
        'id': '46-linhua-zupu',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '10',
        'title': '林樺撰賀香港葛州林氏暨族譜付梓',
        'file': '林樺及代葛聯会撰賀香港葛州林氏暨族譜付梓 、赞葛聯会贤才輩出.docx',
    },
    {
        'id': '47-gezhou-zupu',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '11',
        'title': '代葛州聯誼會撰賀香港葛州林氏暨族譜付梓',
        'file': '林樺及代葛聯会撰賀香港葛州林氏暨族譜付梓 、赞葛聯会贤才輩出.docx',
    },
    {
        'id': '48-gelian-xiancai',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '12',
        'title': '林樺撰贊葛聯會賢才輩出',
        'file': '林樺及代葛聯会撰賀香港葛州林氏暨族譜付梓 、赞葛聯会贤才輩出.docx',
    },
    {
        'id': '49-feihua-taoyuan',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '13',
        'title': '代菲華桃園堂撰賀葛聯會廿六華誕',
        'file': '代菲華桃閭園堂及林桦撰賀葛聯會、林桦撰赠比干廟.docx',
    },
    {
        'id': '50-linhua-gelian26',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '14',
        'title': '林樺撰賀葛聯會廿六華誕',
        'file': '代菲華桃閭園堂及林桦撰賀葛聯會、林桦撰赠比干廟.docx',
    },
    {
        'id': '51-bigan-hefu',
        'section': 'notes',
        'section_title': '第四輯  雜記',
        'num': '15',
        'title': '林樺代葛聯會撰贈衛輝比干紀念會、衛輝比干廟加賀幅',
        'file': '代菲華桃閭園堂及林桦撰賀葛聯會、林桦撰赠比干廟.docx',
    },
]


def clean_para(text: str) -> str:
    t = (text or '').replace('\u00a0', ' ').strip()
    t = re.sub(r'[ \t]+', ' ', t)
    # 標點前多餘空格、句號後誤加逗號
    t = re.sub(r' +([，。！？：；、])', r'\1', t)
    t = re.sub(r'([。！？])\s*，', r'\1', t)
    # 破折號寫成「─-」「—— -」等
    t = re.sub(r'[─–—-]{1,2}\s*-+\s*', '——', t)
    t = re.sub(r'[─–—]{1,2}-', '——', t)
    return t


def is_genre_label(text: str) -> bool:
    t = re.sub(r'[˙•·・\s]', '', (text or '').strip())
    return t in {
        '七律', '七絕', '清平樂', '采桑子', '浣溪沙', '滿庭芳',
        '詩一首', '詩二首',
    } or bool(re.match(r'^(七律|七絕|清平樂|采桑子|浣溪沙|滿庭芳)', t))


def is_date_line(text: str) -> bool:
    t = (text or '').strip()
    if not t or len(t) > 24:
        return False
    # 二0一六年四月 / 2022.中秋 / 二0一八年 新加坡
    if re.match(r'^二[0〇○O0-9]{2,4}', t):
        return True
    if re.match(r'^20\d{2}', t):
        return True
    return False


def should_merge_paras(prev: str, nxt: str, title: str = '', section: str = '') -> bool:
    """合併因 Word 硬換行造成的半句斷段；保留詩句、標題、日期等結構行。"""
    prev = (prev or '').strip()
    nxt = (nxt or '').strip()
    if not prev or not nxt:
        return False

    # 破折號收尾多半是半句（如「古稀遊——」+「風景…」）
    if prev.endswith('——') or prev.endswith('─'):
        return True

    # 已收束的句子（含句末引號）
    if re.search(r'[。！？][」』"\u201d\u2019\'’]*$', prev):
        return False
    if re.search(r'[：；.!?;:][」』"\u201d\u2019\'’]*$', prev):
        return False

    # 逗號／頓號：短詩句保留分行；長文硬換行則合併
    if re.search(r'[，、]$', prev):
        if len(prev) <= 20 and len(nxt) <= 22:
            return False
        if len(prev) > 24 or len(nxt) > 24:
            return True
        return False

    title_key = re.sub(r'[，\s]', '', title or '')
    prev_key = re.sub(r'[，\s]', '', prev)
    if title_key and prev_key == title_key:
        return False

    if is_genre_label(prev) or is_date_line(prev):
        return False
    if is_genre_label(nxt) or is_date_line(nxt):
        return False

    # 對仗小標題（中間有空格），如「杏壇留歲月 鷺島繫情腸」
    if len(prev) <= 18 and ' ' in prev:
        return False

    # 下一行是短詩句 / 結構行：僅在明顯接續或上一行已是長文半句時合併
    cont = '的之了着過著給予」』）、,，'
    if len(nxt) <= 20:
        if nxt[0] in cont or nxt.startswith('給予') or nxt.startswith('詩咏') or nxt.startswith('各領'):
            return True
        if len(prev) > 20:
            return True
        return False

    # 上一句未收束，且下一句為較長正文 → 合併
    return True


def merge_broken_paragraphs(paras: list[str], title: str = '', section: str = '') -> list[str]:
    if not paras:
        return []
    merged = [paras[0]]
    for nxt in paras[1:]:
        prev = merged[-1]
        if should_merge_paras(prev, nxt, title=title, section=section):
            joined = prev.rstrip() + nxt.lstrip()
            merged[-1] = clean_para(joined)
        else:
            merged.append(nxt)
    return merged


# 個別篇目的標點／用字修正（在合併之後套用）
ARTICLE_TEXT_FIXES: dict[str, list[tuple[str, str]]] = {
    '28-gezhou': [
        (r'^我的家鄉葛州$', '我的家鄉葛州，'),
        (r'一澗松風瑟瑟嗚。\s*，?', '一澗松風瑟瑟嗚。'),
        (r'家鄉[─–—\-]{1,3}\s*-*\s*葛州', '家鄉——葛州'),
        (r'^碎光躍石鱗鱗起$', '碎光躍石鱗鱗起，'),
    ],
}


def apply_text_fixes(article_id: str, paras: list[str]) -> list[str]:
    rules = ARTICLE_TEXT_FIXES.get(article_id) or []
    if not rules:
        return paras
    out = []
    for p in paras:
        t = p
        for pat, repl in rules:
            t = re.sub(pat, repl, t)
        out.append(t)
    return out


def extract_paragraphs(docx_path: Path) -> list[str]:
    doc = Document(str(docx_path))
    paras = []
    for p in doc.paragraphs:
        t = clean_para(p.text)
        if t:
            paras.append(t)
    return paras


def find_file(filename: str) -> Path:
    path = SRC_DIR / filename
    if path.exists():
        return path
    # Fallback: tolerate minor whitespace / bullet char differences
    wanted = re.sub(r'\s+', '', filename)
    wanted = wanted.replace('•', '·').replace('˙', '·').replace('•', '·')
    for f in SRC_DIR.glob('*.docx'):
        got = re.sub(r'\s+', '', f.name)
        got = got.replace('•', '·').replace('˙', '·').replace('•', '·')
        if got == wanted:
            return f
    raise FileNotFoundError(f'Missing source file: {filename}')


def main() -> None:
    if not SRC_DIR.exists():
        raise SystemExit(f'Source folder not found: {SRC_DIR}')

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old article json except keep folder
    for old in OUT_DIR.glob('*.json'):
        if old.name in ('data.json',):
            continue
        # keep regenerating all article jsons
        pass

    index_articles = []
    missing = []

    print('Extracting 《雲心文集》 in TOC order...')
    print(f'Source: {SRC_DIR}')
    print(f'Output: {OUT_DIR}')
    print()

    for i, meta in enumerate(ARTICLES):
        try:
            src = find_file(meta['file'])
        except FileNotFoundError as e:
            missing.append(str(e))
            print(f'  FAIL [{meta["id"]}] {e}')
            continue

        paras = extract_paragraphs(src)
        paras = merge_broken_paragraphs(
            paras, title=meta['title'], section=meta['section']
        )
        paras = apply_text_fixes(meta['id'], paras)
        chars = sum(len(p) for p in paras)
        article = {
            'id': meta['id'],
            'zh': meta['title'],
            'title': meta['title'],
            'section': meta['section'],
            'section_title': meta['section_title'],
            'num': meta['num'],
            'order': i,
            'author': '',
            'paragraphs': paras,
            'chars': chars,
            'source_file': src.name,
        }
        out_path = OUT_DIR / f'{meta["id"]}.json'
        out_path.write_text(
            json.dumps(article, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        index_articles.append({
            'id': meta['id'],
            'zh': meta['title'],
            'title': meta['title'],
            'section': meta['section'],
            'section_title': meta['section_title'],
            'num': meta['num'],
            'order': i,
            'chars': chars,
            'href': (
                'yunxin-preface.html'
                if meta['id'] == '00-preface'
                else f'yunxin-article.html?id={meta["id"]}'
            ),
        })
        print(f'  OK  [{i:02d}] {meta["id"]} ← {src.name} ({chars} chars, {len(paras)} paras)')

    if missing:
        raise SystemExit('Missing files:\n' + '\n'.join(missing))

    # Build sectioned TOC data — preserve ARTICLES order exactly
    sections = []
    current = None
    for a in index_articles:
        key = a['section']
        if not current or current['id'] != key:
            current = {
                'id': key,
                'title': a['section_title'],
                'articles': [],
            }
            sections.append(current)
        current['articles'].append(a)

    # 若尚未收錄第四輯正文，保留「待發」占位
    if not any(s['id'] == 'notes' for s in sections):
        sections.append({
            'id': 'notes',
            'title': '第四輯  雜記',
            'pending': True,
            'note': '待發',
            'articles': [],
        })

    data = {
        'book': '雲心文集',
        'author': '林樺',
        'total_articles': len(index_articles),
        'articles': index_articles,
        'sections': sections,
    }
    (OUT_DIR / 'data.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    print()
    print(f'Done. {len(index_articles)} articles written.')
    print('Order check:')
    for a in index_articles:
        print(f'  {a["order"]:02d}. [{a["section"]}] {a["num"]} {a["title"]}')


if __name__ == '__main__':
    main()

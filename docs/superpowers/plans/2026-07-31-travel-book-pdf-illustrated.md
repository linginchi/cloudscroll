# Travel Book Illustrated PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make 《我的人生旅行》四辑整书 PDF include volume cover art and up to 5 curated photos per article, plus a notice that full images are on cloudscroll.net.

**Architecture:** Extend existing client-side `article-pdf.js` (iframe + chunked html2pdf). Pure helpers select/cap/interleave images; loaders attach `coverSrc` + per-article `images`; render waits for `<img>` decode before canvas capture. Yunxin book export unchanged.

**Tech Stack:** Vanilla JS (`src/js/article-pdf.js`), html2pdf.bundle (vendored), Node `assert` for helper unit tests, existing `npm run build` + wrangler deploy.

**Spec:** `docs/superpowers/specs/2026-07-31-travel-book-pdf-illustrated-design.md`

---

## File map

| File | Role |
|---|---|
| `src/js/article-pdf.js` | All PDF logic: helpers, load, chunk, render |
| `scripts/test-pdf-book-helpers.mjs` | Unit tests for pure helpers (Node) |
| `src/shelf.html` | Bump `article-pdf.js?v=` cache query |
| `src/reader.html` | Same cache bump (shared script) |
| `src/yunxin-article.html` / `src/yunxin-preface.html` | Same cache bump |

Image URL conventions (do not invent new paths):

- Cover: `images/cover_v{N}.jpg` (site `src/images/`, copied to `dist/images/` via build)
- Article photos in JSON: `images/{id}_NNN.jpeg` → load as `book/` + src → `book/images/...`

---

### Task 1: Pure helpers + unit tests

**Files:**
- Create: `scripts/test-pdf-book-helpers.mjs`
- Modify: `src/js/article-pdf.js` (add helpers near top after `PDF_WIDTH`)

- [ ] **Step 1: Write the failing test file**

Create `scripts/test-pdf-book-helpers.mjs`:

```js
import assert from 'assert';

// Mirror helpers under test (copy implementations into article-pdf.js in Step 3;
// tests import from a tiny shared file OR re-declare expected behavior via dynamic import).
// Prefer: export helpers on global in browser; for Node, duplicate the pure functions
// in this file ONLY if article-pdf cannot be imported. Instead extract to:
//   src/js/pdf-book-helpers.js  (no DOM) — REQUIRED by this plan.

import {
  MAX_IMAGES_PER_ARTICLE,
  pickArticleImages,
  resolveBookImageUrl,
  volumeCoverSrc,
  interleaveTextAndImages,
  NOTICE_TEXT
} from '../src/js/pdf-book-helpers.js';

assert.strictEqual(MAX_IMAGES_PER_ARTICLE, 5);
assert.strictEqual(volumeCoverSrc(1), 'images/cover_v1.jpg');
assert.strictEqual(volumeCoverSrc(4), 'images/cover_v4.jpg');
assert.strictEqual(volumeCoverSrc(0), 'images/cover_v1.jpg');
assert.strictEqual(volumeCoverSrc(9), 'images/cover_v4.jpg');

assert.strictEqual(resolveBookImageUrl('images/v4-04_001.jpeg'), 'book/images/v4-04_001.jpeg');
assert.strictEqual(resolveBookImageUrl('book/images/x.jpeg'), 'book/images/x.jpeg');

const blocks = [
  { type: 'text', content: 'A' },
  { type: 'image', src: 'images/a_001.jpeg' },
  { type: 'image', src: 'images/a_002.jpeg' },
  { type: 'image', src: 'images/a_003.jpeg' },
  { type: 'image', src: 'images/a_004.jpeg' },
  { type: 'image', src: 'images/a_005.jpeg' },
  { type: 'image', src: 'images/a_006.jpeg' }
];
const picked = pickArticleImages(blocks);
assert.strictEqual(picked.length, 5);
assert.strictEqual(picked[0], 'book/images/a_001.jpeg');
assert.strictEqual(picked[4], 'book/images/a_005.jpeg');

const mixed = interleaveTextAndImages(
  ['p1', 'p2', 'p3', 'p4', 'p5', 'p6'],
  ['book/images/a_001.jpeg', 'book/images/a_002.jpeg']
);
assert.ok(mixed.some((x) => x.kind === 'image'));
assert.ok(mixed.filter((x) => x.kind === 'text').length === 6);
assert.ok(NOTICE_TEXT.indexOf('cloudscroll.net') !== -1);
assert.ok(NOTICE_TEXT.indexOf('精选图文') !== -1 || NOTICE_TEXT.indexOf('精選圖文') !== -1);

console.log('test-pdf-book-helpers: OK');
```

- [ ] **Step 2: Run test — expect FAIL (module missing)**

```powershell
node scripts/test-pdf-book-helpers.mjs
```

Expected: `ERR_MODULE_NOT_FOUND` for `pdf-book-helpers.js`

- [ ] **Step 3: Create `src/js/pdf-book-helpers.js`**

```js
export const MAX_IMAGES_PER_ARTICLE = 5;

export const NOTICE_TEXT =
  '本 PDF 为精选图文版，便于分享阅读。完整配图与排版请在手机打开 cloudscroll.net 在线阅读。';

export function volumeCoverSrc(volume) {
  var n = parseInt(volume, 10) || 1;
  if (n < 1) n = 1;
  if (n > 4) n = 4;
  return 'images/cover_v' + n + '.jpg';
}

export function resolveBookImageUrl(src) {
  var s = String(src || '').trim();
  if (!s) return '';
  if (s.indexOf('book/') === 0 || s.indexOf('images/cover_') === 0) return s;
  if (s.indexOf('images/') === 0) return 'book/' + s;
  return 'book/images/' + s.replace(/^\/+/, '');
}

export function pickArticleImages(blocks) {
  var out = [];
  if (!blocks || !blocks.length) return out;
  for (var i = 0; i < blocks.length; i++) {
    var b = blocks[i];
    if (!b || b.type !== 'image' || !b.src) continue;
    out.push(resolveBookImageUrl(b.src));
    if (out.length >= MAX_IMAGES_PER_ARTICLE) break;
  }
  return out;
}

/** Spread images through paragraphs; leftover images append at end. */
export function interleaveTextAndImages(paragraphs, imageUrls) {
  var paras = paragraphs || [];
  var imgs = (imageUrls || []).slice();
  var items = [];
  if (!imgs.length) {
    for (var i = 0; i < paras.length; i++) {
      if (paras[i]) items.push({ kind: 'text', text: paras[i] });
    }
    return items;
  }
  var gap = Math.max(2, Math.ceil(paras.length / (imgs.length + 1)));
  var ii = 0;
  for (var p = 0; p < paras.length; p++) {
    if (paras[p]) items.push({ kind: 'text', text: paras[p] });
    if (ii < imgs.length && (p + 1) % gap === 0) {
      items.push({ kind: 'image', src: imgs[ii++] });
    }
  }
  while (ii < imgs.length) {
    items.push({ kind: 'image', src: imgs[ii++] });
  }
  return items;
}
```

- [ ] **Step 4: Re-run tests — expect PASS**

```powershell
node scripts/test-pdf-book-helpers.mjs
```

Expected: `test-pdf-book-helpers: OK`

- [ ] **Step 5: Commit**

```powershell
git add src/js/pdf-book-helpers.js scripts/test-pdf-book-helpers.mjs
git commit -m "feat: add helpers for illustrated travel PDF"
```

---

### Task 2: Wire helpers into loader (`loadTravelVolumeBook`)

**Files:**
- Modify: `src/js/article-pdf.js`
- Modify: `scripts/build.js` — ensure `pdf-book-helpers.js` is copied if build only copies listed js files (check copy loop; if it copies whole `src/js/`, no change)

- [ ] **Step 1: Confirm build copies all of `src/js/`**

Open `scripts/build.js` and confirm JS copy is recursive/all files under `src/js`. If whitelist-only, add `pdf-book-helpers.js`.

- [ ] **Step 2: Load helpers in shelf (script tag)**

In `src/shelf.html`, before `article-pdf.js`, add:

```html
<script src="js/pdf-book-helpers.js?v=20260731g" type="module"></script>
```

**Problem:** `article-pdf.js` is a classic IIFE, not a module. Prefer **not** using ES modules on the page.

**Alternative (required):** Keep helpers as ES module for Node tests only, and **duplicate the same function bodies** inside `article-pdf.js` IIFE (or assign from a UMD build). To avoid drift: have `article-pdf.js` contain the functions, and `scripts/test-pdf-book-helpers.mjs` import from a CJS/ESM dual file.

**Chosen approach for this plan:** `src/js/pdf-book-helpers.js` uses UMD-less plain assignments when not under `import`:

Actually simpler: **inline helpers inside `article-pdf.js`**, and make `scripts/test-pdf-book-helpers.mjs` contain a **copy of the same functions** for Node assert (comment: keep in sync with article-pdf.js). Spec YAGNI prefers one browser file.

**Revised Task 1/2 merge for implementer:**

1. Put helpers as named functions inside `article-pdf.js` IIFE.  
2. Expose for tests: `global.CloudscrollPdfHelpers = { pickArticleImages, ... }` at bottom next to `CloudscrollPdf`.  
3. Test file uses `fs.readFileSync` + `vm.runInNewContext` OR dynamic import of a small extract.

Simplest reliable path:

- Create `src/js/pdf-book-helpers.js` as **plain script** (no import/export):

```js
(function (global) {
  'use strict';
  var H = { MAX_IMAGES_PER_ARTICLE: 5, NOTICE_TEXT: '...' };
  H.volumeCoverSrc = function (volume) { /* ... */ };
  H.resolveBookImageUrl = function (src) { /* ... */ };
  H.pickArticleImages = function (blocks) { /* ... */ };
  H.interleaveTextAndImages = function (paragraphs, imageUrls) { /* ... */ };
  global.CloudscrollPdfHelpers = H;
})(typeof window !== 'undefined' ? window : globalThis);
```

- Test: `node --experimental-vm-modules` or:

```js
import fs from 'fs';
import vm from 'vm';
const code = fs.readFileSync('src/js/pdf-book-helpers.js', 'utf8');
const sandbox = { globalThis: {}, console };
vm.runInNewContext(code + '\nthis.CloudscrollPdfHelpers = globalThis.CloudscrollPdfHelpers;', sandbox);
const H = sandbox.globalThis.CloudscrollPdfHelpers;
```

Update Task 1 test accordingly if implementer follows this UMD-global pattern.

- [ ] **Step 3: In `loadTravelVolumeBook`, return cover + images**

Replace article mapping so each article includes images:

```js
return {
  title: art.zh || full.zh || art.id,
  sectionTitle: title,
  paragraphs: blocksToParagraphs(full.blocks),
  images: global.CloudscrollPdfHelpers.pickArticleImages(full.blocks)
};
```

And book object:

```js
return {
  title: '我的人生旅行 · ' + title,
  subtitle: data.title_en || '',
  author: data.author || '林樺',
  volume: vol,
  coverSrc: global.CloudscrollPdfHelpers.volumeCoverSrc(vol),
  articles: cleaned
};
```

- [ ] **Step 4: Manual smoke in DevTools (optional)**

Serve `dist`, open shelf, in console after loading `pdf-book-helpers.js` + `article-pdf.js`:

```js
CloudscrollPdf.loadTravelVolumeBook(4).then((b) => console.log(b.coverSrc, b.articles[3] && b.articles[3].images))
```

Expected: `images/cover_v4.jpg` and an array of up to 5 `book/images/...` URLs for a pictured article.

- [ ] **Step 5: Commit**

```powershell
git add src/js/pdf-book-helpers.js src/js/article-pdf.js src/shelf.html scripts/test-pdf-book-helpers.mjs scripts/build.js
git commit -m "feat: load cover and curated images for travel PDF"
```

---

### Task 3: Cover + notice chunks and CSS

**Files:**
- Modify: `src/js/article-pdf.js` — `ensurePdfFrame` styles, `buildBookChunks`, `buildBookChunkRoot`

- [ ] **Step 1: Add CSS strings inside `ensurePdfFrame` `doc.write` style block**

```css
.cs-pdf-cover{position:relative;width:700px;min-height:990px;margin:0;padding:0;overflow:hidden;background:#1a1510;}
.cs-pdf-cover-img{display:block;width:700px;height:990px;object-fit:cover;}
.cs-pdf-cover-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,0.25) 0%,rgba(20,16,12,0.55) 55%,rgba(20,16,12,0.78) 100%);}
.cs-pdf-cover-text{position:absolute;left:40px;right:40px;bottom:72px;color:#faf6f0;text-align:left;}
.cs-pdf-cover-brand{font-size:14px;letter-spacing:0.28em;margin:0 0 18px;opacity:0.9;}
.cs-pdf-cover-title{font-size:28px;font-weight:700;letter-spacing:0.08em;margin:0 0 10px;line-height:1.35;}
.cs-pdf-cover-sub{font-size:15px;letter-spacing:0.06em;margin:0 0 8px;opacity:0.92;}
.cs-pdf-cover-meta{font-size:13px;letter-spacing:0.12em;margin:12px 0 0;opacity:0.85;}
.cs-pdf-notice{font-size:15px;line-height:1.9;margin:24px 0;text-align:justify;}
.cs-pdf-figure{margin:14px 0 18px;border:1px solid #e0d6c6;border-radius:3px;overflow:hidden;background:#efe8dc;}
.cs-pdf-figure img{display:block;width:100%;height:auto;}
```

- [ ] **Step 2: Update `buildBookChunks(book)`**

```js
chunks.push({
  kind: 'cover',
  title: book.title,
  subtitle: book.subtitle,
  author: book.author,
  coverSrc: book.coverSrc || '',
  showBrand: false
});
chunks.push({
  kind: 'notice',
  text: (global.CloudscrollPdfHelpers && CloudscrollPdfHelpers.NOTICE_TEXT) ||
    '本 PDF 为精选图文版，便于分享阅读。完整配图与排版请在手机打开 cloudscroll.net 在线阅读。',
  showBrand: true
});
// toc unchanged...
// articles: use interleave + smaller batches when images present
```

For each article:

```js
var items = CloudscrollPdfHelpers.interleaveTextAndImages(art.paragraphs || [], art.images || []);
var batch = (art.images && art.images.length) ? 10 : 16;
// chunk items into batches of ~batch entries (keep title on first chunk only)
```

Chunk shape for articles:

```js
{
  kind: 'article',
  title: ...,
  sectionTitle: ...,
  items: [ {kind:'text', text:'...'}, {kind:'image', src:'book/images/...'} ],
  showBrand: ...
}
```

Keep backward compatibility: if `items` missing, fall back to `paragraphs` array as today.

- [ ] **Step 3: Update `buildBookChunkRoot` cover branch**

Remove「全文 PDF（文字版）」. If `chunk.coverSrc`:

```js
var cover = doc.createElement('div');
cover.className = 'cs-pdf-cover';
var img = doc.createElement('img');
img.className = 'cs-pdf-cover-img';
img.src = chunk.coverSrc;
img.alt = '';
cover.appendChild(img);
var shade = doc.createElement('div');
shade.className = 'cs-pdf-cover-shade';
cover.appendChild(shade);
var textWrap = doc.createElement('div');
textWrap.className = 'cs-pdf-cover-text';
textWrap.appendChild(el(doc, 'p', '雲箋文舍', 'cs-pdf-cover-brand'));
textWrap.appendChild(el(doc, 'h1', chunk.title || '我的人生旅行', 'cs-pdf-cover-title'));
if (chunk.subtitle) textWrap.appendChild(el(doc, 'p', chunk.subtitle, 'cs-pdf-cover-sub'));
textWrap.appendChild(el(doc, 'p', (chunk.author || '林樺') + ' · 精选图文版', 'cs-pdf-cover-meta'));
cover.appendChild(textWrap);
wrap.appendChild(cover);
return mountRoot(doc, wrap); // no footer on cover
```

Add `notice` branch:

```js
if (chunk.kind === 'notice') {
  wrap.appendChild(el(doc, 'h2', '說明', 'cs-pdf-h2'));
  wrap.appendChild(el(doc, 'p', chunk.text || '', 'cs-pdf-notice'));
  appendFooter(doc, wrap);
  return mountRoot(doc, wrap);
}
```

- [ ] **Step 4: Commit**

```powershell
git add src/js/article-pdf.js
git commit -m "feat: illustrated cover and notice page for travel PDF"
```

---

### Task 4: Render article images + wait for decode

**Files:**
- Modify: `src/js/article-pdf.js` — `buildBookChunkRoot` article branch, `renderBookChunksToPdf`

- [ ] **Step 1: Article branch renders `chunk.items`**

```js
wrap.appendChild(el(doc, 'h2', chunk.title || '文章', 'cs-pdf-h2'));
if (chunk.sectionTitle) wrap.appendChild(el(doc, 'p', chunk.sectionTitle, 'cs-pdf-sub'));
var items = chunk.items;
if (!items) {
  // legacy paragraphs
  items = (chunk.paragraphs || []).map(function (t) { return { kind: 'text', text: t }; });
}
for (var i = 0; i < items.length; i++) {
  var it = items[i];
  if (!it) continue;
  if (it.kind === 'image' && it.src) {
    var fig = doc.createElement('div');
    fig.className = 'cs-pdf-figure';
    var im = doc.createElement('img');
    im.src = it.src;
    im.alt = '';
    im.loading = 'eager';
    im.decoding = 'sync';
    fig.appendChild(im);
    wrap.appendChild(fig);
  } else if (it.text) {
    wrap.appendChild(el(doc, 'p', it.text, 'cs-pdf-p'));
  }
}
appendFooter(doc, wrap);
return mountRoot(doc, wrap);
```

- [ ] **Step 2: Add `waitForImages(root, timeoutMs)`**

```js
function waitForImages(root, timeoutMs) {
  var imgs = root.querySelectorAll('img');
  if (!imgs.length) return Promise.resolve();
  var limit = timeoutMs || 12000;
  var list = [];
  for (var i = 0; i < imgs.length; i++) {
    (function (img) {
      list.push(new Promise(function (resolve) {
        if (img.complete && img.naturalWidth > 0) { resolve(); return; }
        var done = function () { resolve(); };
        img.onload = done;
        img.onerror = done; // skip broken
        setTimeout(done, limit);
      }));
    })(imgs[i]);
  }
  return Promise.all(list);
}
```

- [ ] **Step 3: In `renderBookChunksToPdf` `step()`, await images before html2pdf**

```js
var root = buildBookChunkRoot(doc, chunks[i]);
waitForImages(root, 12000).then(function () {
  if (i === 0) {
    worker = worker.from(root).toPdf();
  } else {
    worker = worker.get('pdf').then(function (pdf) { pdf.addPage(); })
      .from(root).toContainer().toCanvas().toPdf();
  }
  return Promise.resolve(worker);
}).then(function () {
  i += 1;
  setTimeout(step, 40);
}).catch(fail);
```

- [ ] **Step 4: Optional client-side resize (spec 900px)**

Before setting `img.src` for article photos (not cover), if CORS allows canvas: load into `Image`, draw to canvas max edge 900, set `img.src = canvas.toDataURL('image/jpeg', 0.82)`. Same-origin `book/images` on cloudscroll.net / local serve — OK. On failure, use original URL.

Implement as `function compressImageSrc(url, maxEdge, quality)` returning Promise\<string\>. Call when building items in `buildBookChunks` is heavy (async). **Prefer compress at render time in `buildBookChunkRoot` asynchronously** — then `buildBookChunkRoot` must become async OR pre-compress in `renderBookChunksToPdf` before build.

**Required pattern:**

```js
function prepareChunkRoot(doc, chunk) {
  return expandChunkImages(chunk).then(function (readyChunk) {
    return buildBookChunkRoot(doc, readyChunk);
  });
}
```

`expandChunkImages`: for each image item, replace src with compressed data URL; on error keep original.

- [ ] **Step 5: Commit**

```powershell
git add src/js/article-pdf.js
git commit -m "feat: embed curated photos in travel book PDF chunks"
```

---

### Task 5: Progress copy + cache bust + build copy

**Files:**
- Modify: `src/js/article-pdf.js` progress strings for book export only
- Modify: `src/shelf.html`, `src/reader.html`, `src/yunxin-article.html`, `src/yunxin-preface.html` — `article-pdf.js?v=20260731g` and add `pdf-book-helpers.js?v=20260731g` **before** article-pdf on pages that load book PDF (`shelf.html` required; others optional if helpers only needed for book)

- [ ] **Step 1: Update overlays in `exportBookPdf` / `renderBookChunksToPdf` when exporting travel books**

When `opts` / book has `coverSrc` or always for `exportBook` travel path:

```js
toastWithOverlay(toast, '正在生成精选图文 PDF…（含封面与照片，请稍候） ' + progress + '%');
```

Yunxin path may keep shorter「正在生成 PDF…」.

- [ ] **Step 2: Script tags on `shelf.html`**

```html
<script src="js/pdf-book-helpers.js?v=20260731g"></script>
<script src="js/article-pdf.js?v=20260731g"></script>
```

- [ ] **Step 3: Build + local verify**

```powershell
npm run build
npx --yes serve dist -l 4173
```

Manual: open `http://127.0.0.1:4173/shelf.html` → 第四辑 → 分享／PDF → 下載／分享 PDF. Confirm cover image, notice page with cloudscroll.net, photos in body, no「文字版」.

- [ ] **Step 4: Deploy (author machine)**

```powershell
npx wrangler pages deploy dist --project-name cloudscroll --branch main --commit-dirty=true
```

- [ ] **Step 5: Commit**

```powershell
git add src/js/article-pdf.js src/shelf.html src/reader.html src/yunxin-article.html src/yunxin-preface.html
git commit -m "feat: ship illustrated travel-volume PDF export"
```

---

### Task 6: Acceptance checklist (no code)

- [ ] **Step 1: Volume 4** — cover `cover_v4.jpg`, notice text, ≥1 article with photos, no「文字版」
- [ ] **Step 2: Volume 1** — `cover_v1.jpg` + preface still present
- [ ] **Step 3: Yunxin book PDF** — still text-only (no regression)
- [ ] **Step 4: Run helper tests**

```powershell
node scripts/test-pdf-book-helpers.mjs
```

---

## Spec coverage self-check

| Spec requirement | Task |
|---|---|
| Cover `cover_vN.jpg` full-bleed + titles | Task 3 |
| Notice page + cloudscroll.net | Task 1 constants + Task 3 |
| TOC retained | Task 3 (unchanged path) |
| Max 5 images / article, order preserved | Task 1 `pickArticleImages` |
| Interleave images | Task 1 `interleaveTextAndImages` |
| Compress ~900px / 0.82 | Task 4 |
| Wait for img before capture | Task 4 |
| Skip broken images | Task 4 onerror |
| Progress messaging | Task 5 |
| Yunxin unchanged | Task 2/5 (no loader change) |
| iframe isolation kept | no change to ensurePdfFrame host strategy |

## Placeholder / consistency notes

- Helper global name: `CloudscrollPdfHelpers` everywhere.
- Article chunk field: `items` (not `blocks`).
- Image URLs: always `book/images/...` after resolve; covers stay `images/cover_vN.jpg`.

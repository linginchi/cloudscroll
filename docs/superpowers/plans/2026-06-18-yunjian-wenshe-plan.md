# 雲箋文舍 (Cloudscroll) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a mobile-first static website for author Lin Hua's travel essay collection "My Life's Journey", featuring Chinese ink-wash aesthetics and a book-like page-flip reading experience.

**Architecture:** Pure HTML/CSS/vanilla JS static site. Four pages (cover, shelf, TOC, reader) connected by CSS 3D page-flip transitions. No frameworks. Content stored as Markdown, converted to HTML via a Node.js build script. Deployed on Cloudflare Pages.

**Tech Stack:** HTML5, CSS3 (3D transforms, animations, SVG), Vanilla JS (touch events), Node.js (build script with `marked`), Noto Serif TC font (subset), Cloudflare Pages

---

### Task 0: Project Scaffolding

**Files:**
- Create: `package.json`
- Create: `scripts/build.js`
- Create: `scripts/subset-fonts.js`
- Create: `content/.gitkeep`
- Create: `assets/svg/.gitkeep`
- Create: `assets/images/.gitkeep`
- Create: `assets/fonts/.gitkeep`

- [ ] **Step 1: Create package.json**

```json
{
  "name": "cloudscroll",
  "version": "1.0.0",
  "private": true,
  "description": "雲箋文舍 - Lin Hua's literary works",
  "scripts": {
    "build": "node scripts/build.js"
  },
  "devDependencies": {
    "marked": "^12.0.0"
  }
}
```

- [ ] **Step 2: Create placeholder files for empty directories**

```bash
New-Item -ItemType File -Force -Path "c:\cloudscroll\content\.gitkeep"
New-Item -ItemType File -Force -Path "c:\cloudscroll\assets\svg\.gitkeep"
New-Item -ItemType File -Force -Path "c:\cloudscroll\assets\images\.gitkeep"
New-Item -ItemType File -Force -Path "c:\cloudscroll\assets\fonts\.gitkeep"
```

- [ ] **Step 3: Update .gitignore to exclude build output**

Append to `.gitignore`:
```
# Build deps
node_modules/
package-lock.json
```

- [ ] **Step 4: Create minimal build script skeleton**

```javascript
// scripts/build.js
const fs = require('fs');
const path = require('path');

console.log('Cloudscroll build starting...');

// Step 1: Copy static assets (HTML, CSS, JS, SVG) to dist/
// Step 2: Convert content/*.md to dist/articles/*.html using page template
// Step 3: Generate TOC from article metadata

console.log('Build complete.');
```

- [ ] **Step 5: Install dependencies**

```bash
npm install
```

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: scaffold project structure and build pipeline"
```

---

### Task 1: Global CSS — Page Frame, Colors, Fonts

**Files:**
- Create: `src/css/style.css`
- Create: `src/css/theme.css`

- [ ] **Step 1: Create CSS color variables**

```css
/* src/css/theme.css */
:root {
  --color-page: #f5f0e8;
  --color-card: #faf7f2;
  --color-text-primary: #3d2b1f;
  --color-text-secondary: #8b7355;
  --color-text-faint: #a09080;
  --color-border: #c4a882;
  --color-divider: #e8dcc8;

  --font-serif: 'Noto Serif TC', 'Noto Serif SC', 'Songti SC', 'PMingLiU', '新細明體', serif;
  --font-size-body: 18px;
  --font-size-small: 13px;
  --font-size-quote: 22px;
  --line-height-body: 2.0;
}
```

- [ ] **Step 2: Create global reset and page frame styles**

```css
/* src/css/style.css */
@import './theme.css';

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #2a2018;
  font-family: var(--font-serif);
  -webkit-tap-highlight-color: transparent;
  user-select: none;
  -webkit-user-select: none;
}

/* Page container — each "page" is a full-screen container */
.page {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-page);
  overflow: hidden;
}

/* Page inner frame with border */
.page-inner {
  width: 100%;
  height: 100%;
  max-width: 480px;
  margin: 0 auto;
  border: 2px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 12px;
  background: var(--color-page);
  position: relative;
}

/* Header */
.page-header {
  text-align: center;
  padding: 16px 8px 12px;
  border-bottom: 1px solid var(--color-divider);
}

.page-header .article-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.12em;
}

.page-header .author {
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
  margin-top: 4px;
  letter-spacing: 0.3em;
}

/* Content area — flex grow to fill space */
.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 4px;
  -webkit-overflow-scrolling: touch;
}

.page-content::-webkit-scrollbar {
  width: 4px;
}

.page-content::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

/* Footer */
.page-footer {
  text-align: center;
  padding: 12px 8px 16px;
  border-top: 1px solid var(--color-divider);
  font-size: var(--font-size-small);
  color: var(--color-text-faint);
  letter-spacing: 0.08em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-footer .book-name {
  letter-spacing: 0.12em;
}

.page-footer .page-num {
  letter-spacing: 0.08em;
}
```

- [ ] **Step 3: Commit**

```bash
git add src/css/
git commit -m "feat: add global CSS theme and page frame styles"
```

---

### Task 2: Cover Page — SVG Background + Animations

**Files:**
- Create: `src/index.html`
- Create: `src/css/cover.css`

- [ ] **Step 1: Create cover page HTML structure**

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>雲箋文舍 — Cloudscroll</title>
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/cover.css">
</head>
<body>
  <div class="page" id="cover-page">
    <div class="page-inner cover-inner">
      <!-- Background layers container -->
      <div class="cover-bg" id="cover-bg"></div>

      <!-- Quote -->
      <div class="cover-quote">
        <p class="quote-line">九曲溪頭，竹排一葉。</p>
        <p class="quote-line">行到水窮處，坐看雲起時。</p>
      </div>

      <!-- Site name -->
      <div class="cover-site-name">
        <p class="site-cn">雲箋文舍</p>
        <p class="site-en">Cloudscroll</p>
      </div>
    </div>
  </div>
  <script src="js/cover.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create SVG background layers inline in cover.js**

```javascript
// src/js/cover.js
(function() {
  const bg = document.getElementById('cover-bg');
  if (!bg) return;

  bg.innerHTML = `
    <!-- Layer 1: Far mountains (distant, faint) -->
    <svg class="bg-layer layer-mountains-far" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:20%;left:0;width:100%;height:50%;opacity:0.15;">
      <path d="M-20,400 Q60,180 140,300 Q220,120 300,280 Q380,100 500,320 L500,450 L-20,450 Z"
            fill="#8b7355"/>
    </svg>

    <!-- Layer 2: Mid mountains (Wuyi style peaks) -->
    <svg class="bg-layer layer-mountains-mid" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:20%;left:0;width:100%;height:45%;opacity:0.22;">
      <path d="M-30,380 Q30,160 100,300 Q180,80 250,260 Q320,100 410,280 Q460,140 530,340 L530,500 L-30,500 Z"
            fill="#7a6b52"/>
      <!-- Add a few sharper Wuyi peaks -->
      <path d="M160,270 L180,120 L200,270" fill="#7a6b52" opacity="0.6"/>
      <path d="M340,260 L360,100 L380,260" fill="#7a6b52" opacity="0.5"/>
    </svg>

    <!-- Layer 3: Near shore / stream hint -->
    <svg class="bg-layer layer-stream" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:20%;left:0;width:100%;height:35%;opacity:0.25;">
      <!-- Jiuqu stream -- winding curve -->
      <path d="M-20,380 Q120,340 200,370 Q300,400 420,360 Q460,350 500,370"
            stroke="#a09080" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- Stream width hint -->
      <path d="M-20,370 Q120,330 200,360 Q300,390 420,350 Q460,340 500,360"
            stroke="#a09080" stroke-width="1" fill="none" stroke-linecap="round" opacity="0.5"/>
    </svg>

    <!-- Layer 4: Bamboo raft + fisherman silhouette -->
    <svg class="bg-layer layer-raft" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:22%;left:0;width:100%;height:15%;opacity:0.35;">
      <!-- Raft -->
      <rect x="220" y="90" width="80" height="6" rx="3" fill="#3d2b1f"/>
      <!-- Fisherman with pole (standing at back) -->
      <line x1="285" y1="90" x2="285" y2="30" stroke="#3d2b1f" stroke-width="1.5"/>
      <circle cx="285" cy="20" r="4" fill="#3d2b1f"/> <!-- head -->
      <line x1="285" y1="65" x2="265" y2="55" stroke="#3d2b1f" stroke-width="1"/> <!-- arm -->
      <!-- Couple sitting at front -->
      <circle cx="240" cy="55" r="4" fill="#3d2b1f"/>
      <circle cx="255" cy="58" r="4" fill="#3d2b1f"/>
    </svg>

    <!-- Layer 5: Setting sun glow -->
    <svg class="bg-layer layer-sun" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:5%;right:10%;width:80px;height:80px;opacity:0.4;">
      <defs>
        <radialGradient id="sunGlow">
          <stop offset="0%" stop-color="#d4b896"/>
          <stop offset="100%" stop-color="transparent"/>
        </radialGradient>
      </defs>
      <circle cx="40" cy="40" r="40" fill="url(#sunGlow)"/>
    </svg>

    <!-- Layer 6: Clouds (animated via CSS) -->
    <svg class="bg-layer layer-clouds" viewBox="0 0 480 200" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:12%;left:0;width:100%;height:25%;opacity:0.18;">
      <ellipse class="cloud cloud-1" cx="100" cy="50" rx="60" ry="20" fill="#a09080"/>
      <ellipse class="cloud cloud-2" cx="300" cy="80" rx="50" ry="15" fill="#a09080"/>
      <ellipse class="cloud cloud-3" cx="200" cy="30" rx="40" ry="12" fill="#a09080" opacity="0.6"/>
    </svg>

    <!-- Layer 7: Geese flying north (animated via CSS) -->
    <svg class="bg-layer layer-geese" viewBox="0 0 480 200" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:18%;left:0;width:100%;height:20%;opacity:0.25;">
      <!-- V-formation geese -->
      <g class="geese-group">
        <path d="M60,50 L55,45 M60,50 L65,45" stroke="#3d2b1f" stroke-width="1" fill="none"/>
        <path d="M80,55 L75,50 M80,55 L85,50" stroke="#3d2b1f" stroke-width="1" fill="none"/>
        <path d="M70,60 L65,55 M70,60 L75,55" stroke="#3d2b1f" stroke-width="1" fill="none"/>
        <path d="M90,65 L85,60 M90,65 L95,60" stroke="#3d2b1f" stroke-width="1" fill="none"/>
      </g>
    </svg>
  `;
})();
```

- [ ] **Step 3: Create CSS animations for cover**

```css
/* src/css/cover.css */
.cover-inner {
  position: relative;
  padding: 0;
  border: 2px solid var(--color-border);
  background: linear-gradient(180deg,
    #f0ebe0 0%,
    #f5f0e8 30%,
    #f5f0e8 70%,
    #ede4d4 100%);
}

.cover-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

/* Cloud breathing animation */
.cloud-1 { animation: cloudBreathe 5s ease-in-out infinite; }
.cloud-2 { animation: cloudBreathe 4s ease-in-out 1s infinite; }
.cloud-3 { animation: cloudBreathe 6s ease-in-out 2s infinite; }

@keyframes cloudBreathe {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}

/* Geese flying animation */
.geese-group {
  animation: geeseFly 40s linear infinite;
}

@keyframes geeseFly {
  from { transform: translateX(480px); }
  to   { transform: translateX(-200px); }
}

/* Slow parallax drift on mountains */
.layer-mountains-far {
  animation: driftSlow 60s ease-in-out infinite alternate;
}
.layer-mountains-mid {
  animation: driftSlow 45s ease-in-out 5s infinite alternate;
}

@keyframes driftSlow {
  from { transform: translateX(-8px); }
  to   { transform: translateX(8px); }
}

/* Quote */
.cover-quote {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60%;
  padding: 0 32px;
}

.quote-line {
  font-family: var(--font-serif);
  font-size: var(--font-size-quote);
  font-weight: 300;
  color: var(--color-text-primary);
  line-height: 2.2;
  letter-spacing: 0.15em;
  text-align: center;
  opacity: 0;
  animation: quoteFadeIn 2s ease-out forwards;
}

.quote-line:last-child {
  animation-delay: 0.8s;
}

@keyframes quoteFadeIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Site name */
.cover-site-name {
  position: absolute;
  bottom: 40px;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 2;
}

.site-cn {
  font-family: var(--font-serif);
  font-size: var(--font-size-small);
  color: var(--color-text-faint);
  letter-spacing: 0.4em;
}

.site-en {
  font-family: var(--font-serif);
  font-size: 11px;
  color: var(--color-text-faint);
  letter-spacing: 0.2em;
  margin-top: 4px;
}

/* Click anywhere hint */
.cover-inner::after {
  content: '';
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 32px;
  border-right: 1px solid var(--color-text-faint);
  border-bottom: 1px solid var(--color-text-faint);
  transform: translateX(-50%) rotate(45deg);
  opacity: 0.3;
  animation: hintPulse 2s ease-in-out infinite;
}

@keyframes hintPulse {
  0%, 100% { opacity: 0.15; }
  50% { opacity: 0.45; }
}
```

- [ ] **Step 4: Add click-to-navigate to cover page**

Append to `cover.js`:
```javascript
// Click anywhere on cover to navigate to shelf
document.getElementById('cover-page').addEventListener('click', function() {
  // Store that we need to transition
  sessionStorage.setItem('transition', 'cover-to-shelf');
  window.location.href = 'shelf.html';
});
```

- [ ] **Step 5: Commit**

```bash
git add src/index.html src/css/cover.css src/js/cover.js
git commit -m "feat: add cover page with SVG landscape and animations"
```

---

### Task 3: Shelf Page — Book Card

**Files:**
- Create: `src/shelf.html`
- Create: `src/css/shelf.css`

- [ ] **Step 1: Create shelf page HTML**

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>書架 — 雲箋文舍</title>
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/shelf.css">
</head>
<body>
  <div class="page" id="shelf-page">
    <div class="page-inner">
      <div class="page-content shelf-content">
        <!-- Book card -->
        <div class="book-card" id="book-card">
          <div class="book-cover">
            <div class="book-spine"></div>
            <div class="book-face">
              <p class="book-title">我的人生旅行</p>
              <p class="book-subtitle">My Life's Journey</p>
              <div class="book-divider"></div>
              <p class="book-author">林樺 著</p>
            </div>
          </div>
        </div>

        <!-- Entry hint -->
        <p class="entry-hint">翻開書頁</p>
      </div>

      <div class="page-footer">
        <span class="book-name">雲箋文舍</span>
        <span>Cloudscroll</span>
      </div>
    </div>
  </div>
  <script src="js/shelf.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create shelf CSS**

```css
/* src/css/shelf.css */
.shelf-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 32px;
}

/* Book card — mimics a physical book */
.book-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.book-card:active {
  transform: scale(0.97);
}

.book-cover {
  position: relative;
  width: 180px;
  height: 260px;
  background: linear-gradient(135deg, #faf7f2 0%, #f5f0e8 100%);
  border: 1px solid var(--color-border);
  border-radius: 2px;
  box-shadow:
    2px 2px 8px rgba(0,0,0,0.08),
    0 0 0 1px rgba(0,0,0,0.03);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Book spine shadow */
.book-spine {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 8px;
  background: linear-gradient(90deg,
    rgba(0,0,0,0.08) 0%,
    rgba(0,0,0,0.03) 50%,
    transparent 100%);
  border-right: 1px solid rgba(0,0,0,0.06);
}

.book-face {
  text-align: center;
  padding: 32px 24px;
  margin-left: 8px;
}

.book-title {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.15em;
  line-height: 1.6;
}

.book-subtitle {
  font-family: var(--font-serif);
  font-size: 11px;
  color: var(--color-text-faint);
  margin-top: 8px;
  letter-spacing: 0.12em;
  font-style: italic;
}

.book-divider {
  width: 40px;
  height: 1px;
  background: var(--color-border);
  margin: 16px auto;
}

.book-author {
  font-family: var(--font-serif);
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
  letter-spacing: 0.2em;
}

.entry-hint {
  font-family: var(--font-serif);
  font-size: var(--font-size-small);
  color: var(--color-text-faint);
  letter-spacing: 0.15em;
  animation: hintPulse 2s ease-in-out infinite;
}

@keyframes hintPulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
```

- [ ] **Step 3: Add click handler to navigate to TOC**

```javascript
// src/js/shelf.js
document.getElementById('book-card').addEventListener('click', function() {
  window.location.href = 'toc.html';
});
```

- [ ] **Step 4: Commit**

```bash
git add src/shelf.html src/css/shelf.css src/js/shelf.js
git commit -m "feat: add shelf page with book card"
```

---

### Task 4: TOC Page — Article List

**Files:**
- Create: `src/toc.html`
- Create: `data/articles.json`

- [ ] **Step 1: Create article data**

```json
[
  { "id": "preface", "title": "《我的人生旅行》自序", "file": "00-preface.md" },
  { "id": "taiwan", "title": "台灣屢遊散記", "file": "01-taiwan.md" },
  { "id": "macau", "title": "屢次澳門遊蹤紀", "file": "02-macau.md" },
  { "id": "nz", "title": "新西蘭奧克蘭遊目騁懷", "file": "03-new-zealand.md" },
  { "id": "penang", "title": "檳島親遊札記", "file": "04-penang.md" },
  { "id": "kinmen", "title": "浯洲遊蹤記", "file": "05-kinmen.md" },
  { "id": "philippines", "title": "菲島情懷 春露秋霜", "file": "06-philippines.md" },
  { "id": "korea", "title": "長今尋縱 韓地攬勝", "file": "07-korea.md" },
  { "id": "genting", "title": "霧鎖雲頂 燈耀雙塔", "file": "08-genting.md" },
  { "id": "vietnam", "title": "麗星馳碧浪，郵旅覽越南", "file": "09-vietnam.md" }
]
```

- [ ] **Step 2: Create TOC page**

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>目錄 — 雲箋文舍</title>
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/toc.css">
</head>
<body>
  <div class="page">
    <div class="page-inner">
      <div class="page-header">
        <p class="article-title">《我的人生旅行》</p>
        <p class="author">目錄 — 林樺</p>
      </div>

      <div class="page-content">
        <ul class="toc-list" id="toc-list"></ul>
      </div>

      <div class="page-footer">
        <span class="book-name">《我的人生旅行》</span>
        <span class="page-num">目錄 · i</span>
      </div>
    </div>
  </div>
  <script src="js/toc.js"></script>
</body>
</html>
```

- [ ] **Step 3: Create TOC CSS**

```css
/* src/css/toc.css */
.toc-list {
  list-style: none;
  padding: 0;
}

.toc-list li {
  border-bottom: 1px dotted var(--color-divider);
}

.toc-list li:last-child {
  border-bottom: none;
}

.toc-list a {
  display: flex;
  align-items: center;
  padding: 18px 12px;
  text-decoration: none;
  color: var(--color-text-primary);
  font-size: 17px;
  letter-spacing: 0.08em;
  transition: background 0.15s ease;
}

.toc-list a:active {
  background: rgba(196, 168, 130, 0.1);
}

.toc-num {
  font-family: var(--font-serif);
  font-size: var(--font-size-small);
  color: var(--color-text-faint);
  min-width: 28px;
  font-variant-numeric: tabular-nums;
}

.toc-title {
  flex: 1;
  line-height: 1.6;
}

.toc-arrow {
  font-size: 14px;
  color: var(--color-text-faint);
}
```

- [ ] **Step 4: Create TOC JS — load articles.json and populate list**

```javascript
// src/js/toc.js
(async function() {
  const list = document.getElementById('toc-list');
  if (!list) return;

  try {
    const resp = await fetch('../data/articles.json');
    const articles = await resp.json();

    articles.forEach((article, i) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <a href="reader.html?id=${article.id}">
          <span class="toc-num">${String(i + 1).padStart(2, '0')}</span>
          <span class="toc-title">${article.title}</span>
          <span class="toc-arrow">→</span>
        </a>
      `;
      list.appendChild(li);
    });
  } catch (err) {
    list.innerHTML = '<li style="text-align:center;padding:40px;color:var(--color-text-faint);">目錄載入中...</li>';
  }
})();
```

- [ ] **Step 5: Commit**

```bash
git add src/toc.html src/css/toc.css src/js/toc.js data/articles.json
git commit -m "feat: add TOC page with article list"
```

---

### Task 5: Reader Page — Article Display + Page Flip Engine

**Files:**
- Create: `src/reader.html`
- Create: `src/css/reader.css`
- Create: `src/js/page-flip.js`

- [ ] **Step 1: Create reader page HTML**

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>閱讀 — 雲箋文舍</title>
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/reader.css">
</head>
<body>
  <!-- Page flip container -->
  <div class="flip-container" id="flip-container">
    <!-- Front page (current) -->
    <div class="flip-page flip-front" id="page-front">
      <div class="page-inner">
        <div class="page-header" id="page-header">
          <p class="article-title" id="header-title"></p>
          <p class="author">林樺</p>
        </div>
        <div class="page-content" id="page-content"></div>
        <div class="page-footer">
          <span class="book-name">《我的人生旅行》</span>
          <span class="page-num" id="page-num">p1</span>
        </div>
      </div>
    </div>

    <!-- Back page (next, revealed on flip) -->
    <div class="flip-page flip-back" id="page-back">
      <div class="page-inner">
        <div class="page-header">
          <p class="article-title" id="back-header-title"></p>
          <p class="author">林樺</p>
        </div>
        <div class="page-content" id="back-content"></div>
        <div class="page-footer">
          <span class="book-name">《我的人生旅行》</span>
          <span class="page-num" id="back-page-num">p2</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Article data store -->
  <script src="data/articles.json" id="articles-data" type="application/json" style="display:none;"></script>
  <script src="js/page-flip.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create reader CSS with page flip transforms**

```css
/* src/css/reader.css */
/* Flip container — provides 3D perspective */
.flip-container {
  position: fixed;
  inset: 0;
  perspective: 2000px;
  perspective-origin: left center;
}

/* Each page side */
.flip-page {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  overflow: hidden;
}

/* Front: current page */
.flip-front {
  z-index: 2;
  transform-origin: left center;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Back: next page (pre-rendered, invisible from front) */
.flip-back {
  z-index: 1;
  transform: rotateY(180deg);
}

/* Flipped state — applied via JS */
.flip-container.flipped .flip-front {
  transform: rotateY(-180deg);
}

/* Paper shadow overlay during flip */
.flip-front::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg,
    rgba(0,0,0,0.15) 0%,
    transparent 30%);
  opacity: 0;
  transition: opacity 0.5s ease;
  pointer-events: none;
}

.flip-container.flipped .flip-front::after {
  opacity: 1;
}

/* Paper back visible effect */
.flip-front .page-inner {
  background: linear-gradient(90deg,
    var(--color-page) 0%,
    #f0ebe0 100%);
}

/* Reader page specific: center text block */
.reader-text {
  font-family: var(--font-serif);
  font-size: var(--font-size-body);
  line-height: var(--line-height-body);
  color: var(--color-text-primary);
  letter-spacing: 0.04em;
  padding: 8px 4px;
}

.reader-text p {
  margin-bottom: 1em;
  text-indent: 2em;
}

/* Back link in header */
.back-link {
  position: absolute;
  left: 12px;
  top: 16px;
  font-size: var(--font-size-small);
  color: var(--color-text-faint);
  text-decoration: none;
  letter-spacing: 0.1em;
  z-index: 10;
}

.back-link:active {
  color: var(--color-text-secondary);
}
```

- [ ] **Step 3: Create page-flip.js engine**

```javascript
// src/js/page-flip.js
(function() {
  const container = document.getElementById('flip-container');
  if (!container) return;

  // --- State ---
  let articles = [];
  let currentIndex = 0;
  let currentPage = 1; // page within article
  let flipTarget = null;
  const PAGES_PER_ARTICLE = 10; // mock: how many pages per article

  // --- Article loading ---
  async function init() {
    // Get article ID from URL
    const params = new URLSearchParams(window.location.search);
    const articleId = params.get('id');

    // Load article list
    try {
      const resp = await fetch('data/articles.json');
      articles = await resp.json();
    } catch (e) {
      articles = [];
    }

    if (articleId) {
      currentIndex = articles.findIndex(a => a.id === articleId);
      if (currentIndex < 0) currentIndex = 0;
    }

    await loadContent(currentIndex, currentPage);

    // Set up touch handler
    setupTouch();
  }

  // --- Content loading ---
  async function loadContent(articleIdx, page) {
    const article = articles[articleIdx];
    if (!article) {
      document.getElementById('page-content').innerHTML = '<p class="reader-text">文章載入中...</p>';
      return;
    }

    // Update header
    document.getElementById('header-title').textContent = article.title;
    document.getElementById('page-num').textContent = `p${page}`;

    // Load article markdown content
    try {
      const resp = await fetch(`articles/${article.file.replace('.md', '.html')}`);
      if (resp.ok) {
        const html = await resp.text();
        document.getElementById('page-content').innerHTML = `<div class="reader-text">${html}</div>`;
      } else {
        // Placeholder until content is ready
        document.getElementById('page-content').innerHTML =
          `<div class="reader-text">
            <p>${article.title}</p>
            <p>文章內容即將上線。</p>
            <p>Content coming soon.</p>
          </div>`;
      }
    } catch (e) {
      document.getElementById('page-content').innerHTML =
        `<div class="reader-text"><p>${article.title}</p><p>載入中...</p></div>`;
    }
  }

  // --- Preload next page into back ---
  async function preloadNext() {
    let nextIdx = currentIndex;
    let nextPageNum = currentPage + 1;

    if (nextPageNum > PAGES_PER_ARTICLE) {
      nextIdx = currentIndex + 1;
      nextPageNum = 1;
    }

    if (nextIdx >= articles.length) {
      // Last page — show ending
      document.getElementById('back-header-title').textContent = '完';
      document.getElementById('back-content').innerHTML =
        '<div class="reader-text" style="text-align:center;padding-top:40%;">' +
        '<p>— 全書完 —</p></div>';
      document.getElementById('back-page-num').textContent = '';
      return;
    }

    const article = articles[nextIdx];
    document.getElementById('back-header-title').textContent = article.title;
    document.getElementById('back-page-num').textContent = `p${nextPageNum}`;

    try {
      const resp = await fetch(`articles/${article.file.replace('.md', '.html')}`);
      if (resp.ok) {
        document.getElementById('back-content').innerHTML =
          `<div class="reader-text">${await resp.text()}</div>`;
      }
    } catch (e) {}
  }

  // --- Execute flip ---
  function flip() {
    container.classList.add('flipped');

    // After animation completes, swap pages
    setTimeout(() => {
      // Swap front and back content
      const frontContent = document.getElementById('page-content');
      const backContent = document.getElementById('back-content');
      const frontHeader = document.getElementById('header-title');
      const backHeader = document.getElementById('back-header-title');
      const frontPageNum = document.getElementById('page-num');
      const backPageNum = document.getElementById('back-page-num');

      // Swap
      const tempContent = frontContent.innerHTML;
      const tempHeader = frontHeader.textContent;
      const tempPageNum = frontPageNum.textContent;

      frontContent.innerHTML = backContent.innerHTML;
      frontHeader.textContent = backHeader.textContent;
      frontPageNum.textContent = backPageNum.textContent;

      backContent.innerHTML = tempContent;
      backHeader.textContent = tempHeader;
      backPageNum.textContent = tempPageNum;

      // Update state
      currentPage++;
      if (currentPage > PAGES_PER_ARTICLE) {
        currentIndex++;
        currentPage = 1;
      }

      // Reset flip
      container.classList.remove('flipped');

      // Preload next
      preloadNext();
    }, 650);
  }

  // --- Touch handling ---
  function setupTouch() {
    let startX = 0;
    let startY = 0;

    container.addEventListener('touchstart', function(e) {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    }, { passive: true });

    container.addEventListener('touchend', function(e) {
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      const dx = endX - startX;
      const dy = endY - startY;

      // Right-to-left swipe (swipe left: negative dx)
      if (Math.abs(dx) > Math.abs(dy) && dx < -40) {
        flip();
      }
      // Left-to-right swipe (swipe right: positive dx) — go back
      if (Math.abs(dx) > Math.abs(dy) && dx > 40 && (currentPage > 1 || currentIndex > 0)) {
        flipBack();
      }
    });
  }

  function flipBack() {
    // Simplified: just navigate back in history
    if (currentPage > 1) {
      currentPage--;
      // Reload with correct page
      loadContent(currentIndex, currentPage);
    } else if (currentIndex > 0) {
      currentIndex--;
      currentPage = PAGES_PER_ARTICLE;
      loadContent(currentIndex, currentPage);
    } else {
      window.location.href = 'toc.html';
    }
  }

  // --- Start ---
  init();
})();
```

- [ ] **Step 4: Commit**

```bash
git add src/reader.html src/css/reader.css src/js/page-flip.js
git commit -m "feat: add reader page with CSS 3D page flip engine"
```

---

### Task 6: Build Script — Markdown to HTML Conversion

**Files:**
- Modify: `scripts/build.js`

- [ ] **Step 1: Write complete build script**

```javascript
// scripts/build.js
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const ROOT = path.resolve(__dirname, '..');
const CONTENT_DIR = path.join(ROOT, 'content');
const SRC_DIR = path.join(ROOT, 'src');
const DIST_DIR = path.join(ROOT, 'dist');

console.log('Cloudscroll build starting...\n');

// Ensure dist directories
const dirs = ['dist', 'dist/css', 'dist/js', 'dist/articles', 'dist/data', 'dist/assets'];
dirs.forEach(d => {
  const full = path.join(ROOT, d);
  if (!fs.existsSync(full)) fs.mkdirSync(full, { recursive: true });
});

// Copy static assets
function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  fs.readdirSync(src).forEach(file => {
    const srcPath = path.join(src, file);
    const destPath = path.join(dest, file);
    const stat = fs.statSync(srcPath);
    if (stat.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  });
}

console.log('Copying static files...');
copyDir(path.join(SRC_DIR, 'css'), path.join(ROOT, 'dist/css'));
copyDir(path.join(SRC_DIR, 'js'), path.join(ROOT, 'dist/js'));
copyDir(path.join(ROOT, 'data'), path.join(ROOT, 'dist/data'));
copyDir(path.join(ROOT, 'assets'), path.join(ROOT, 'dist/assets'));

// Copy HTML pages (root level)
['index.html', 'shelf.html', 'toc.html', 'reader.html'].forEach(file => {
  const src = path.join(SRC_DIR, file);
  const dest = path.join(DIST_DIR, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
    console.log(`  Copied: ${file}`);
  }
});

// Convert markdown articles
console.log('\nConverting articles...');
if (!fs.existsSync(CONTENT_DIR)) {
  console.log('  No content/ directory, skipping.');
} else {
  const mdFiles = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith('.md'));
  mdFiles.forEach(file => {
    const mdPath = path.join(CONTENT_DIR, file);
    const mdContent = fs.readFileSync(mdPath, 'utf-8');
    const htmlContent = marked.parse(mdContent);
    const htmlFile = file.replace('.md', '.html');
    const htmlPath = path.join(ROOT, 'dist/articles', htmlFile);
    fs.writeFileSync(htmlPath, htmlContent, 'utf-8');
    console.log(`  ${file} -> articles/${htmlFile}`);
  });
}

console.log('\nBuild complete! Output in dist/');
```

- [ ] **Step 2: Update package.json build script**

Ensure `package.json` has:
```json
"scripts": {
  "build": "node scripts/build.js",
  "build:watch": "node --watch scripts/build.js"
}
```

If it doesn't, update it.

- [ ] **Step 3: Test the build**

```bash
node scripts/build.js
```

Expected: `dist/` folder created with all HTML, CSS, JS, and article files.

- [ ] **Step 4: Commit**

```bash
git add scripts/build.js package.json
git commit -m "feat: add build script for markdown-to-HTML conversion"
```

---

### Task 7: Font Subsetting Script

**Files:**
- Create: `scripts/subset-fonts.js`

- [ ] **Step 1: Create font subsetting script**

```javascript
// scripts/subset-fonts.js
// This script extracts all unique Chinese characters from the built HTML files
// and generates a minimal WOFF2 font subset.
//
// Prerequisites:
//   1. Download Noto Serif TC Regular from Google Fonts:
//      https://fonts.google.com/noto/specimen/Noto+Serif+TC
//   2. Install fonttools: pip install fonttools brotli
//
// Usage:
//   node scripts/subset-fonts.js
//   Then run: pyftsubset NotoSerifTC-Regular.ttf --text-file=chars.txt --output-file=assets/fonts/NotoSerifTC-subset.woff2 --flavor=woff2

const fs = require('fs');
const path = require('path');

const DIST_DIR = path.resolve(__dirname, '..', 'dist');

// Collect all unique Chinese characters from HTML files
function collectChars(dir) {
  const chars = new Set();
  const files = walkDir(dir, '.html');

  files.forEach(file => {
    const content = fs.readFileSync(file, 'utf-8');
    // Match CJK characters (U+4E00 to U+9FFF)
    const cjk = content.match(/[\u4e00-\u9fff]/g);
    if (cjk) cjk.forEach(c => chars.add(c));
    // Match fullwidth punctuation
    const punct = content.match(/[\u3000-\u303f\uff00-\uffef]/g);
    if (punct) punct.forEach(c => chars.add(c));
  });

  return Array.from(chars).sort().join('');
}

function walkDir(dir, ext) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  fs.readdirSync(dir).forEach(file => {
    const full = path.join(dir, file);
    if (fs.statSync(full).isDirectory()) {
      results.push(...walkDir(full, ext));
    } else if (file.endsWith(ext)) {
      results.push(full);
    }
  });
  return results;
}

const chars = collectChars(DIST_DIR);
const charsFile = path.resolve(__dirname, '..', 'chars.txt');
fs.writeFileSync(charsFile, chars, 'utf-8');

console.log(`Collected ${chars.length} unique characters.`);
console.log(`Written to: ${charsFile}`);
console.log('\nNext step:');
console.log('  pyftsubset NotoSerifTC-Regular.ttf \\');
console.log('    --text-file=chars.txt \\');
console.log('    --output-file=assets/fonts/NotoSerifTC-subset.woff2 \\');
console.log('    --flavor=woff2');
```

- [ ] **Step 2: Commit**

```bash
git add scripts/subset-fonts.js
git commit -m "feat: add font subsetting script"
```

---

### Task 8: Content — Convert PDF to Markdown

**Files:**
- Create: `content/00-preface.md`
- Create: `content/01-taiwan.md`
- Create: `content/02-macau.md`
  ... (10 articles total)

- [ ] **Step 1: Create first article (preface) as a sample**

Extract text from `《我的人生旅行》自序.pdf`. Since the PDF is encoded, manually create a sample markdown with the preface title and a placeholder.

```markdown
---
title: 《我的人生旅行》自序
author: 林樺
date: 2025
---

# 《我的人生旅行》自序

（文章內容將從 PDF 中提取並以繁體中文呈現。）

人生如旅，天地為逆旅，光陰為過客。余自退休以來，閒暇之日，遍遊四方，所見所聞，筆之於書。此集所錄，乃近年遊蹤之紀，凡十篇。

或登山以望遠，或臨水而興懷。台灣之秀，澳門之古，新西蘭之曠，檳島之幽，浯洲之樸，菲島之情，韓國之韻，雲頂之奇，越南之麗——皆入吾筆端。

今輯為一編，命曰《我的人生旅行》。非敢言文，聊記鴻爪而已。

林樺 識
```

- [ ] **Step 2: Create remaining 9 articles as placeholder markdown files**

Same format as above with appropriate titles.

- [ ] **Step 3: Run build script and verify**

```bash
node scripts/build.js
```

Check that `dist/articles/` contains all 10 `.html` files.

- [ ] **Step 4: Commit**

```bash
git add content/
git commit -m "feat: add article markdown content (preface + placeholders)"
```

---

### Task 9: Cloudflare Pages Deploy

**Files:**
- None (Cloudflare configuration)

- [ ] **Step 1: Set up Cloudflare Pages**

1. Go to Cloudflare Dashboard > Workers & Pages > Pages
2. Connect to GitHub repo `linginchi/cloudscroll`
3. Set build settings:
   - Production branch: `main`
   - Framework preset: **None**
   - Build command: `node scripts/build.js`
   - Build output directory: `dist`
4. Click "Save and Deploy"

- [ ] **Step 2: Verify initial deploy**

Check that the site is live at `cloudscroll.pages.dev`.

- [ ] **Step 3: Set up custom domain**

1. In Cloudflare Pages > cloudscroll > Custom domains
2. Add `cloudscroll.net`
3. Cloudflare will auto-configure DNS (since the domain is already on Cloudflare)

- [ ] **Step 4: Verify on mobile**

Open `https://cloudscroll.net` on a phone in portrait mode. Verify:
- Cover page renders with landscape and quote
- Click cover → shelf page with book card
- Click book card → TOC with article list
- Click article → reader page
- Swipe left → page flip animation works

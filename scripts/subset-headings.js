/**
 * scripts/subset-headings.js
 *
 * Subset Source Han Serif TC Heavy to only the characters used in headings
 * (cover quote, site name, book title, toc heading, article titles, footer).
 * Output: dist/fonts/SourceHanSerifTC-Heavy.subset.woff2
 *
 * Requires: Python fonttools (pyftsubset) installed.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const SRC_DIR = path.join(ROOT, 'src');
const DATA_DIR = path.join(ROOT, 'data');
const FONT_SOURCE = path.join(ROOT, 'fonts', 'SourceHanSerifTC-Heavy.otf');
const DIST_DIR = path.join(ROOT, 'dist');
const FONT_OUT_DIR = path.join(DIST_DIR, 'fonts');
const FONT_OUT = path.join(FONT_OUT_DIR, 'SourceHanSerifTC-Heavy.subset.woff2');

// All heading text across the site that should render in the heavy serif.
function collectHeadingText() {
  let text = '';

  // Cover quote + site name (index.html)
  text += '九曲溪頭，竹排一葉。行到水窮處，坐看雲起時。';
  text += '雲箋文舍 Cloudscroll';

  // Shelf page (book title + author)
  text += '我的人生旅行 A Life Unfolded in Miles 林樺 著 雲箋文舍 Cloudscroll 翻開書頁';

  // TOC page (heading + footer)
  text += '目錄 Table of Contents 林樺 我的人生旅行 雲箋文舍 Cloudscroll';

  // Reader page (header/footer fallback text)
  text += '文章標題 雲箋文舍 Cloudscroll 中 EN';

  // Article titles from data/articles.json (zh + en)
  const articles = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'articles.json'), 'utf-8'));
  articles.forEach(a => { text += a.zh + ' ' + a.en + ' '; });

  // Also scan toc.js inline article list (in case of drift)
  const tocJs = fs.readFileSync(path.join(SRC_DIR, 'js', 'toc.js'), 'utf-8');
  text += tocJs;

  return text;
}

function extractUniqueChars(text) {
  const chars = new Set();
  for (const ch of text) {
    const code = ch.codePointAt(0);
    // CJK + extensions + CJK punctuation + Latin/digits/space/punct
    if (
      (code >= 0x4E00 && code <= 0x9FFF) ||   // CJK Unified
      (code >= 0x3400 && code <= 0x4DBF) ||   // CJK Ext A
      (code >= 0x3000 && code <= 0x303F) ||   // CJK Symbols/Punct
      (code >= 0xFF00 && code <= 0xFFEF) ||   // Halfwidth/Fullwidth
      (code >= 0x0020 && code <= 0x007E) ||   // Basic Latin
      ch === '—' || ch === '·' || ch === '…'
    ) {
      chars.add(ch);
    }
  }
  return Array.from(chars).sort().join('');
}

function main() {
  console.log('Heading font subsetting starting...');

  if (!fs.existsSync(FONT_SOURCE)) {
    console.error('  Source font not found:', FONT_SOURCE);
    process.exit(1);
  }

  fs.mkdirSync(FONT_OUT_DIR, { recursive: true });

  const headingText = collectHeadingText();
  const uniqueChars = extractUniqueChars(headingText);
  console.log('  Unique heading characters:', uniqueChars.length);

  const charsFile = path.join(FONT_OUT_DIR, '_heading_chars.txt');
  fs.writeFileSync(charsFile, uniqueChars, 'utf-8');

  try {
    execSync(
      `pyftsubset "${FONT_SOURCE}" --text-file="${charsFile}" --output-file="${FONT_OUT}" --flavor=woff2 --no-hinting --desubroutinize`,
      { stdio: 'pipe' }
    );
    const sizeKB = Math.round(fs.statSync(FONT_OUT).size / 1024);
    console.log(`  Subsetted -> ${path.basename(FONT_OUT)} (${sizeKB} KB)`);
  } catch (e) {
    console.error('  pyftsubset failed:', e.message);
    console.error('  Make sure fonttools is installed: pip install fonttools brotli');
    process.exit(1);
  }

  console.log('Heading font subsetting complete.');
}

main();

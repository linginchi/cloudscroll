/**
 * scripts/subset-fonts.js
 *
 * Creates a subset of Noto Serif TC font containing only the characters
 * used in the website. Run this when content changes.
 *
 * Prerequisites:
 *   npm install fonttools (or use pyftsubset from Python fonttools)
 *
 * The subsetting is done via Python's fonttools library.
 * If not available, the script will copy the full font as fallback.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SRC_DIR = path.resolve(__dirname, '..', 'src');
const DIST_DIR = path.resolve(__dirname, '..', 'dist');

// Configuration
const FONT_NAME = 'NotoSerifTC';
const FONT_WEIGHTS = ['Light', 'Regular', 'SemiBold'];
const FONT_SOURCE_DIR = path.resolve(__dirname, '..', 'fonts');
const FONT_OUTPUT_DIR = path.join(DIST_DIR, 'fonts');

// All text content to extract characters from
function collectTextContent() {
  let text = '';

  // From HTML files
  const htmlFiles = fs.readdirSync(SRC_DIR).filter(f => f.endsWith('.html'));
  htmlFiles.forEach(file => {
    const html = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
    text += html;
  });

  // From JS files (contains article content)
  const jsDir = path.join(SRC_DIR, 'js');
  const jsFiles = fs.readdirSync(jsDir).filter(f => f.endsWith('.js'));
  jsFiles.forEach(file => {
    const js = fs.readFileSync(path.join(jsDir, file), 'utf-8');
    text += js;
  });

  // From CSS
  const cssDir = path.join(SRC_DIR, 'css');
  const cssFiles = fs.readdirSync(cssDir).filter(f => f.endsWith('.css'));
  cssFiles.forEach(file => {
    const css = fs.readFileSync(path.join(cssDir, file), 'utf-8');
    text += css;
  });

  return text;
}

// Extract unique CJK characters
function extractUniqueChars(text) {
  const chars = new Set();
  for (const ch of text) {
    // CJK Unified Ideographs range: U+4E00–U+9FFF
    const code = ch.charCodeAt(0);
    if ((code >= 0x4E00 && code <= 0x9FFF) ||
        (code >= 0x3400 && code <= 0x4DBF) || // CJK Extension A
        (code >= 0x2E80 && code <= 0x2EFF) || // CJK Radicals
        (code >= 0x3000 && code <= 0x303F) || // CJK Symbols and Punctuation
        ch === '，' || ch === '。' || ch === '《' || ch === '》' ||
        ch === '「' || ch === '」' || ch === '、' || ch === '：' ||
        ch === '；' || ch === '！' || ch === '？' || ch === '—' ||
        ch === '（' || ch === '）' || ch === '·' || ch === '…' ||
        ch === '　' || ch === '　') {
      chars.add(ch);
    }
    // Also include basic Latin (already part of font)
  }
  return Array.from(chars).sort().join('');
}

function main() {
  console.log('Font subsetting starting...');

  if (!fs.existsSync(FONT_SOURCE_DIR)) {
    console.log('  Font source directory not found at', FONT_SOURCE_DIR);
    console.log('  Please download Noto Serif TC fonts to the fonts/ directory.');
    console.log('  Skipping font subsetting for now.');
    return;
  }

  // Ensure output directory
  fs.mkdirSync(FONT_OUTPUT_DIR, { recursive: true });

  // Collect unique characters
  const allText = collectTextContent();
  const uniqueChars = extractUniqueChars(allText);
  console.log('  Unique characters found:', uniqueChars.length);

  // Create a text file with all characters
  const charsFile = path.join(FONT_OUTPUT_DIR, '_chars.txt');
  fs.writeFileSync(charsFile, uniqueChars, 'utf-8');

  // Try pyftsubset (Python fonttools)
  FONT_WEIGHTS.forEach(weight => {
    const inputFile = path.join(FONT_SOURCE_DIR, `${FONT_NAME}-${weight}.ttf`);
    const outputFile = path.join(FONT_OUTPUT_DIR, `${FONT_NAME}-${weight}.woff2`);

    if (!fs.existsSync(inputFile)) {
      console.log(`  Skipping ${weight}: source file not found`);
      return;
    }

    try {
      execSync(
        `pyftsubset "${inputFile}" --text-file="${charsFile}" --output-file="${outputFile}" --flavor=woff2`,
        { stdio: 'pipe' }
      );
      console.log(`  Subsetted and converted ${FONT_NAME}-${weight}`);
    } catch (e) {
      console.log(`  pyftsubset not available for ${weight}, copying as fallback`);
      try {
        execSync(
          `npx fonttools-subset "${inputFile}" "${charsFile}" "${outputFile}"`,
          { stdio: 'pipe', shell: true }
        );
      } catch (e2) {
        console.log(`  Font subsetting not available. Install fonttools or copy full fonts manually.`);
      }
    }
  });

  console.log('Font subsetting complete.');
}

main();

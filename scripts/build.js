const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SRC_DIR = path.resolve(__dirname, '..', 'src');
const CONTENT_DIR = path.resolve(__dirname, '..', 'content');
const DATA_DIR = path.resolve(__dirname, '..', 'data');
const DIST_DIR = path.resolve(__dirname, '..', 'dist');

console.log('Cloudscroll build starting...');

// Ensure dist directory
if (fs.existsSync(DIST_DIR)) {
  fs.rmSync(DIST_DIR, { recursive: true });
}
fs.mkdirSync(DIST_DIR, { recursive: true });

// Step 0: Run book extraction script
console.log('\n[Step 0] Extracting book content...');
try {
  execSync('python scripts/extract-book.py', {
    cwd: path.resolve(__dirname, '..'),
    stdio: 'inherit',
    encoding: 'utf-8',
    timeout: 120000,
  });
  console.log('[Step 0] Book extraction complete.\n');
} catch (e) {
  console.error('[Step 0] Book extraction failed:', e.message);
  process.exit(1);
}

// Step 0.5: Generate EN translations
console.log('\n[Step 0.5] Generating EN translations...');
try {
  execSync('python scripts/translate-en.py', {
    cwd: path.resolve(__dirname, '..'),
    stdio: 'inherit',
    encoding: 'utf-8',
    timeout: 60000,
  });
  console.log('[Step 0.5] EN translations ready.\n');
} catch (e) {
  console.warn('[Step 0.5] EN translations skipped:', e.message);
}

// Step 1: Copy static assets (CSS, JS) to dist/
const assetsDir = path.join(SRC_DIR, 'css');
const jsDir = path.join(SRC_DIR, 'js');
const distCss = path.join(DIST_DIR, 'css');
const distJs = path.join(DIST_DIR, 'js');

fs.mkdirSync(distCss, { recursive: true });
fs.mkdirSync(distJs, { recursive: true });

// Copy CSS files
if (fs.existsSync(assetsDir)) {
  const cssFiles = fs.readdirSync(assetsDir).filter(f => f.endsWith('.css'));
  cssFiles.forEach(file => {
    fs.copyFileSync(path.join(assetsDir, file), path.join(distCss, file));
    console.log('  Copied css/' + file);
  });
}

// Copy JS files
if (fs.existsSync(jsDir)) {
  const jsFiles = fs.readdirSync(jsDir).filter(f => f.endsWith('.js'));
  jsFiles.forEach(file => {
    fs.copyFileSync(path.join(jsDir, file), path.join(distJs, file));
    console.log('  Copied js/' + file);
  });
}

// Copy HTML pages
const htmlFiles = fs.readdirSync(SRC_DIR).filter(f => f.endsWith('.html'));
htmlFiles.forEach(file => {
  let html = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
  html = html.replace(/href="css\//g, 'href="./css/');
  html = html.replace(/src="js\//g, 'src="./js/');
  fs.writeFileSync(path.join(DIST_DIR, file), html, 'utf-8');
  console.log('  Copied ' + file);
});

// Step 2: Convert content/*.md to dist/articles/*.html
const articlesDir = path.join(DIST_DIR, 'articles');
fs.mkdirSync(articlesDir, { recursive: true });

if (fs.existsSync(CONTENT_DIR)) {
  const mdFiles = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith('.md'));
  mdFiles.forEach(file => {
    const mdContent = fs.readFileSync(path.join(CONTENT_DIR, file), 'utf-8');
    const { marked } = require('marked');
    const htmlContent = marked(mdContent);
    const articleName = path.basename(file, '.md');
    const outPath = path.join(articlesDir, articleName + '.html');
    fs.writeFileSync(outPath, htmlContent, 'utf-8');
    console.log('  Converted content/' + file + ' -> articles/' + articleName + '.html');
  });
}

// Step 3: Copy article metadata
if (fs.existsSync(path.join(DATA_DIR, 'articles.json'))) {
  fs.copyFileSync(path.join(DATA_DIR, 'articles.json'), path.join(DIST_DIR, 'articles.json'));
  console.log('  Copied articles.json');
}

// Copy fonts
const fontsDir = path.join(SRC_DIR, 'fonts');
const distFonts = path.join(DIST_DIR, 'fonts');
if (fs.existsSync(fontsDir)) {
  if (!fs.existsSync(distFonts)) fs.mkdirSync(distFonts, { recursive: true });
  const fontFiles = fs.readdirSync(fontsDir);
  fontFiles.forEach(file => {
    fs.copyFileSync(path.join(fontsDir, file), path.join(distFonts, file));
  });
  console.log('  Copied fonts');
}

console.log('\nCloudscroll build complete.');

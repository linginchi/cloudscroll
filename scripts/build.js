const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SRC_DIR = path.resolve(__dirname, '..', 'src');
const CONTENT_DIR = path.resolve(__dirname, '..', 'content');
const DATA_DIR = path.resolve(__dirname, '..', 'data');
const DIST_DIR = path.resolve(__dirname, '..', 'dist');

console.log('Cloudscroll build starting...');

function copyRecursive(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  var entries = fs.readdirSync(src, { withFileTypes: true });
  for (var i = 0; i < entries.length; i++) {
    var e = entries[i];
    var s = path.join(src, e.name);
    var d = path.join(dest, e.name);
    if (e.isDirectory()) {
      copyRecursive(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

// Ensure dist directory
if (fs.existsSync(DIST_DIR)) {
  fs.rmSync(DIST_DIR, { recursive: true });
}
fs.mkdirSync(DIST_DIR, { recursive: true });

const ON_CI = !!(process.env.CF_PAGES || process.env.CI);
function runPython(label, script, opts) {
  opts = opts || {};
  if (ON_CI) {
    console.warn('[' + label + '] CI/Pages — skipping Python step: ' + script);
    return false;
  }
  try {
    execSync('python ' + script, {
      cwd: path.resolve(__dirname, '..'),
      stdio: 'inherit',
      encoding: 'utf-8',
      timeout: opts.timeout || 60000,
    });
    return true;
  } catch (e) {
    if (opts.fatal) {
      console.error('[' + label + '] failed:', e.message);
      process.exit(1);
    }
    console.warn('[' + label + '] skipped:', e.message);
    return false;
  }
}

// Step 0: Run book extraction script (skipped when book/ is absent, e.g. Cloud Agents / Pages)
console.log('\n[Step 0] Extracting book content...');
const BOOK_DIR = path.resolve(__dirname, '..', 'book');
if (!fs.existsSync(BOOK_DIR)) {
  console.warn('[Step 0] book/ not found — skipping Word extraction (use committed src assets).');
} else if (runPython('Step 0', 'scripts/extract-book.py', { timeout: 120000, fatal: true })) {
  console.log('[Step 0] Book extraction complete.\n');
}

// Step 0.5: Generate EN translations
console.log('\n[Step 0.5] Generating EN translations...');
if (runPython('Step 0.5', 'scripts/translate-en.py')) {
  console.log('[Step 0.5] EN translations ready.\n');
}

// Step 0.55: Copy custom cover images and avatar to dist/book/images/
console.log('\n[Step 0.55] Copying custom covers and avatar...');
const distBookImages = path.join(DIST_DIR, 'book', 'images');
fs.mkdirSync(distBookImages, { recursive: true });
const srcImages = path.join(SRC_DIR, 'images');
const customFiles = ['cover_v1.jpg', 'cover_v2.jpg', 'cover_v3.jpg', 'cover_v4.jpg', 'lin_hua.jpg'];
customFiles.forEach(file => {
  const src = path.join(srcImages, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(distBookImages, file));
    console.log('  Copied ' + file);
  } else {
    console.log('  Skipped (not found): ' + file);
  }
});

// Step 0.56: Extract + copy 《雲心文集》
console.log('\n[Step 0.56] Building Yunxin Wenji assets...');
const yunxinSrcDir = path.resolve(__dirname, '..', 'book', '雲心文集');
if (fs.existsSync(yunxinSrcDir)) {
  runPython('Step 0.56', 'scripts/extract-yunxin.py');
} else {
  console.warn('[Step 0.56] book/雲心文集 not found — using committed src/yunxin/.');
}
const distImages = path.join(DIST_DIR, 'images');
fs.mkdirSync(distImages, { recursive: true });
// 复制 src/images 全部媒体（含线上已有、后来补进仓库的图／视频），避免部署时漏文件覆盖生产
if (fs.existsSync(srcImages)) {
  const imageFiles = fs.readdirSync(srcImages).filter(function (f) {
    return /\.(jpg|jpeg|png|webp|gif|mp4|webm|svg|ico)$/i.test(f);
  });
  imageFiles.forEach(function (file) {
    fs.copyFileSync(path.join(srcImages, file), path.join(distImages, file));
    console.log('  Copied images/' + file);
  });
} else {
  console.warn('  src/images not found');
}
const srcYunxin = path.join(SRC_DIR, 'yunxin');
const distYunxin = path.join(DIST_DIR, 'yunxin');
if (fs.existsSync(srcYunxin)) {
  copyRecursive(srcYunxin, distYunxin);
  console.log('  Copied yunxin/');
}

// Step 0.6: Generate cover images
console.log('\n[Step 0.6] Generating cover images...');
if (runPython('Step 0.6', 'scripts/generate-cover.py')) {
  console.log('[Step 0.6] Cover images generated.\n');
}

// Step 0.7: Generate icons and OG image
console.log('\n[Step 0.7] Generating icons and OG image...');
if (runPython('Step 0.7', 'scripts/generate-icons.py')) {
  console.log('[Step 0.7] Icons and OG image generated.\n');
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

// Copy manifest.json
const manifestSrc = path.join(SRC_DIR, 'manifest.json');
const manifestDist = path.join(DIST_DIR, 'manifest.json');
if (fs.existsSync(manifestSrc)) {
  fs.copyFileSync(manifestSrc, manifestDist);
  console.log('  Copied manifest.json');
}

// Copy _worker.js (Pages Functions entry)
const workerSrc = path.join(SRC_DIR, '_worker.js');
const workerDist = path.join(DIST_DIR, '_worker.js');
if (fs.existsSync(workerSrc)) {
  fs.copyFileSync(workerSrc, workerDist);
  console.log('  Copied _worker.js');
}

// Remove functions/ dir if exists (we use _worker.js instead)
const functionsDist = path.join(DIST_DIR, 'functions');
if (fs.existsSync(functionsDist)) {
  fs.rmSync(functionsDist, { recursive: true });
  console.log('  Removed functions/ (using _worker.js)');
}

// Step 2: Convert content/*.md to dist/articles/*.html
const articlesDir = path.join(DIST_DIR, 'articles');
fs.mkdirSync(articlesDir, { recursive: true });

if (fs.existsSync(CONTENT_DIR)) {
  var markedParse = null;
  try {
    // Prefer vendored copy so Cloudflare Pages builds do not depend on npm install layout
    var markedMod = require(path.join(__dirname, 'vendor', 'marked'));
    markedParse = markedMod.marked || markedMod;
  } catch (e1) {
    try {
      var markedNpm = require('marked');
      markedParse = markedNpm.marked || markedNpm;
    } catch (e2) {
      console.warn('[Step 2] marked not available — skipping markdown conversion:', e2.message);
    }
  }
  if (markedParse) {
    const mdFiles = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith('.md'));
    mdFiles.forEach(file => {
      const mdContent = fs.readFileSync(path.join(CONTENT_DIR, file), 'utf-8');
      const htmlContent = markedParse(mdContent);
      const articleName = path.basename(file, '.md');
      const outPath = path.join(articlesDir, articleName + '.html');
      fs.writeFileSync(outPath, htmlContent, 'utf-8');
      console.log('  Converted content/' + file + ' -> articles/' + articleName + '.html');
    });
  }
}

// Step 3: Copy article metadata
if (fs.existsSync(path.join(DATA_DIR, 'articles.json'))) {
  fs.copyFileSync(path.join(DATA_DIR, 'articles.json'), path.join(DIST_DIR, 'articles.json'));
  console.log('  Copied articles.json');
}

console.log('\nCloudscroll build complete.');

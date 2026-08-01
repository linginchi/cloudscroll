const fs = require('fs');
const path = require('path');
const childProcess = require('child_process');

const SRC_DIR = path.resolve(__dirname, '..', 'src');
const CONTENT_DIR = path.resolve(__dirname, '..', 'content');
const DATA_DIR = path.resolve(__dirname, '..', 'data');
const DIST_DIR = path.resolve(__dirname, '..', 'dist');
const ON_PAGES = !!(process.env.CF_PAGES || process.env.CI);

function execSync(cmd, opts) {
  if (ON_PAGES && /^python\b/.test(String(cmd))) {
    console.warn('[CI/Pages] skip:', cmd);
    return Buffer.from('');
  }
  return childProcess.execSync(cmd, opts);
}

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

// Step 0: Run book extraction script (skipped when book/ is absent, e.g. Cloud Agents)
console.log('\n[Step 0] Extracting book content...');
const BOOK_DIR = path.resolve(__dirname, '..', 'book');
if (!fs.existsSync(BOOK_DIR)) {
  console.warn('[Step 0] book/ not found — skipping Word extraction (use committed src assets).');
} else {
  try {
    execSync('python scripts/extract-book.py', {
      cwd: path.resolve(__dirname, '..'),
      stdio: 'inherit',
      encoding: 'utf-8',
      timeout: 120000,
    });
    console.log('[Step 0] Book extraction complete.\n');
  } catch (e) {
    console.warn('[Step 0] Book extraction failed — continuing with committed assets:', e.message);
  }
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
  try {
    execSync('python scripts/extract-yunxin.py', {
      cwd: path.resolve(__dirname, '..'),
      stdio: 'inherit',
      encoding: 'utf-8',
      timeout: 60000,
    });
  } catch (e) {
    console.warn('[Step 0.56] Yunxin extract warning:', e.message);
  }
} else {
  console.warn('[Step 0.56] book/雲心文集 not found — using committed src/yunxin/.');
}
const distImages = path.join(DIST_DIR, 'images');
fs.mkdirSync(distImages, { recursive: true });
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
try {
  execSync('python scripts/generate-cover.py', {
    cwd: path.resolve(__dirname, '..'),
    stdio: 'inherit',
    encoding: 'utf-8',
    timeout: 60000,
  });
  console.log('[Step 0.6] Cover images generated.\n');
} catch (e) {
  console.warn('[Step 0.6] Cover generation skipped:', e.message);
}

// Step 0.7: Generate icons and OG image
console.log('\n[Step 0.7] Generating icons and OG image...');
try {
  execSync('python scripts/generate-icons.py', {
    cwd: path.resolve(__dirname, '..'),
    stdio: 'inherit',
    encoding: 'utf-8',
    timeout: 60000,
  });
  console.log('[Step 0.7] Icons and OG image generated.\n');
} catch (e) {
  console.warn('[Step 0.7] Icon generation skipped:', e.message);
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
  const jsFiles = fs.readdirSync(jsDir).filter(f => f.endsWith('.js') && f !== 'html2pdf.bundle.min.js');
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
    markedParse = require('marked').marked;
  } catch (e) {
    console.warn('[Step 2] marked missing — skip md conversion:', e.message);
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

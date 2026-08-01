#!/usr/bin/env node
/**
 * 从线上 cloudscroll.net 补齐本地缺失的媒体文件。
 * 规则：本地已有则跳过，绝不覆盖（避免误伤作者本机或线上已发布资源）。
 *
 * 用法：
 *   node scripts/sync-prod-assets.js
 *   node scripts/sync-prod-assets.js --dest dist/images   # 部署前补齐 dist
 */
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const ROOT = path.resolve(__dirname, '..');
const PROD = 'https://cloudscroll.net';
const DEFAULT_DEST = path.join(ROOT, 'src', 'images');

function parseArgs(argv) {
  var dest = DEFAULT_DEST;
  for (var i = 2; i < argv.length; i++) {
    if (argv[i] === '--dest' && argv[i + 1]) {
      dest = path.resolve(ROOT, argv[++i]);
    }
  }
  return { dest: dest };
}

function walkFiles(dir, out) {
  if (!fs.existsSync(dir)) return;
  var entries = fs.readdirSync(dir, { withFileTypes: true });
  for (var i = 0; i < entries.length; i++) {
    var e = entries[i];
    var p = path.join(dir, e.name);
    if (e.isDirectory()) walkFiles(p, out);
    else out.push(p);
  }
}

function collectImageRefs() {
  var roots = [
    path.join(ROOT, 'src', 'js'),
    path.join(ROOT, 'src'),
  ];
  var files = [];
  for (var i = 0; i < roots.length; i++) {
    var r = roots[i];
    if (!fs.existsSync(r)) continue;
    if (fs.statSync(r).isFile()) files.push(r);
    else walkFiles(r, files);
  }

  var re = /(?:["'`(]|url\()(?:\.\/)?images\/([A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp|gif|mp4|webm))/g;
  var set = Object.create(null);
  for (var f = 0; f < files.length; f++) {
    var file = files[f];
    if (!/\.(js|html|css|json|md)$/i.test(file)) continue;
    var text = fs.readFileSync(file, 'utf8');
    var m;
    while ((m = re.exec(text))) {
      set[m[1]] = true;
    }
  }

  // 构建脚本白名单中的封面等（可能未被正则扫到）
  var extras = [
    'cover_v5.jpg',
    'yunxin-cover.jpg',
    'yunxin-flyleaf.jpg',
    'yunxin-flyleaf-bg.mp4',
    'beijing-anim.mp4',
    'yunxin-weihui-bigan.jpg',
    'yunxin-guishan-autumn.jpg',
  ];
  for (var e = 0; e < extras.length; e++) set[extras[e]] = true;

  return Object.keys(set).sort();
}

function fetchToFile(url, destPath) {
  return new Promise(function (resolve, reject) {
    var mod = url.startsWith('https') ? https : http;
    var req = mod.get(url, { headers: { 'User-Agent': 'cloudscroll-sync/1.0' } }, function (res) {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        fetchToFile(res.headers.location, destPath).then(resolve, reject);
        return;
      }
      if (res.statusCode !== 200) {
        res.resume();
        reject(new Error('HTTP ' + res.statusCode + ' for ' + url));
        return;
      }
      var ctype = String(res.headers['content-type'] || '');
      if (ctype.indexOf('text/html') === 0) {
        res.resume();
        reject(new Error('Got HTML instead of asset for ' + url));
        return;
      }
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      var tmp = destPath + '.partial';
      var out = fs.createWriteStream(tmp);
      res.pipe(out);
      out.on('finish', function () {
        out.close(function () {
          fs.renameSync(tmp, destPath);
          resolve();
        });
      });
      out.on('error', function (err) {
        try { fs.unlinkSync(tmp); } catch (e) {}
        reject(err);
      });
    });
    req.on('error', reject);
  });
}

async function main() {
  var opts = parseArgs(process.argv);
  var destDir = opts.dest;
  var names = collectImageRefs();
  var skipped = 0;
  var downloaded = 0;
  var failed = 0;

  console.log('sync-prod-assets → ' + destDir);
  console.log('refs: ' + names.length + '（本地已有则跳过，绝不覆盖）\n');

  for (var i = 0; i < names.length; i++) {
    var name = names[i];
    var dest = path.join(destDir, name);
    if (fs.existsSync(dest) && fs.statSync(dest).size > 0) {
      console.log('  skip (exists): ' + name);
      skipped++;
      continue;
    }
    var url = PROD + '/images/' + name;
    try {
      await fetchToFile(url, dest);
      var size = fs.statSync(dest).size;
      console.log('  fetched: ' + name + ' (' + size + ' bytes)');
      downloaded++;
    } catch (err) {
      console.warn('  miss: ' + name + ' — ' + err.message);
      failed++;
    }
  }

  console.log('\nDone. fetched=' + downloaded + ' skipped=' + skipped + ' failed=' + failed);
  if (failed > 0 && downloaded === 0 && skipped === 0) process.exit(1);
}

main().catch(function (err) {
  console.error(err);
  process.exit(1);
});

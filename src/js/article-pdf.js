// Shared article / book → PDF export & share helper (html2pdf)
(function (global) {
  'use strict';

  // A4 usable width ≈ 190mm ≈ 718px @96dpi; keep a safe content box.
  var PDF_WIDTH = 700;

  function sanitizeFilename(name) {
    var s = String(name || 'article')
      .replace(/[\\/:*?"<>|]+/g, '')
      .replace(/\s+/g, ' ')
      .trim();
    if (!s) s = 'article';
    if (s.length > 80) s = s.slice(0, 80);
    return s + '.pdf';
  }

  function ensureHtml2Pdf(callback) {
    if (typeof global.html2pdf === 'function') {
      callback(null);
      return;
    }
    var existing = document.querySelector('script[data-cloudscroll-html2pdf]');
    if (existing) {
      existing.addEventListener('load', function () { callback(null); });
      existing.addEventListener('error', function () {
        callback(new Error('html2pdf load failed'));
      });
      return;
    }
    var script = document.createElement('script');
    // Load from CDN so Pages Git builds are not blocked by the large vendored bundle
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
    script.crossOrigin = 'anonymous';
    script.async = true;
    script.setAttribute('data-cloudscroll-html2pdf', '1');
    script.onload = function () { callback(null); };
    script.onerror = function () { callback(new Error('html2pdf load failed')); };
    document.head.appendChild(script);
  }

  function fetchJson(url) {
    return new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url, true);
      xhr.timeout = 20000;
      xhr.onload = function () {
        if (xhr.status !== 200) {
          reject(new Error('HTTP ' + xhr.status));
          return;
        }
        try {
          resolve(JSON.parse(xhr.responseText));
        } catch (e) {
          reject(e);
        }
      };
      xhr.onerror = function () { reject(new Error('network')); };
      xhr.ontimeout = function () { reject(new Error('timeout')); };
      xhr.send();
    });
  }

  function showPdfOverlay(msg) {
    var old = document.getElementById('cs-pdf-overlay');
    if (old) {
      var t = old.querySelector('.cs-pdf-overlay-text');
      if (t && msg) t.textContent = msg;
      return old;
    }
    var overlay = document.createElement('div');
    overlay.id = 'cs-pdf-overlay';
    overlay.setAttribute('aria-live', 'polite');
    overlay.style.cssText = [
      'position:fixed',
      'inset:0',
      'z-index:2147483600',
      'background:rgba(250,246,240,0.96)',
      'display:flex',
      'align-items:center',
      'justify-content:center',
      'padding:24px',
      'box-sizing:border-box'
    ].join(';');
    var text = document.createElement('div');
    text.className = 'cs-pdf-overlay-text';
    text.textContent = msg || '正在生成 PDF…';
    text.style.cssText = [
      'font-family:"Noto Serif TC","Noto Serif SC","Songti SC","PMingLiU",serif',
      'font-size:16px',
      'letter-spacing:0.06em',
      'color:#2c2416',
      'text-align:center',
      'line-height:1.7',
      'max-width:280px'
    ].join(';');
    overlay.appendChild(text);
    document.body.appendChild(overlay);
    return overlay;
  }

  function hidePdfOverlay() {
    var old = document.getElementById('cs-pdf-overlay');
    if (old && old.parentNode) old.parentNode.removeChild(old);
  }

  function toastWithOverlay(toast, msg) {
    showPdfOverlay(msg);
    toast(msg);
  }

  function destroyPdfFrame() {
    var iframe = document.getElementById('cs-pdf-frame');
    if (iframe && iframe.parentNode) iframe.parentNode.removeChild(iframe);
  }

  /**
   * Isolated iframe avoids site CSS (overflow:clip, flex .page, transforms)
   * which otherwise clip/offset html2canvas output → misaligned PDF.
   */
  function ensurePdfFrame(callback) {
    var existing = document.getElementById('cs-pdf-frame');
    if (existing && existing.contentDocument && existing.contentDocument.body) {
      callback(existing.contentDocument, existing);
      return;
    }

    destroyPdfFrame();

    var iframe = document.createElement('iframe');
    iframe.id = 'cs-pdf-frame';
    iframe.setAttribute('aria-hidden', 'true');
    iframe.style.cssText = [
      'position:fixed',
      'left:0',
      'top:0',
      'width:' + PDF_WIDTH + 'px',
      'height:100vh',
      'border:0',
      'margin:0',
      'padding:0',
      'z-index:2147483000',
      'background:#faf6f0'
    ].join(';');
    document.body.appendChild(iframe);

    var doc = iframe.contentDocument || iframe.contentWindow.document;
    doc.open();
    doc.write(
      '<!DOCTYPE html><html><head><meta charset="utf-8">' +
      '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&family=Noto+Serif+SC:wght@400;700&display=swap">' +
      '<style>' +
      'html,body{margin:0;padding:0;background:#faf6f0;width:' + PDF_WIDTH + 'px;}' +
      'body{font-family:"Noto Serif TC","Noto Serif SC","Songti SC","PMingLiU","Microsoft YaHei",serif;color:#2c2416;}' +
      '*,*::before,*::after{box-sizing:border-box;}' +
      'h1,h2,p,ol,li,div,section,figure{margin:0;padding:0;max-width:100%;}' +
      'h1,h2,p{word-wrap:break-word;overflow-wrap:anywhere;}' +
      'img{max-width:100%;height:auto;display:block;}' +
      '.cs-pdf-root{display:block;width:' + PDF_WIDTH + 'px;padding:28px 32px;background:#faf6f0;line-height:1.85;}' +
      '.cs-pdf-brand{font-size:13px;letter-spacing:0.12em;color:#8a7a66;margin:0 0 16px;}' +
      '.cs-pdf-title{font-size:22px;font-weight:700;letter-spacing:0.04em;margin:0 0 10px;line-height:1.45;}' +
      '.cs-pdf-sub{font-size:13px;color:#8a7a66;margin:0 0 10px;letter-spacing:0.03em;line-height:1.5;}' +
      '.cs-pdf-h2{font-size:18px;font-weight:700;letter-spacing:0.04em;margin:0 0 12px;line-height:1.45;}' +
      '.cs-pdf-p{font-size:15px;margin:0 0 12px;text-align:justify;letter-spacing:0.02em;line-height:1.85;}' +
      '.cs-pdf-ol{margin:0;padding-left:1.35em;}' +
      '.cs-pdf-ol li{margin:5px 0;font-size:14px;letter-spacing:0.02em;line-height:1.55;}' +
      '.cs-pdf-foot{margin-top:24px;padding-top:12px;border-top:1px solid #e0d6c6;font-size:12px;color:#8a7a66;letter-spacing:0.06em;}' +
      '.cs-pdf-cover{position:relative;width:' + PDF_WIDTH + 'px;min-height:990px;margin:0;padding:0;overflow:hidden;background:#1a1510;}' +
      '.cs-pdf-cover-img{display:block;width:' + PDF_WIDTH + 'px;height:990px;object-fit:cover;}' +
      '.cs-pdf-cover-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,0.25) 0%,rgba(20,16,12,0.55) 55%,rgba(20,16,12,0.78) 100%);}' +
      '.cs-pdf-cover-text{position:absolute;left:40px;right:40px;bottom:72px;color:#faf6f0;text-align:left;}' +
      '.cs-pdf-cover-brand{font-size:14px;letter-spacing:0.28em;margin:0 0 18px;opacity:0.9;}' +
      '.cs-pdf-cover-title{font-size:28px;font-weight:700;letter-spacing:0.08em;margin:0 0 10px;line-height:1.35;}' +
      '.cs-pdf-cover-sub{font-size:15px;letter-spacing:0.06em;margin:0 0 8px;opacity:0.92;}' +
      '.cs-pdf-cover-meta{font-size:13px;letter-spacing:0.12em;margin:12px 0 0;opacity:0.85;}' +
      '.cs-pdf-notice{font-size:15px;line-height:1.9;margin:24px 0;text-align:justify;}' +
      '.cs-pdf-figure{margin:14px 0 18px;border:1px solid #e0d6c6;border-radius:3px;overflow:hidden;background:#efe8dc;}' +
      '.cs-pdf-figure img{display:block;width:100%;height:auto;}' +
      '</style></head><body></body></html>'
    );
    doc.close();

    setTimeout(function () {
      callback(doc, iframe);
    }, 40);
  }

  function clearFrameBody(doc) {
    while (doc.body.firstChild) doc.body.removeChild(doc.body.firstChild);
  }

  function mountRoot(doc, wrap) {
    clearFrameBody(doc);
    doc.body.appendChild(wrap);
    // Force layout in iframe
    void wrap.offsetHeight;
    return wrap;
  }

  function waitForImages(root, timeoutMs) {
    var imgs = root ? root.querySelectorAll('img') : [];
    if (!imgs.length) return Promise.resolve();

    return new Promise(function (resolve) {
      var done = false;
      var remaining = imgs.length;
      var cleanups = [];
      var timeout = setTimeout(finish, timeoutMs || 12000);

      function finish() {
        if (done) return;
        done = true;
        clearTimeout(timeout);
        for (var c = 0; c < cleanups.length; c++) cleanups[c]();
        resolve();
      }

      function markDone() {
        if (done) return;
        remaining -= 1;
        if (remaining <= 0) finish();
      }

      function decodeThenDone(img) {
        if (typeof img.decode === 'function' && img.naturalWidth) {
          Promise.resolve(img.decode()).catch(function () {}).then(markDone);
          return;
        }
        markDone();
      }

      for (var i = 0; i < imgs.length; i++) {
        (function (img) {
          if (img.complete) {
            decodeThenDone(img);
            return;
          }

          function onLoad() {
            remove();
            decodeThenDone(img);
          }

          function onError() {
            remove();
            markDone();
          }

          function remove() {
            img.removeEventListener('load', onLoad);
            img.removeEventListener('error', onError);
          }

          cleanups.push(remove);
          img.addEventListener('load', onLoad);
          img.addEventListener('error', onError);
        })(imgs[i]);
      }
    });
  }

  function isSameOriginUrl(url) {
    try {
      var loc = global.location;
      if (!loc || !loc.origin) return false;
      var resolved = new URL(url, loc.href || document.baseURI);
      return resolved.origin === loc.origin;
    } catch (e) {
      return false;
    }
  }

  function compressImageSrc(url, maxEdge, quality) {
    var src = String(url || '').trim();
    if (!src || !isSameOriginUrl(src)) return Promise.resolve(src);

    return new Promise(function (resolve) {
      var img = new Image();
      img.onload = function () {
        try {
          var w = img.naturalWidth || img.width;
          var h = img.naturalHeight || img.height;
          var edge = maxEdge || 900;
          if (!w || !h) {
            resolve(src);
            return;
          }

          var scale = Math.min(1, edge / Math.max(w, h));
          var canvas = document.createElement('canvas');
          canvas.width = Math.max(1, Math.round(w * scale));
          canvas.height = Math.max(1, Math.round(h * scale));
          var ctx = canvas.getContext('2d');
          if (!ctx) {
            resolve(src);
            return;
          }
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          resolve(canvas.toDataURL('image/jpeg', quality || 0.82));
        } catch (e) {
          resolve(src);
        }
      };
      img.onerror = function () { resolve(src); };
      img.src = src;
    });
  }

  function prepareBookChunk(chunk) {
    if (!chunk || !chunk.items || !chunk.items.length) return Promise.resolve(chunk);

    var jobs = [];
    for (var i = 0; i < chunk.items.length; i++) {
      (function (item) {
        if (!item || item.kind !== 'image' || !item.src) {
          jobs.push(Promise.resolve(item));
          return;
        }
        jobs.push(compressImageSrc(item.src, 900, 0.82).then(function (compressedSrc) {
          if (compressedSrc === item.src) return item;
          var copy = {};
          for (var key in item) {
            if (Object.prototype.hasOwnProperty.call(item, key)) copy[key] = item[key];
          }
          copy.src = compressedSrc;
          return copy;
        }));
      })(chunk.items[i]);
    }

    return Promise.all(jobs).then(function (items) {
      var copy = {};
      for (var key in chunk) {
        if (Object.prototype.hasOwnProperty.call(chunk, key)) copy[key] = chunk[key];
      }
      copy.items = items;
      return copy;
    });
  }

  function createRootShell(doc) {
    var wrap = doc.createElement('div');
    wrap.className = 'cs-pdf-root';
    return wrap;
  }

  function appendBrand(doc, wrap) {
    var brand = doc.createElement('div');
    brand.className = 'cs-pdf-brand';
    brand.textContent = '雲箋文舍';
    wrap.appendChild(brand);
  }

  function appendFooter(doc, wrap) {
    var foot = doc.createElement('div');
    foot.className = 'cs-pdf-foot';
    foot.textContent = 'cloudscroll.net';
    wrap.appendChild(foot);
  }

  function el(doc, tag, text, className) {
    var node = doc.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function buildPrintRoot(doc, sourceEl, title, subtitle) {
    var wrap = createRootShell(doc);
    appendBrand(doc, wrap);

    if (title) wrap.appendChild(el(doc, 'h1', title, 'cs-pdf-title'));
    if (subtitle) wrap.appendChild(el(doc, 'p', subtitle, 'cs-pdf-sub'));

    var body = doc.createElement('div');
    body.className = 'cs-pdf-body';
    // Import HTML into iframe document
    body.innerHTML = sourceEl.innerHTML;

    var removeSelectors = [
      'nav', '.yunxin-pager', '.reader-actions', 'button',
      'a.yunxin-pager-btn', '.yunxin-author-block', '#flaps-avatar'
    ];
    for (var i = 0; i < removeSelectors.length; i++) {
      var nodes = body.querySelectorAll(removeSelectors[i]);
      for (var j = 0; j < nodes.length; j++) {
        if (nodes[j].parentNode) nodes[j].parentNode.removeChild(nodes[j]);
      }
    }

    var paragraphs = body.querySelectorAll('p, h1, h2, h3, li, div');
    for (var p = 0; p < paragraphs.length; p++) {
      paragraphs[p].style.maxWidth = '100%';
      paragraphs[p].style.overflowWrap = 'anywhere';
      paragraphs[p].style.wordWrap = 'break-word';
    }

    var imgs = body.querySelectorAll('img');
    for (var k = 0; k < imgs.length; k++) {
      imgs[k].style.maxWidth = '100%';
      imgs[k].style.height = 'auto';
      imgs[k].style.display = 'block';
      imgs[k].style.margin = '12px auto';
    }

    wrap.appendChild(body);
    appendFooter(doc, wrap);
    return mountRoot(doc, wrap);
  }

  function buildBookChunkRoot(doc, chunk) {
    if (chunk.kind === 'cover') {
      if (!chunk.coverSrc) {
        var textWrap = createRootShell(doc);
        if (chunk.showBrand !== false) appendBrand(doc, textWrap);
        textWrap.appendChild(el(doc, 'h1', chunk.title || '文集', 'cs-pdf-title'));
        if (chunk.subtitle) {
          textWrap.appendChild(el(doc, 'p', chunk.subtitle, 'cs-pdf-sub'));
        }
        textWrap.appendChild(el(
          doc,
          'p',
          (chunk.author || '林樺') + ' · 雲箋文舍',
          'cs-pdf-sub'
        ));
        appendFooter(doc, textWrap);
        return mountRoot(doc, textWrap);
      }

      var cover = doc.createElement('section');
      cover.className = 'cs-pdf-cover';
      var coverImg = doc.createElement('img');
      coverImg.className = 'cs-pdf-cover-img';
      coverImg.src = chunk.coverSrc;
      coverImg.alt = chunk.title || '文集';
      cover.appendChild(coverImg);
      var shade = doc.createElement('div');
      shade.className = 'cs-pdf-cover-shade';
      cover.appendChild(shade);
      var text = doc.createElement('div');
      text.className = 'cs-pdf-cover-text';
      text.appendChild(el(doc, 'p', '雲箋文舍', 'cs-pdf-cover-brand'));
      text.appendChild(el(doc, 'h1', chunk.title || '文集', 'cs-pdf-cover-title'));
      if (chunk.subtitle) {
        text.appendChild(el(doc, 'p', chunk.subtitle, 'cs-pdf-cover-sub'));
      }
      text.appendChild(el(
        doc,
        'p',
        (chunk.author || '林樺') + ' · 精选图文版',
        'cs-pdf-cover-meta'
      ));
      cover.appendChild(text);
      return mountRoot(doc, cover);
    }

    var wrap = createRootShell(doc);
    if (chunk.showBrand !== false) appendBrand(doc, wrap);

    if (chunk.kind === 'notice') {
      wrap.appendChild(el(doc, 'h2', '說明', 'cs-pdf-h2'));
      wrap.appendChild(el(doc, 'p', chunk.text || '', 'cs-pdf-notice'));
      appendFooter(doc, wrap);
      return mountRoot(doc, wrap);
    }

    if (chunk.kind === 'toc') {
      wrap.appendChild(el(doc, 'h2', '目錄', 'cs-pdf-h2'));
      var toc = el(doc, 'ol', null, 'cs-pdf-ol');
      var titles = chunk.titles || [];
      for (var t = 0; t < titles.length; t++) {
        var li = doc.createElement('li');
        li.textContent = titles[t] || ('第' + (t + 1) + '篇');
        toc.appendChild(li);
      }
      wrap.appendChild(toc);
      appendFooter(doc, wrap);
      return mountRoot(doc, wrap);
    }

    wrap.appendChild(el(doc, 'h2', chunk.title || '文章', 'cs-pdf-h2'));
    if (chunk.sectionTitle) {
      wrap.appendChild(el(doc, 'p', chunk.sectionTitle, 'cs-pdf-sub'));
    }
    var items = chunk.items || [];
    if (items.length) {
      for (var i = 0; i < items.length; i++) {
        if (!items[i]) continue;
        if (items[i].kind === 'image' && items[i].src) {
          var figure = doc.createElement('div');
          figure.className = 'cs-pdf-figure';
          var img = doc.createElement('img');
          img.src = items[i].src;
          img.alt = chunk.title || '文章配圖';
          figure.appendChild(img);
          wrap.appendChild(figure);
        } else if (items[i].kind === 'text' && items[i].text) {
          wrap.appendChild(el(doc, 'p', items[i].text, 'cs-pdf-p'));
        }
      }
    } else {
      var paras = chunk.paragraphs || [];
      for (var p = 0; p < paras.length; p++) {
        if (!paras[p]) continue;
        wrap.appendChild(el(doc, 'p', paras[p], 'cs-pdf-p'));
      }
    }
    appendFooter(doc, wrap);
    return mountRoot(doc, wrap);
  }

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
  }

  function tryShareFile(file, meta, onShared, onFallback) {
    var payload = {
      files: [file],
      title: meta.title || file.name,
      text: meta.text || meta.title || file.name
    };
    if (typeof navigator.canShare === 'function' && navigator.canShare(payload) && typeof navigator.share === 'function') {
      navigator.share(payload).then(onShared).catch(function (err) {
        if (err && err.name === 'AbortError') {
          onShared();
          return;
        }
        onFallback();
      });
      return;
    }
    onFallback();
  }

  function finishWithBlob(blob, opts) {
    var toast = opts.toast;
    var onDone = opts.onDone;
    var title = opts.title || '';
    var filename = opts.filename;

    destroyPdfFrame();
    hidePdfOverlay();

    var file;
    try {
      file = new File([blob], filename, { type: 'application/pdf' });
    } catch (e) {
      file = null;
    }

    function finishDownload() {
      downloadBlob(blob, filename);
      toast('PDF 已下載。可從檔案管理器分享到微信');
      onDone();
    }

    if (file) {
      tryShareFile(
        file,
        { title: title || filename, text: (title || '') + ' — 雲箋文舍' },
        function () {
          toast('已打開系統分享');
          onDone();
        },
        finishDownload
      );
      return;
    }
    finishDownload();
  }

  function pdfOptions(filename) {
    return {
      // Keep margins modest; content width already sized for A4.
      margin: [10, 10, 12, 10],
      filename: filename || 'cloudscroll.pdf',
      image: { type: 'jpeg', quality: 0.92 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#faf6f0',
        width: PDF_WIDTH,
        windowWidth: PDF_WIDTH,
        scrollX: 0,
        scrollY: 0,
        x: 0,
        y: 0
      },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['css', 'legacy'] }
    };
  }

  function renderRootToPdf(root, opts) {
    var toast = opts.toast;
    var onDone = opts.onDone;
    var onError = opts.onError;
    var title = opts.title || '';
    var filename = opts.filename;

    var worker = global.html2pdf()
      .set(pdfOptions(filename))
      .from(root)
      .outputPdf('blob');

    return Promise.resolve(worker).then(function (blob) {
      if (!blob || !blob.size) {
        destroyPdfFrame();
        hidePdfOverlay();
        toast('PDF 生成失敗：內容為空');
        onError(new Error('empty pdf'));
        return;
      }
      finishWithBlob(blob, {
        toast: toast,
        onDone: onDone,
        title: title,
        filename: filename
      });
    }).catch(function (e) {
      destroyPdfFrame();
      hidePdfOverlay();
      toast('PDF 生成失敗，請稍後再試');
      onError(e);
    });
  }

  function renderBookChunksToPdf(chunks, opts) {
    var toast = opts.toast;
    var onDone = opts.onDone;
    var onError = opts.onError;
    var title = opts.title || '';
    var filename = opts.filename;
    var opt = pdfOptions(filename);

    if (!chunks.length) {
      destroyPdfFrame();
      hidePdfOverlay();
      toast('全書內容為空');
      onError(new Error('no chunks'));
      return;
    }

    ensurePdfFrame(function (doc) {
      var worker = global.html2pdf().set(opt);
      var i = 0;

      function fail(e) {
        destroyPdfFrame();
        hidePdfOverlay();
        toast('PDF 生成失敗，請稍後再試');
        onError(e);
      }

      function step() {
        if (i >= chunks.length) {
          Promise.resolve(worker.outputPdf('blob')).then(function (blob) {
            if (!blob || !blob.size || blob.size < 8000) {
              destroyPdfFrame();
              hidePdfOverlay();
              toast('PDF 生成失敗：內容為空');
              onError(new Error('empty pdf'));
              return;
            }
            finishWithBlob(blob, {
              toast: toast,
              onDone: onDone,
              title: title,
              filename: filename
            });
          }).catch(fail);
          return;
        }

        var progress = Math.round((i / chunks.length) * 100);
        toastWithOverlay(toast, '正在生成 PDF… ' + progress + '%');

        prepareBookChunk(chunks[i]).then(function (chunk) {
          var root = buildBookChunkRoot(doc, chunk);
          return waitForImages(root, 12000).then(function () {
            if (i === 0) {
              worker = worker.from(root).toPdf();
            } else {
              worker = worker.get('pdf').then(function (pdf) {
                pdf.addPage();
              }).from(root).toContainer().toCanvas().toPdf();
            }
            return Promise.resolve(worker);
          });
        }).then(function () {
          i += 1;
          setTimeout(step, 30);
        }).catch(fail);
      }

      showPdfOverlay('正在生成 PDF…');
      step();
    });
  }

  function exportArticlePdf(options) {
    var opts = options || {};
    var sourceEl = opts.sourceEl;
    var toast = typeof opts.onToast === 'function' ? opts.onToast : function () {};
    var onDone = typeof opts.onDone === 'function' ? opts.onDone : function () {};
    var onError = typeof opts.onError === 'function' ? opts.onError : function () {};

    if (!sourceEl) {
      onError(new Error('no source'));
      toast('找不到文章內容');
      return;
    }

    var title = opts.title || '';
    var filename = sanitizeFilename(opts.filename || title || 'article');
    toastWithOverlay(toast, '正在生成 PDF…');

    ensureHtml2Pdf(function (err) {
      if (err || typeof global.html2pdf !== 'function') {
        hidePdfOverlay();
        toast('PDF 組件載入失敗，請稍後再試');
        onError(err || new Error('html2pdf missing'));
        return;
      }

      ensurePdfFrame(function (doc) {
        try {
          var root = buildPrintRoot(doc, sourceEl, title, opts.subtitle || '');
          setTimeout(function () {
            renderRootToPdf(root, {
              toast: toast,
              onDone: onDone,
              onError: onError,
              title: title,
              filename: filename
            });
          }, 50);
        } catch (e) {
          destroyPdfFrame();
          hidePdfOverlay();
          toast('PDF 生成失敗');
          onError(e);
        }
      });
    });
  }

  function blocksToParagraphs(blocks) {
    var out = [];
    if (!blocks || !blocks.length) return out;
    for (var i = 0; i < blocks.length; i++) {
      var b = blocks[i];
      if (!b) continue;
      if (b.type === 'text' && b.content) out.push(String(b.content).trim());
      else if (typeof b === 'string' && b.trim()) out.push(b.trim());
    }
    return out;
  }

  var pdfHelpersPromise = null;

  function ensurePdfHelpers(callback) {
    if (global.CloudscrollPdfHelpers) {
      callback(null);
      return;
    }
    if (!pdfHelpersPromise) {
      pdfHelpersPromise = import('./pdf-book-helpers.js').then(function (mod) {
        global.CloudscrollPdfHelpers = mod;
        return mod;
      }).catch(function (err) {
        pdfHelpersPromise = null;
        throw err;
      });
    }
    pdfHelpersPromise.then(function () {
      callback(null);
    }).catch(function (err) {
      callback(err);
    });
  }

  function loadTravelVolumeBook(volume) {
    var vol = parseInt(volume, 10) || 1;
    return new Promise(function (resolve, reject) {
      ensurePdfHelpers(function (err) {
        if (err) {
          reject(err);
          return;
        }
        var H = global.CloudscrollPdfHelpers;
        fetchJson('book/data.json').then(function (data) {
          var chapters = data.chapters || [];
          var ch = chapters[vol - 1];
          if (!ch) throw new Error('volume not found');

          var list = ch.articles || [];
          var title = ch.zh || ('第' + vol + '輯');
          var jobs = [];

          if (vol === 1) {
            jobs.push(
              fetchJson('book/00-preface.json').then(function (pref) {
                return {
                  title: pref.zh || '自序',
                  sectionTitle: '自序',
                  paragraphs: blocksToParagraphs(pref.blocks),
                  images: H.pickArticleImages(pref.blocks)
                };
              }).catch(function () { return null; })
            );
          }

          for (var i = 0; i < list.length; i++) {
            (function (art) {
              jobs.push(
                fetchJson('book/' + art.id + '.json').then(function (full) {
                  return {
                    title: art.zh || full.zh || art.id,
                    sectionTitle: title,
                    paragraphs: blocksToParagraphs(full.blocks),
                    images: H.pickArticleImages(full.blocks)
                  };
                }).catch(function () {
                  return {
                    title: art.zh || art.id,
                    sectionTitle: title,
                    paragraphs: [art.subtitle || '（本文暫未能載入）'],
                    images: []
                  };
                })
              );
            })(list[i]);
          }

          return Promise.all(jobs).then(function (articles) {
            var cleaned = [];
            for (var j = 0; j < articles.length; j++) {
              if (articles[j]) cleaned.push(articles[j]);
            }
            return {
              title: '我的人生旅行 · ' + title,
              subtitle: data.title_en || '',
              author: data.author || '林樺',
              volume: vol,
              coverSrc: H.volumeCoverSrc(vol),
              articles: cleaned
            };
          });
        }).then(resolve).catch(reject);
      });
    });
  }

  function loadYunxinBook() {
    return fetchJson('yunxin/data.json').then(function (data) {
      var list = data.articles || [];
      var jobs = [];
      for (var i = 0; i < list.length; i++) {
        (function (art) {
          jobs.push(
            fetchJson('yunxin/' + art.id + '.json').then(function (full) {
              var paras = full.paragraphs || [];
              var cleaned = [];
              for (var p = 0; p < paras.length; p++) {
                if (paras[p]) cleaned.push(String(paras[p]).trim());
              }
              return {
                title: art.title || art.zh || full.title || art.id,
                sectionTitle: art.section_title || '',
                paragraphs: cleaned
              };
            }).catch(function () {
              return {
                title: art.title || art.zh || art.id,
                sectionTitle: art.section_title || '',
                paragraphs: ['（本文暫未能載入）']
              };
            })
          );
        })(list[i]);
      }

      return Promise.all(jobs).then(function (articles) {
        return {
          title: data.book || '雲心文集',
          subtitle: '詩．詞．散文．雜記',
          author: data.author || '林樺',
          articles: articles
        };
      });
    });
  }

  function buildBookChunks(book) {
    var articles = book.articles || [];
    var chunks = [];
    var H = global.CloudscrollPdfHelpers || {};
    var hasCoverImage = !!book.coverSrc;
    var noticeText = H.NOTICE_TEXT ||
      '本 PDF 为精选图文版，便于分享阅读。完整内容请在手机打开 cloudscroll.net 在线阅读。';

    chunks.push({
      kind: 'cover',
      title: book.title,
      subtitle: book.subtitle,
      author: book.author,
      coverSrc: book.coverSrc || '',
      showBrand: !hasCoverImage
    });

    if (hasCoverImage) {
      chunks.push({
        kind: 'notice',
        text: noticeText,
        showBrand: true
      });
    }

    var titles = [];
    for (var i = 0; i < articles.length; i++) {
      titles.push(articles[i].title || ('第' + (i + 1) + '篇'));
    }

    var tocSize = 35;
    for (var t = 0; t < titles.length || t === 0; t += tocSize) {
      if (!titles.length && t > 0) break;
      chunks.push({
        kind: 'toc',
        titles: titles.slice(t, t + tocSize),
        showBrand: t === 0
      });
      if (!titles.length) break;
    }

    for (var a = 0; a < articles.length; a++) {
      var art = articles[a];
      var paras = art.paragraphs || [];
      var images = art.images || [];
      var interleave = H.interleaveTextAndImages;
      var items = typeof interleave === 'function'
        ? interleave(paras, images)
        : [];
      var batch = images.length ? 10 : 16;
      if (!items.length && !paras.length) {
        chunks.push({
          kind: 'article',
          title: art.title,
          sectionTitle: art.sectionTitle,
          items: [{ kind: 'text', text: '（無正文）' }],
          paragraphs: ['（無正文）']
        });
        continue;
      }
      if (!items.length) {
        for (var p = 0; p < paras.length; p += batch) {
          chunks.push({
            kind: 'article',
            title: p === 0 ? art.title : (art.title + '（續）'),
            sectionTitle: p === 0 ? (art.sectionTitle || '') : '',
            paragraphs: paras.slice(p, p + batch),
            showBrand: p === 0
          });
        }
        continue;
      }
      for (var itemStart = 0; itemStart < items.length; itemStart += batch) {
        chunks.push({
          kind: 'article',
          title: itemStart === 0 ? art.title : (art.title + '（續）'),
          sectionTitle: itemStart === 0 ? (art.sectionTitle || '') : '',
          items: items.slice(itemStart, itemStart + batch),
          showBrand: itemStart === 0
        });
      }
    }
    return chunks;
  }

  function exportBookPdf(options) {
    var opts = options || {};
    var toast = typeof opts.onToast === 'function' ? opts.onToast : function () {};
    var onDone = typeof opts.onDone === 'function' ? opts.onDone : function () {};
    var onError = typeof opts.onError === 'function' ? opts.onError : function () {};

    toastWithOverlay(toast, '正在載入全書內容…');

    var loader = opts.kind === 'yunxin'
      ? loadYunxinBook()
      : new Promise(function (resolve, reject) {
          ensurePdfHelpers(function (err) {
            if (err) {
              reject(err);
              return;
            }
            loadTravelVolumeBook(opts.volume).then(resolve).catch(reject);
          });
        });

    loader.then(function (book) {
      if (!book.articles || !book.articles.length) {
        hidePdfOverlay();
        toast('全書內容為空');
        onError(new Error('no articles'));
        return;
      }

      ensureHtml2Pdf(function (err) {
        if (err || typeof global.html2pdf !== 'function') {
          hidePdfOverlay();
          toast('PDF 組件載入失敗，請稍後再試');
          onError(err || new Error('html2pdf missing'));
          return;
        }

        var chunks = buildBookChunks(book);
        toastWithOverlay(toast, '正在生成 PDF（分段渲染，請稍候）…');
        renderBookChunksToPdf(chunks, {
          toast: toast,
          onDone: onDone,
          onError: onError,
          title: book.title,
          filename: sanitizeFilename(book.title || 'book')
        });
      });
    }).catch(function (e) {
      hidePdfOverlay();
      toast('全書載入失敗，請稍後再試');
      onError(e);
    });
  }

  global.CloudscrollPdf = {
    exportArticle: exportArticlePdf,
    exportBook: exportBookPdf,
    loadTravelVolumeBook: loadTravelVolumeBook,
    loadYunxinBook: loadYunxinBook,
    sanitizeFilename: sanitizeFilename
  };
})(typeof window !== 'undefined' ? window : this);

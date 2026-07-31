(function() {
  'use strict';

  var shareOverlay = document.getElementById('share-overlay');
  var shareCloseBtn = document.getElementById('share-close-btn');
  var currentBookMeta = null;

  function loadData() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/data.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          renderShelf(data);
        } catch(e) {
          renderShelf(null);
        }
      } else {
        renderShelf(null);
      }
    };
    xhr.onerror = function() { renderShelf(null); };
    xhr.send();
  }

  function isWeChat() {
    return /MicroMessenger/i.test(navigator.userAgent);
  }

  function isMobile() {
    return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  }

  function showToast(msg, durationMs) {
    var old = document.getElementById('shelf-share-toast');
    if (old) old.remove();
    var el = document.createElement('div');
    el.id = 'shelf-share-toast';
    el.className = 'reader-share-toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function() { el.classList.add('show'); }, 10);
    setTimeout(function() {
      el.classList.remove('show');
      setTimeout(function() { if (el.parentNode) el.parentNode.removeChild(el); }, 250);
    }, durationMs || 2400);
  }

  function closeShare() {
    if (shareOverlay) shareOverlay.classList.remove('show');
  }

  function updateShareDialogForEnv() {
    var tip = document.getElementById('share-wx-tip');
    var friendBtn = document.getElementById('share-friend-btn');
    var timelineBtn = document.getElementById('share-timeline-btn');
    var copyBtn = document.getElementById('share-copy-btn');
    if (!tip) return;

    if (isWeChat()) {
      tip.style.display = 'block';
      tip.textContent = '微信中請點擊右上角「…」分享連結；也可下載 PDF 後從檔案發送給朋友。';
      if (friendBtn) friendBtn.style.display = 'none';
      if (timelineBtn) timelineBtn.style.display = 'none';
      if (copyBtn) copyBtn.style.display = '';
      return;
    }

    if (!isMobile()) {
      tip.style.display = 'block';
      tip.textContent = '電腦可複製連結或下載 PDF；再到微信（或其他應用）貼上／發送檔案。';
      if (friendBtn) friendBtn.style.display = 'none';
      if (timelineBtn) timelineBtn.style.display = 'none';
      if (copyBtn) copyBtn.style.display = '';
      return;
    }

    tip.style.display = 'none';
    if (friendBtn) friendBtn.style.display = '';
    if (timelineBtn) timelineBtn.style.display = '';
    if (copyBtn) copyBtn.style.display = '';
  }

  function copyShareLink(link) {
    var finished = false;
    function done() {
      if (finished) return;
      finished = true;
      closeShare();
      showToast('連結已複製。請打開微信，貼上發送給朋友或發到朋友圈');
    }

    try {
      var ta = document.createElement('textarea');
      ta.value = link;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    } catch (e) {}

    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        navigator.clipboard.writeText(link).then(done).catch(done);
      } catch (e) {
        done();
        return;
      }
      setTimeout(done, 250);
      return;
    }
    done();
  }

  function doShare(options) {
    var d = window.__wxShareData || currentBookMeta || {};
    if (isWeChat() && typeof WeixinJSBridge !== 'undefined') {
      WeixinJSBridge.invoke(options.method, {
        title: d.title || '',
        desc: options.desc ? (d.desc || '') : '',
        link: d.link || '',
        img_url: d.imgUrl || ''
      }, function() { closeShare(); });
      return;
    }

    if (typeof navigator.share === 'function' && isMobile()) {
      navigator.share({
        title: d.title || '',
        text: d.desc || '',
        url: d.link || ''
      }).then(closeShare).catch(function(err) {
        if (err && err.name === 'AbortError') {
          closeShare();
          return;
        }
        copyShareLink(d.link || '');
      });
      return;
    }

    copyShareLink(d.link || '');
  }

  function openBookShare(meta) {
    currentBookMeta = meta;
    window.__wxShareData = {
      title: meta.title,
      desc: meta.desc,
      link: meta.link,
      imgUrl: meta.imgUrl
    };
    updateShareDialogForEnv();
    if (shareOverlay) shareOverlay.classList.add('show');
  }

  function exportCurrentBookPdf() {
    if (!currentBookMeta) return;
    if (!window.CloudscrollPdf || typeof window.CloudscrollPdf.exportBook !== 'function') {
      showToast('PDF 功能暫不可用');
      return;
    }

    var opts = {
      onToast: function(msg) {
        var long = /正在|已下載|系統分享|載入/.test(msg);
        showToast(msg, long ? 5000 : 2400);
      },
      onDone: closeShare
    };

    if (currentBookMeta.kind === 'yunxin') {
      opts.kind = 'yunxin';
    } else {
      opts.kind = 'travel';
      opts.volume = currentBookMeta.volume;
    }

    window.CloudscrollPdf.exportBook(opts);
  }

  function renderShelf(data) {
    var container = document.getElementById('shelf-books');
    if (!container) return;

    var chapters = data ? data.chapters : [];
    var covers = data ? data.covers || {} : {};
    var origin = window.location.origin || '';

    var html = '';
    for (var i = 0; i < chapters.length; i++) {
      var ch = chapters[i];
      var vol = i + 1;
      var coverSrc = covers['v' + vol] ? 'book/' + covers['v' + vol] : '';
      var volLabel = ch.zh ? ch.zh.split(' ').pop() : '';
      var volClass = 'v' + vol;
      var bookTitle = ch.zh || ('第' + vol + '輯');

      html += '<div class="book-slot">';
      html += '<div class="book-card ' + volClass + '" data-volume="' + vol + '">';
      html += '<div class="book-spine">';
      html +=   '<div class="spine-ridge"></div>';
      html +=   '<div class="spine-ridge"></div>';
      html +=   '<div class="spine-ridge"></div>';
      html +=   '<span class="spine-label">' + volLabel + '</span>';
      html += '</div>';
      html += '<div class="book-body">';
      html += '<div class="book-cover" style="background-image:url(' + coverSrc + ')">';
      html +=   '<div class="cover-sheen"></div>';
      html += '</div>';
      html += '<div class="book-pages">';
      for (var p = 0; p < 10; p++) html += '<div class="page-line"></div>';
      html += '</div>';
      html += '</div>';
      html += '<div class="book-shadow"></div>';
      html += '</div>';
      html += '<div class="book-meta">';
      html +=   '<span class="book-meta-title">' + bookTitle + '</span>';
      html +=   '<button class="book-share-btn" type="button"';
      html +=     ' data-kind="travel" data-volume="' + vol + '"';
      html +=     ' data-title="我的人生旅行 · ' + bookTitle + '"';
      html +=     ' data-desc="林樺先生旅行文集——' + bookTitle + '，來自雲箋文舍"';
      html +=     ' data-link="' + origin + '/volume.html?volume=' + vol + '"';
      html +=     ' data-img="' + origin + '/' + coverSrc + '"';
      html +=   '>分享／PDF</button>';
      html += '</div>';
      html += '</div>';
    }

    html += '<div class="book-slot">';
    html += '<div class="book-card v5 reserved-book" data-reserved="true" data-preview-url="yunxin.html">';
    html +=   '<div class="book-spine">';
    html +=     '<div class="spine-ridge"></div>';
    html +=     '<div class="spine-ridge"></div>';
    html +=     '<div class="spine-ridge"></div>';
    html +=     '<span class="spine-label">雲心文集</span>';
    html +=   '</div>';
    html +=   '<div class="book-body">';
    html +=     '<div class="book-cover" style="background-image:url(images/yunxin-cover.jpg)">';
    html +=       '<div class="cover-sheen"></div>';
    html +=       '<div class="book-reserved-badge">新作</div>';
    html +=     '</div>';
    html +=     '<div class="book-pages">';
    for (var q = 0; q < 10; q++) html += '<div class="page-line"></div>';
    html +=     '</div>';
    html +=   '</div>';
    html +=   '<div class="book-shadow"></div>';
    html += '</div>';
    html += '<div class="book-meta">';
    html +=   '<span class="book-meta-title">雲心文集</span>';
    html +=   '<button class="book-share-btn" type="button"';
    html +=     ' data-kind="yunxin"';
    html +=     ' data-title="雲心文集"';
    html +=     ' data-desc="《雲心文集》——林樺，詩．詞．散文．雜記，來自雲箋文舍"';
    html +=     ' data-link="' + origin + '/yunxin.html"';
    html +=     ' data-img="' + origin + '/images/yunxin-cover.jpg"';
    html +=   '>分享／PDF</button>';
    html += '</div>';
    html += '</div>';

    container.innerHTML = html;

    var cards = container.querySelectorAll('.book-card');
    for (var j = 0; j < cards.length; j++) {
      (function(card) {
        card.addEventListener('click', function() {
          if (this.getAttribute('data-reserved') === 'true') {
            var previewUrl = this.getAttribute('data-preview-url');
            if (previewUrl) window.location.href = previewUrl;
            return;
          }
          var volume = this.getAttribute('data-volume');
          sessionStorage.setItem('volume', volume);
          window.location.href = 'volume.html?volume=' + volume;
        });
      })(cards[j]);
    }

    var shareBtns = container.querySelectorAll('.book-share-btn');
    for (var s = 0; s < shareBtns.length; s++) {
      shareBtns[s].addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var btn = e.currentTarget;
        openBookShare({
          kind: btn.getAttribute('data-kind'),
          volume: btn.getAttribute('data-volume'),
          title: (btn.getAttribute('data-title') || '雲箋文舍') + ' — 雲箋文舍',
          desc: btn.getAttribute('data-desc') || '',
          link: btn.getAttribute('data-link') || (origin + '/shelf.html'),
          imgUrl: btn.getAttribute('data-img') || (origin + '/og-image.png')
        });
      });
    }
  }

  function bindShareOverlay() {
    var shareFriendBtn = document.getElementById('share-friend-btn');
    var shareTimelineBtn = document.getElementById('share-timeline-btn');
    var shareCopyBtn = document.getElementById('share-copy-btn');
    var sharePdfBtn = document.getElementById('share-pdf-btn');

    if (shareFriendBtn) {
      shareFriendBtn.addEventListener('click', function() {
        doShare({ method: 'sendAppMessage', desc: true });
      });
    }
    if (shareTimelineBtn) {
      shareTimelineBtn.addEventListener('click', function() {
        doShare({ method: 'shareTimeline', desc: false });
      });
    }
    if (shareCopyBtn) {
      shareCopyBtn.addEventListener('click', function() {
        var d = window.__wxShareData || {};
        copyShareLink(d.link || '');
      });
    }
    if (sharePdfBtn) {
      sharePdfBtn.addEventListener('click', function() {
        exportCurrentBookPdf();
      });
    }
    if (shareCloseBtn) {
      shareCloseBtn.addEventListener('click', closeShare);
    }
    if (shareOverlay) {
      shareOverlay.addEventListener('click', function(e) {
        if (e.target === shareOverlay) closeShare();
      });
    }
  }

  bindShareOverlay();
  loadData();
})();

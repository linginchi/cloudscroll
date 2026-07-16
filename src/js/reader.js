// src/js/reader.js
// Continuous scroll reading mode
(function() {
  'use strict';

  var scrollEl = document.getElementById('reader-scroll');
  var innerEl = document.getElementById('reader-inner');
  var articleTitle = document.getElementById('article-title');
  var langToggle = document.getElementById('lang-toggle');
  var langOptions = langToggle ? langToggle.querySelectorAll('.lang-option') : null;
  var pageNumEl = document.getElementById('page-num');
  var progressBar = document.getElementById('progress-bar');
  var likeBtn = document.getElementById('like-btn');
  var likeIcon = document.getElementById('like-icon');
  var likeCountEl = document.getElementById('like-count');
  var viewsEl = document.getElementById('stat-views');
  var shareBtn = document.getElementById('share-btn');
  var shareOverlay = document.getElementById('share-overlay');
  var shareCloseBtn = document.getElementById('share-close-btn');
  var backBtn = document.getElementById('back-btn');

  if (!scrollEl || !innerEl) return;

  var currentLang = 'zh';
  var masterData = null;
  var articleData = null;
  var articleBlocks = null;
  var articleBlocksEn = null;
  var articleIndex = -1;
  var liked = false;

  function loadMasterData(callback) {
    var xhr = new XMLHttpRequest();
    xhr.timeout = 8000;
    xhr.open('GET', 'book/data.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { masterData = JSON.parse(xhr.responseText); callback(null); }
        catch(e) { callback(e); }
      } else { callback(new Error('Failed')); }
    };
    xhr.onerror = function() { callback(new Error('Network error')); };
    xhr.ontimeout = function() { callback(new Error('Timeout')); };
    xhr.send();
  }

  function loadArticleBlocks(articleId, lang, callback) {
    var suffix = lang === 'en' ? 'en-' : '';
    var xhr = new XMLHttpRequest();
    xhr.timeout = 8000;
    xhr.open('GET', 'book/' + suffix + articleId + '.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { var data = JSON.parse(xhr.responseText); callback(null, data.blocks || []); }
        catch(e) { callback(e); }
      } else if (lang === 'en') { callback(null, null); }
      else { callback(new Error('Failed')); }
    };
    xhr.onerror = function() { callback(new Error('Network error')); };
    xhr.ontimeout = function() { callback(new Error('Timeout')); };
    xhr.send();
  }

  function getArticleSummary(articleId) {
    if (!masterData) return null;
    for (var i = 0; i < masterData.articles.length; i++) {
      if (masterData.articles[i].id === articleId) {
        articleIndex = i;
        return masterData.articles[i];
      }
    }
    return null;
  }

  function getArticleVolume(articleId) {
    if (!masterData || !masterData.chapters) return 1;
    for (var c = 0; c < masterData.chapters.length; c++) {
      var arts = masterData.chapters[c].articles || [];
      for (var a = 0; a < arts.length; a++) {
        if (arts[a].id === articleId) return c + 1;
      }
    }
    return 1;
  }

  function render() {
    var blocks = currentLang === 'en' && articleBlocksEn ? articleBlocksEn : articleBlocks;
    if (!blocks) blocks = articleBlocks;

    var html = '';

    // Chapter cover
    var zh = articleData.zh || '';
    var en = articleData.en || '';
    var enTitle = articleData.en || '';
    var subtitle = currentLang === 'en' ? (articleData.en_subtitle || '') : (articleData.subtitle || '');
    var authorLine = currentLang === 'en' ? 'Lin Hua' : '林 樺';
    var num = '';
    if (articleData.id !== '00-preface' && articleIndex >= 2) {
      num = currentLang === 'en' ? 'Essay ' + (articleIndex - 2) : '第 ' + (articleIndex - 2) + ' 篇';
    }

    html += '<div class="chapter-cover' + (currentLang === 'en' ? ' chapter-cover-en-mode' : '') + '">' +
      (num ? '<div class="chapter-cover-num">' + num + '</div>' : '') +
      '<div class="chapter-cover-zh">' + esc(currentLang === 'en' ? enTitle : zh) + '</div>' +
      (en && currentLang === 'zh' ? '<div class="chapter-cover-en">' + esc(en) + '</div>' : '') +
      '<div class="chapter-cover-line"></div>' +
      (subtitle ? '<p class="chapter-cover-sub">' + esc(subtitle) + '</p>' : '') +
      '<div class="chapter-cover-author">' + authorLine + '</div>' +
      '</div>';

    // 《屢次京城勝跡記》：標題後插入「今日北京」動畫
    if (articleData.id === 'v2-01') {
      html += '<div class="article-feature-media">' +
        '<div class="article-feature-video-wrap">' +
          '<video class="article-feature-video" src="images/beijing-anim.mp4" autoplay muted loop playsinline webkit-playsinline preload="metadata"></video>' +
        '</div>' +
        '<p class="article-feature-title">今日北京</p>' +
        '<p class="article-feature-date">2026年7月7日</p>' +
        '</div>';
    }

    // Body
    html += '<div class="book-content">';
    for (var i = 0; i < blocks.length; i++) {
      var block = blocks[i];
      if (block.type === 'text') {
        var text = block.content;
        var cls = /^【.*】/.test(text.trim()) ? ' class="section-title"' : '';
        html += '<p' + cls + '>' + esc(text) + '</p>';
      } else if (block.type === 'image') {
        html += '<div class="book-image-wrapper"><img src="book/' + block.src + '" alt="" loading="lazy" draggable="false"></div>';
      }
    }
    html += '</div>';
    html += '<div class="chapter-end">— ◆ —</div>';

    innerEl.innerHTML = html;

    // 確保插入的視頻開始播放
    var featureVideos = innerEl.querySelectorAll('.article-feature-video');
    for (var vi = 0; vi < featureVideos.length; vi++) {
      var fv = featureVideos[vi];
      var playPromise = fv.play();
      if (playPromise && typeof playPromise.catch === 'function') {
        playPromise.catch(function () {});
      }
    }

    scrollEl.scrollTop = 0;
    updateProgress();
  }

  function updateProgress() {
    var pct = 0;
    if (scrollEl.scrollHeight > scrollEl.clientHeight) {
      pct = Math.round((scrollEl.scrollTop / (scrollEl.scrollHeight - scrollEl.clientHeight)) * 100);
    }
    if (progressBar) progressBar.style.width = pct + '%';
    if (pageNumEl) pageNumEl.textContent = pct + '%';
  }

  scrollEl.addEventListener('scroll', updateProgress, { passive: true });

  function init() {
    try {
      var stored = sessionStorage.getItem('currentArticle');
      if (stored) articleData = JSON.parse(stored);
    } catch(e) {}

    if (!articleData || !articleData.id) {
      var params = new URLSearchParams(window.location.search);
      var idFromUrl = params.get('id');
      if (idFromUrl) articleData = { id: idFromUrl, zh: '文章', en: 'Article' };
      else articleData = { id: '00-preface', zh: '自序', en: 'Preface' };
    }

    if (articleTitle) articleTitle.textContent = articleData.zh;
    innerEl.innerHTML = '<div class="loading-state">載入中…</div>';

    // 加載文章內容（不依賴 data.json，獨立執行）
    loadArticleBlocks(articleData.id, 'zh', function(err2, blocks) {
      if (err2 || !blocks || blocks.length === 0) {
        innerEl.innerHTML = '<div class="loading-state" style="color:#999">無法載入文章內容</div>';
        return;
      }
      articleBlocks = blocks;

      // 並行加載英文翻譯（可選）
      loadArticleBlocks(articleData.id, 'en', function(err3, enBlocks) {
        articleBlocksEn = enBlocks;
      });

      render();
    });

    // 同時加載 data.json（用來補全資訊、側欄、回目錄路徑）
    loadMasterData(function(err) {
      if (!err && masterData) {
        var fullInfo = getArticleSummary(articleData.id);
        if (fullInfo) {
          articleData = fullInfo;
          if (articleTitle) articleTitle.textContent = articleData.zh;
        }
        var vol = getArticleVolume(articleData.id);
        var backLink = document.getElementById('reader-back');
        if (backLink) backLink.href = 'volume.html?volume=' + vol + '&scrollToToc=1';
        var tocLink = document.getElementById('reader-toc-link');
        if (tocLink) tocLink.href = 'volume.html?volume=' + vol + '&scrollToToc=1';
        renderDesktopSidebar();
        // 重新配置微信分享（此時 articleData 已有完整標題）
        setupWechatShare();
      }
    });

    if (backBtn) {
      backBtn.addEventListener('click', function() {
        var vol = getArticleVolume(articleData.id);
        window.location.href = 'volume.html?volume=' + vol + '&scrollToToc=1';
      });
    }

    function isWeChat() {
      return /MicroMessenger/i.test(navigator.userAgent);
    }

    function isMobile() {
      return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    }

    function showShareToast(msg) {
      var old = document.getElementById('reader-share-toast');
      if (old) old.remove();
      var el = document.createElement('div');
      el.id = 'reader-share-toast';
      el.className = 'reader-share-toast';
      el.textContent = msg;
      document.body.appendChild(el);
      setTimeout(function() { el.classList.add('show'); }, 10);
      setTimeout(function() {
        el.classList.remove('show');
        setTimeout(function() { if (el.parentNode) el.parentNode.removeChild(el); }, 250);
      }, 2400);
    }

    function updateShareDialogForEnv() {
      var tip = document.getElementById('share-wx-tip');
      var friendBtn = document.getElementById('share-friend-btn');
      var timelineBtn = document.getElementById('share-timeline-btn');
      var copyBtn = document.getElementById('share-copy-btn');
      if (!tip) return;

      if (isWeChat()) {
        tip.style.display = 'block';
        tip.textContent = '微信中請點擊右上角「…」，選擇分享給朋友或朋友圈';
        if (friendBtn) friendBtn.style.display = 'none';
        if (timelineBtn) timelineBtn.style.display = 'none';
        if (copyBtn) copyBtn.style.display = '';
        return;
      }

      // 桌面 Chrome / Edge：無法一鍵分享到微信，只保留「複製連結」並說明清楚
      if (!isMobile()) {
        tip.style.display = 'block';
        tip.textContent = '電腦瀏覽器無法一鍵分享到微信。請先點「複製連結」，再到微信（或其他應用）貼上發送。';
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

    if (shareBtn && shareOverlay) {
      shareBtn.addEventListener('click', function() {
        var shareUrl = window.location.origin + '/reader.html';
        if (articleData && articleData.id) shareUrl += '?id=' + encodeURIComponent(articleData.id);
        var shareTitle = articleData ? (articleData.zh || '文章') : '雲箋文舍';
        var shareDesc = '林樺先生旅行散文：《' + shareTitle + '》——來自雲箋文舍';
        var shareImg = window.location.origin + '/og-image.png';

        window.__wxShareData = {
          title: shareTitle + ' — 雲箋文舍',
          desc: shareDesc,
          link: shareUrl,
          imgUrl: shareImg
        };

        updateShareDialogForEnv();
        shareOverlay.classList.add('show');
      });
    }

    function doShare(options) {
      var d = window.__wxShareData || {};
      // 安全備援：如果 __wxShareData 未設定或過期，用 articleData 重建
      if (!d.title || !d.link) {
        var fallbackUrl = window.location.origin + '/reader.html';
        if (articleData && articleData.id) fallbackUrl += '?id=' + encodeURIComponent(articleData.id);
        var fallbackTitle = articleData ? (articleData.zh || '文章') : '雲箋文舍';
        d = {
          title: fallbackTitle + ' — 雲箋文舍',
          desc: '林樺先生旅行散文：《' + fallbackTitle + '》——來自雲箋文舍',
          link: fallbackUrl,
          imgUrl: window.location.origin + '/og-image.png'
        };
        window.__wxShareData = d;
      }
      // 1) WeixinJSBridge (WeChat webview / PWA opened from WeChat)
      if (typeof WeixinJSBridge !== 'undefined') {
        WeixinJSBridge.invoke(options.method, {
          title: d.title || '',
          desc: options.desc ? (d.desc || '') : '',
          link: d.link || '',
          img_url: d.imgUrl || '',
        }, function() {
          shareOverlay.classList.remove('show');
        });
        return;
      }
      // 2) 手機系統分享
      var canNativeShare = typeof navigator.share === 'function' && isMobile();
      if (canNativeShare) {
        navigator.share({
          title: d.title || '',
          text: d.desc || '',
          url: d.link || '',
        }).then(function() {
          shareOverlay.classList.remove('show');
        }).catch(function(err) {
          if (err && err.name === 'AbortError') {
            shareOverlay.classList.remove('show');
            return;
          }
          copyShareLink(d.link || '');
        });
        return;
      }
      // 3) 桌面端：複製連結並提示
      copyShareLink(d.link || '');
    }

    function copyShareLink(link) {
      var finished = false;
      function done() {
        if (finished) return;
        finished = true;
        shareOverlay.classList.remove('show');
        showShareToast('連結已複製。請打開微信，貼上發送給朋友或發到朋友圈');
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

    var shareFriendBtn = document.getElementById('share-friend-btn');
    var shareTimelineBtn = document.getElementById('share-timeline-btn');
    var shareCopyBtn = document.getElementById('share-copy-btn');

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

    if (shareCloseBtn) shareCloseBtn.addEventListener('click', function() { shareOverlay.classList.remove('show'); });
    if (shareOverlay) shareOverlay.addEventListener('click', function(e) { if (e.target === shareOverlay) shareOverlay.classList.remove('show'); });
    if (likeBtn) likeBtn.addEventListener('click', toggleLike);

    // 微信原生分享預配置 — 頁面加載時就設定好，
    // 用戶點微信右上角「...」選單也能一鍵分享
    setupWechatShare();
  }

  if (langToggle && langOptions) {
    langOptions.forEach(function(opt) {
      opt.addEventListener('click', function() {
        var lang = this.getAttribute('data-lang');
        if (lang === currentLang) return;
        currentLang = lang;
        langOptions.forEach(function(o) { o.classList.remove('active'); });
        this.classList.add('active');
        if (articleTitle) articleTitle.textContent = lang === 'zh' ? articleData.zh : (articleData.en || articleData.zh);
        var backLink = document.getElementById('reader-back');
        if (backLink) backLink.textContent = lang === 'zh' ? '← 目錄' : '← Contents';
        var tocLink = document.getElementById('reader-toc-link');
        if (tocLink) tocLink.textContent = lang === 'zh' ? '目錄' : 'Contents';

        if (lang === 'en') {
          if (articleBlocksEn) { render(); }
          else {
            loadArticleBlocks(articleData.id, 'en', function(err, enBlocks) {
              if (enBlocks) { articleBlocksEn = enBlocks; render(); }
              else {
                var ex = document.getElementById('en-pending-notice');
                if (!ex) {
                  var n = document.createElement('div'); n.id = 'en-pending-notice';
                  n.textContent = 'English translation in progress — displaying Chinese original';
                  var tb = document.querySelector('.reader-topbar');
                  if (tb && tb.parentNode) tb.parentNode.insertBefore(n, tb.nextSibling);
                }
                currentLang = 'zh';
                langOptions.forEach(function(o) { o.classList.remove('active'); });
                var zhOpt = document.querySelector('.lang-option[data-lang="zh"]');
                if (zhOpt) zhOpt.classList.add('active');
              }
            });
          }
        } else {
          var notice = document.getElementById('en-pending-notice');
          if (notice) notice.remove();
          render();
        }
      });
    });
  }

  function renderDesktopSidebar() {
    var sidebar = document.getElementById('desktop-sidebar');
    if (!sidebar || window.innerWidth < 1024) return;
    if (!masterData || !masterData.chapters) return;
    var currentId = articleData.id;
    var html = '<div class="sidebar-header"><div class="sidebar-title">雲箋文舍</div><div class="sidebar-subtitle">Cloudscroll</div></div><div class="sidebar-nav">';
    var chapters = masterData.chapters;
    for (var ci = 0; ci < chapters.length; ci++) {
      var ch = chapters[ci];
      html += '<div class="sidebar-chapter">' + ch.zh + '</div>';
      var arts = ch.articles || [];
      for (var ai = 0; ai < arts.length; ai++) {
        var art = arts[ai];
        var n = ai + 1; var ns = n < 10 ? '0' + n : '' + n;
        var active = art.id === currentId ? ' active' : '';
        html += '<span class="sidebar-article' + active + '" data-id="' + art.id + '" data-title="' + art.zh.replace(/"/g, '&quot;') + '" data-en="' + (art.en || '').replace(/"/g, '&quot;') + '"><span class="sidebar-num">' + ns + '</span>' + art.zh + '</span>';
      }
    }
    html += '</div><a class="sidebar-back" href="shelf.html">← 返回書架</a>';
    sidebar.innerHTML = html;
    var items = sidebar.querySelectorAll('.sidebar-article');
    for (var si = 0; si < items.length; si++) {
      (function(item) {
        item.addEventListener('click', function() {
          var id = this.getAttribute('data-id');
          var zh = this.getAttribute('data-title');
          var en = this.getAttribute('data-en');
          sessionStorage.setItem('currentArticle', JSON.stringify({ id: id, zh: zh, en: en }));
          window.location.reload();
        });
      })(items[si]);
    }
  }

  function getStats() {
    if (!articleData || !articleData.id) return;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/stats?article=' + encodeURIComponent(articleData.id), true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        if (viewsEl) viewsEl.textContent = '閱讀 ' + data.views;
        if (likeCountEl) likeCountEl.textContent = data.likes + ' 讚';
        if (data.liked) { liked = true; if (likeIcon) likeIcon.textContent = '♥'; if (likeBtn) likeBtn.classList.add('liked'); }
      }
    };
    xhr.send();
  }

  function recordView() {
    if (!articleData || !articleData.id) return;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/stats?article=' + encodeURIComponent(articleData.id), true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        if (viewsEl) viewsEl.textContent = '閱讀 ' + data.views;
      }
    };
    xhr.send(JSON.stringify({ action: 'view' }));
  }

  /**
   * 預配置微信原生分享 — 在頁面加載時將分享參數設定到 WeixinJSBridge。
   * 微信內建瀏覽器會自動讀取這些設定，用戶點右上角「...」即可一鍵分享，
   * 包含標題、描述、縮圖和連結 — 就像 App 原生分享一樣。
   */
  function setupWechatShare() {
    if (!/MicroMessenger/i.test(navigator.userAgent)) return;

    var shareUrl = window.location.origin + '/reader.html';
    if (articleData && articleData.id) shareUrl += '?id=' + encodeURIComponent(articleData.id);
    var shareTitle = articleData ? (articleData.zh || '文章') : '雲箋文舍';
    var shareDesc = '林樺先生旅行散文：《' + shareTitle + '》——來自雲箋文舍';
    var shareImg = window.location.origin + '/og-image.png';

    var data = {
      title: shareTitle + ' — 雲箋文舍',
      desc: shareDesc,
      link: shareUrl,
      imgUrl: shareImg,
    };

    // Store for our custom buttons
    window.__wxShareData = data;

    // Pre-configure WeixinJSBridge for native menu sharing
    function onBridgeReady() {
      // 分享給朋友
      WeixinJSBridge.on('menu:share:appmessage', function(argv) {
        WeixinJSBridge.invoke('sendAppMessage', {
          title: data.title,
          desc: data.desc,
          link: data.link,
          img_url: data.imgUrl,
        }, function(res) {});
      });
      // 分享到朋友圈
      WeixinJSBridge.on('menu:share:timeline', function(argv) {
        WeixinJSBridge.invoke('shareTimeline', {
          title: data.title,
          link: data.link,
          img_url: data.imgUrl,
        }, function(res) {});
      });
    }

    if (typeof WeixinJSBridge === 'undefined') {
      document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
    } else {
      onBridgeReady();
    }
  }

  function toggleLike() {
    if (!articleData || !articleData.id) return;
    var action = liked ? 'unlike' : 'like';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/stats?article=' + encodeURIComponent(articleData.id), true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        if (likeCountEl) likeCountEl.textContent = data.likes + ' 讚';
        liked = !liked;
        if (likeIcon) likeIcon.textContent = liked ? '♥' : '♡';
        if (likeBtn) { if (liked) likeBtn.classList.add('liked'); else likeBtn.classList.remove('liked'); }
      }
    };
    xhr.send(JSON.stringify({ action: action }));
  }

  function esc(text) {
    if (!text) return '';
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  init();

  setTimeout(function() { getStats(); recordView(); }, 800);

  window.addEventListener('resize', function() { renderDesktopSidebar(); });

  // Protect images from downloading
  document.addEventListener('contextmenu', function(e) {
    var el = e.target;
    if (el && el.closest && el.closest('.book-image-wrapper')) {
      e.preventDefault();
      return false;
    }
  });
})();

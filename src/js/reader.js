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
    xhr.open('GET', 'book/data.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { masterData = JSON.parse(xhr.responseText); callback(null); }
        catch(e) { callback(e); }
      } else { callback(new Error('Failed')); }
    };
    xhr.onerror = function() { callback(new Error('Network error')); };
    xhr.send();
  }

  function loadArticleBlocks(articleId, lang, callback) {
    var suffix = lang === 'en' ? 'en-' : '';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/' + suffix + articleId + '.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { var data = JSON.parse(xhr.responseText); callback(null, data.blocks || []); }
        catch(e) { callback(e); }
      } else if (lang === 'en') { callback(null, null); }
      else { callback(new Error('Failed')); }
    };
    xhr.onerror = function() { callback(new Error('Network error')); };
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

    // Body
    html += '<div class="book-content">';
    for (var i = 0; i < blocks.length; i++) {
      var block = blocks[i];
      if (block.type === 'text') {
        var text = block.content;
        var cls = /^【.*】/.test(text.trim()) ? ' class="section-title"' : '';
        html += '<p' + cls + '>' + esc(text) + '</p>';
      } else if (block.type === 'image') {
        html += '<div class="book-image-wrapper"><img src="book/' + block.src + '" alt="" loading="lazy"></div>';
      }
    }
    html += '</div>';
    html += '<div class="chapter-end">— ◆ —</div>';

    innerEl.innerHTML = html;
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

    loadMasterData(function(err) {
      if (!err && masterData) {
        var fullInfo = getArticleSummary(articleData.id);
        if (fullInfo) {
          articleData = fullInfo;
          if (articleTitle) articleTitle.textContent = articleData.zh;
        }
        var vol = getArticleVolume(articleData.id);
        var backLink = document.getElementById('reader-back');
        if (backLink) backLink.href = 'volume.html?volume=' + vol;
      }

      loadArticleBlocks(articleData.id, 'zh', function(err2, blocks) {
        if (err2 || !blocks || blocks.length === 0) {
          innerEl.innerHTML = '<div class="loading-state" style="color:#999">無法載入文章內容</div>';
          return;
        }
        articleBlocks = blocks;

        loadArticleBlocks(articleData.id, 'en', function(err3, enBlocks) {
          articleBlocksEn = enBlocks;
        });

        render();
        renderDesktopSidebar();
      });
    });

    if (backBtn) {
      backBtn.addEventListener('click', function() {
        var vol = getArticleVolume(articleData.id);
        window.location.href = 'volume.html?volume=' + vol;
      });
    }

    if (shareBtn && shareOverlay) {
      shareBtn.addEventListener('click', function() {
        var shareUrl = window.location.origin + window.location.pathname;
        if (articleData && articleData.id) shareUrl += '?id=' + encodeURIComponent(articleData.id);
        var linkText = document.getElementById('share-link-text');
        if (linkText) linkText.textContent = shareUrl;
        try {
          var ta = document.createElement('textarea');
          ta.value = shareUrl; ta.style.position = 'fixed'; ta.style.left = '-9999px';
          document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
        } catch(e) {}
        shareOverlay.classList.add('show');
        if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
          setTimeout(function() { window.location.href = 'weixin://'; }, 600);
        }
      });
    }

    if (shareCloseBtn) shareCloseBtn.addEventListener('click', function() { shareOverlay.classList.remove('show'); });
    if (shareOverlay) shareOverlay.addEventListener('click', function(e) { if (e.target === shareOverlay) shareOverlay.classList.remove('show'); });
    if (likeBtn) likeBtn.addEventListener('click', toggleLike);
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
})();

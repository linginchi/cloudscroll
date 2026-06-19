// src/js/reader.js
// 連續滾動閱讀模式 — 從 JSON 載入文章，圖文混排，董橋風格
(function() {
  'use strict';

  // ---- DOM refs ----
  var scrollEl = document.getElementById('reader-scroll');
  var innerEl = document.getElementById('reader-inner');
  var articleTitle = document.getElementById('article-title');
  var langToggle = document.getElementById('lang-toggle');
  var langOptions = langToggle ? langToggle.querySelectorAll('.lang-option') : null;
  var pageNum = document.getElementById('page-num');
  var progressBar = document.getElementById('progress-bar');

  if (!scrollEl || !innerEl) return;

  // ---- State ----
  var currentLang = 'zh';
  var masterData = null;
  var articleData = null;
  var articleBlocks = null;
  var articleBlocksEn = null;
  var totalArticles = 0;
  var articleIndex = -1;

  // ---- 載入 master data ----
  function loadMasterData(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/data.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { masterData = JSON.parse(xhr.responseText); callback(null); }
        catch(e) { callback(e); }
      } else { callback(new Error('Failed to load book/data.json')); }
    };
    xhr.onerror = function() { callback(new Error('Network error')); };
    xhr.send();
  }

  // ---- 載入文章 JSON ----
  function loadArticleBlocks(articleId, lang, callback) {
    var suffix = lang === 'en' ? 'en-' : '';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/' + suffix + articleId + '.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { var data = JSON.parse(xhr.responseText); callback(null, data.blocks || []); }
        catch(e) { callback(e); }
      } else if (lang === 'en') { callback(null, null); }
      else { callback(new Error('Failed to load')); }
    };
    xhr.onerror = function() { callback(new Error('Network error')); };
    xhr.send();
  }

  // ---- 從 master 找文章摘要 ----
  function getArticleSummary(articleId) {
    if (!masterData) return null;
    for (var i = 0; i < masterData.articles.length; i++) {
      if (masterData.articles[i].id === articleId) {
        articleIndex = i;
        totalArticles = masterData.articles.length;
        return masterData.articles[i];
      }
    }
    return null;
  }

  // ---- 初始化 ----
  function init() {
    // Get article info
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
      }

      loadArticleBlocks(articleData.id, 'zh', function(err2, blocks) {
        if (err2 || !blocks || blocks.length === 0) {
          innerEl.innerHTML = '<div class="loading-state" style="color:#999">❌ 無法載入文章內容</div>';
          return;
        }
        articleBlocks = blocks;

        loadArticleBlocks(articleData.id, 'en', function(err3, enBlocks) {
          articleBlocksEn = enBlocks;
        });

        renderAll();
      });
    });
  }

  // ---- 渲染完整文章 ----
  function renderAll() {
    var blocks = currentLang === 'en' && articleBlocksEn ? articleBlocksEn : articleBlocks;
    if (!blocks) blocks = articleBlocks;

    var html = '';

    // 章節扉頁
    html += buildChapterCover();

    // 正文
    html += '<div class="book-content">';

    for (var i = 0; i < blocks.length; i++) {
      var block = blocks[i];

      if (block.type === 'text') {
        var text = block.content;
        var className = '';
        if (/^【.*】/.test(text.trim())) {
          className = 'section-title';
        }
        var pClass = className ? ' class="' + className + '"' : '';
        html += '<p' + pClass + '>' + escapeHtml(text) + '</p>';
      }
      else if (block.type === 'image') {
        html += '<div class="book-image-wrapper">' +
          '<img src="book/' + block.src + '" alt="" loading="lazy">' +
          '</div>';
      }
    }

    html += '</div>'; // book-content

    // 篇尾
    html += '<div class="chapter-end">— ◆ —</div>';

    innerEl.innerHTML = html;

    updateProgress();
  }

  // ---- 章節扉頁 ----
  function buildChapterCover() {
    var zh = articleData.zh || '';
    var en = articleData.en || '';
    var enTitle = articleData.en || '';
    var subtitle = currentLang === 'en' ? (articleData.en_subtitle || '') : (articleData.subtitle || '');
    var authorLine = currentLang === 'en' ? 'Lin Hua' : '林 樺';

    var num = '';
    if (articleData.id === '00-preface') {}
    else if (articleIndex >= 2) {
      num = currentLang === 'en' ? 'Essay ' + (articleIndex - 2) : '第 ' + (articleIndex - 2) + ' 篇';
    }

    return '<div class="chapter-cover' + (currentLang === 'en' ? ' chapter-cover-en-mode' : '') + '">' +
      (num ? '<div class="chapter-cover-num">' + num + '</div>' : '') +
      '<div class="chapter-cover-zh">' + escapeHtml(currentLang === 'en' ? enTitle : zh) + '</div>' +
      (en && currentLang === 'zh' ? '<div class="chapter-cover-en">' + escapeHtml(en) + '</div>' : '') +
      '<div class="chapter-cover-line"></div>' +
      (subtitle ? '<p class="chapter-cover-sub">' + escapeHtml(subtitle) + '</p>' : '') +
      '<div class="chapter-cover-author">' + authorLine + '</div>' +
      '</div>';
  }

  // ---- 進度 ----
  function updateProgress() {
    // Use scroll position to calculate progress
    function onScroll() {
      var scrollTop = scrollEl.scrollTop;
      var scrollHeight = scrollEl.scrollHeight - scrollEl.clientHeight;
      var pct = scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;
      progressBar.style.width = pct + '%';
      pageNum.textContent = pct + '%';
    }

    scrollEl.removeEventListener('scroll', onScroll);
    scrollEl.addEventListener('scroll', onScroll, { passive: true });
    // Initial update
    setTimeout(onScroll, 100);
  }

  // ---- 語言切換 ----
  if (langToggle && langOptions) {
    langOptions.forEach(function(opt) {
      opt.addEventListener('click', function() {
        var lang = this.getAttribute('data-lang');
        if (lang === currentLang) return;
        currentLang = lang;
        langOptions.forEach(function(o) { o.classList.remove('active'); });
        this.classList.add('active');

        // 頂欄雙語
        if (articleTitle) {
          articleTitle.textContent = lang === 'zh' ? articleData.zh : (articleData.en || articleData.zh);
        }
        var backLink = document.getElementById('reader-back');
        if (backLink) {
          backLink.textContent = lang === 'zh' ? '← 目錄' : '← Contents';
        }

        var bookNameEl = document.querySelector('.reader-meta .book-name');
        if (bookNameEl) {
          bookNameEl.textContent = lang === 'zh' ? '雲箋文舍' : 'Cloudscroll';
        }

        if (lang === 'en') {
          if (articleBlocksEn) {
            scrollEl.scrollTop = 0;
            renderAll();
          } else {
            loadArticleBlocks(articleData.id, 'en', function(err, enBlocks) {
              if (enBlocks) {
                articleBlocksEn = enBlocks;
                scrollEl.scrollTop = 0;
                renderAll();
              } else {
                langOptions.forEach(function(o) { o.classList.remove('active'); });
                document.querySelector('.lang-option[data-lang="zh"]').classList.add('active');
                currentLang = 'zh';
                alert('英文版翻譯尚未完成，將繼續顯示中文。');
              }
            });
          }
        } else {
          scrollEl.scrollTop = 0;
          renderAll();
        }
      });
    });
  }

  // ---- Helpers ----
  function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // ---- Start ----
  init();

})();

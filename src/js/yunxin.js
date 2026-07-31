// src/js/yunxin.js — 《雲心文集》自序 / 文章閱讀
(function () {
  'use strict';

  var path = (window.location.pathname || '').toLowerCase();
  var isPrefacePage = path.indexOf('yunxin-preface') !== -1;
  var params = new URLSearchParams(window.location.search);
  var articleKey = isPrefacePage ? '00-preface' : (params.get('id') || '');
  var ARTICLE_ID = 'yunxin-' + (articleKey || 'unknown');
  var ARTICLE_TITLE = '雲心文集';
  var ARTICLE_HREF = isPrefacePage
    ? (window.location.origin + '/yunxin-preface.html')
    : (window.location.origin + '/yunxin-article.html?id=' + encodeURIComponent(articleKey));

  var likeBtn = document.getElementById('like-btn');
  var likeIcon = document.getElementById('like-icon');
  var likeCountEl = document.getElementById('like-count');
  var viewsEl = document.getElementById('stat-views');
  var shareBtn = document.getElementById('share-btn');
  var shareOverlay = document.getElementById('share-overlay');
  var shareCloseBtn = document.getElementById('share-close-btn');
  var backBtn = document.getElementById('back-btn');
  var liked = false;
  var likeBusy = false;
  var likeStorageKey = 'cs:liked:' + ARTICLE_ID;
  var likeCount = 0;
  var masterData = null;
  var langToggle = document.getElementById('yunxin-lang-toggle');
  var langButtons = langToggle ? langToggle.querySelectorAll('[data-lang]') : [];
  var storedLang = localStorage.getItem('cs:yunxin-lang') || '';
  var currentLang = params.get('lang') === 'en' || storedLang === 'en' ? 'en' : 'zh';
  var currentArticle = null;
  var currentArticleIndex = -1;
  var currentArticles = [];

  function bodyEl() {
    return document.getElementById('yunxin-article-body') ||
      document.getElementById('yunxin-preface-body');
  }

  function signEl() {
    return document.getElementById('yunxin-article-sign') ||
      document.getElementById('yunxin-preface-sign');
  }

  function titleEl() {
    return document.getElementById('yunxin-article-title');
  }

  function syncLangButtons() {
    for (var i = 0; i < langButtons.length; i++) {
      var lang = langButtons[i].getAttribute('data-lang');
      langButtons[i].classList.toggle('active', lang === currentLang);
    }
    document.documentElement.lang = currentLang === 'en' ? 'en' : 'zh-Hant';
  }

  function langHref(href) {
    if (currentLang !== 'en') return href;
    return href.indexOf('?') >= 0 ? href + '&lang=en' : href + '?lang=en';
  }

  function uiLabel(zh, en) {
    return currentLang === 'en' ? en : zh;
  }

  function isGenreLabel(text) {
    var t = String(text || '').trim().replace(/[˙•·・]/g, '');
    return /^(七\s*律|七\s*絕|七絕|清平樂|采桑子|浣溪沙|滿庭芳|詩一首|詩二首)(\s|$)/.test(t) ||
      t === '七律' || t === '七絕' || t === '清平樂' || t === '采桑子' ||
      t === '浣溪沙' || t === '滿庭芳' || t === '詩一首' || t === '詩二首';
  }

  function normalizeTitleKey(s) {
    return String(s || '')
      .replace(/[《》\s˙•·・]/g, '')
      .replace(/^七[律絕]/, '')
      .replace(/^(清平樂|采桑子|浣溪沙|滿庭芳)/, '');
  }

  function isPoemTitleLine(text, title) {
    var t = String(text || '').trim();
    if (!t || t.length > 24) return false;
    if (isGenreLabel(t)) return false;
    var key = normalizeTitleKey(t);
    var titleKey = normalizeTitleKey(title);
    if (!key || !titleKey) return false;
    return key === titleKey || titleKey.indexOf(key) === 0 || key.indexOf(titleKey) === 0;
  }

  function isEndAnnotation(text) {
    return /^[註注]\s*[：:]/.test(String(text || '').trim());
  }

  function findPoemStartIndex(paras, title) {
    var i;
    for (i = 0; i < paras.length; i++) {
      if (isGenreLabel(paras[i])) return i;
    }
    for (i = 0; i < paras.length; i++) {
      if (isPoemTitleLine(paras[i], title)) return i;
    }
    return 0;
  }

  function mergeNoteParagraphs(notes) {
    if (!notes.length) return [];
    var merged = [notes[0]];
    for (var i = 1; i < notes.length; i++) {
      var prev = merged[merged.length - 1];
      var cur = String(notes[i] || '').trim();
      if (!cur) continue;
      var prevTrim = prev.trim();
      // 短行（如小題）单独成段；Word 换行拆段才并回
      if (prevTrim.length <= 12 || /[。！？：；.!?:」』]$/.test(prevTrim)) {
        merged.push(cur);
      } else {
        merged[merged.length - 1] = prevTrim + cur;
      }
    }
    return merged;
  }

  function isLeadLine(text) {
    var t = String(text || '').trim();
    if (!t) return false;
    if (t.length <= 28) return true;
    if (/[；;]$/.test(t) && t.length <= 40) return true;
    return false;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderParagraphs(paras, title, opts) {
    paras = paras || [];
    opts = opts || {};
    var html = '';
    // 僅詩／詞做「注釋 vs 正文」切分；自序與散文整篇按正文渲染
    var skipNotes = isPrefacePage || opts.section === 'prose' || opts.section === 'preface' || opts.section === 'notes';
    var poemStart = skipNotes ? 0 : findPoemStartIndex(paras, title || ARTICLE_TITLE);
    var noteParas = poemStart > 0 ? mergeNoteParagraphs(paras.slice(0, poemStart)) : [];
    var bodyParas = poemStart > 0 ? paras.slice(poemStart) : paras;

    if (noteParas.length) {
      html += '<div class="yunxin-note-block">';
      for (var n = 0; n < noteParas.length; n++) {
        html += '<p class="is-note">' + escapeHtml(noteParas[n]) + '</p>';
      }
      html += '</div>';
    }

    for (var i = 0; i < bodyParas.length; i++) {
      var text = bodyParas[i];
      if (isEndAnnotation(text)) {
        html += '<p class="is-note is-note-end">' + escapeHtml(text) + '</p>';
        continue;
      }
      var cls = isLeadLine(text) ? ' class="is-lead"' : '';
      html += '<p' + cls + '>' + escapeHtml(text) + '</p>';
    }
    return html;
  }

  function articleHref(item) {
    if (!item) return 'yunxin-toc.html';
    if (item.id === '00-preface') return 'yunxin-preface.html';
    return 'yunxin-article.html?id=' + encodeURIComponent(item.id);
  }

  function setupPager(articles, index) {
    var prevBtn = document.getElementById('yunxin-prev');
    var nextBtn = document.getElementById('yunxin-next');
    var label = document.getElementById('yunxin-pager-label');
    if (!prevBtn && !nextBtn) return;

    var prev = index > 0 ? articles[index - 1] : null;
    var next = index < articles.length - 1 ? articles[index + 1] : null;

    if (prevBtn) {
      if (prev) {
        prevBtn.href = langHref(articleHref(prev));
        prevBtn.classList.remove('is-disabled');
        prevBtn.textContent = uiLabel('← 上一篇', '← Previous');
      } else if (isPrefacePage) {
        // 自序上一頁仍是扉頁（HTML 已寫好）
        prevBtn.href = langHref('yunxin-flyleaf.html');
        prevBtn.textContent = uiLabel('← 上一頁', '← Previous');
      } else {
        prevBtn.href = langHref('yunxin-toc.html');
        prevBtn.textContent = uiLabel('← 目錄', '← Contents');
      }
    }

    if (nextBtn) {
      if (next) {
        nextBtn.href = langHref(articleHref(next));
        nextBtn.classList.remove('is-disabled');
        nextBtn.textContent = uiLabel('下一篇 →', 'Next →');
      } else if (isPrefacePage) {
        // 自序下一頁仍是目錄（HTML 已寫好）
        nextBtn.href = langHref('yunxin-toc.html');
        nextBtn.textContent = uiLabel('下一頁 →', 'Next →');
      } else {
        nextBtn.href = langHref('yunxin-toc.html');
        nextBtn.textContent = uiLabel('回目錄 →', 'Contents →');
      }
    }

    if (label) {
      var cur = articles[index];
      if (cur && cur.section === 'preface') label.textContent = currentLang === 'en' ? 'Preface' : '自序';
      else if (cur) label.textContent = (cur.num || '') + '';
      else label.textContent = currentLang === 'en' ? 'Article' : '文章';
    }
  }

  var ARTICLE_HEROES = {
    '24-weihui': {
      src: 'images/yunxin-weihui-bigan.jpg',
      alt: '比干聖像'
    },
    '30-guishan': {
      src: 'images/yunxin-guishan-autumn.jpg?v=20260714c',
      alt: '飽覽天下桂山秋'
    }
  };

  // 標題下方嵌入媒體（影片／圖）
  var ARTICLE_EMBEDS = {
    '37-xiyang-huanghun': [{
      type: 'video',
      src: 'images/yunxin-xiyang-wuxianhao-wm.mp4?v=20260719c',
      title: '夕陽無限好',
      position: 'after-title'
    }],
    '10-jiangshan': [{
      type: 'video',
      src: 'images/yunxin-guilin-landscape-wm.mp4?v=20260719d',
      title: '桂林山水',
      position: 'after-body'
    }],
    '39-rensheng-ganwu': [{
      type: 'image',
      src: 'images/yunxin-ganwu-rensheng.jpg?v=20260719e',
      title: '感悟人生',
      position: 'after-body'
    }],
    '06-pengcheng': [{
      type: 'video',
      src: 'images/yunxin-yun-feinia-wm.mp4?v=20260719f',
      title: '雲和飛鳥',
      position: 'after-title'
    }],
    '08-cishan': [
      {
        type: 'image',
        src: 'images/yunxin-cishan-1.jpg?v=20260719h',
        title: '慈山寺1',
        position: 'after-title',
        scale: 0.5
      },
      {
        type: 'image',
        src: 'images/yunxin-cishan-2.jpg?v=20260719h',
        title: '慈山寺2',
        position: 'after-body',
        scale: 0.5
      },
      {
        type: 'image',
        src: 'images/yunxin-cishan-3.jpg?v=20260719h',
        title: '慈山寺3',
        position: 'after-body',
        scale: 0.5
      },
      {
        type: 'image',
        src: 'images/yunxin-cishan-4.jpg?v=20260719h',
        title: '慈山寺4',
        position: 'after-body',
        scale: 0.5
      }
    ],
    '28-gezhou': [{
      type: 'video',
      src: 'images/yunxin-gezhou-linchangqing-wm.mp4?v=20260719j',
      title: '葛州村',
      position: 'after-title'
    }],
    '02-mao-statue': [{
      type: 'image',
      src: 'images/yunxin-mao-statue-wm.jpg?v=20260719m',
      title: '毛澤東銅像',
      position: 'after-title'
    }],
    '09-guilin-landscape': [{
      type: 'video',
      src: 'images/yunxin-guilin-jiatianxia-wm.mp4?v=20260720a',
      title: '桂林山水甲天下',
      position: 'after-title'
    }]
  };

  function appendMediaItem(wrap, meta) {
    if (!meta || (meta.type !== 'video' && meta.type !== 'image')) return false;
    var half = meta.scale === 0.5;
    if (meta.type === 'video') {
      var video = document.createElement('video');
      video.className = 'yunxin-article-embed-video' + (half ? ' is-half' : '');
      video.src = meta.src;
      video.controls = true;
      video.playsInline = true;
      video.setAttribute('playsinline', '');
      video.setAttribute('webkit-playsinline', '');
      video.preload = 'metadata';
      if (meta.title) video.setAttribute('aria-label', meta.title);
      wrap.appendChild(video);
      return true;
    }
    var img = document.createElement('img');
    img.className = 'yunxin-article-embed-img' + (half ? ' is-half' : '');
    img.src = meta.src;
    img.alt = meta.title || '';
    img.loading = 'lazy';
    wrap.appendChild(img);
    return true;
  }

  function fillMediaEmbed(wrap, items) {
    wrap.innerHTML = '';
    if (!items || !items.length) {
      wrap.hidden = true;
      return;
    }
    var added = 0;
    for (var i = 0; i < items.length; i++) {
      if (appendMediaItem(wrap, items[i])) added++;
    }
    wrap.hidden = added === 0;
  }

  function applyArticleEmbed(data) {
    var afterTitle = document.getElementById('yunxin-article-embed');
    var afterBody = document.getElementById('yunxin-article-embed-after');
    var list = ARTICLE_EMBEDS[data.id] || [];
    if (list && !Array.isArray(list)) list = [list];

    var titleItems = [];
    var bodyItems = [];
    for (var i = 0; i < list.length; i++) {
      var item = list[i];
      var pos = item.position || 'after-title';
      if (pos === 'after-body') bodyItems.push(item);
      else titleItems.push(item);
    }

    if (afterTitle) fillMediaEmbed(afterTitle, titleItems);
    if (afterBody) fillMediaEmbed(afterBody, bodyItems);
  }

  function applyArticleMeta(data) {
    ARTICLE_TITLE = data.title || data.en || data.zh || '雲心文集';
    document.title = ARTICLE_TITLE + ' — ' + (currentLang === 'en' ? 'Cloudscroll' : '雲箋文舍');

    var topTitle = document.getElementById('reader-title');
    if (topTitle) topTitle.textContent = ARTICLE_TITLE;

    var h1 = titleEl();
    if (h1) h1.textContent = ARTICLE_TITLE;

    var authorBlock = document.getElementById('yunxin-author-block');
    if (authorBlock) {
      authorBlock.style.display = (data.id === '00-preface') ? '' : 'none';
    }

    var hero = document.getElementById('yunxin-article-hero');
    var heroImg = document.getElementById('yunxin-article-hero-img');
    var heroMeta = ARTICLE_HEROES[data.id];
    if (hero && heroImg) {
      if (heroMeta) {
        heroImg.src = heroMeta.src;
        heroImg.alt = heroMeta.alt || ARTICLE_TITLE;
        hero.hidden = false;
      } else {
        hero.hidden = true;
        heroImg.removeAttribute('src');
        heroImg.alt = '';
      }
    }

    applyArticleEmbed(data);

    var ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) ogTitle.setAttribute('content', ARTICLE_TITLE + ' — 雲箋文舍');
  }

  function loadArticleJson(id, lang, callback) {
    var xhr = new XMLHttpRequest();
    var prefix = lang === 'en' ? 'yunxin/en-' : 'yunxin/';
    xhr.open('GET', prefix + encodeURIComponent(id) + '.json', true);
    xhr.onload = function () {
      if (xhr.status !== 200) {
        callback(new Error('load failed'));
        return;
      }
      try {
        callback(null, JSON.parse(xhr.responseText));
      } catch (e) {
        callback(e);
      }
    };
    xhr.onerror = function () { callback(new Error('network')); };
    xhr.send();
  }

  function renderArticle(article) {
    var body = bodyEl();
    if (!body || !article) return;
    currentArticle = article;
    syncLangButtons();
    updateStaticLabels();
    applyArticleMeta(article);
    body.innerHTML = renderParagraphs(
      article.paragraphs || [],
      article.title || article.en || article.zh || ARTICLE_TITLE,
      { section: article.section || '' }
    );
    var sign = signEl();
    if (sign) {
      var author = currentLang === 'en' ? (article.author_en || 'Lin Hua') : article.author;
      if (author) {
        sign.style.display = '';
        sign.textContent = author;
      } else {
        sign.style.display = 'none';
      }
    }
    if (currentArticles.length && currentArticleIndex >= 0) setupPager(currentArticles, currentArticleIndex);
    window.__wxShareData = buildShareData();
    setupWechatShare();
  }

  function updateStaticLabels() {
    var readerBack = document.querySelector('.reader-back');
    if (readerBack) {
      readerBack.textContent = currentLang === 'en' ? '← Contents' : '← 目錄';
      readerBack.href = langHref('yunxin-toc.html');
    }

    var topLinks = document.querySelectorAll('.reader-top-links a');
    for (var i = 0; i < topLinks.length; i++) {
      var href = topLinks[i].getAttribute('href') || '';
      if (href.indexOf('index.html') >= 0) topLinks[i].textContent = currentLang === 'en' ? 'Home' : '首頁';
      if (href.indexOf('shelf.html') >= 0) topLinks[i].textContent = currentLang === 'en' ? 'Shelf' : '書架';
      if (href.indexOf('yunxin.html') >= 0) topLinks[i].textContent = currentLang === 'en' ? 'Cover' : '封面';
      if (href.indexOf('yunxin-toc.html') >= 0) topLinks[i].textContent = currentLang === 'en' ? 'Contents' : '目錄';
    }

    var actionLabels = document.querySelectorAll('.reader-actions .btn-label');
    if (actionLabels.length >= 3) {
      actionLabels[0].textContent = currentLang === 'en' ? 'Like' : '點讚';
      actionLabels[1].textContent = currentLang === 'en' ? 'Share' : '分享';
      actionLabels[2].textContent = currentLang === 'en' ? 'Contents' : '回目錄';
    }

    var shareTitle = document.querySelector('.share-dialog-title');
    if (shareTitle) shareTitle.textContent = currentLang === 'en' ? 'Share Article' : '分享文章';
    var closeBtn = document.getElementById('share-close-btn');
    if (closeBtn) closeBtn.textContent = currentLang === 'en' ? 'Close' : '關閉';
    var pdfLabel = document.querySelector('#share-pdf-btn .share-wx-label');
    if (pdfLabel) pdfLabel.textContent = currentLang === 'en' ? 'Download / Share PDF' : '下載／分享 PDF';
    var copyLabel = document.querySelector('#share-copy-btn .share-wx-label');
    if (copyLabel) copyLabel.textContent = currentLang === 'en' ? 'Copy Link' : '複製連結';
    var friendLabel = document.querySelector('#share-friend-btn .share-wx-label');
    if (friendLabel) friendLabel.textContent = currentLang === 'en' ? 'Share to Friends' : '分享給朋友';
    var timelineLabel = document.querySelector('#share-timeline-btn .share-wx-label');
    if (timelineLabel) timelineLabel.textContent = currentLang === 'en' ? 'Share to Moments' : '分享到朋友圈';
  }

  function loadAndRenderArticle() {
    var body = bodyEl();
    if (!body) return;
    body.textContent = currentLang === 'en' ? 'Loading...' : '載入中…';
    loadArticleJson(articleKey, currentLang, function (err, article) {
      if (!err && article) {
        renderArticle(article);
        return;
      }
      if (currentLang === 'en') {
        loadArticleJson(articleKey, 'zh', function (fallbackErr, fallbackArticle) {
          if (fallbackErr || !fallbackArticle) {
            body.textContent = 'Article failed to load. Please try again later.';
            return;
          }
          renderArticle(fallbackArticle);
        });
        return;
      }
      body.textContent = '文章載入失敗，請稍後再試。';
    });
  }

  function loadMaster(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'yunxin/data.json', true);
    xhr.onload = function () {
      if (xhr.status !== 200) {
        callback(new Error('toc failed'));
        return;
      }
      try {
        masterData = JSON.parse(xhr.responseText);
        callback(null, masterData);
      } catch (e) {
        callback(e);
      }
    };
    xhr.onerror = function () { callback(new Error('network')); };
    xhr.send();
  }

  function bootContent() {
    var body = bodyEl();
    if (!body) return;

    if (!isPrefacePage && !articleKey) {
      body.textContent = '未指定文章。';
      return;
    }

    if (!isPrefacePage && articleKey === '00-preface') {
      window.location.replace('yunxin-preface.html');
      return;
    }

    loadMaster(function (err, data) {
      var articles = (data && data.articles) || [];
      var index = -1;
      for (var i = 0; i < articles.length; i++) {
        if (articles[i].id === articleKey) {
          index = i;
          break;
        }
      }

      if (!isPrefacePage && index < 0) {
        body.textContent = '找不到此篇文章。';
        return;
      }

      currentArticles = articles;
      currentArticleIndex = index;
      loadAndRenderArticle();
    });
  }

  for (var lb = 0; lb < langButtons.length; lb++) {
    langButtons[lb].addEventListener('click', function () {
      var lang = this.getAttribute('data-lang');
      if (!lang || lang === currentLang) return;
      currentLang = lang;
      localStorage.setItem('cs:yunxin-lang', lang);
      loadAndRenderArticle();
    });
  }

  function isWeChat() {
    return /MicroMessenger/i.test(navigator.userAgent);
  }

  function buildShareData() {
    return {
      title: ARTICLE_TITLE + ' — 雲箋文舍',
      desc: '《雲心文集》——' + ARTICLE_TITLE + '，來自雲箋文舍',
      link: ARTICLE_HREF,
      imgUrl: window.location.origin + '/images/yunxin-cover.jpg'
    };
  }

  function setLikeUI(nextLiked, nextCount) {
    liked = !!nextLiked;
    if (typeof nextCount === 'number' && !isNaN(nextCount)) {
      likeCount = Math.max(0, nextCount);
    }
    if (likeCountEl) likeCountEl.textContent = likeCount + ' 讚';
    if (likeIcon) likeIcon.textContent = liked ? '♥' : '♡';
    if (likeBtn) {
      if (liked) likeBtn.classList.add('liked');
      else likeBtn.classList.remove('liked');
    }
    try {
      if (liked) localStorage.setItem(likeStorageKey, '1');
      else localStorage.removeItem(likeStorageKey);
    } catch (e) {}
  }

  function showToast(msg, durationMs) {
    var old = document.getElementById('yunxin-toast');
    if (old) old.remove();
    var el = document.createElement('div');
    el.id = 'yunxin-toast';
    el.className = 'yunxin-toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function () { el.classList.add('show'); }, 10);
    setTimeout(function () {
      el.classList.remove('show');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 250);
    }, durationMs || 2200);
  }

  function closeShare() {
    if (shareOverlay) shareOverlay.classList.remove('show');
  }

  function shareArticlePdf() {
    var source =
      document.getElementById('yunxin-article') ||
      document.getElementById('yunxin-preface');
    var title = ARTICLE_TITLE || '';
    if (!title && currentArticle) {
      title = currentArticle.title || currentArticle.zh || currentArticle.en || '';
    }
    if (!title) {
      var h1 = titleEl();
      if (h1) title = (h1.textContent || '').trim();
    }
    if (!title) title = isPrefacePage ? '我的人生路' : '雲心文集';

    if (!window.CloudscrollPdf || typeof window.CloudscrollPdf.exportArticle !== 'function') {
      showToast('PDF 功能暫不可用');
      return;
    }

    window.CloudscrollPdf.exportArticle({
      sourceEl: source,
      title: title,
      subtitle: '林樺 · 雲心文集 · 雲箋文舍',
      filename: title,
      onToast: function (msg) {
        var long = /正在生成|已下載|系統分享/.test(msg);
        showToast(msg, long ? 4200 : 2200);
      },
      onDone: closeShare
    });
  }

  function getStats() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/stats?article=' + encodeURIComponent(ARTICLE_ID), true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          if (viewsEl) viewsEl.textContent = '閱讀 ' + (data.views || 0);
          likeCount = +data.likes || 0;
          var localLiked = false;
          try { localLiked = localStorage.getItem(likeStorageKey) === '1'; } catch (e) {}
          setLikeUI(localLiked, likeCount);
        } catch (e) {}
      }
    };
    xhr.send();
  }

  function recordView() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/stats?article=' + encodeURIComponent(ARTICLE_ID), true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          if (viewsEl) viewsEl.textContent = '閱讀 ' + (data.views || 0);
        } catch (e) {}
      }
    };
    xhr.send(JSON.stringify({ action: 'view' }));
  }

  function toggleLike() {
    if (likeBusy) return;
    likeBusy = true;

    var nextLiked = !liked;
    var optimisticCount = likeCount + (nextLiked ? 1 : -1);
    setLikeUI(nextLiked, optimisticCount);

    var action = nextLiked ? 'like' : 'unlike';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/stats?article=' + encodeURIComponent(ARTICLE_ID), true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
      likeBusy = false;
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          setLikeUI(nextLiked, +data.likes || 0);
        } catch (e) {
          showToast('點讚失敗，請稍後再試');
        }
      } else {
        setLikeUI(!nextLiked, likeCount + (nextLiked ? -1 : 1));
        showToast('點讚失敗，請稍後再試');
      }
    };
    xhr.onerror = function () {
      likeBusy = false;
      setLikeUI(!nextLiked, likeCount + (nextLiked ? -1 : 1));
      showToast('網絡異常，點讚未成功');
    };
    xhr.send(JSON.stringify({ action: action }));
  }

  function copyLink(link, successMsg) {
    var finished = false;
    function done() {
      if (finished) return;
      finished = true;
      closeShare();
      showToast(successMsg || '連結已複製。請打開微信，貼上發送給朋友或發到朋友圈');
    }

    fallbackCopy(link);

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

  function fallbackCopy(link) {
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
  }

  function doShare(options) {
    var d = window.__wxShareData || buildShareData();
    window.__wxShareData = d;

    if (isWeChat()) {
      if (typeof WeixinJSBridge !== 'undefined') {
        try {
          WeixinJSBridge.invoke(options.method, {
            title: d.title || '',
            desc: options.desc ? (d.desc || '') : '',
            link: d.link || '',
            img_url: d.imgUrl || ''
          }, function () {});
        } catch (e) {}
      }
      closeShare();
      showToast('請點右上角「…」分享給朋友或朋友圈');
      return;
    }

    var canNativeShare = typeof navigator.share === 'function' &&
      /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

    if (canNativeShare) {
      navigator.share({
        title: d.title || '',
        text: d.desc || '',
        url: d.link || ''
      }).then(function () {
        closeShare();
      }).catch(function (err) {
        if (err && err.name === 'AbortError') {
          closeShare();
          return;
        }
        copyLink(d.link || '');
      });
      return;
    }

    copyLink(d.link || '');
  }

  function setupWechatShare() {
    if (!isWeChat()) return;
    var data = buildShareData();
    window.__wxShareData = data;

    function onBridgeReady() {
      WeixinJSBridge.on('menu:share:appmessage', function () {
        WeixinJSBridge.invoke('sendAppMessage', {
          title: data.title,
          desc: data.desc,
          link: data.link,
          img_url: data.imgUrl
        }, function () {});
      });
      WeixinJSBridge.on('menu:share:timeline', function () {
        WeixinJSBridge.invoke('shareTimeline', {
          title: data.title,
          link: data.link,
          img_url: data.imgUrl
        }, function () {});
      });
    }

    if (typeof WeixinJSBridge === 'undefined') {
      document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
    } else {
      onBridgeReady();
    }
  }

  function isMobile() {
    return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
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

  function bindActions() {
    if (!likeBtn && !shareBtn) return;

    if (backBtn) {
      backBtn.addEventListener('click', function () {
        window.location.href = 'yunxin-toc.html';
      });
    }

    if (shareBtn && shareOverlay) {
      shareBtn.addEventListener('click', function () {
        window.__wxShareData = buildShareData();
        updateShareDialogForEnv();
        shareOverlay.classList.add('show');
      });
    }

    var shareFriendBtn = document.getElementById('share-friend-btn');
    var shareTimelineBtn = document.getElementById('share-timeline-btn');
    var shareCopyBtn = document.getElementById('share-copy-btn');
    var sharePdfBtn = document.getElementById('share-pdf-btn');

    if (shareFriendBtn) {
      shareFriendBtn.addEventListener('click', function () {
        doShare({ method: 'sendAppMessage', desc: true });
      });
    }
    if (shareTimelineBtn) {
      shareTimelineBtn.addEventListener('click', function () {
        doShare({ method: 'shareTimeline', desc: false });
      });
    }
    if (shareCopyBtn) {
      shareCopyBtn.addEventListener('click', function () {
        var d = window.__wxShareData || buildShareData();
        copyLink(d.link || '');
      });
    }
    if (sharePdfBtn) {
      sharePdfBtn.addEventListener('click', function () {
        shareArticlePdf();
      });
    }
    if (shareCloseBtn) {
      shareCloseBtn.addEventListener('click', closeShare);
    }
    if (shareOverlay) {
      shareOverlay.addEventListener('click', function (e) {
        if (e.target === shareOverlay) closeShare();
      });
    }
    if (likeBtn) likeBtn.addEventListener('click', toggleLike);

    setTimeout(function () { getStats(); recordView(); }, 800);
  }

  bootContent();
  bindActions();
})();

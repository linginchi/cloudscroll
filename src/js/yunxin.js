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
    var skipNotes = isPrefacePage || opts.section === 'prose' || opts.section === 'preface';
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
        prevBtn.href = articleHref(prev);
        prevBtn.classList.remove('is-disabled');
        prevBtn.textContent = '← 上一篇';
      } else if (isPrefacePage) {
        // 自序上一頁仍是扉頁（HTML 已寫好）
      } else {
        prevBtn.href = 'yunxin-toc.html';
        prevBtn.textContent = '← 目錄';
      }
    }

    if (nextBtn) {
      if (next) {
        nextBtn.href = articleHref(next);
        nextBtn.classList.remove('is-disabled');
        nextBtn.textContent = '下一篇 →';
      } else if (isPrefacePage) {
        // 自序下一頁仍是目錄（HTML 已寫好）
      } else {
        nextBtn.href = 'yunxin-toc.html';
        nextBtn.textContent = '回目錄 →';
      }
    }

    if (label) {
      var cur = articles[index];
      if (cur && cur.section === 'preface') label.textContent = '自序';
      else if (cur) label.textContent = (cur.num || '') + '';
      else label.textContent = '文章';
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

  function applyArticleMeta(data) {
    ARTICLE_TITLE = data.title || data.zh || '雲心文集';
    document.title = ARTICLE_TITLE + ' — 雲箋文舍';

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

    var ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) ogTitle.setAttribute('content', ARTICLE_TITLE + ' — 雲箋文舍');
  }

  function loadArticleJson(id, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'yunxin/' + encodeURIComponent(id) + '.json', true);
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

      if (index >= 0 && !isPrefacePage) setupPager(articles, index);

      loadArticleJson(articleKey, function (err2, article) {
        if (err2 || !article) {
          body.textContent = '文章載入失敗，請稍後再試。';
          return;
        }
        applyArticleMeta(article);
        body.innerHTML = renderParagraphs(
          article.paragraphs || [],
          article.title || article.zh || ARTICLE_TITLE,
          { section: article.section || '' }
        );
        var sign = signEl();
        if (sign) {
          if (article.author) sign.textContent = article.author;
          else sign.style.display = 'none';
        }
        window.__wxShareData = buildShareData();
        setupWechatShare();
      });
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

  function showToast(msg) {
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
    }, 2200);
  }

  function closeShare() {
    if (shareOverlay) shareOverlay.classList.remove('show');
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
      tip.textContent = '微信中請點擊右上角「…」，選擇分享給朋友或朋友圈';
      if (friendBtn) friendBtn.style.display = 'none';
      if (timelineBtn) timelineBtn.style.display = 'none';
      if (copyBtn) copyBtn.style.display = '';
      return;
    }

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

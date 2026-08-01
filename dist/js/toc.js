// src/js/toc.js
// 從 data.json 載入真實文章目錄，按輯分組顯示，支援中EN切換、卷跳轉
(function() {
  'use strict';

  var articleList = document.getElementById('article-list');
  if (!articleList) return;

  var masterData = null;
  var currentLang = 'zh';

  // Get target volume from URL params
  var params = new URLSearchParams(window.location.search);
  var targetVolume = parseInt(params.get('volume')) || 0;

  // Language toggle buttons
  var langToggle = document.getElementById('toc-lang-toggle');
  var langOptions = langToggle ? langToggle.querySelectorAll('.lang-option') : null;

  // Header/footer DOM refs
  var headerRight = document.querySelector('.header-right');
  var homeLink = document.querySelector('.home-link');
  var footerBookName = document.querySelector('.page-footer .book-name');

  // Volume labels (populated dynamically from data)
  var volumeLabels = {};

  // Inject volume selector into header area (called after data loads)
  function injectVolumeSelector(chapters) {
    var header = document.querySelector('.page-header');
    if (!header) return;

    var existing = document.getElementById('toc-vol-selector');
    if (existing) existing.remove();

    var selector = document.createElement('div');
    selector.className = 'toc-volume-selector';
    selector.id = 'toc-vol-selector';

    var parts = [];
    chapters.forEach(function(ch, i) {
      var vol = i + 1;
      var activeClass = targetVolume === vol || (targetVolume === 0 && i === 0) ? ' active' : '';
      // Extract roman numeral from chapter.en or use volume number
      var partLabel = ch.en || 'Part ' + vol;
      volumeLabels[String(vol)] = {
        zh: '我的人生旅行 · ' + ch.zh,
        en: 'A Life Unfolded in Miles · ' + partLabel,
      };
      // Build short label from chapter.zh (e.g. "第一輯 向世界出發" → "第一輯")
      var shortZh = ch.zh.split(' ')[0];
      parts.push('<span class="vol-option' + activeClass + '" data-vol="' + vol + '">' + shortZh + '</span>');
      if (i < chapters.length - 1) {
        parts.push('<span class="vol-sep">|</span>');
      }
    });

    selector.innerHTML = parts.join('');
    header.appendChild(selector);

    var volOptions = selector.querySelectorAll('.vol-option');
    volOptions.forEach(function(opt) {
      opt.addEventListener('click', function() {
        var vol = this.getAttribute('data-vol');
        jumpToChapter(parseInt(vol));
      });
    });
  }

  function updateVolumeSelector(activeVol) {
    var volOptions = document.querySelectorAll('#toc-vol-selector .vol-option');
    volOptions.forEach(function(opt) {
      opt.classList.toggle('active', opt.getAttribute('data-vol') === String(activeVol));
    });
  }

  function jumpToChapter(volume) {
    if (!masterData) return;
    var chIdx = volume - 1;
    var headers = articleList.querySelectorAll('.toc-chapter-header');
    if (headers.length > chIdx) {
      headers[chIdx].scrollIntoView({ behavior: 'smooth', block: 'start' });
      updateVolumeSelector(volume);
      targetVolume = volume;

      // Build header label
      var label = volumeLabels[String(volume)];
      if (label) {
        if (headerRight) {
          headerRight.textContent = currentLang === 'zh' ? label.zh : label.en;
        }
        document.title = currentLang === 'zh'
          ? '目錄 — ' + label.zh
          : 'Contents — ' + label.en.split(' · ')[0];
      }
    }
  }

  // Language switch handler
  if (langOptions) {
    langOptions.forEach(function(opt) {
      opt.addEventListener('click', function() {
        var lang = this.getAttribute('data-lang');
        if (lang === currentLang) return;
        currentLang = lang;
        langOptions.forEach(function(o) { o.classList.remove('active'); });
        this.classList.add('active');

        // Header bilingual
        if (headerRight && targetVolume) {
          var label = volumeLabels[String(targetVolume)];
          headerRight.textContent = lang === 'zh'
            ? (label ? label.zh : '我的人生旅行')
            : (label ? label.en : 'A Life Unfolded in Miles');
        } else if (headerRight) {
          headerRight.textContent = lang === 'zh' ? '我的人生旅行' : 'A Life Unfolded in Miles';
        }
        if (homeLink) {
          homeLink.textContent = lang === 'zh' ? '☰ 首頁' : '☰ Home';
        }
        if (footerBookName) {
          footerBookName.textContent = lang === 'zh' ? '雲箋文舍' : 'Cloudscroll';
        }
        document.title = lang === 'zh' ? '目錄 — 雲箋文舍' : 'Contents — Cloudscroll';

        if (masterData) renderTOC(masterData);
      });
    });
  }

  // Show loading state
  articleList.innerHTML = '<li class="toc-loading">載入中…</li>';

  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'book/data.json', true);

  xhr.onload = function() {
    if (xhr.status !== 200) {
      articleList.innerHTML = '<li class="toc-loading" style="color:#999">無法載入目錄</li>';
      return;
    }
    try {
      masterData = JSON.parse(xhr.responseText);
      injectVolumeSelector(masterData.chapters || []);
      renderTOC(masterData);

      // Scroll to target chapter after rendering
      if (targetVolume) {
        var vol = targetVolume;
        targetVolume = 0;
        jumpToChapter(vol);
      }
    } catch (e) {
      articleList.innerHTML = '<li class="toc-loading" style="color:#999">數據解析錯誤</li>';
    }
  };

  xhr.onerror = function() {
    articleList.innerHTML = '<li class="toc-loading" style="color:#999">無法載入目錄</li>';
  };

  xhr.send();

  function renderTOC(data) {
    articleList.innerHTML = '';

    // 1) Preface
    var preface = data.articles.find(function(a) { return a.id === '00-preface'; });
    if (preface) {
      var prefaceItem = document.createElement('li');
      prefaceItem.className = 'toc-item toc-item-preface';
      var prefaceEn = preface.en || 'Preface';
      prefaceItem.innerHTML =
        '<span class="toc-item-zh">' +
          '<span class="toc-item-num">◆</span>' +
          (currentLang === 'en' ? prefaceEn : preface.zh) +
        '</span>' +
        '<span class="toc-item-en">' + (currentLang === 'en' ? '' : prefaceEn) + '</span>';
      prefaceItem.addEventListener('click', function() {
        openArticle(preface);
      });
      articleList.appendChild(prefaceItem);
    }

    // 2) Each chapter
    data.chapters.forEach(function(chapter, ci) {
      var chapterHeader = document.createElement('li');
      chapterHeader.className = 'toc-chapter-header';
      chapterHeader.id = 'chapter-' + (ci + 1);
      chapterHeader.innerHTML =
        '<span class="toc-chapter-zh">' + (currentLang === 'en' ? chapter.en : chapter.zh) + '</span>' +
        '<span class="toc-chapter-en">' + (currentLang === 'en' ? '' : chapter.en) + '</span>';
      articleList.appendChild(chapterHeader);

      chapter.articles.forEach(function(article, ai) {
        var item = document.createElement('li');
        item.className = 'toc-item';

        var num = ('0' + (ai + 1)).slice(-2);
        var title = currentLang === 'en' ? (article.en || article.zh) : article.zh;
        var subtitle = '';

        if (currentLang === 'en') {
          subtitle = article.en_subtitle || '';
          if (subtitle) subtitle = subtitle.slice(0, 40) + '…';
        } else {
          subtitle = article.subtitle || '';
          if (subtitle) subtitle = subtitle.slice(0, 30) + '…';
        }

        var subtitleHtml = subtitle
          ? '<span class="toc-item-sub">' + subtitle + '</span>'
          : '';

        item.innerHTML =
          '<span class="toc-item-zh">' +
            '<span class="toc-item-num">' + num + '.</span>' + title +
          '</span>' +
          subtitleHtml;

        item.addEventListener('click', function() {
          openArticle(article);
        });

        articleList.appendChild(item);
      });
    });
  }

  function openArticle(article) {
    sessionStorage.setItem('currentArticle', JSON.stringify(article));
    sessionStorage.setItem('currentVolume', targetVolume || 1);
    window.location.href = 'reader.html';
  }

})();

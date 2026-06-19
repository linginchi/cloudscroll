// src/js/toc.js
// 從 data.json 載入真實文章目錄，按輯分組顯示，支援中EN切換
(function() {
  'use strict';

  var articleList = document.getElementById('article-list');
  if (!articleList) return;

  var masterData = null;
  var currentLang = 'zh';

  // 語言切換按鈕
  var langToggle = document.getElementById('toc-lang-toggle');
  var langOptions = langToggle ? langToggle.querySelectorAll('.lang-option') : null;

  // 頂欄/底欄 DOM refs
  var headerRight = document.querySelector('.header-right');
  var homeLink = document.querySelector('.home-link');
  var footerBookName = document.querySelector('.page-footer .book-name');

  if (langOptions) {
    langOptions.forEach(function(opt) {
      opt.addEventListener('click', function() {
        var lang = this.getAttribute('data-lang');
        if (lang === currentLang) return;
        currentLang = lang;
        langOptions.forEach(function(o) { o.classList.remove('active'); });
        this.classList.add('active');

        // 頂欄雙語
        if (headerRight) {
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

  // 顯示加載狀態
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
      renderTOC(masterData);
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

    // 1) 序文
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

    // 2) 各輯
    data.chapters.forEach(function(chapter, ci) {
      var chapterHeader = document.createElement('li');
      chapterHeader.className = 'toc-chapter-header';
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
    window.location.href = 'reader.html';
  }

})();

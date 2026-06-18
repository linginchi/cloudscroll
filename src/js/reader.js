// src/js/reader.js
(function() {
  'use strict';

  // ---- DOM refs ----
  var pageTop = document.getElementById('page-top');
  var pageUnder = document.getElementById('page-under');
  var pageText = document.getElementById('page-text');
  var pageUnderText = pageUnder ? pageUnder.querySelector('.page-text') : null;
  var pageNum = document.getElementById('page-num');
  var progressBar = document.getElementById('progress-bar');
  var articleTitle = document.getElementById('article-title');
  var langToggle = document.getElementById('lang-toggle');
  var langOptions = langToggle ? langToggle.querySelectorAll('.lang-option') : null;
  var bookContainer = document.getElementById('book-container');

  if (!pageTop || !pageUnder || !pageText || !pageUnderText || !pageNum || !progressBar) return;

  // ---- State ----
  var currentLang = 'zh';
  var currentPage = 0;
  var allPages = [];
  var isFlipping = false;
  var touchStartX = 0;
  var touchStartY = 0;
  var hasMoved = false;

  // ---- Article data ----
  var articleData = null;
  try {
    var stored = sessionStorage.getItem('currentArticle');
    if (stored) {
      articleData = JSON.parse(stored);
    }
  } catch (e) { /* ignore */ }

  if (!articleData || !articleData.id) {
    // Fallback: use first article
    articleData = {
      id: '01-wuyi-mountain',
      zh: '武夷山紀行',
      en: 'A Journey to Wuyi Mountain'
    };
  }

  // Update title
  if (articleTitle) {
    articleTitle.textContent = articleData.zh;
  }

  function getArticleKey() {
    return 'article_' + articleData.id + '_' + currentLang;
  }

  // ---- Content data (hardcoded sample content for each article) ----
  var articlesContent = {
    '01-wuyi-mountain': [
      '武夷山位於福建省西北部，是聯合國教科文組織世界文化與自然遺產。我曾兩度造訪這座名山，每一次都有不同的感受。第一次是春末，滿山杜鵑盛開，紅白相間，像是為這座千年名山披上了一件彩衣。',
      '第二次是深秋，山上的楓葉紅了，夾雜在蒼翠的松柏之間，層林盡染，美不勝收。登臨天遊峰，俯瞰九曲溪蜿蜒如帶，竹筏點點，遊人如織。',
      '九曲溪發源於武夷山自然保護區，全長約十公里，因河道彎曲而得名。乘坐竹筏順流而下，兩岸峰巒疊嶂，景色變幻，移步換景，令人目不暇給。',
      '筏工是當地的茶農，一邊撐筏一邊為我們講述武夷山的傳說。玉女峰與大王峰的愛情故事，至今仍在山間流傳。'
    ],
    'default': [
      '這是《我的人生旅行》中的一篇遊記。作者林樺以細膩的筆觸記錄了旅途中的所見所聞，將自然風光與人文情懷融為一體。',
      '每篇文章都承載著作者對人生的感悟和對自然的熱愛。從江南水鄉到西北大漠，從雪山之巔到海島之濱，足跡遍布祖國的大好河山。',
      '感謝您閱讀這些文字。希望通過這些遊記，您能感受到作者筆下山川的壯美與人生的況味。正如蘇東坡所言：「人生如逆旅，我亦是行人。」',
      '讓我們一起翻開書頁，跟隨作者的腳步，開始這場跨越時空的人生旅行。每一篇文章都是一扇窗，讓我們看到不同的風景，體會不同的人生。'
    ]
  };

  // Generate EN content
  var articlesContentEN = {};
  var enMap = {
    '01-wuyi-mountain': [
      'Mount Wuyi is located in northwestern Fujian Province, a UNESCO World Cultural and Natural Heritage site. I have visited this famous mountain twice, each time with a different feeling.',
      'The first visit was in late spring, when the mountains were covered with blooming azaleas in red and white, like a colorful garment draped over this millennium-old mountain.',
      'The second visit was in deep autumn, when the maple leaves had turned red, intermingling with the verdant pines and cypresses, creating a breathtaking tapestry.',
      'Riding a bamboo raft down the winding Nine-Bend Stream, with peaks towering on both sides, the scenery changed with every turn.'
    ],
    'default': [
      'This is a travel essay from "My Life\'s Journey". Author Lin Hua records his observations and experiences with delicate brushstrokes, blending natural scenery with human sentiment.',
      'Each article carries the author\'s reflections on life and love for nature. From the water towns of Jiangnan to the deserts of the Northwest, from snowy peaks to coastal islands.',
      'Thank you for reading these words. Through these travel essays, may you feel the grandeur of the landscapes and the flavor of life as described by the author.',
      'As Su Dongpo said: "Life is like a journey, and I am but a traveler." Let us turn the pages together and follow the author on this journey across time and space.'
    ]
  };

  function getContent(lang) {
    var key = articleData.id;
    var source = lang === 'zh' ? articlesContent : articlesContentEN;
    return source[key] || source['default'];
  }

  // ---- Content pagination ----
  function paginateContent(paragraphs) {
    var pages = [];
    var currentPage = [];

    paragraphs.forEach(function(p) {
      // If the paragraph alone is too long, split it
      if (p.length > 300) {
        if (currentPage.length > 0) {
          pages.push(currentPage);
          currentPage = [];
        }
        // Split long paragraph into chunks
        var chunks = splitLongParagraph(p);
        chunks.forEach(function(chunk) {
          pages.push(['<p>' + chunk + '</p>']);
        });
      } else {
        currentPage.push('<p>' + p + '</p>');
        // Check if current page is full
        var totalLen = currentPage.join('').length;
        if (totalLen > 500 || currentPage.length >= 4) {
          pages.push(currentPage);
          currentPage = [];
        }
      }
    });

    if (currentPage.length > 0) {
      pages.push(currentPage);
    }

    if (pages.length === 0) {
      pages.push(['<p>（未完待續）</p>']);
    }

    return pages;
  }

  function splitLongParagraph(text) {
    var chunks = [];
    var size = 150;
    for (var i = 0; i < text.length; i += size) {
      chunks.push(text.slice(i, i + size));
    }
    return chunks;
  }

  // ---- Render page ----
  function renderPages() {
    var content = getContent(currentLang);
    allPages = paginateContent(content);
    currentPage = 0;
    showPage(0, false);
  }

  function showPage(index, animate) {
    if (index < 0 || index >= allPages.length) return;
    currentPage = index;

    // Set top page content
    pageText.innerHTML = allPages[currentPage].join('');

    // Set under page content (next or prev)
    var underIndex = currentPage < allPages.length - 1 ? currentPage + 1 : null;
    if (underIndex !== null) {
      pageUnderText.innerHTML = allPages[underIndex].join('');
    } else {
      pageUnderText.innerHTML = '<p style="color:var(--color-text-faint);text-align:center;">— 本篇完 —</p>';
    }

    updateProgress();
  }

  function updateProgress() {
    var total = allPages.length;
    var pct = total > 1 ? Math.round(((currentPage + 1) / total) * 100) : 100;
    pageNum.textContent = (currentPage + 1) + ' / ' + total;
    progressBar.style.width = pct + '%';
  }

  // ---- Page flip ----
  function flipForward() {
    if (isFlipping) return;
    if (currentPage >= allPages.length - 1) return;

    isFlipping = true;

    // Set under page to next content
    var nextIndex = currentPage + 1;
    if (nextIndex < allPages.length) {
      pageUnderText.innerHTML = allPages[nextIndex].join('');
    } else {
      pageUnderText.innerHTML = '<p style="color:var(--color-text-faint);text-align:center;">— 本篇完 —</p>';
    }

    pageTop.classList.add('flipping');

    setTimeout(function() {
      currentPage = nextIndex;
      pageText.innerHTML = allPages[currentPage].join('');
      pageTop.classList.remove('flipping');

      // Update under page
      var underNext = currentPage + 1;
      if (underNext < allPages.length) {
        pageUnderText.innerHTML = allPages[underNext].join('');
      } else {
        pageUnderText.innerHTML = '<p style="color:var(--color-text-faint);text-align:center;">— 本篇完 —</p>';
      }

      updateProgress();
      isFlipping = false;
    }, 500);
  }

  function flipBackward() {
    if (isFlipping) return;
    if (currentPage <= 0) return;

    isFlipping = true;

    // Set under page to current content (it will be revealed)
    pageUnderText.innerHTML = allPages[currentPage].join('');
    // Set top page to prev content
    var prevIndex = currentPage - 1;
    pageText.innerHTML = allPages[prevIndex].join('');

    // We need to show the page flipping back from the left
    // First reset, then apply transform
    pageTop.classList.remove('flipping');
    // Force reflow
    void pageTop.offsetWidth;
    pageTop.classList.add('flipping-back');

    setTimeout(function() {
      currentPage = prevIndex;
      pageText.innerHTML = allPages[currentPage].join('');
      pageTop.classList.remove('flipping-back');

      var underNext = currentPage + 1;
      if (underNext < allPages.length) {
        pageUnderText.innerHTML = allPages[underNext].join('');
      } else {
        pageUnderText.innerHTML = '<p style="color:var(--color-text-faint);text-align:center;">— 本篇完 —</p>';
      }

      updateProgress();
      isFlipping = false;
    }, 500);
  }

  // ---- Touch events ----
  if (bookContainer) {
    bookContainer.addEventListener('touchstart', function(e) {
      var touch = e.touches[0];
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
      hasMoved = false;
    }, { passive: true });

    bookContainer.addEventListener('touchmove', function(e) {
      hasMoved = true;
    }, { passive: true });

    bookContainer.addEventListener('touchend', function(e) {
      if (hasMoved) {
        // Swipe detected during move
        return;
      }

      // Tap — determine left/right area
      var touch = e.changedTouches[0];
      var rect = bookContainer.getBoundingClientRect();
      var x = touch.clientX - rect.left;
      var midX = rect.width / 2;

      if (x < midX) {
        flipBackward();
      } else {
        flipForward();
      }
    }, { passive: true });
  }

  // ---- Language toggle ----
  if (langToggle && langOptions) {
    langOptions.forEach(function(opt) {
      opt.addEventListener('click', function() {
        var lang = this.getAttribute('data-lang');
        if (lang === currentLang) return;

        currentLang = lang;
        langOptions.forEach(function(o) { o.classList.remove('active'); });
        this.classList.add('active');

        // Update title
        if (articleTitle) {
          articleTitle.textContent = lang === 'zh' ? articleData.zh : articleData.en;
        }

        // Update footer
        var langZh = document.querySelector('.lang-zh');
        var langEn = document.querySelector('.lang-en');
        if (langZh && langEn) {
          if (lang === 'zh') {
            langZh.style.display = 'inline';
            langEn.style.display = 'none';
          } else {
            langZh.style.display = 'none';
            langEn.style.display = 'inline';
          }
        }

        // Re-render pages
        renderPages();
      });
    });
  }

  // ---- Initialize ----
  renderPages();
  updateProgress();
})();

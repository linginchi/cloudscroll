(function() {
  'use strict';

  var volumeFromUrl = new URLSearchParams(window.location.search).get('volume');
  var storedVolume = sessionStorage.getItem('volume');
  var targetVolume = parseInt(volumeFromUrl) || parseInt(storedVolume) || 1;

  var masterData = null;
  var allArticles = [];

  // Load data
  function loadData(cb) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/data.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try { masterData = JSON.parse(xhr.responseText); cb(); }
        catch(e) { cb(); }
      } else { cb(); }
    };
    xhr.onerror = function() { cb(); };
    xhr.send();
  }

  function render() {
    if (!masterData) return;
    var chapters = masterData.chapters || [];
    allArticles = masterData.articles || [];
    var chIdx = targetVolume - 1;
    if (chIdx < 0 || chIdx >= chapters.length) { chIdx = 0; targetVolume = 1; }

    var chapter = chapters[chIdx];
    var articles = chapter.articles || [];
    var chapterTitle = chapter.zh || '';
    var chapterEn = chapter.en || '';
    var author = masterData.author || '林樺';

    // Update document title
    document.title = chapterTitle + ' — 雲箋文舍';

    // --- Flaps scroll hint ---
    document.getElementById('flaps-scroll-hint').addEventListener('click', function() {
      scrollToToc();
    });

    // --- TOC ---
    document.getElementById('toc-section-title').textContent = chapterTitle;

    var listEl = document.getElementById('article-list');
    var html = '';
    for (var i = 0; i < articles.length; i++) {
      var art = articles[i];
      var num = (i + 1);
      var numStr = num < 10 ? '0' + num : '' + num;
      var title = art.zh || '';
      var subtitle = art.subtitle || '';
      if (!subtitle && art.stats && art.stats.paragraphs) {
        // Could generate an excerpt but that's complex; just use subtitle if available
      }
      html += '<li class="toc-item" data-id="' + art.id + '" data-title="' + art.zh.replace(/"/g, '&quot;') + '" data-en="' + (art.en || '').replace(/"/g, '&quot;') + '">';
      html += '<div class="toc-item-row">';
      html += '<span class="toc-item-num">' + numStr + '</span>';
      html += '<span class="toc-item-title">' + escapeHtml(title) + '</span>';
      html += '</div>';
      if (subtitle) {
        html += '<div class="toc-item-sub">' + escapeHtml(subtitle.substring(0, 60)) + '</div>';
      }
      html += '</li>';
    }
    listEl.innerHTML = html;

    // Attach click handlers to TOC items
    var items = listEl.querySelectorAll('.toc-item');
    for (var j = 0; j < items.length; j++) {
      (function(item) {
        item.addEventListener('click', function() {
          var id = this.getAttribute('data-id');
          var zh = this.getAttribute('data-title');
          var en = this.getAttribute('data-en');
          sessionStorage.setItem('currentArticle', JSON.stringify({ id: id, zh: zh, en: en }));
          sessionStorage.setItem('currentVolume', targetVolume);
          window.location.href = 'reader.html';
        });
      })(items[j]);
    }

    // --- Get the correct scroll container ---
    // Desktop (≥1024px): .desktop-main has overflow-y: auto
    // Mobile: .volume-page-inner has overflow-y: auto
    function getScrollContainer() {
      if (window.innerWidth >= 1024) {
        return document.querySelector('.desktop-main');
      }
      return document.querySelector('.volume-page-inner');
    }

    // Shared scroll-to-TOC function — waits until preface is fully loaded
    var _tocScrollDone = false;
    function scrollToToc() {
      var toc = document.getElementById('volume-toc');
      if (!toc) return;
      // 確保自序內容（含英文）已完全渲染後再定位
      var sc = getScrollContainer();
      if (sc) {
        // 先用 getBoundingClientRect 取得 toc 相對於可視區的位置
        var scRect = sc.getBoundingClientRect();
        var tocRect = toc.getBoundingClientRect();
        sc.scrollTop = sc.scrollTop + (tocRect.top - scRect.top) - 16;
      }
      // 如果定位後位置明顯不對（還在頁面頂部附近），稍後重試
      if (sc && sc.scrollTop < 100 && !_tocScrollDone) {
        _tocScrollDone = true;
        setTimeout(function() { scrollToToc(); }, 600);
      }
    }

    // --- Load author preface ---
    loadPreface();

    // --- Auto-scroll to TOC when returning from reader ---
    if (sessionStorage.getItem('scrollToToc') === '1' || new URLSearchParams(window.location.search).get('scrollToToc') === '1') {
      sessionStorage.removeItem('scrollToToc');
      // 等自序內容（含英文翻譯）非同步載入完成後再定位
      setTimeout(function() { scrollToToc(); }, 800);
    }

    // --- Desktop sidebar ---
    if (window.innerWidth >= 1024) {
      renderDesktopSidebar(chapters, chapter, chIdx);
    }
    window.addEventListener('resize', function() {
      if (window.innerWidth >= 1024) {
        renderDesktopSidebar(chapters, chapter, chIdx);
      }
    });
  }

  function renderDesktopSidebar(chapters, currentChapter, currentChIdx) {
    var sidebar = document.getElementById('desktop-sidebar');
    if (!sidebar) return;

    var html = '<div class="sidebar-header">';
    html += '<div class="sidebar-title">雲箋文舍</div>';
    html += '<div class="sidebar-subtitle">Cloudscroll</div>';
    html += '</div>';
    html += '<div class="sidebar-nav">';

    for (var ci = 0; ci < chapters.length; ci++) {
      var ch = chapters[ci];
      html += '<div class="sidebar-chapter">' + ch.zh + '</div>';
      var arts = ch.articles || [];
      for (var ai = 0; ai < arts.length; ai++) {
        var art = arts[ai];
        var num = ai + 1;
        var numStr = num < 10 ? '0' + num : '' + num;
        var isActive = (ci === currentChIdx) ? ' active' : '';
        html += '<span class="sidebar-article' + isActive + '" data-vol="' + (ci + 1) + '" data-id="' + art.id + '" data-title="' + art.zh.replace(/"/g, '&quot;') + '" data-en="' + (art.en || '').replace(/"/g, '&quot;') + '">';
        html += '<span class="sidebar-num">' + numStr + '</span>' + art.zh;
        html += '</span>';
      }
    }
    html += '</div>';
    html += '<a class="sidebar-back" href="shelf.html">← 返回書架</a>';

    sidebar.innerHTML = html;

    // Attach click handlers
    var sidebarItems = sidebar.querySelectorAll('.sidebar-article');
    for (var si = 0; si < sidebarItems.length; si++) {
      (function(item) {
        item.addEventListener('click', function() {
          var id = this.getAttribute('data-id');
          var zh = this.getAttribute('data-title');
          var en = this.getAttribute('data-en');
          var vol = this.getAttribute('data-vol');
          sessionStorage.setItem('currentArticle', JSON.stringify({ id: id, zh: zh, en: en }));
          sessionStorage.setItem('currentVolume', vol);
          window.location.href = 'reader.html';
        });
      })(sidebarItems[si]);
    }
  }

  function loadPreface() {
    var flapsText = document.getElementById('flaps-text');
    if (!flapsText) return;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/00-preface.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          var blocks = data.blocks || [];
          var paragraphs = [];
          for (var i = 0; i < blocks.length; i++) {
            if (blocks[i].type === 'text') {
              var t = blocks[i].content.trim();
              if (t) {
                paragraphs.push(t);
              }
            }
          }
          if (paragraphs.length > 0) {
            flapsText.innerHTML = '';
            for (var p = 0; p < paragraphs.length; p++) {
              var el = document.createElement('p');
              el.style.cssText = 'margin-bottom:1.2em;text-indent:2em;text-align:justify;';
              el.textContent = paragraphs[p];
              flapsText.appendChild(el);
            }
            // 載入英文翻譯
            loadPrefaceEn();
          } else {
            flapsText.textContent = '序言內容暫缺';
          }
        } catch(e) {
          flapsText.textContent = '序言內容加載失敗';
        }
      } else {
        flapsText.textContent = '序言內容暫缺';
      }
    };
    xhr.onerror = function() { flapsText.textContent = '序言內容暫缺'; };
    xhr.send();
  }

  function loadPrefaceEn() {
    var flapsTextEn = document.getElementById('flaps-text-en');
    var enDivider = document.getElementById('flaps-en-divider');
    if (!flapsTextEn) return;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'book/en-00-preface.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          var blocks = data.blocks || [];
          var paragraphs = [];
          for (var i = 0; i < blocks.length; i++) {
            if (blocks[i].type === 'text') {
              var t = blocks[i].content.trim();
              if (t) {
                paragraphs.push(t);
              }
            }
          }
          if (paragraphs.length > 0) {
            flapsTextEn.style.display = '';
            if (enDivider) enDivider.style.display = '';
            flapsTextEn.innerHTML = '';
            for (var p = 0; p < paragraphs.length; p++) {
              var el = document.createElement('p');
              el.style.cssText = 'margin-bottom:1.2em;text-indent:2em;text-align:justify;';
              el.textContent = paragraphs[p];
              flapsTextEn.appendChild(el);
            }
          } else {
            flapsTextEn.style.display = 'none';
            if (enDivider) enDivider.style.display = 'none';
          }
        } catch(e) {
          flapsTextEn.style.display = 'none';
          if (enDivider) enDivider.style.display = 'none';
        }
      } else {
        flapsTextEn.style.display = 'none';
        if (enDivider) enDivider.style.display = 'none';
      }
    };
    xhr.onerror = function() {
      flapsTextEn.style.display = 'none';
      if (enDivider) enDivider.style.display = 'none';
    };
    xhr.send();
  }

  function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  loadData(render);
})();

(function() {
  'use strict';

  // Load data.json to get book info and cover paths
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

  function renderShelf(data) {
    var container = document.getElementById('shelf-books');
    if (!container) return;

    var chapters = data ? data.chapters : [];
    var covers = data ? data.covers || {} : {};

    var html = '';
    for (var i = 0; i < chapters.length; i++) {
      var ch = chapters[i];
      var vol = i + 1;
      var coverSrc = covers['v' + vol] ? 'book/' + covers['v' + vol] : '';
      var volLabel = ch.zh ? ch.zh.split(' ').pop() : '';
      var volClass = 'v' + vol;

      html += '<div class="book-card ' + volClass + '" data-volume="' + vol + '">';

      // 書脊 — 左側彩色縱條，含橫向裝訂線與卷標籤
      html += '<div class="book-spine">';
      html +=   '<div class="spine-ridge"></div>';
      html +=   '<div class="spine-ridge"></div>';
      html +=   '<div class="spine-ridge"></div>';
      html +=   '<span class="spine-label">' + volLabel + '</span>';
      html += '</div>';

      // 書本主體
      html += '<div class="book-body">';

      // 封面圖
      html += '<div class="book-cover" style="background-image:url(' + coverSrc + ')">';
      html +=   '<div class="cover-sheen"></div>';
      html += '</div>';

      // 紙邊（右側頁緣）
      html += '<div class="book-pages">';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html +=   '<div class="page-line"></div>';
      html += '</div>';

      html += '</div>'; // body

      // 案頭陰影
      html += '<div class="book-shadow"></div>';

      html += '</div>'; // card
    }

    // 《雲心文集》獨立書：點擊進入封面 → 扉頁 → 自序 → 目錄
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
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=       '<div class="page-line"></div>';
    html +=     '</div>';
    html +=   '</div>';
    html +=   '<div class="book-shadow"></div>';
    html += '</div>';

    container.innerHTML = html;

    // Attach click handlers
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
  }

  loadData();
})();

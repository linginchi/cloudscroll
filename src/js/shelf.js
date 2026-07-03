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
          // Fallback: hard-coded shelf (shouldn't happen)
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
    var container = document.getElementById('shelf-content');
    if (!container) return;

    var chapters = data ? data.chapters : [];
    var covers = data ? data.covers || {} : {};
    var author = data ? data.author || '林樺' : '林樺';

    var html = '';
    for (var i = 0; i < chapters.length; i++) {
      var ch = chapters[i];
      var vol = i + 1;
      var coverSrc = covers['v' + vol] ? 'book/' + covers['v' + vol] : '';
      var title = ch.zh || '';
      var subtitle = title.split(' ').slice(1).join(' ') || title;
      var en = ch.en || '';
      var hint = ch.hint || '';

      html += '<div class="book-card" data-volume="' + vol + '">';
      // Cover background
      html += '<div class="book-cover-bg" style="background-image:url(' + coverSrc + ')">';
      html += '<div class="book-cover-overlay">';
      html += '<div class="book-title">' + title + '</div>';
      html += '<div class="book-subtitle">' + subtitle + '</div>';
      if (en) html += '<div class="book-subtitle-en">' + en + '</div>';
      html += '<div class="book-author-line">' + author + ' 著</div>';
      html += '<div class="book-open-btn">翻開書頁</div>';
      html += '</div></div>';
      if (hint) html += '<p class="book-hint">' + hint + '</p>';
      html += '</div>';
    }

    container.innerHTML = html;

    // Attach click handlers
    var cards = container.querySelectorAll('.book-card');
    for (var j = 0; j < cards.length; j++) {
      (function(card) {
        card.addEventListener('click', function() {
          var volume = this.getAttribute('data-volume');
          sessionStorage.setItem('volume', volume);
          window.location.href = 'volume.html?volume=' + volume;
        });
      })(cards[j]);
    }
  }

  loadData();
})();

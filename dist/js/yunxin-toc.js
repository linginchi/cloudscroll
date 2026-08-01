// src/js/yunxin-toc.js — render 《雲心文集》 TOC in exact data.json order
(function () {
  'use strict';

  var root = document.getElementById('yunxin-toc-root');
  if (!root) return;

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function render(data) {
    var sections = data.sections || [];
    var html = '';

    for (var i = 0; i < sections.length; i++) {
      var sec = sections[i];
      html += '<div class="yunxin-toc-section">';
      html +=   '<div class="yunxin-toc-section-head">';
      html +=     '<span class="yunxin-toc-section-title">' + escapeHtml(sec.title) + '</span>';
      if (sec.pending) {
        html +=   '<span class="yunxin-toc-pending">' + escapeHtml(sec.note || '待發') + '</span>';
      }
      html +=   '</div>';

      if (sec.pending) {
        html += '<p class="yunxin-toc-pending-note">正文完稿後將於此處陸續開放。</p>';
        html += '</div>';
        continue;
      }

      var articles = sec.articles || [];
      html += '<ul class="toc-list">';
      for (var j = 0; j < articles.length; j++) {
        var a = articles[j];
        var num = a.section === 'preface' ? '序' : a.num;
        html += '<li class="toc-item" data-href="' + escapeHtml(a.href) + '">';
        html +=   '<div class="toc-item-row">';
        html +=     '<span class="toc-item-num">' + escapeHtml(num) + '</span>';
        html +=     '<span class="toc-item-title">' + escapeHtml(a.title) + '</span>';
        html +=   '</div>';
        html += '</li>';
      }
      html += '</ul>';
      html += '</div>';
    }

    root.innerHTML = html;

    var items = root.querySelectorAll('.toc-item[data-href]');
    for (var k = 0; k < items.length; k++) {
      items[k].addEventListener('click', function () {
        window.location.href = this.getAttribute('data-href');
      });
    }
  }

  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'yunxin/data.json', true);
  xhr.onload = function () {
    if (xhr.status !== 200) {
      root.innerHTML = '<p class="yunxin-toc-loading">目錄載入失敗，請稍後再試。</p>';
      return;
    }
    try {
      render(JSON.parse(xhr.responseText));
    } catch (e) {
      root.innerHTML = '<p class="yunxin-toc-loading">目錄解析失敗。</p>';
    }
  };
  xhr.onerror = function () {
    root.innerHTML = '<p class="yunxin-toc-loading">目錄載入失敗，請稍後再試。</p>';
  };
  xhr.send();
})();

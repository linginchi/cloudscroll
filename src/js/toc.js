// src/js/toc.js
(function() {
  const articleList = document.getElementById('article-list');
  if (!articleList) return;

  // Inline article data for immediate rendering
  var articles = [
    { "id": "01-wuyi-mountain", "zh": "武夷山紀行", "en": "A Journey to Wuyi Mountain" },
    { "id": "02-lijiang-river", "zh": "灕江煙雨", "en": "Misty Rain on the Li River" },
    { "id": "03-jiuzhaigou", "zh": "九寨溝歸來", "en": "Return from Jiuzhaigou" },
    { "id": "04-yangtze-gorge", "zh": "三峽行", "en": "Traveling the Three Gorges" },
    { "id": "05-west-lake", "zh": "西湖四季", "en": "Four Seasons at West Lake" },
    { "id": "06-mogao-caves", "zh": "莫高窟心影", "en": "Echoes of the Mogao Caves" },
    { "id": "07-huangshan", "zh": "黃山雲海", "en": "Sea of Clouds at Mount Huangshan" },
    { "id": "08-guilin-landscape", "zh": "桂林山水", "en": "The Landscape of Guilin" },
    { "id": "09-tibet", "zh": "西藏之旅", "en": "Journey to Tibet" },
    { "id": "10-yunnan", "zh": "彩雲之南", "en": "Beyond the Colorful Clouds" }
  ];

  articles.forEach(function(article, index) {
    var item = document.createElement('li');
    item.className = 'toc-item';
    var num = ('0' + (index + 1)).slice(-2);

    item.innerHTML =
      '<span class="toc-item-zh"><span class="toc-item-num">' + num + '.</span>' + article.zh + '</span>' +
      '<span class="toc-item-en">' + article.en + '</span>';

    item.addEventListener('click', function() {
      sessionStorage.setItem('currentArticle', JSON.stringify(article));
      window.location.href = 'reader.html';
    });

    articleList.appendChild(item);
  });
})();

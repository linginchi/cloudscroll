// src/js/shelf.js
(function() {
  const bookCard = document.getElementById('book-card');
  if (!bookCard) return;

  bookCard.addEventListener('click', function() {
    window.location.href = 'toc.html';
  });
})();

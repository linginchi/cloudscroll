export const MAX_IMAGES_PER_ARTICLE = 5;

export const NOTICE_TEXT =
  '本 PDF 为精选图文版，便于分享阅读。完整配图与排版请在手机打开 cloudscroll.net 在线阅读。';

export function volumeCoverSrc(volume) {
  var n = parseInt(volume, 10) || 1;
  if (n < 1) n = 1;
  if (n > 4) n = 4;
  return 'images/cover_v' + n + '.jpg';
}

export function resolveBookImageUrl(src) {
  var s = String(src || '').trim();
  if (!s) return '';
  if (s.indexOf('book/') === 0 || s.indexOf('images/cover_') === 0) return s;
  if (s.indexOf('images/') === 0) return 'book/' + s;
  return 'book/images/' + s.replace(/^\/+/, '');
}

export function pickArticleImages(blocks) {
  var out = [];
  if (!blocks || !blocks.length) return out;
  for (var i = 0; i < blocks.length; i++) {
    var b = blocks[i];
    if (!b || b.type !== 'image' || !b.src) continue;
    out.push(resolveBookImageUrl(b.src));
    if (out.length >= MAX_IMAGES_PER_ARTICLE) break;
  }
  return out;
}

/** Spread images through paragraphs; leftover images append at end. */
export function interleaveTextAndImages(paragraphs, imageUrls) {
  var paras = paragraphs || [];
  var imgs = (imageUrls || []).slice();
  var items = [];
  if (!imgs.length) {
    for (var i = 0; i < paras.length; i++) {
      if (paras[i]) items.push({ kind: 'text', text: paras[i] });
    }
    return items;
  }
  var gap = Math.max(2, Math.ceil(paras.length / (imgs.length + 1)));
  var ii = 0;
  for (var p = 0; p < paras.length; p++) {
    if (paras[p]) items.push({ kind: 'text', text: paras[p] });
    if (ii < imgs.length && (p + 1) % gap === 0) {
      items.push({ kind: 'image', src: imgs[ii++] });
    }
  }
  while (ii < imgs.length) {
    items.push({ kind: 'image', src: imgs[ii++] });
  }
  return items;
}

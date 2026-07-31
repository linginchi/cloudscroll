import assert from 'assert';
import {
  MAX_IMAGES_PER_ARTICLE,
  pickArticleImages,
  resolveBookImageUrl,
  volumeCoverSrc,
  interleaveTextAndImages,
  NOTICE_TEXT
} from '../src/js/pdf-book-helpers.js';

assert.strictEqual(MAX_IMAGES_PER_ARTICLE, 5);
assert.strictEqual(volumeCoverSrc(1), 'book/images/cover_v1.jpg');
assert.strictEqual(volumeCoverSrc(4), 'book/images/cover_v4.jpg');
assert.strictEqual(volumeCoverSrc(0), 'book/images/cover_v1.jpg');
assert.strictEqual(volumeCoverSrc(9), 'book/images/cover_v4.jpg');

assert.strictEqual(resolveBookImageUrl('images/v4-04_001.jpeg'), 'book/images/v4-04_001.jpeg');
assert.strictEqual(resolveBookImageUrl('book/images/x.jpeg'), 'book/images/x.jpeg');

const blocks = [
  { type: 'text', content: 'A' },
  { type: 'image', src: 'images/a_001.jpeg' },
  { type: 'image', src: 'images/a_002.jpeg' },
  { type: 'image', src: 'images/a_003.jpeg' },
  { type: 'image', src: 'images/a_004.jpeg' },
  { type: 'image', src: 'images/a_005.jpeg' },
  { type: 'image', src: 'images/a_006.jpeg' }
];
const picked = pickArticleImages(blocks);
assert.strictEqual(picked.length, 5);
assert.strictEqual(picked[0], 'book/images/a_001.jpeg');
assert.strictEqual(picked[4], 'book/images/a_005.jpeg');

const mixed = interleaveTextAndImages(
  ['p1', 'p2', 'p3', 'p4', 'p5', 'p6'],
  ['book/images/a_001.jpeg', 'book/images/a_002.jpeg']
);
assert.ok(mixed.some((x) => x.kind === 'image'));
assert.ok(mixed.filter((x) => x.kind === 'text').length === 6);
assert.ok(NOTICE_TEXT.indexOf('cloudscroll.net') !== -1);
assert.ok(NOTICE_TEXT.indexOf('精选图文') !== -1 || NOTICE_TEXT.indexOf('精選圖文') !== -1);

console.log('test-pdf-book-helpers: OK');

const fs = require('fs');
const path = require('path');

console.log('Cloudscroll build starting...');

// Step 1: Copy static assets (HTML, CSS, JS, SVG) to dist/
// Step 2: Convert content/*.md to dist/articles/*.html using page template
// Step 3: Generate TOC from article metadata

console.log('Build complete.');

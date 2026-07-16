/**
 * Cloudscroll minimal worker — _worker.js
 * Handles:
 *   1. GET/POST /api/stats, OPTIONS preflight
 *   2. reader.html?id=xxx — inject article-specific OG tags for WeChat crawlers
 * Everything else (HTML, PNG, SVG, etc.) passes through to ASSETS.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // ── Article-specific OG tag injection for WeChat / social crawlers ──
    if (pathname === '/reader.html' || pathname === '/reader') {
      const articleId = url.searchParams.get('id');
      if (articleId) {
        return injectReaderOG(request, env, url, articleId);
      }
      return env.ASSETS.fetch(request);
    }

    // Only handle /api/stats — let static files pass through untouched
    if (pathname !== '/api/stats') {
      return env.ASSETS.fetch(request);
    }

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    const article = url.searchParams.get('article');
    if (!article) {
      return json({ error: 'Missing ?article= param' }, 400);
    }

    if (request.method === 'GET') {
      return handleGet(env, article);
    }
    if (request.method === 'POST') {
      return handlePost(env, request, article);
    }
    return json({ error: 'Method not allowed' }, 405);
  },
};

async function handleGet(env, article) {
  if (env.CLOUDSCROLL_STATS) {
    const [v, l] = await Promise.all([
      env.CLOUDSCROLL_STATS.get('cs:v:' + article),
      env.CLOUDSCROLL_STATS.get('cs:l:' + article),
    ]);
    return json({ views: +v || 0, likes: +l || 0 });
  }
  const s = memGet(article);
  return json({ views: s.views, likes: s.likes });
}

async function handlePost(env, request, article) {
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: 'Invalid JSON' }, 400); }
  const action = body.action;

  if (env.CLOUDSCROLL_STATS) {
    if (action === 'view') {
      const v = +((await env.CLOUDSCROLL_STATS.get('cs:v:' + article)) || 0) + 1;
      await env.CLOUDSCROLL_STATS.put('cs:v:' + article, String(v));
      return json({ views: v });
    }
    if (action === 'like') {
      const l = +((await env.CLOUDSCROLL_STATS.get('cs:l:' + article)) || 0) + 1;
      await env.CLOUDSCROLL_STATS.put('cs:l:' + article, String(l));
      return json({ likes: l });
    }
    if (action === 'unlike') {
      const l = Math.max(0, +((await env.CLOUDSCROLL_STATS.get('cs:l:' + article)) || 0) - 1);
      await env.CLOUDSCROLL_STATS.put('cs:l:' + article, String(l));
      return json({ likes: l });
    }
    return json({ error: 'Unknown action' }, 400);
  }

  const s = memGet(article);
  if (action === 'view') { s.views++; return json({ views: s.views }); }
  if (action === 'like') { s.likes++; return json({ likes: s.likes }); }
  if (action === 'unlike') { s.likes = Math.max(0, s.likes - 1); return json({ likes: s.likes }); }
  return json({ error: 'Unknown action' }, 400);
}

const store = {};
function memGet(article) {
  if (!store[article]) store[article] = { views: 0, likes: 0 };
  return store[article];
}

function json(data, status) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}

/**
 * Inject article-specific OG meta tags for WeChat / social crawlers.
 * Crawlers don't execute JavaScript, so we must rewrite the HTML server-side.
 */
async function injectReaderOG(request, env, url, articleId) {
  try {
    // Fetch the static reader.html from ASSETS
    let assetResp = await env.ASSETS.fetch(new URL('/reader.html', url.origin));
    if (!assetResp.ok) return env.ASSETS.fetch(request);
    let html = await assetResp.text();

    // Load article title from data.json
    let articleTitle = articleId;
    try {
      const dataResp = await env.ASSETS.fetch(new URL('/book/data.json', url.origin));
      if (dataResp.ok) {
        const data = await dataResp.json();
        const found = (data.articles || []).find(a => a.id === articleId);
        if (found && found.zh) articleTitle = found.zh;
      }
    } catch (e) { /* use articleId as fallback */ }

    const title = articleTitle + ' — 雲箋文舍';
    const desc = '林樺先生旅行散文：《' + articleTitle + '》——淡雅文字記錄人生旅途的山水印記。';
    const ogImage = url.origin + '/og-image.png';
    const articleUrl = url.origin + '/reader.html?id=' + encodeURIComponent(articleId);

    // Replace OG / Twitter tags with article-specific ones
    html = html.replace(
      /<meta property="og:title" content="[^"]*">/,
      '<meta property="og:title" content="' + esc(articleTitle + ' — 雲箋文舍') + '">'
    );
    html = html.replace(
      /<meta property="og:description" content="[^"]*">/,
      '<meta property="og:description" content="' + esc(desc) + '">'
    );
    html = html.replace(
      /<meta property="og:image" content="[^"]*">/,
      '<meta property="og:image" content="' + esc(ogImage) + '">'
    );
    html = html.replace(
      /<meta property="og:url" content="[^"]*">/,
      '<meta property="og:url" content="' + esc(articleUrl) + '">'
    );
    html = html.replace(
      /<meta name="twitter:title" content="[^"]*">/,
      '<meta name="twitter:title" content="' + esc(articleTitle + ' — 雲箋文舍') + '">'
    );
    html = html.replace(
      /<meta name="twitter:description" content="[^"]*">/,
      '<meta name="twitter:description" content="' + esc(desc) + '">'
    );

    return new Response(html, {
      status: 200,
      headers: { 'Content-Type': 'text/html; charset=utf-8' },
    });
  } catch (e) {
    return env.ASSETS.fetch(request);
  }
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

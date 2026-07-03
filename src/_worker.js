/**
 * Cloudscroll stats endpoint — _worker.js
 * Supports GET (fetch stats) and POST (view/like/unlike).
 * Uses Cloudflare KV if bound, falls back to in-memory.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Only handle /api/stats
    if (url.pathname !== '/api/stats') {
      return env.ASSETS.fetch(request);
    }

    const article = url.searchParams.get('article');
    if (!article) {
      return json({ error: 'Missing ?article= param' }, 400);
    }

    // Try KV, fall back to memory
    const stats = env.CLOUDSCROLL_STATS ? await kvStats(env.CLOUDSCROLL_STATS, request, article)
                                        : memStats(request, article);

    return stats;
  },
};

/** Return JSON response helper */
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}

/** KV-backed stats */
async function kvStats(kv, request, article) {
  const prefix = 'cs:';
  try {
    if (request.method === 'GET') {
      const [v, l] = await Promise.all([
        kv.get(prefix + 'v:' + article),
        kv.get(prefix + 'l:' + article),
      ]);
      return json({ views: +v || 0, likes: +l || 0 });
    }
    if (request.method === 'POST') {
      const body = await request.json();
      const a = body.action;
      if (a === 'view') {
        const v = +((await kv.get(prefix + 'v:' + article)) || 0) + 1;
        await kv.put(prefix + 'v:' + article, String(v));
        return json({ views: v });
      }
      if (a === 'like') {
        const l = +((await kv.get(prefix + 'l:' + article)) || 0) + 1;
        await kv.put(prefix + 'l:' + article, String(l));
        return json({ likes: l });
      }
      if (a === 'unlike') {
        const l = Math.max(0, +((await kv.get(prefix + 'l:' + article)) || 0) - 1);
        await kv.put(prefix + 'l:' + article, String(l));
        return json({ likes: l });
      }
      return json({ error: 'Unknown action' }, 400);
    }
    return json({ error: 'Method not allowed' }, 405);
  } catch (e) {
    return json({ error: e.message }, 500);
  }
}

/** In-memory fallback (resets on cold start) */
const store = {};
function memStats(request, article) {
  if (!store[article]) store[article] = { views: 0, likes: 0 };
  const s = store[article];
  if (request.method === 'GET') return json({ views: s.views, likes: s.likes });
  if (request.method === 'POST') {
    return request.json().then(body => {
      if (body.action === 'view') { s.views++; return json({ views: s.views }); }
      if (body.action === 'like') { s.likes++; return json({ likes: s.likes }); }
      if (body.action === 'unlike') { s.likes = Math.max(0, s.likes - 1); return json({ likes: s.likes }); }
      return json({ error: 'Unknown action' }, 400);
    });
  }
  return json({ error: 'Method not allowed' }, 405);
}

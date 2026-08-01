# AGENTS.md — Cloudscroll / 雲箋文舍

## Project overview

Static literary site for 林樺's works, deployed to Cloudflare Pages (`cloudscroll.net`).

- Source UI: `src/`
- Book JSON content: `src/yunxin/`（《雲心文集》）, and `dist/book/` after build（《我的人生旅行》）
- Original Word sources live in `book/` (gitignored; available on the author's local machine only)

## Local / production deploy (author machine)

Cloudflare Pages Git auto-build fails (missing Python deps on CI). Always:

```bash
# 先补齐本地缺失媒体（线上已有则下载；本地已有绝不覆盖）
node scripts/sync-prod-assets.js
npm run build
# 部署前再把线上已有、仓库未收录的媒体补进 dist（仍不覆盖本地已有文件）
node scripts/sync-prod-assets.js --dest dist/images
npx wrangler pages deploy dist --project-name cloudscroll --branch main --commit-dirty=true
```

PowerShell: use `; if ($LASTEXITCODE -eq 0) { ... }` instead of `&&`.

**重要：`wrangler pages deploy` 会用整包 `dist` 替换线上站点。**  
部分图／视频只存在于生产、未进 git。若用残缺 `dist` 直接部署，会删掉线上已有媒体。  
部署前务必跑 `sync-prod-assets.js`；该脚本**只补缺失、从不覆盖**已有文件。云端代理无完整媒体时**禁止**对生产执行 wrangler deploy。

## Cursor Cloud specific instructions

Cloud agents clone this GitHub repo into a VM. Use them from:

- Phone: [Cursor iOS](https://cursor.com/docs/cloud-agent/mobile) or Android via [cursor.com/agents](https://cursor.com/agents) (Install App / PWA)
- Desktop: agent input → select **Cloud**
- Web: [cursor.com/agents](https://cursor.com/agents)

### What works in cloud

- Edit `src/**` HTML / CSS / JS
- Edit `src/yunxin/*.json` article text and `src/yunxin/data.json` TOC
- Run `npm install` and a partial/full `npm run build` (see below)
- Commit and open PRs / push to GitHub (if the Cursor GitHub account has write access)

### What does NOT work in cloud without extra setup

- `book/` Word sources are **not** in git. Do not expect `python scripts/extract-book.py` or `extract-yunxin.py` to re-extract from docx unless the author has uploaded sources another way.
- Production wrangler deploy needs Cloudflare credentials. Prefer merging to `main` and letting the author run local wrangler, unless `CLOUDFLARE_API_TOKEN` (and account access) are configured in Cursor Secrets.

### Build behavior without `book/`

If `book/` is missing, `npm run build` skips Word extraction and continues with already-committed assets under `src/` (including `src/yunxin/`). Prefer editing JSON/HTML/CSS directly in cloud.

### Repo for agents

GitHub: `https://github.com/linginchi/cloudscroll`  
Default branch: `main`

Before starting a cloud agent from a phone, ensure Cursor Settings → Integrations has GitHub connected to an account that can access this repository.

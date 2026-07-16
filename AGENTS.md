# AGENTS.md — Cloudscroll / 雲箋文舍

## Project overview

Static literary site for 林樺's works, deployed to Cloudflare Pages (`cloudscroll.net`).

- Source UI: `src/`
- Book JSON content: `src/yunxin/`（《雲心文集》）, and `dist/book/` after build（《我的人生旅行》）
- Original Word sources live in `book/` (gitignored; available on the author's local machine only)

## Local / production deploy (author machine)

Cloudflare Pages Git auto-build fails (missing Python deps on CI). Always:

```bash
npm run build
npx wrangler pages deploy dist --project-name cloudscroll --branch main --commit-dirty=true
```

PowerShell: use `; if ($LASTEXITCODE -eq 0) { ... }` instead of `&&`.

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

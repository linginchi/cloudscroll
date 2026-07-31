# Handoff：PDF 分享功能 → 本地 Cursor IDE 接手部署

> 写给本地 Cursor IDE / 本机代理。云端代理已完成代码并合并到 `main`，**尚未 wrangler 上线**（云端无 Cloudflare 凭证）。

## 当前状态（截至 2026-07-31）

| 项 | 状态 |
|---|---|
| 代码仓库 | `https://github.com/linginchi/cloudscroll` |
| 分支 | 已合并进 **`main`**（commit `9657615`） |
| PR | https://github.com/linginchi/cloudscroll/pull/1 （MERGED） |
| 生产站 `cloudscroll.net` | **未包含本次 iframe 版面修复**；需本机 `wrangler pages deploy` |
| 云端 `CLOUDFLARE_API_TOKEN` | 未配置，无法代部署 |

## 你要做的事（本机唯一阻塞项）

在作者机器上（有 `book/` Word 源、已登录 wrangler）执行：

```powershell
cd C:\cloudscroll
git pull origin main
npm run build
; if ($LASTEXITCODE -eq 0) {
  npx wrangler pages deploy dist --project-name cloudscroll --branch main --commit-dirty=true
}
```

**注意：**

- 不要用 `&&`（PowerShell 行为不同）；用 `; if ($LASTEXITCODE -eq 0)`。
- Cloudflare Pages 的 Git 自动构建会因缺 Python 依赖失败，**必须本地 build + wrangler**。
- 云端 clone **没有** `book/`（gitignored）。本机 build 会重新提取旅行文集到 `dist/book/`；云端若强行 deploy 会缺旅行卷正文。

部署成功后自测：

1. https://cloudscroll.net/shelf.html → 任一书下方「分享／PDF」→「下載／分享 PDF」
2. 打开 PDF：封面标题完整、无左侧裁切、无右侧竖条空白
3. 任意文章页分享 →「下載／分享 PDF」仍可用

## 本次已交付功能（代码已在 main）

### 1. 文章级 PDF
- 页面：`reader.html`、`yunxin-article.html`、`yunxin-preface.html`
- 分享弹层增加「下載／分享 PDF」
- 支持系统分享文件；否则下载到本地

### 2. 整书级 PDF
- 书架 `shelf.html` 每本书下方「分享／PDF」
- 《我的人生旅行》四辑各自一份；《雲心文集》整本一份
- 内容：封面页 + 目录 + 全文（文字版，旅行辑不含大量配图）

### 3. 版面错位修复（关键）
- **原因**：PDF 节点挂在主文档，受 `html/body { overflow: clip }`、全屏 `.page` 等影响，`html2canvas` 裁切/偏移
- **修复**：在干净 **iframe** 内渲染；内容宽 700px，匹配 A4；`html2canvas` 的 `width`/`windowWidth` 对齐

## 关键文件

| 路径 | 说明 |
|---|---|
| `src/js/article-pdf.js` | PDF 导出核心（文章 / 整书、iframe 隔离） |
| `src/js/html2pdf.bundle.min.js` | html2pdf 依赖（已 vendored） |
| `src/js/shelf.js` | 书架分享弹层 + 整书 PDF |
| `src/js/reader.js` / `src/js/yunxin.js` | 文章分享 + PDF |
| `src/css/shelf.css` | `.book-slot` / `.book-share-btn` |
| `src/shelf.html` 等 | 分享弹层 UI + script 引用 `?v=20260731f` |

## 已知限制 / 勿踩坑

1. **整书 PDF 生成较慢**（分段渲染），UI 有进度遮罩；第二辑文章多，请等进度走完。
2. **微信内**通常无法一键把 PDF 塞进会话：下载后从文件管理器转发；非微信手机可走系统分享。
3. 旅行卷 PDF 为**文字版**（刻意跳过大量图片，避免手机 OOM）。
4. 不要用 `position:fixed/absolute` 作为 html2canvas 截图根节点（高度会变成 0 → 空白 PDF）；当前用 iframe + 正常文档流。
5. 站点全局 `*` reset / `overflow:clip` 不能再套在 PDF 容器上；保持 iframe 隔离。

## 建议本地 IDE 开场任务

```
请按 docs/HANDOFF-pdf-deploy.md 完成本机部署：
1. git pull origin main
2. npm run build
3. wrangler pages deploy dist --project-name cloudscroll --branch main --commit-dirty=true
4. 打开 shelf.html 验证整书 PDF 版面不再错位
```

## 可选后续

- 在 Cursor Cloud Environment Secrets 添加 `CLOUDFLARE_API_TOKEN`（Pages Edit），以后云端可代部署。
- 若需「带图的旅行卷 PDF」，需另做服务端/预生成方案，勿在手机端一次 html2canvas 千张图。

## 相关链接

- 生产站：https://cloudscroll.net  
- 仓库：https://github.com/linginchi/cloudscroll  
- 已合并 PR：https://github.com/linginchi/cloudscroll/pull/1  
- 云端说明：`AGENTS.md`

# 實體書翻頁閱讀體驗 — 改造記錄

## 時間
2026-07-04 ～ 2026-07-05

## 目標
將 reader.html 的滾動閱讀模式改造為 3D 紙張卷曲翻頁效果（turn.js），支援手機/桌面設備。

## 技術方案
- **翻頁引擎**：turn.js v3（透過 CDN 載入 jQuery + turn.js）
- **分頁引擎**：自訂 runtime 分頁演算法，將 article blocks 依頁面高度切分
- **每頁結構**：body（正文）+ footer（標題左 + 頁碼右），取消 header 節省空間
- **雙頁模式**：桌面 >=768px 雙頁跨頁展示
- **手勢**：僅右側拖拽向前翻頁，左側翻頁角 CSS 隱藏
- **縮放**：雙指捏合縮放 (1x~3x)，雙擊切換 2x/1x

## 失敗原因
- 在 iPad、iPhone、Windows desktop 三部設備渲染不一致
- turn.js 與現有頁面布局（flex column、sidebar、fixed page container）衝突
- turn.js CDN v3 版本老舊，現代手機觸控事件處理不佳
- 自訂分頁引擎與 turn.js 的頁面模型整合複雜度高
- 所有設備均無法正常互動操作

## 涉及檔案
- src/reader.html — DOM 結構重寫
- src/js/reader.js — 核心邏輯：分頁引擎 + turn.js + 手勢 + 縮放
- src/css/reader.css — 翻頁書樣式

## 後續建議
- 考慮使用更現代的純 CSS/CSS Houdini 翻頁效果庫
- 考慮使用 Canvas/WebGL 自行實現翻頁（效能更好，手勢控制更靈活）
- 先在小範圍 demo 頁測試，確認跨設備一致性後再整合到正式站點
- 或考慮使用成熟的電子書閱讀器框架（如 Epub.js）

## 回退方式
```bash
git checkout HEAD -- src/reader.html src/js/reader.js src/css/reader.css
```

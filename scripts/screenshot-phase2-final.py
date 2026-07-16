"""Comprehensive Phase 2 verification screenshots"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # 1. 首頁手機
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/index.html')
        await page.wait_for_timeout(4000)
        await page.screenshot(path='screenshots/phase2-final-home-mobile.png', full_page=True)
        print('1. 首頁 — 手機')

        # 2. 書架手機
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/phase2-final-shelf-mobile.png', full_page=True)
        print('2. 書架 — 手機')

        # 3. 書架桌面
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/phase2-final-shelf-desktop.png', full_page=True)
        print('3. 書架 — 桌面')

        # 4. V1 卷首手機
        await page.set_viewport_size({'width': 420, 'height': 900})
        await page.goto(f'{BASE}/volume.html?volume=1')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/phase2-final-volume-v1-mobile.png', full_page=True)
        print('4. 第一輯封面 — 手機')

        # 5. V2 卷首手機
        await page.goto(f'{BASE}/volume.html?volume=2')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/phase2-final-volume-v2-mobile.png', full_page=True)
        print('5. 第二輯封面 — 手機')

        # 6. V3 卷首手機
        await page.goto(f'{BASE}/volume.html?volume=3')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/phase2-final-volume-v3-mobile.png', full_page=True)
        print('6. 第三輯封面 — 手機')

        await browser.close()
        print('\n=== Phase 2 截圖完成 ===')

asyncio.run(main())

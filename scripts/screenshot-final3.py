"""Three screenshots: home-mobile, shelf-desktop (1440), shelf-mobile"""
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
        await page.screenshot(path='screenshots/home-mobile-final.png', full_page=True)
        print('1. 首頁手機')

        # 2. 書架桌面 1440x900
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/shelf-desktop-final.png', full_page=False)
        print('2. 書架桌面')

        # 3. 書架手機
        await page.set_viewport_size({'width': 420, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/shelf-mobile-final.png', full_page=True)
        print('3. 書架手機')

        await browser.close()
        print('done')
asyncio.run(main())

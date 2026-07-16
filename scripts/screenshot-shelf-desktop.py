"""Screenshot shelf at 1440x900"""
import asyncio
from playwright.async_api import async_playwright
BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # 1440x900 — full above-the-fold
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/shelf-1440.png', full_page=False)
        print('1440x900 saved')

        # Also check 1280x900
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/shelf-1280.png', full_page=False)
        print('1280x900 saved')

        await browser.close()
asyncio.run(main())

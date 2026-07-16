"""Quick screenshot: shelf page with mini avatar"""
import asyncio
from playwright.async_api import async_playwright
BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/shelf-avatar-mobile.png', full_page=True)
        print('shelf-avatar saved')
        await browser.close()
asyncio.run(main())

"""Screenshot homepage for readability verification"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/index.html')
        await page.wait_for_timeout(4000)
        await page.screenshot(path='screenshots/home-mobile-v2.png', full_page=True)
        print('home mobile saved')

        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/index.html')
        await page.wait_for_timeout(4000)
        await page.screenshot(path='screenshots/home-desktop-v2.png', full_page=True)
        print('home desktop saved')

        await browser.close()
        print('done')

asyncio.run(main())

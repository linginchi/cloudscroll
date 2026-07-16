"""Screenshot shelf page for 案頭三卷 verification"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Mobile
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/shelf-v3-mobile.png', full_page=True)
        print('1. shelf mobile saved')

        # Desktop
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='screenshots/shelf-v3-desktop.png', full_page=True)
        print('2. shelf desktop saved')

        await browser.close()
        print('\n=== Done ===')

asyncio.run(main())

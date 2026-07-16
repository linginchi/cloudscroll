"""Screenshot shelf + volume pages for Phase 2 verification"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # --- Mobile: shelf page ---
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/phase2-shelf-mobile-v2.png', full_page=True)
        print('1. shelf mobile saved')

        # --- Desktop: shelf page ---
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/phase2-shelf-desktop-v2.png', full_page=True)
        print('2. shelf desktop saved')

        # --- Mobile: V1 volume page ---
        await page.set_viewport_size({'width': 420, 'height': 900})
        await page.goto(f'{BASE}/volume.html?vol=1')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/phase2-volume-v1-mobile-v2.png', full_page=True)
        print('3. volume V1 mobile saved')

        # --- Mobile: V2 volume page ---
        await page.goto(f'{BASE}/volume.html?vol=2')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/phase2-volume-v2-mobile-v2.png', full_page=True)
        print('4. volume V2 mobile saved')

        # --- Mobile: V3 volume page ---
        await page.goto(f'{BASE}/volume.html?vol=3')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/phase2-volume-v3-mobile-v2.png', full_page=True)
        print('5. volume V3 mobile saved')

        # --- Desktop: V2 volume page ---
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/volume.html?vol=2')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshots/phase2-volume-v2-desktop-v2.png', full_page=True)
        print('6. volume V2 desktop saved')

        await browser.close()
        print('\n=== All Phase 2 screenshots saved ===')

asyncio.run(main())

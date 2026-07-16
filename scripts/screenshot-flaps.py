"""Screenshot flaps (author intro) for avatar verification"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Flaps section on V1 volume page (scroll down past cover)
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/volume.html?volume=1')
        await page.wait_for_timeout(2000)

        # Click "翻開書頁" to scroll to flaps
        btn = await page.query_selector('#cover-open-btn')
        if btn:
            await btn.click()
            await page.wait_for_timeout(1500)

        # Scroll to show flaps section fully
        await page.evaluate('document.getElementById("volume-flaps").scrollIntoView()')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='screenshots/flaps-avatar-mobile.png', full_page=False)
        print('1. flaps avatar mobile saved')

        # Desktop view
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(f'{BASE}/volume.html?volume=1')
        await page.wait_for_timeout(2000)
        btn = await page.query_selector('#cover-open-btn')
        if btn:
            await btn.click()
            await page.wait_for_timeout(1500)
        await page.evaluate('document.getElementById("volume-flaps").scrollIntoView()')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='screenshots/flaps-avatar-desktop.png', full_page=False)
        print('2. flaps avatar desktop saved')

        await browser.close()
        print('done')

asyncio.run(main())

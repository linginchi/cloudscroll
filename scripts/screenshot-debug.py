"""Debug screenshot with full_page=True and element checks"""
import asyncio
from playwright.async_api import async_playwright
BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto(f'{BASE}/shelf.html')
        await page.wait_for_timeout(4000)

        # Check if book cards exist
        count = await page.evaluate('document.querySelectorAll(".book-card").length')
        print(f'Book cards found: {count}')

        # Check heights
        header_h = await page.evaluate('document.querySelector(".shelf-header")?.offsetHeight || 0')
        books_h = await page.evaluate('document.querySelector(".shelf-books")?.offsetHeight || 0')
        inner_h = await page.evaluate('document.querySelector(".shelf-page-inner")?.scrollHeight || 0')
        page_h = await page.evaluate('document.querySelector("#shelf-page")?.scrollHeight || 0')
        print(f'Header height: {header_h}px')
        print(f'Books height: {books_h}px')
        print(f'Inner scrollHeight: {inner_h}px')
        print(f'Page scrollHeight: {page_h}px')

        # Check overflow
        shelf_overflow = await page.evaluate(
            'getComputedStyle(document.querySelector("#shelf-page")).overflow'
        )
        print(f'#shelf-page overflow: {shelf_overflow}')

        # Full page screenshot
        await page.screenshot(path='screenshots/shelf-debug.png', full_page=True)
        print('shelf-debug.png saved (full_page=True)')

        await browser.close()
        print('done')
asyncio.run(main())

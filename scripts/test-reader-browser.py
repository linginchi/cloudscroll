# -*- coding: utf-8 -*-
"""Browser-level check of the reader page"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'https://0cc2d28b.cloudscroll.pages.dev'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 420, 'height': 800})

        # 1) Go to toc, see if articles are listed
        await page.goto(f'{BASE}/toc.html')
        await page.wait_for_timeout(3000)
        toc_items = await page.query_selector_all('.toc-item')
        print(f'TOC items found: {len(toc_items)}')

        # 2) Click first article
        if toc_items:
            await toc_items[0].click()
            await page.wait_for_timeout(5000)

            # 3) Check page content
            page_text = await page.query_selector('#page-text')
            if page_text:
                html = await page_text.inner_html()
                text = await page_text.inner_text()
                print(f'Page text inner HTML length: {len(html)}')
                print(f'Page text first 200 chars: {text[:200]}')

            # 4) Check for chapter cover
            cover = await page.query_selector('.chapter-cover')
            if cover:
                print('Chapter cover found!')
                cover_text = await cover.inner_text()
                print(f'Cover text: {cover_text.strip()[:100]}')
            else:
                print('No chapter cover found')

            # 5) Screenshot
            await page.screenshot(path='screenshot-fix-verify.png')
            print('Screenshot saved')

        await browser.close()

asyncio.run(main())

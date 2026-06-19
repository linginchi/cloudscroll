# -*- coding: utf-8 -*-
"""Test scroll reader locally"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8081'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 420, 'height': 800})

        # Go to toc and click first article
        await page.goto(f'{BASE}/toc.html')
        await page.wait_for_timeout(2000)
        items = await page.query_selector_all('.toc-item')
        if items:
            await items[0].click()
            await page.wait_for_timeout(3000)

            # Check content rendered
            inner = await page.query_selector('#reader-inner')
            if inner:
                html = await inner.inner_html()
                text = await inner.inner_text()
                print(f'Reader content length: {len(html)}')
                print(f'First 300 chars: {text[:300]}')

                # Check for chapter cover
                cover = await inner.query_selector('.chapter-cover')
                if cover:
                    print('Chapter cover: FOUND')
                else:
                    print('Chapter cover: NOT FOUND')

                # Check for paragraphs
                ps = await inner.query_selector_all('p')
                print(f'Paragraphs: {len(ps)}')

                # Check scroll works
                scroll_top = await page.evaluate('document.getElementById("reader-scroll").scrollTop')
                print(f'Initial scrollTop: {scroll_top}')

            # Screenshot
            await page.screenshot(path='screenshot-scroll-reader.png')
            print('Screenshot saved')

        await browser.close()

asyncio.run(main())

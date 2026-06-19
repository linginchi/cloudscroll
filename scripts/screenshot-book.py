# -*- coding: utf-8 -*-
"""Screenshot the book reader with Playwright"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8081'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 420, 'height': 800})

        # 1) 目錄頁
        await page.goto(f'{BASE}/toc.html')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshot-toc.png', full_page=True)
        print('1. toc.html screenshot saved')

        # 2) 點擊序文（目錄第一個 .toc-item，應該是 preface）
        toc_items = await page.query_selector_all('.toc-item')
        if toc_items:
            await toc_items[0].click()
            await page.wait_for_timeout(3000)

            # 3) 檢查是否有章節扉頁
            cover_el = await page.query_selector('.chapter-cover')
            if cover_el:
                await page.screenshot(path='screenshot-preface-cover.png')
                print('2. Preface chapter cover screenshot saved')
            else:
                await page.screenshot(path='screenshot-preface.png')
                print('2. Preface screenshot saved')

            # 4) 翻頁到正片（點擊右半部分觸發翻頁）
            for i in range(3):
                box = await page.query_selector('.book-container')
                if box:
                    bbox = await box.bounding_box()
                    if bbox:
                        await page.mouse.click(bbox['x'] + bbox['width'] * 0.75, bbox['y'] + bbox['height'] * 0.5)
                        await page.wait_for_timeout(700)

            await page.wait_for_timeout(500)
            await page.screenshot(path='screenshot-content.png')
            print('3. Content page screenshot saved')

            # 5) 回到目錄選菲律賓篇（有圖）
            await page.goto(f'{BASE}/toc.html')
            await page.wait_for_timeout(2000)

            all_items = await page.query_selector_all('.toc-item')
            for item in all_items:
                text = await item.text_content()
                if '菲' in text:
                    await item.click()
                    await page.wait_for_timeout(3000)
                    break

            # 翻幾頁找圖
            for i in range(5):
                box = await page.query_selector('.book-container')
                if box:
                    bbox = await box.bounding_box()
                    if bbox:
                        await page.mouse.click(bbox['x'] + bbox['width'] * 0.75, bbox['y'] + bbox['height'] * 0.5)
                        await page.wait_for_timeout(700)

            await page.screenshot(path='screenshot-image-page.png')
            print('4. Image page screenshot saved')

        await browser.close()
        print('\n=== All screenshots saved ===')

asyncio.run(main())

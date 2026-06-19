# -*- coding: utf-8 -*-
"""Full EN/ZH screenshot verification"""
import asyncio
from playwright.async_api import async_playwright

BASE = 'http://localhost:8081'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 420, 'height': 800})

        # 1) TOC in ZH
        await page.goto(f'{BASE}/toc.html')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshot-toc-zh.png')
        print('1. TOC ZH saved')

        # 2) TOC in EN
        en_btn = await page.query_selector('#toc-lang-toggle .lang-option[data-lang="en"]')
        if en_btn:
            await en_btn.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path='screenshot-toc-en.png')
            print('2. TOC EN saved')

        # 3) Click first article (preface) - in EN mode
        toc_items = await page.query_selector_all('.toc-item')
        if toc_items:
            await toc_items[0].click()
            await page.wait_for_timeout(3000)

            # 4) Preface in EN
            await page.screenshot(path='screenshot-preface-en-v2.png')
            print('3. Preface EN saved')

            # 5) Flip a page to see EN content
            box = await page.query_selector('.book-container')
            if box:
                bbox = await box.bounding_box()
                if bbox:
                    await page.mouse.click(bbox['x'] + bbox['width'] * 0.75, bbox['y'] + bbox['height'] * 0.5)
                    await page.wait_for_timeout(700)

            await page.screenshot(path='screenshot-content-en-v2.png')
            print('4. Content EN saved')

        await browser.close()
        print('\n=== Done ===')

asyncio.run(main())

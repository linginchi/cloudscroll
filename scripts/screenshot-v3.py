"""Robust v3 screenshots with scrollTop=0 and content-ready checks"""
import asyncio
from playwright.async_api import async_playwright
BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # ── 1. 首頁手機 ──
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto(f'{BASE}/index.html', wait_until='networkidle')
        await page.wait_for_timeout(3000)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.screenshot(path='screenshots/home-mobile-v3.png', full_page=True)
        title = await page.title()
        st = await page.evaluate('window.scrollY')
        print(f'1. home-mobile-v3  title="{title}"  scrollTop={st}')

        # ── 2. 書架桌面 1440×900 ──
        page2 = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page2.goto(f'{BASE}/shelf.html', wait_until='networkidle')
        await page2.wait_for_timeout(5000)

        # Ensure scrollTop = 0
        await page2.evaluate('window.scrollTo(0, 0)')

        # Wait for books to be rendered
        try:
            await page2.wait_for_function(
                'document.querySelectorAll(".book-card").length >= 3',
                timeout=10000
            )
        except:
            pass

        # Check book card presence and visibility
        cnt = await page2.evaluate('document.querySelectorAll(".book-card").length')
        # Check first card's bounding rect
        rect = await page2.evaluate("""() => {
            const c = document.querySelector('.book-card');
            if (!c) return null;
            const r = c.getBoundingClientRect();
            return {top: r.top, bottom: r.bottom, left: r.left, right: r.right, width: r.width, height: r.height};
        }""")
        sc = await page2.evaluate('window.scrollY')
        title2 = await page2.title()
        page_url = page2.url
        print(f'2. shelf-desktop-v3  title="{title2}"  url="{page_url}"  cards={cnt}  scrollTop={sc}  firstCard={rect}')

        # Additional: check if child divs have expected structure
        children = await page2.evaluate("""() => {
            const cards = document.querySelectorAll('.book-card');
            if (cards.length === 0) return [];
            return Array.from(cards).map((c, i) => ({
                index: i,
                childCount: c.children.length,
                hasCoverBg: c.querySelector('.book-cover') ? window.getComputedStyle(c.querySelector('.book-cover')).backgroundImage !== 'none' : false,
                coverW: c.querySelector('.book-cover')?.offsetWidth || 0,
                coverH: c.querySelector('.book-cover')?.offsetHeight || 0
            }));
        }""")
        print(f'   card-details: {children}')

        await page2.screenshot(path='screenshots/shelf-desktop-v3.png', full_page=True)
        print('   screenshot saved')
        print('done')

        await browser.close()
asyncio.run(main())

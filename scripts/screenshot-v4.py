"""shelf-desktop-v4.png — verify 3 books visible at scrollTop=0, 1440x900"""
import asyncio
from playwright.async_api import async_playwright
BASE = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--disable-cache', '--incognito'])
        ctx = await browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1, no_viewport=False)

        page = await ctx.new_page()
        # add cache-busting timestamp
        import time
        url = f'{BASE}/shelf.html?t={int(time.time())}'
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_timeout(6000)

        # scroll to absolute top
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(500)

        # wait for books present
        await page.wait_for_function('document.querySelectorAll(".book-card").length >= 3', timeout=15000)

        cnt = await page.evaluate('document.querySelectorAll(".book-card").length')
        st  = await page.evaluate('window.scrollY')
        url = page.url
        title = await page.title()

        print(f'url={url}  title="{title}"  cards={cnt}  scrollTop={st}')

        if cnt < 3:
            print('ERROR: less than 3 book cards found!')
            await browser.close()
            return

        # check first card visibility in viewport
        vis = await page.evaluate("""() => {
            const c = document.querySelector('.book-card');
            if (!c) return 'no-card';
            const r = c.getBoundingClientRect();
            const vpW = window.innerWidth;
            const vpH = window.innerHeight;
            if (r.bottom <= 0 || r.top >= vpH) return 'off-screen';
            return `in-view (top=${Math.round(r.top)} bottom=${Math.round(r.bottom)} width=${Math.round(r.width)} height=${Math.round(r.height)})`;
        }""")
        print(f'firstCard: {vis}')

        await page.screenshot(path='screenshots/shelf-desktop-v4.png', full_page=True)
        print('shelf-desktop-v4.png saved')
        await browser.close()
        print('done')

asyncio.run(main())

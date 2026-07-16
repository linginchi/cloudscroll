const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  let errors = [];

  // Test 1: Mobile Shelf — no "先讀作者自序"
  console.log('\n=== Test 1: Mobile Shelf ===');
  {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
    const page = await ctx.newPage();
    await page.goto('https://cloudscroll.net/shelf.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    const prefaceEntry = await page.$('#preface-entry');
    if (prefaceEntry) {
      errors.push('Mobile shelf still has #preface-entry');
      console.log('  FAIL: #preface-entry found');
    } else {
      console.log('  PASS: #preface-entry removed');
    }
    await ctx.close();
  }

  // Test 2: Mobile — click book → volume page
  console.log('\n=== Test 2: Mobile Book Click ===');
  {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
    const page = await ctx.newPage();
    await page.goto('https://cloudscroll.net/shelf.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    const firstBook = await page.$('.book-card.v1');
    if (firstBook) {
      await firstBook.click();
      await page.waitForTimeout(2000);
      console.log('  INFO: URL = ' + page.url());
      if (page.url().includes('volume')) {
        console.log('  PASS: navigated to volume.html');
      } else {
        errors.push('Book click did not navigate to volume.html');
        console.log('  FAIL: wrong URL');
      }
    } else {
      errors.push('No .book-card.v1 found');
      console.log('  FAIL: no book card');
    }
    await ctx.close();
  }

  // Test 3: Mobile — avatar and scroll
  console.log('\n=== Test 3: Mobile Avatar + Scroll ===');
  {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
    const page = await ctx.newPage();
    await page.goto('https://cloudscroll.net/volume.html?volume=1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);

    // Avatar
    const avatarImg = await page.$('.flaps-avatar-img');
    if (avatarImg) {
      const w = await avatarImg.evaluate(el => el.naturalWidth);
      console.log('  ' + (w > 0 ? 'PASS' : 'FAIL') + ': avatar naturalWidth=' + w);
      if (w === 0) errors.push('Mobile avatar not loaded');
    } else {
      errors.push('Mobile .flaps-avatar-img not found');
      console.log('  FAIL: no .flaps-avatar-img');
    }

    // Scroll
    const btn = await page.$('#cover-open-btn');
    if (btn) {
      const sc = '.volume-page-inner';
      const before = await page.$eval(sc, el => el.scrollTop);
      console.log('  INFO: scrollTop before=' + before);
      await btn.click();
      await page.waitForTimeout(3000);
      const after = await page.$eval(sc, el => el.scrollTop);
      console.log('  INFO: scrollTop after=' + after);
      if (after > 100) {
        console.log('  PASS: scrolled');
      } else {
        errors.push('Mobile scroll did not work (scrollTop=' + after + ')');
        console.log('  FAIL: no scroll');
      }
    }
    await ctx.close();
  }

  // Test 4: Desktop — avatar and scroll
  console.log('\n=== Test 4: Desktop Avatar + Scroll ===');
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto('https://cloudscroll.net/volume.html?volume=1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);

    const avatarImg = await page.$('.flaps-avatar-img');
    if (avatarImg) {
      const w = await avatarImg.evaluate(el => el.naturalWidth);
      console.log('  ' + (w > 0 ? 'PASS' : 'FAIL') + ': desktop avatar naturalWidth=' + w);
      if (w === 0) errors.push('Desktop avatar not loaded');
    }

    const btn = await page.$('#cover-open-btn');
    if (btn) {
      const sc = '.desktop-main';
      const before = await page.$eval(sc, el => el.scrollTop);
      console.log('  INFO: desktop scrollTop before=' + before);
      await btn.click();
      await page.waitForTimeout(3000);
      const after = await page.$eval(sc, el => el.scrollTop);
      console.log('  INFO: desktop scrollTop after=' + after);
      if (after > 100) {
        console.log('  PASS: desktop scrolled');
      } else {
        errors.push('Desktop scroll did not work (scrollTop=' + after + ')');
        console.log('  FAIL: no desktop scroll');
      }
    }
    await ctx.close();
  }

  await browser.close();

  console.log('\n========================================');
  if (errors.length === 0) {
    console.log('PASS: All tests passed');
  } else {
    console.log('FAIL: ' + errors.length + ' test(s) failed:');
    errors.forEach(e => console.log('  - ' + e));
  }
  console.log('========================================\n');
  process.exit(errors.length > 0 ? 1 : 0);
})();

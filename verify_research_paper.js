const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const filePath = 'file://' + path.resolve('tgi_research_paper.html');
  await page.goto(filePath);
  await page.setViewportSize({ width: 1280, height: 2000 });
  await page.screenshot({ path: 'research_paper_v8.png', fullPage: true });
  await browser.close();
  console.log('Screenshot saved to research_paper_v8.png');
})();

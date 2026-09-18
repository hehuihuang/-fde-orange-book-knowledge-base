// QA only. PLAYWRIGHT_MODULE and CHROMIUM_PATH may point to a local runtime.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const path=require('path');
const fs=require('fs');
const {pathToFileURL}=require('url');
(async()=>{
  const root=path.resolve(__dirname,'..'),dir=path.join(root,'qa/edition4');
  fs.mkdirSync(dir,{recursive:true});
  const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
  const page=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root,'dist/FDE橙皮书.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:path.join(dir,'reader-desktop.png')});
  await page.locator('.read-links a[href="#ch-01"]').click();
  await page.locator('#ch-01').waitFor({state:'visible'});
  await page.locator('#ch-01 .local-toc summary').click();
  const section=await page.locator('#ch-01 .local-toc a').nth(2).getAttribute('href');
  await page.locator('#ch-01 .local-toc a').nth(2).click();
  if(await page.locator('#ch-01').isHidden())throw Error('Section link hid chapter');
  if(await page.locator('#home').isVisible())throw Error('Section route returned home');
  if(page.url().split('#')[1]!==section.slice(1))throw Error('Wrong section anchor');
  await page.goto(pathToFileURL(path.join(root,'dist/FDE橙皮书.html')).href+'#ch-01');
  await page.screenshot({path:path.join(dir,'reader-chapter.png')});
  await page.locator('#ch-01 .chapter-nav a').last().click();
  await page.locator('#ch-02').waitFor({state:'visible'});
  await page.selectOption('#theme','wheat');
  if(await page.getAttribute('body','data-theme')!=='wheat')throw Error('Theme failed');
  await page.locator('#font').click();
  if(await page.locator('#ch-02').evaluate(el=>getComputedStyle(el).fontSize)!=='21px')throw Error('Font control failed');
  await page.selectOption('#theme','paper');
  await page.locator('#font').click();
  const download=await page.locator('.download').getAttribute('href');
  if(!fs.existsSync(path.join(root,'dist',download)))throw Error('Missing PDF');
  await page.setViewportSize({width:390,height:844});
  await page.locator('.menu').click();
  await page.locator('#sidebar a[href="#ch-27"]').click();
  await page.locator('#ch-27').waitFor({state:'visible'});
  if(await page.locator('.menu').getAttribute('aria-expanded')!=='false')throw Error('Menu not closed');
  await page.screenshot({path:path.join(dir,'reader-mobile.png')});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  if(overflow)throw Error('Mobile overflow');
  for(const key of ['05','06','07','08','09','10','27']){
    await page.goto(pathToFileURL(path.join(root,'dist/FDE橙皮书.html')).href+'#ch-'+key);
    if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw Error('Mobile overflow in chapter '+key);
  }
  await page.locator('#ch-27 .chapter-nav a').last().click();
  await page.locator('#home').waitFor({state:'visible'});
  await page.screenshot({path:path.join(dir,'reader-mobile-cover.png')});
  await page.setViewportSize({width:960,height:920});
  for(const theme of ['paper','terra','wheat']){
    await page.selectOption('#theme',theme);
    await page.locator('.cover').screenshot({path:path.join(dir,`cover-${theme}.png`)});
  }
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync(path.join(dir,'reader-test.json'),JSON.stringify({errors,overflow,checks:['chapter navigation','section anchors','next chapter','last chapter home','theme','font size','mobile navigation','technical code overflow','PDF target']},null,2));
  console.log('Reader QA passed: navigation, themes, font, PDF target, mobile, zero page errors.');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

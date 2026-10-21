// Headless mobile check for the Historical Kitchen.
//
// The browser tool cannot resize the viewport, so the media queries
// never fire and the mobile bugs hide. This runs Chrome at a real
// 390x844 (iPhone 14 size) and reports the overflow.
//
// Usage: node mobile_check.js <file-or-url>

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const target = process.argv[2];
if (!target) { console.error('usage: node mobile_check.js <url>'); process.exit(1); }

const script = `
const puppeteerless = true;
`;

// We drive Chrome over the DevTools protocol with plain HTTP + WS is
// heavy; instead use --dump-dom with a window size, plus a tiny
// injected script via a wrapper page.
const wrapper = path.join(os.tmpdir(), 'mobile_check_wrapper.html');
const probe = `
<script>
window.addEventListener('load', function(){
  setTimeout(function(){
    var d = document.documentElement;
    var out = {
      viewport: window.innerWidth + 'x' + window.innerHeight,
      docScrollWidth: d.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      overflow: d.scrollWidth > window.innerWidth + 1,
      overflowing: []
    };
    var all = document.querySelectorAll('body *');
    for (var i=0; i<all.length; i++){
      var e = all[i];
      var r = e.getBoundingClientRect();
      if (r.width > 0 && r.right > window.innerWidth + 1){
        out.overflowing.push({
          tag: e.tagName,
          cls: (e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className) || '',
          id: e.id || '',
          right: Math.round(r.right),
          width: Math.round(r.width)
        });
      }
    }
    out.overflowing = out.overflowing.slice(0, 14);
    // key element widths
    out.key = {};
    ['eraRail','eraSeg','cuisineSeg','foodStrip','kindSeg','bookSeg'].forEach(function(id){
      var e = document.getElementById(id);
      if(e) out.key[id] = {scroll: e.scrollWidth, client: e.clientWidth, overflowX: getComputedStyle(e).overflowX};
    });
    out.tabs = [...document.querySelectorAll('.tab')].map(t=>t.textContent);
    // also measure the fiction tab
    document.querySelector('.tab[data-tab=fiction]').click();
    out.fiction = {
      visible: getComputedStyle(document.getElementById('fictionTab')).display,
      litCards: document.querySelectorAll('.lit').length,
      count: document.getElementById('fictionCount')?.textContent,
      foodChips: document.querySelectorAll('.food-chip').length,
      docScrollWidth: document.documentElement.scrollWidth,
      overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      strip: (function(){var e=document.getElementById('foodStrip');return {scroll:e.scrollWidth, client:e.clientWidth, ox:getComputedStyle(e).overflowX};})(),
      kind: (function(){var e=document.getElementById('kindSeg');return {scroll:e.scrollWidth, client:e.clientWidth, ox:getComputedStyle(e).overflowX};})(),
      book: (function(){var e=document.getElementById('bookSeg');return {scroll:e.scrollWidth, client:e.clientWidth, ox:getComputedStyle(e).overflowX};})(),
    };
    document.querySelector('.tab[data-tab=recipes]').click();
    out.cards = document.querySelectorAll('.card').length;
    out.lit = document.querySelectorAll('.lit').length;
    document.title = 'RESULT:' + JSON.stringify(out);
  }, 900);
});
</script>
`;

const src = fs.readFileSync(target, 'utf8');
fs.writeFileSync(wrapper, src.replace('</body>', probe + '</body>'));

const outFile = path.join(os.tmpdir(), 'mobile_dump.html');
execFile('google-chrome', [
  '--headless=new',
  '--disable-gpu',
  '--no-sandbox',
  '--disable-dev-shm-usage',
  '--window-size=390,844',
  '--virtual-time-budget=4000',
  '--dump-dom',
  'file://' + wrapper,
], { maxBuffer: 200 * 1024 * 1024 }, (err, stdout) => {
  if (err) { console.error('chrome error:', err.message); process.exit(1); }
  const m = stdout.match(/RESULT:(\{.*?\})<\/title>/s);
  if (!m) {
    console.error('no result captured. title=', (stdout.match(/<title>([^<]*)/) || [])[1]);
    process.exit(1);
  }
  console.log(JSON.stringify(JSON.parse(m[1]), null, 1));
});

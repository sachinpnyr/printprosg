from playwright.sync_api import sync_playwright
import time

html = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; padding: 30px; display: flex; flex-direction: column; gap: 20px; background: #222; }
.row { padding: 20px 30px; display: inline-block; }
.dark { background: #111; }
.mid { background: #1a1a1a; }
.white { background: white; }
img { display: block; height: 50px; width: auto; }
</style>
</head>
<body>
  <div class="row dark">
    <img src="img/logo-white.png">
  </div>
  <div class="row mid">
    <img src="img/logo-white.png">
  </div>
  <div class="row white">
    <img src="img/logo-transparent.png">
  </div>
</body>
</html>"""

with open('/home/ubuntu/printprosg/logo_fix_verify.html', 'w') as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 500, 'height': 400})
    page.goto('file:///home/ubuntu/printprosg/logo_fix_verify.html')
    time.sleep(1)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/logo_white_fixed.png')
    print("Saved logo_white_fixed.png")
    browser.close()

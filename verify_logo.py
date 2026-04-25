from playwright.sync_api import sync_playwright
import time

html = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; padding: 30px; display: flex; flex-direction: column; gap: 20px; }
.on-white { background: white; padding: 16px 24px; display: inline-block; border: 1px solid #eee; }
.on-dark { background: #1a1a1a; padding: 16px 24px; display: inline-block; }
.on-red { background: #e8192c; padding: 16px 24px; display: inline-block; }
img { display: block; height: 44px; width: auto; }
</style>
</head>
<body>
  <div class="on-white">
    <img src="img/logo-transparent.png">
  </div>
  <div class="on-dark">
    <img src="img/logo-transparent.png">
  </div>
  <div class="on-red">
    <img src="img/logo-transparent.png">
  </div>
</body>
</html>"""

with open('/home/ubuntu/printprosg/logo_verify.html', 'w') as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 500, 'height': 400})
    page.goto('file:///home/ubuntu/printprosg/logo_verify.html')
    time.sleep(1)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/logo_verify.png')
    print("Saved logo_verify.png")
    browser.close()

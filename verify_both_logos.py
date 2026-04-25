from playwright.sync_api import sync_playwright
import time

html = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; padding: 30px; display: flex; flex-direction: column; gap: 20px; font-family: sans-serif; }
.row { display: flex; align-items: center; gap: 20px; padding: 16px 24px; }
.on-white { background: white; border: 1px solid #eee; }
.on-dark { background: #1a1a1a; }
.on-footer { background: #111111; }
label { font-size: 12px; color: #999; min-width: 80px; }
img { display: block; height: 40px; width: auto; }
</style>
</head>
<body>
  <div class="row on-white">
    <label>Navbar (white bg):</label>
    <img src="img/logo-transparent.png">
  </div>
  <div class="row on-dark">
    <label style="color:#666">Footer (dark bg):</label>
    <img src="img/logo-white.png">
  </div>
  <div class="row on-footer">
    <label style="color:#555">Footer alt:</label>
    <img src="img/logo-white.png">
  </div>
</body>
</html>"""

with open('/home/ubuntu/printprosg/logo_both.html', 'w') as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 500, 'height': 350})
    page.goto('file:///home/ubuntu/printprosg/logo_both.html')
    time.sleep(1)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/logo_both.png')
    print("Saved logo_both.png")
    browser.close()

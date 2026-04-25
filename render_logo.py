from playwright.sync_api import sync_playwright
import time, os

# Render the SVG logo at large size for visual check
html = """<!DOCTYPE html>
<html>
<head>
<style>
body { background: white; padding: 40px; display: flex; flex-direction: column; gap: 30px; }
.on-white { background: white; padding: 20px; display: inline-block; }
.on-dark { background: #1a1a1a; padding: 20px; display: inline-block; }
img { display: block; }
</style>
</head>
<body>
  <div class="on-white">
    <img src="img/logo-vector.svg" width="300" height="80">
  </div>
  <div class="on-dark">
    <img src="img/logo-vector.svg" width="300" height="80">
  </div>
</body>
</html>"""

with open('/home/ubuntu/printprosg/logo_test.html', 'w') as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 500, 'height': 300})
    page.goto('file:///home/ubuntu/printprosg/logo_test.html')
    time.sleep(1)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/logo_check.png')
    print("Logo screenshot saved")
    browser.close()

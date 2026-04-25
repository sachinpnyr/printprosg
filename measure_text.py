from playwright.sync_api import sync_playwright
import time

html = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; padding: 20px; background: white; }
#measure {
  font-family: 'Arial Black', 'Helvetica Neue', Arial, sans-serif;
  font-size: 44px;
  font-weight: 900;
  letter-spacing: -0.5px;
  color: #333;
  display: inline-block;
  white-space: nowrap;
}
</style>
</head>
<body>
  <span id="measure">Print Pr</span>
</body>
</html>"""

with open('/home/ubuntu/printprosg/measure_text.html', 'w') as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 800, 'height': 200})
    page.goto('file:///home/ubuntu/printprosg/measure_text.html')
    time.sleep(0.5)
    
    dims = page.evaluate("""() => {
        const el = document.getElementById('measure');
        const rect = el.getBoundingClientRect();
        return {
            width: rect.width,
            height: rect.height,
            x: rect.x,
            y: rect.y,
            right: rect.right
        };
    }""")
    print("Text 'Print Pr' dimensions:", dims)
    browser.close()

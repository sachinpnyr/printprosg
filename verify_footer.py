from playwright.sync_api import sync_playwright
from PIL import Image
import io, os

os.makedirs('/home/ubuntu/printprosg/v52_verify', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop full page
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    # Full page screenshot
    full_bytes = page.screenshot(full_page=True)
    full_img = Image.open(io.BytesIO(full_bytes))
    w, h = full_img.size
    print(f'Desktop full page: {w}x{h}')

    # Crop footer (last 500px)
    footer_crop = full_img.crop((0, h - 500, w, h))
    footer_crop.save('/home/ubuntu/printprosg/v52_verify/11_footer.png')

    # Crop services section with show more button (need to find it)
    # Take services screenshot
    services = page.locator('#services')
    services.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    bb = services.bounding_box()
    if bb:
        svc_crop = full_img.crop((0, int(bb['y']), w, min(h, int(bb['y']) + 800)))
        svc_crop.save('/home/ubuntu/printprosg/v52_verify/06b_services_full.png')

    # Mobile full page
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    full_bytes_m = page.screenshot(full_page=True)
    full_img_m = Image.open(io.BytesIO(full_bytes_m))
    wm, hm = full_img_m.size
    print(f'Mobile full page: {wm}x{hm}')

    # Mobile footer
    footer_m = full_img_m.crop((0, hm - 500, wm, hm))
    footer_m.save('/home/ubuntu/printprosg/v52_verify/16_mobile_footer.png')

    # Mobile services
    services_m = page.locator('#services')
    services_m.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    bb_m = services_m.bounding_box()
    if bb_m:
        svc_m = full_img_m.crop((0, int(bb_m['y']), wm, min(hm, int(bb_m['y']) + 700)))
        svc_m.save('/home/ubuntu/printprosg/v52_verify/15_mobile_services.png')

    browser.close()

print("Footer and services screenshots captured.")

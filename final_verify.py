from playwright.sync_api import sync_playwright
from PIL import Image
import io, os

os.makedirs('/home/ubuntu/printprosg/v52_verify', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Mobile 390px
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    full_bytes = page.screenshot(full_page=True)
    full_img = Image.open(io.BytesIO(full_bytes))
    w, h = full_img.size
    print(f'Mobile full page: {w}x{h}')

    # Show More button at y=3028
    show_more_crop = full_img.crop((0, 2950, w, 3130))
    show_more_crop.save('/home/ubuntu/printprosg/v52_verify/show_more_mobile.png')

    # Mobile footer logo at y=6018
    footer_logo_crop = full_img.crop((0, 5900, w, 6200))
    footer_logo_crop.save('/home/ubuntu/printprosg/v52_verify/mobile_footer_logo.png')

    # Mobile services section at y ~2500
    # Find services section
    svc = page.locator('#services')
    svc.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    bb = svc.bounding_box()
    if bb:
        svc_crop = full_img.crop((0, int(bb['y']), w, min(h, int(bb['y']) + 800)))
        svc_crop.save('/home/ubuntu/printprosg/v52_verify/mobile_services_correct.png')

    # Desktop 1440px — services with Show More button
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    full_d = page.screenshot(full_page=True)
    full_img_d = Image.open(io.BytesIO(full_d))
    wd, hd = full_img_d.size
    print(f'Desktop full page: {wd}x{hd}')

    # Services section
    svc_d = page.locator('#services')
    svc_d.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    bb_d = svc_d.bounding_box()
    if bb_d:
        svc_crop_d = full_img_d.crop((0, int(bb_d['y']), wd, min(hd, int(bb_d['y']) + 900)))
        svc_crop_d.save('/home/ubuntu/printprosg/v52_verify/desktop_services_showmore.png')

    # Desktop footer
    footer_d = full_img_d.crop((0, hd - 600, wd, hd))
    footer_d.save('/home/ubuntu/printprosg/v52_verify/desktop_footer_full.png')

    browser.close()

print("Final verification screenshots done.")

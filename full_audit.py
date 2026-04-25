from playwright.sync_api import sync_playwright
import json, os

OUT = "/home/ubuntu/printprosg/audit_compare"
os.makedirs(OUT, exist_ok=True)

VIEWPORT = {"width": 390, "height": 844}  # iPhone 14 Pro

def audit_page(page, label, out_prefix):
    results = {}

    # Full page screenshot
    page.screenshot(path=f"{OUT}/{out_prefix}_full.png", full_page=True)

    # Viewport screenshot (above fold)
    page.screenshot(path=f"{OUT}/{out_prefix}_viewport.png")

    # 1. Navbar / header height
    for sel in ['header', 'nav', '#navbar', '.navbar', '[role="banner"]']:
        el = page.query_selector(sel)
        if el:
            box = el.bounding_box()
            if box and box['height'] > 0:
                results['navbar_height'] = round(box['height'])
                results['navbar_selector'] = sel
                break

    # 2. Touch target sizes — all clickable elements
    buttons = page.query_selector_all('a, button, [role="button"], input[type="submit"]')
    small_targets = []
    for btn in buttons:
        box = btn.bounding_box()
        if box and box['width'] > 0 and box['height'] > 0:
            if box['width'] < 44 or box['height'] < 44:
                text = page.evaluate('el => el.innerText || el.getAttribute("aria-label") || el.tagName', btn)
                small_targets.append({
                    'text': str(text)[:40],
                    'w': round(box['width']),
                    'h': round(box['height'])
                })
    results['small_touch_targets'] = len(small_targets)
    results['small_touch_target_examples'] = small_targets[:5]

    # 3. Font sizes — check for text smaller than 12px
    small_fonts = page.evaluate("""() => {
        const els = document.querySelectorAll('p, span, a, li, td, label, h1, h2, h3, h4, h5, h6');
        const small = [];
        for (const el of els) {
            const style = window.getComputedStyle(el);
            const size = parseFloat(style.fontSize);
            const rect = el.getBoundingClientRect();
            if (size < 12 && rect.width > 0 && el.innerText && el.innerText.trim().length > 2) {
                small.push({ text: el.innerText.trim().slice(0, 30), size: size, tag: el.tagName });
            }
        }
        return small.slice(0, 10);
    }""")
    results['small_font_count'] = len(small_fonts)
    results['small_font_examples'] = small_fonts

    # 4. Horizontal overflow (content wider than viewport)
    overflow = page.evaluate("""() => {
        const body = document.body;
        const html = document.documentElement;
        const vw = window.innerWidth;
        const overflow_els = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
            const rect = el.getBoundingClientRect();
            if (rect.right > vw + 5) {
                overflow_els.push({
                    tag: el.tagName,
                    cls: el.className.toString().slice(0, 40),
                    right: Math.round(rect.right),
                    vw: vw
                });
            }
        }
        return overflow_els.slice(0, 10);
    }""")
    results['horizontal_overflow_count'] = len(overflow)
    results['horizontal_overflow_examples'] = overflow

    # 5. Viewport meta
    viewport_meta = page.evaluate("""() => {
        const meta = document.querySelector('meta[name="viewport"]');
        return meta ? meta.getAttribute('content') : 'MISSING';
    }""")
    results['viewport_meta'] = viewport_meta

    # 6. Image alt tags
    imgs_no_alt = page.evaluate("""() => {
        const imgs = document.querySelectorAll('img');
        let count = 0;
        for (const img of imgs) {
            if (!img.alt || img.alt.trim() === '') count++;
        }
        return count;
    }""")
    results['images_missing_alt'] = imgs_no_alt

    # 7. Input field sizes
    inputs = page.query_selector_all('input, textarea, select')
    small_inputs = []
    for inp in inputs:
        box = inp.bounding_box()
        if box and box['height'] < 44 and box['height'] > 0:
            itype = page.evaluate('el => el.type || el.tagName', inp)
            small_inputs.append({'type': itype, 'h': round(box['height'])})
    results['small_inputs'] = len(small_inputs)
    results['small_input_examples'] = small_inputs[:5]

    # 8. Page total height
    total_h = page.evaluate("() => document.documentElement.scrollHeight")
    results['total_page_height'] = total_h

    # 9. Above-fold CTA visibility
    cta = page.query_selector('a.btn, button.btn, .btn-primary, [class*="cta"]')
    if cta:
        box = cta.bounding_box()
        results['cta_above_fold'] = box['y'] < 844 if box else False
        results['cta_height'] = round(box['height']) if box else 0

    # 10. Line height / readability check on body text
    line_height = page.evaluate("""() => {
        const p = document.querySelector('p');
        if (!p) return null;
        const style = window.getComputedStyle(p);
        return { fontSize: style.fontSize, lineHeight: style.lineHeight };
    }""")
    results['body_text_style'] = line_height

    print(f"\n=== {label} ===")
    for k, v in results.items():
        if not isinstance(v, list):
            print(f"  {k}: {v}")
    if results.get('small_touch_target_examples'):
        print(f"  small_touch_targets (examples):")
        for t in results['small_touch_target_examples']:
            print(f"    '{t['text']}' — {t['w']}x{t['h']}px")
    if results.get('horizontal_overflow_examples'):
        print(f"  overflow elements:")
        for o in results['horizontal_overflow_examples']:
            print(f"    {o['tag']}.{o['cls']} right={o['right']}px")
    if results.get('small_font_examples'):
        print(f"  small fonts:")
        for f in results['small_font_examples']:
            print(f"    <{f['tag']}> '{f['text']}' = {f['size']}px")

    return results

with sync_playwright() as p:
    browser = p.chromium.launch()

    # --- Google.com ---
    page_g = browser.new_page(viewport=VIEWPORT)
    page_g.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"})
    page_g.goto("https://www.google.com", wait_until="networkidle", timeout=30000)
    page_g.wait_for_timeout(2000)
    google_results = audit_page(page_g, "GOOGLE.COM", "google")

    # --- PrintProSG ---
    page_p = browser.new_page(viewport=VIEWPORT)
    page_p.goto("file:///home/ubuntu/printprosg/index.html", wait_until="networkidle")
    page_p.wait_for_timeout(2000)
    printpro_results = audit_page(page_p, "PRINTPROSG", "printpro")

    browser.close()

# Save comparison JSON
with open(f"{OUT}/comparison.json", "w") as f:
    json.dump({"google": google_results, "printpro": printpro_results}, f, indent=2)

print("\n\n=== COMPARISON SUMMARY ===")
checks = [
    ("navbar_height", "Navbar height (px)", lambda g, p: abs(g-p) <= 10),
    ("small_touch_targets", "Small touch targets (<44px)", lambda g, p: p <= g + 5),
    ("small_font_count", "Text < 12px count", lambda g, p: p <= g + 3),
    ("horizontal_overflow_count", "Horizontal overflow elements", lambda g, p: p == 0),
    ("small_inputs", "Form inputs < 44px height", lambda g, p: p == 0),
    ("images_missing_alt", "Images missing alt text", lambda g, p: p <= 3),
]
for key, label, ok_fn in checks:
    g_val = google_results.get(key, "N/A")
    p_val = printpro_results.get(key, "N/A")
    if isinstance(g_val, (int, float)) and isinstance(p_val, (int, float)):
        status = "✅" if ok_fn(g_val, p_val) else "❌"
    else:
        status = "ℹ️"
    print(f"  {status} {label}: Google={g_val}, PrintPro={p_val}")

print("\nDone! Screenshots saved to", OUT)

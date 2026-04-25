import os, re

HTML_DIR = '/home/ubuntu/printprosg'

# Files to update
html_files = [
    'index.html',
    'about.html',
    'faq.html',
    'delivery.html',
    'design-services.html',
    'artwork-guidelines.html',
    '404.html',
    'product.html',
]

# New navbar logo img tag
NEW_NAV_LOGO = '<img alt="Print Pro Singapore" class="logo-img" src="img/logo-transparent.png" style="height:40px;width:auto;"/>'

# New footer logo img tag
NEW_FOOTER_LOGO_IMG = '<img alt="Print Pro Singapore" class="footer-logo-img" src="img/logo-white.png" style="height:36px;width:auto;margin-bottom:12px;"/>'

for fname in html_files:
    fpath = os.path.join(HTML_DIR, fname)
    if not os.path.exists(fpath):
        print(f"SKIP (not found): {fname}")
        continue
    
    with open(fpath, 'r') as f:
        content = f.read()
    
    original = content
    
    # 1. Replace navbar logo img (logo-vector.svg or any logo img inside nav-logo)
    content = re.sub(
        r'<img[^>]*class="logo-img"[^>]*/?>',
        NEW_NAV_LOGO,
        content
    )
    
    # 2. Replace footer text-only logo: <span class="footer-logo-text">Print Pro</span>
    content = content.replace(
        '<span class="footer-logo-text">Print Pro</span>',
        NEW_FOOTER_LOGO_IMG
    )
    
    # 3. Replace footer span-based logos: <div class="footer-logo"><span...>Print</span><span...>Pro</span>...</div>
    content = re.sub(
        r'<div class="footer-logo">.*?</div>',
        NEW_FOOTER_LOGO_IMG,
        content,
        flags=re.DOTALL
    )
    
    # 4. Replace nav-logo spans (404 page and others that use text spans)
    # Pattern: <a ... class="nav-logo">...<span class="logo-print">...</span>...</a>
    # Replace the inner content of nav-logo anchor with the img tag
    content = re.sub(
        r'(<a[^>]*class="nav-logo"[^>]*>)\s*<span[^>]*>.*?</span>\s*<span[^>]*>.*?</span>(?:\s*<span[^>]*>.*?</span>)?\s*(</a>)',
        r'\1' + NEW_NAV_LOGO + r'\2',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"UPDATED: {fname}")
    else:
        print(f"NO CHANGE: {fname}")

print("\nDone!")

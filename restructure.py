"""
Restructure index.html:
1. Remove #products section (lines 146-346, the HTML comment block)
2. Remove #design-services section (lines 423-460)
3. Remove #blog section (lines 700-741)
4. Fix footer logo: replace <img> with plain text "Print Pro"
5. Update nav-cat links from #products to #services
6. Update mobile nav links from #products to #services
"""

with open('/home/ubuntu/printprosg/index.html', 'r') as f:
    lines = f.readlines()

# Convert to 0-indexed
# Products section: lines 146-346 (0-indexed: 145-345) — the HTML comment block
# design-services: lines 423-460 (0-indexed: 422-459)
# blog: lines 700-741 (0-indexed: 699-740)

# We'll work with the content as a string for easier manipulation
content = ''.join(lines)

# 1. Remove the products comment block (from "<!-- PRODUCTS SECTION REMOVED" to just before "<!-- REVIEWS -->")
import re

# Remove the big products comment block
content = re.sub(
    r'<!-- PRODUCTS SECTION REMOVED.*?-->\n',
    '',
    content,
    flags=re.DOTALL
)

# 2. Remove design-services section
content = re.sub(
    r'<!-- ===== DESIGN SERVICES.*?</section>\n',
    '',
    content,
    flags=re.DOTALL
)

# Also try without the comment
content = re.sub(
    r'<section id="design-services">.*?</section>\n',
    '',
    content,
    flags=re.DOTALL
)

# 3. Remove blog section
content = re.sub(
    r'<!-- ===== BLOG.*?</section>\n',
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'<!-- BLOG.*?</section>\n',
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'<section id="blog">.*?</section>\n',
    '',
    content,
    flags=re.DOTALL
)

# 4. Fix footer logo: replace img tag with text
content = content.replace(
    '<img alt="Print Pro Singapore" class="footer-logo" src="img/logo-white.svg"/>',
    '<span class="footer-logo-text">Print Pro</span>'
)

# 5. Update nav-cat links from #products to #services
content = content.replace('href="#products"', 'href="#services"')

# 6. Update mobile nav links
content = content.replace('<li><a href="#products">Products</a></li>', '<li><a href="#services">Services</a></li>')

# 7. Update hero CTA "Explore Products" to "Explore Services"
content = content.replace(
    '<a class="btn-secondary" href="#products">Explore Products</a>',
    '<a class="btn-secondary" href="#services">Explore Services</a>'
)

# 8. Update hero product cards to link to #services instead of product.html
# Keep product.html links as they are (they're fine)

# Write the result
with open('/home/ubuntu/printprosg/index.html', 'w') as f:
    f.write(content)

# Count lines
with open('/home/ubuntu/printprosg/index.html', 'r') as f:
    new_lines = f.readlines()

print(f"Done! New line count: {len(new_lines)} (was 1075)")

# Verify sections present/absent
content_check = ''.join(new_lines)
sections = ['id="reviews"', 'id="design-services"', 'id="about"', 'id="how-it-works"', 
            'id="services"', 'id="blog"', 'id="clients"', 'id="locations"', 
            'id="faq"', 'id="contact"', 'id="footer"']
for s in sections:
    present = s in content_check
    print(f"  {s}: {'PRESENT' if present else 'REMOVED'}")

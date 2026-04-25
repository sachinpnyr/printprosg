#!/usr/bin/env python3
"""Fix all remaining HTML issues in index.html"""

with open('index.html', 'r') as f:
    content = f.read()

original = content

# ── 1. Fix blog card 6 - uses same image as card 4 (printing-hero.jpg)
# Card 4 is at idx 59848, card 6 is at idx 61057
# Replace the 3rd occurrence of printing-hero.jpg in blog section with slider3.webp
# Find blog section
blog_start = content.find('<section id="blog">')
blog_end = content.find('</section>', blog_start + 100)
blog_section = content[blog_start:blog_end]

# Count occurrences of printing-hero.jpg in blog section
count = blog_section.count('printing-hero.jpg')
print(f"printing-hero.jpg in blog section: {count}")

# Replace the 2nd occurrence of printing-hero.jpg in blog section
first_idx = blog_section.find('printing-hero.jpg')
second_idx = blog_section.find('printing-hero.jpg', first_idx + 1)
print(f"First at: {first_idx}, Second at: {second_idx}")

if second_idx != -1:
    blog_section_fixed = blog_section[:second_idx] + 'slider3.webp' + blog_section[second_idx + len('printing-hero.jpg'):]
    content = content[:blog_start] + blog_section_fixed + content[blog_end:]
    print("Fixed blog card 6 image")

# ── 2. Fix bcs-card 3 (Folded Business Cards) - use a completely different image
# Currently uses services/name_card.jpg (same as card 2 which uses services/name_card.webp)
# Use services/post_card.webp for card 3 instead (it's a different type of card)
content = content.replace(
    '<div class="bcs-img"><img src="img/services/name_card.jpg" alt="Folded Business Cards"',
    '<div class="bcs-img"><img src="img/services/post_card.webp" alt="Folded Business Cards"'
)
print("Fixed bcs-card 3 image")

# ── 3. Add eyebrow to promotions section
content = content.replace(
    '<div class="promo-header reveal">\n      <h2>CHECK OUT THESE <span class="promo-highlight">PROMOTIONS AND CAMPAIGNS</span></h2>',
    '<div class="promo-header reveal">\n      <span class="eyebrow">Special Offers</span>\n      <h2>CHECK OUT THESE <span class="promo-highlight">PROMOTIONS AND CAMPAIGNS</span></h2>'
)
print("Added eyebrow to promotions section")

# ── 4. Add scroll-margin-top to all sections via data attribute (we'll handle via CSS)
# This is handled in CSS

# ── 5. Fix the hero product showcase - make images fill the card better
# This is handled in CSS

# ── 6. Fix the hero background - add a subtle gradient
# This is handled in CSS

# ── 7. Delay chat popup to 15 seconds (it's already 5 seconds, increase to 15)
# This is in chatbot.js

# Write the fixed content
with open('index.html', 'w') as f:
    f.write(content)

print(f"\nTotal changes: {sum(1 for a, b in zip(original, content) if a != b)} character differences")
print("Done!")

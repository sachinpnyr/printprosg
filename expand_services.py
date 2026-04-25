with open('/home/ubuntu/printprosg/index.html', 'r') as f:
    content = f.read()

# New expanded services grid with data-category on every card
# Categories map to nav tabs:
# most-popular, name-cards, flyers, stickers, booklets, stationery, marketing, signages, promo, displays

NEW_GRID = '''<div class="services-grid" id="services-grid">
<a class="service-card reveal" href="product.html?id=name-cards" data-category="most-popular name-cards">
<div class="service-img"><img alt="Name Card Printing" loading="lazy" src="img/products/name_cards.webp"/></div>
<div class="service-body">
<h3>Name Cards</h3>
<p>Premium business cards in various finishes — matte, gloss, spot UV, embossed, and more.</p>
<div class="service-footer"><span class="service-price">From $30</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-1" href="product.html?id=flyers" data-category="most-popular flyers marketing">
<div class="service-img"><img alt="Flyers" loading="lazy" src="img/products/flyers.webp"/></div>
<div class="service-body">
<h3>Flyers &amp; Leaflets</h3>
<p>Eye-catching flyers and leaflets in A4, A5, DL, and custom sizes for promotions and events.</p>
<div class="service-footer"><span class="service-price">From $25</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-2" href="product.html?id=stickers" data-category="most-popular stickers marketing">
<div class="service-img"><img alt="Sticker Printing" loading="lazy" src="img/products/stickers.webp"/></div>
<div class="service-body">
<h3>Stickers &amp; Labels</h3>
<p>Custom die-cut stickers, roll labels, and product stickers in gloss, matte, or clear finish.</p>
<div class="service-footer"><span class="service-price">From $20</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal" href="product.html?id=booklets" data-category="most-popular booklets marketing">
<div class="service-img"><img alt="Booklet Printing" loading="lazy" src="img/products/booklets.webp"/></div>
<div class="service-body">
<h3>Booklets &amp; Catalogues</h3>
<p>Saddle-stitched or perfect-bound booklets, brochures, and catalogues in full colour.</p>
<div class="service-footer"><span class="service-price">From $80</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-1" href="product.html?id=roll-up-banners" data-category="most-popular displays signages">
<div class="service-img"><img alt="Roll-up Banner Printing" loading="lazy" src="img/products/rollup_banner.webp"/></div>
<div class="service-body">
<h3>Roll-up Banners</h3>
<p>Portable, professional pull-up banners for events, exhibitions, and retail displays.</p>
<div class="service-footer"><span class="service-price">From $65</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-2" href="product.html?id=vinyl-banners" data-category="signages displays marketing">
<div class="service-img"><img alt="Banner Printing" loading="lazy" src="img/products/vinyl_banner.webp"/></div>
<div class="service-body">
<h3>Banners &amp; Signage</h3>
<p>Large format vinyl banners, foam boards, and outdoor signage for maximum visibility.</p>
<div class="service-footer"><span class="service-price">From $45</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal" href="product.html?id=envelopes" data-category="stationery marketing">
<div class="service-img"><img alt="Envelope Printing" loading="lazy" src="img/products/envelope.webp"/></div>
<div class="service-body">
<h3>Envelopes</h3>
<p>Custom-printed envelopes in DL, C4, C5, and other sizes for a professional brand image.</p>
<div class="service-footer"><span class="service-price">From $40</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-1" href="product.html?id=postcards" data-category="stationery marketing">
<div class="service-img"><img alt="Postcard Printing" loading="lazy" src="img/products/postcards.webp"/></div>
<div class="service-body">
<h3>Postcards &amp; Flyers</h3>
<p>Vibrant postcards and promotional cards in A5, A6, and custom sizes — ideal for direct mail.</p>
<div class="service-footer"><span class="service-price">From $35</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-2" href="product.html?id=greeting-cards" data-category="stationery promo">
<div class="service-img"><img alt="Greeting Cards" loading="lazy" src="img/products/greeting_cards.webp"/></div>
<div class="service-body">
<h3>Greeting Cards</h3>
<p>Personalised greeting cards for corporate gifting, festive seasons, and special occasions.</p>
<div class="service-footer"><span class="service-price">From $50</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal" href="product.html?id=brochures" data-category="marketing flyers booklets">
<div class="service-img"><img alt="Brochure Printing" loading="lazy" src="img/products/brochures.webp"/></div>
<div class="service-body">
<h3>Brochures</h3>
<p>Tri-fold, bi-fold, and Z-fold brochures in premium paper stocks for marketing campaigns.</p>
<div class="service-footer"><span class="service-price">From $60</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-1" href="product.html?id=foam-boards" data-category="signages displays">
<div class="service-img"><img alt="Foam Board Printing" loading="lazy" src="img/products/foam_board.webp"/></div>
<div class="service-body">
<h3>Foam Boards</h3>
<p>Lightweight, rigid foam boards for indoor signage, exhibitions, and retail point-of-sale.</p>
<div class="service-footer"><span class="service-price">From $55</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-2" href="product.html?id=fabric-display" data-category="displays signages">
<div class="service-img"><img alt="Fabric Display" loading="lazy" src="img/products/fabric_display.webp"/></div>
<div class="service-body">
<h3>Fabric Displays</h3>
<p>Premium tension fabric displays and backdrops for events, trade shows, and exhibitions.</p>
<div class="service-footer"><span class="service-price">From $120</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal" href="product.html?id=tshirts" data-category="promo marketing">
<div class="service-img"><img alt="T-shirt Printing" loading="lazy" src="img/products/tshirt.webp"/></div>
<div class="service-body">
<h3>T-shirt Printing</h3>
<p>Custom screen-printed or DTG t-shirts for events, uniforms, and corporate merchandise.</p>
<div class="service-footer"><span class="service-price">From $12</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-1" href="product.html?id=corporate-gifts" data-category="promo most-popular">
<div class="service-img"><img alt="Corporate Gifts" loading="lazy" src="img/products/corporate_gifts.webp"/></div>
<div class="service-body">
<h3>Corporate Gifts</h3>
<p>Branded corporate gifts and merchandise — notebooks, pens, bags, and more with your logo.</p>
<div class="service-footer"><span class="service-price">From $5</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
<a class="service-card reveal reveal-delay-2" href="product.html?id=gift-vouchers" data-category="promo stationery">
<div class="service-img"><img alt="Gift Vouchers" loading="lazy" src="img/products/gift_vouchers.webp"/></div>
<div class="service-body">
<h3>Gift Vouchers</h3>
<p>Premium printed gift vouchers and certificates with serial numbering and security features.</p>
<div class="service-footer"><span class="service-price">From $45</span><span class="service-cta">Get Quote <i class="fas fa-arrow-right"></i></span></div>
</div>
</a>
</div>'''

# Replace the old services grid
old_grid_start = '<div class="services-grid">'
old_grid_end = '</div>\n</div>\n</section>\n<!-- MID-PAGE CTA BANNER -->'
new_grid_end = '\n</div>\n</section>\n<!-- MID-PAGE CTA BANNER -->'

# Find and replace the services grid
start_idx = content.find('<div class="services-grid">')
end_marker = '</div>\n</div>\n</section>\n<!-- MID-PAGE CTA BANNER -->'
end_idx = content.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: Could not find services grid. start={start_idx}, end={end_idx}")
    # Try alternate end marker
    end_marker2 = '</div>\n</section>\n<!-- MID-PAGE CTA BANNER -->'
    end_idx2 = content.find(end_marker2, start_idx)
    print(f"Alternate end marker at: {end_idx2}")
else:
    # Replace from services-grid div to end of section
    old_section = content[start_idx:end_idx]
    print(f"Found services grid at lines {start_idx}-{end_idx}")
    print(f"Old grid preview: {old_section[:100]}")
    
    new_content = content[:start_idx] + NEW_GRID + content[end_idx:]
    
    with open('/home/ubuntu/printprosg/index.html', 'w') as f:
        f.write(new_content)
    print("Services grid replaced successfully!")

# Full Visual Audit — PrintProSG Mobile (390px)

## ISSUES TO FIX

### CRITICAL

1. **Reviews section — review cards invisible (blank area)**
   - Section heading, star rating, "4.8/5", "from 200+ reviews" all show correctly
   - But the carousel area between the rating and pagination dots is completely blank
   - The review card content is not rendering visibly
   - Pagination dots show (dot 3 active), prev/next arrows show
   - Fix needed: ensure review cards are visible and positioned correctly

2. **FAQ questions truncated with ellipsis**
   - "What is the minimum order quant..." — truncated
   - Fix needed: allow full question text to wrap

3. **Contact form — textarea placeholder text cut off at bottom**
   - "Tell us about your project — quantity, size, deadline, any special requirements" — last line cut off
   - The textarea is too short; the Send Enquiry button is immediately below with no gap
   - Fix needed: increase textarea min-height and add margin-bottom

### MODERATE

4. **Hero — "Explore Products" button right edge cut off**
   - The outline button extends slightly past the right viewport edge
   - Fix needed: constrain button max-width or add right padding

5. **About section — "View Our Services" button left-aligned, not centered**
   - The button is left-aligned within the section
   - Fix needed: center the button

6. **How It Works — cards 03 and 04 descriptions cut off at viewport bottom**
   - "Your job is printed on premium stock with industry-leading equipment." — cut off
   - "Delivered to your door across Singapore..." — cut off
   - Fix needed: ensure the section scrolls fully or cards show complete text (already fixed for clamp, but viewport clips)

7. **Portfolio — filter tab "Print Materia..." truncated**
   - Third tab is cut off: "Print Materia..." should read "Print Materials"
   - This is expected horizontal scroll behavior — tab is scrollable, not broken

8. **Footer — "© 2026 Print Pro Singapore. All rights reserved. | GST Reg No: 12345678..." — GST number truncated**
   - The copyright line is truncated at the right edge
   - Fix needed: allow text to wrap to second line

9. **Back-to-top button overlaps content in multiple sections**
   - The ↑ button (bottom-right) overlaps cards/content in How It Works, Locations, FAQ, Contact
   - Fix needed: ensure it doesn't overlap important content (position fixed bottom-right is correct, but z-index may be too high or position needs adjustment)

### MINOR

10. **Clients logo bar — logos partially visible**
    - "RBIT" (Orbit), "PEARL EVENTS", "SKYLIN..." (Skyline Properties) — logos cut off on left/right edges
    - This is expected carousel/marquee behavior

11. **Cookie banner overlaps hero content**
    - Expected behavior — cookie banner is standard

## SECTIONS CONFIRMED OK

- Navbar: logo left, hamburger right, 48px height ✅
- Hero: headline, description, "Get a Free Quote" button fully visible ✅
- About stats: 32+ / 483+ / 48+ numbers and labels ✅
- About feature cards: 2-col layout ✅
- How It Works: 2x2 grid, full descriptions ✅
- Services: 2-col grid, titles wrap, prices visible ✅
- Portfolio: filter tabs scrollable, 2-col image grid ✅
- Locations: Singapore/UAE/India cards with WhatsApp+Directions buttons ✅
- Footer: brand description full text, social icons, nav links, copyright ✅

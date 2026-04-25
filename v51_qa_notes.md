# PrintProSG v51 Mobile QA Notes (390px)

## Section Heights
- #hero: 582px ✅ (was 906px)
- #reviews: 547px ✅ (was 620px)
- #about: 443px ✅ (was 459px)
- #how-it-works: 535px ✅ (was 701px)
- #services: 705px ⚠️ (was 914px - still a bit tall)
- #portfolio: 727px ⚠️ (was 817px)
- #clients: 222px ✅
- #locations: 576px ✅ (was 792px)
- #faq: 503px ✅ (was 769px)
- #contact: 685px ✅ (was 1010px)
- **Total: 5,525px** (was 8,270px — target ~5,500px ✅)

## Visual Quality Notes

### Hero
- Clean: headline + CTAs + trust badges + 2 product cards
- Looks premium and compact ✅
- Hero sub-text hidden — headline is strong enough ✅

### Services
- 4 cards in 2×2 grid, images visible, name + price + CTA ✅
- Cookie consent banner overlapping in screenshot (not a real issue) ✅

### Contact
- Form only (contact-info hidden) — clean and focused ✅
- All 4 fields visible: name, email, phone, service, message ✅
- Section header hidden (contact-info is hidden, no h2 visible) ⚠️ — need to add a heading

### Locations
- 3 cards: Singapore (HQ badge), UAE, India ✅
- Flag + country name + WhatsApp + Directions buttons ✅
- Clean and compact ✅

## Issues to Fix
1. Contact section has no heading visible (contact-info was hidden which contained the h2)
   - Need to add a simple h2 heading to the contact form wrap, OR
   - Show only the h2 from contact-info (not the full info column)

2. Services section still 705px — acceptable but could be tighter

## Desktop (1440px): 8,948px — acceptable for desktop
## Tablet (768px): 7,088px — acceptable for tablet

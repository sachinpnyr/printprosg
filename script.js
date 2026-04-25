/* ============================================================
   PRINT PRO SINGAPORE — script.js v2 (9+ Edition)
   Features: Reveal animations, Testimonial carousel, Portfolio
   lightbox + filter, FAQ accordion, Stats counter, Navbar,
   Mobile CTA bar, Back-to-top, Announcement bar
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- HERO CAROUSEL ---- */
  const heroCarousel = document.getElementById('hero-carousel');
  if (heroCarousel) {
    const slides = Array.from(heroCarousel.querySelectorAll('.hero-slide'));
    const dots = Array.from(document.querySelectorAll('.hero-dot'));
    const prevBtn = document.getElementById('hero-prev');
    const nextBtn = document.getElementById('hero-next');
    let current = 0;
    let heroTimer = null;

    function goToSlide(n) {
      slides[current].classList.remove('active');
      dots[current] && dots[current].classList.remove('active');
      current = ((n % slides.length) + slides.length) % slides.length;
      slides[current].classList.add('active');
      dots[current] && dots[current].classList.add('active');
    }

    function startHeroAuto() {
      stopHeroAuto();
      heroTimer = setInterval(() => goToSlide(current + 1), 5000);
    }
    function stopHeroAuto() {
      if (heroTimer) { clearInterval(heroTimer); heroTimer = null; }
    }

    if (prevBtn) prevBtn.addEventListener('click', () => { goToSlide(current - 1); startHeroAuto(); });
    if (nextBtn) nextBtn.addEventListener('click', () => { goToSlide(current + 1); startHeroAuto(); });
    dots.forEach((dot, i) => dot.addEventListener('click', () => { goToSlide(i); startHeroAuto(); }));

    // Touch swipe
    let heroTouchX = 0;
    heroCarousel.addEventListener('touchstart', e => { heroTouchX = e.touches[0].clientX; }, { passive: true });
    heroCarousel.addEventListener('touchend', e => {
      const diff = heroTouchX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) { goToSlide(diff > 0 ? current + 1 : current - 1); startHeroAuto(); }
    });

    heroCarousel.addEventListener('mouseenter', stopHeroAuto);
    heroCarousel.addEventListener('mouseleave', startHeroAuto);
    startHeroAuto();
  }

  /* ---- NAV SEARCH ---- */
  const searchInput = document.getElementById('nav-search-input');
  const searchDropdown = document.getElementById('search-dropdown');
  const searchItems = [
    { icon: 'fa-id-card', label: 'Name Cards', href: '#services' },
    { icon: 'fa-file-alt', label: 'Flyers & Brochures', href: '#services' },
    { icon: 'fa-flag', label: 'Banners & Signage', href: '#services' },
    { icon: 'fa-book-open', label: 'Booklets & Catalogues', href: '#services' },
    { icon: 'fa-tag', label: 'Stickers & Labels', href: '#services' },
    { icon: 'fa-tshirt', label: 'T-shirt Printing', href: '#services' },
    { icon: 'fa-gift', label: 'Corporate Gifts', href: '#services' },
    { icon: 'fa-box', label: 'Packaging', href: '#services' },
    { icon: 'fa-envelope', label: 'Envelopes', href: '#services' },
    { icon: 'fa-image', label: 'Posters', href: '#services' },
  ];
  if (searchInput && searchDropdown) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      if (!q) { searchDropdown.classList.remove('active'); searchDropdown.innerHTML = ''; return; }
      const results = searchItems.filter(i => i.label.toLowerCase().includes(q));
      if (!results.length) { searchDropdown.classList.remove('active'); searchDropdown.innerHTML = ''; return; }
      searchDropdown.innerHTML = results.map(r =>
        `<a class="search-result-item" href="${r.href}"><i class="fas ${r.icon}"></i>${r.label}</a>`
      ).join('');
      searchDropdown.classList.add('active');
    });
    document.addEventListener('click', e => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.classList.remove('active');
      }
    });
  }

  /* ---- ANNOUNCEMENT BANNER ---- */
  const bar = document.getElementById('announcement-bar');
  const closeBtn = document.getElementById('close-announcement');
  function dismissAnnBar() {
    if (!bar || bar.classList.contains('hidden')) return;
    bar.classList.add('hidden');
    document.documentElement.style.setProperty('--ann-h', '0px');
    var nav = document.getElementById('navbar');
    if (nav) nav.style.top = '0px';
    var hero = document.getElementById('hero');
    if (hero) hero.style.paddingTop = '';
  }
  if (closeBtn && bar) {
    // click (desktop)
    closeBtn.addEventListener('click', function(e) {
      e.preventDefault(); e.stopPropagation();
      dismissAnnBar();
    });
    // touchend (iOS Safari — fires reliably even at screen edge)
    closeBtn.addEventListener('touchend', function(e) {
      e.preventDefault(); e.stopPropagation();
      dismissAnnBar();
    }, { passive: false });
    // Swipe-up on the bar itself also dismisses (extra affordance)
    var annTouchStartY = 0;
    bar.addEventListener('touchstart', function(e) {
      annTouchStartY = e.touches[0].clientY;
    }, { passive: true });
    bar.addEventListener('touchend', function(e) {
      if (e.changedTouches[0].clientY - annTouchStartY < -20) dismissAnnBar();
    }, { passive: true });
  }
  /* Rotate announcement slides every 4 seconds */
  (function() {
    var annSlides = document.querySelectorAll('#announcement-slides .ann-slide');
    if (annSlides.length < 2) return;
    var annCurrent = 0;
    annSlides.forEach(function(s) { s.classList.remove('active'); });
    annSlides[0].classList.add('active');
    setInterval(function() {
      annSlides[annCurrent].classList.remove('active');
      annCurrent = (annCurrent + 1) % annSlides.length;
      annSlides[annCurrent].classList.add('active');
    }, 4000);
  })();

  /* ---- HAMBURGER MENU ---- */
  const hamburger = document.getElementById('nav-toggle');
  const navLinksEl = document.getElementById('nav-links');
  if (hamburger && navLinksEl) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navLinksEl.classList.toggle('open');
    });
    navLinksEl.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navLinksEl.classList.remove('open');
      });
    });
  }

  /* ---- NAVBAR SCROLL EFFECT ---- */
  const navbar = document.getElementById('navbar');

  /* ---- BACK TO TOP ---- */
  const backToTop = document.getElementById('back-to-top') || document.getElementById('scroll-top');
  if (backToTop) {
    backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ---- SMOOTH SCROLL ---- */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const navH = navbar ? navbar.offsetHeight : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - navH;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ---- ACTIVE NAV LINK + SCROLL EFFECTS ---- */
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    // Navbar shadow
    if (navbar) navbar.classList.toggle('scrolled', scrollY > 50);
    // Back-to-top
    if (backToTop) backToTop.classList.toggle('visible', scrollY > 400);
    // Also handle scroll-top id
    const scrollTopBtn = document.getElementById('scroll-top');
    if (scrollTopBtn) scrollTopBtn.classList.toggle('visible', scrollY > 400);
    // Active nav
    const navH = navbar ? navbar.offsetHeight : 80;
    let current = '';
    sections.forEach(sec => {
      if (scrollY >= sec.offsetTop - navH - 60) current = sec.id;
    });
    navItems.forEach(a => {
      a.classList.remove('active');
      if (a.getAttribute('href') === '#' + current) a.classList.add('active');
    });
  }, { passive: true });

  /* ---- SCROLL REVEAL ---- */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    // Enable CSS reveal animations (progressive enhancement)
    document.documentElement.classList.add('js-reveal-ready');
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Stagger siblings
          const siblings = Array.from(entry.target.parentElement.querySelectorAll('.reveal'));
          const idx = siblings.indexOf(entry.target);
          setTimeout(() => entry.target.classList.add('visible'), idx * 80);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px 0px 0px' });
    reveals.forEach(el => revealObserver.observe(el));
    // Fallback: reveal all elements after 2s in case IntersectionObserver fails
    setTimeout(() => {
      reveals.forEach(el => el.classList.add('visible'));
    }, 2000);
  }

  /* ---- COUNTER ANIMATION ---- */
  const counters = document.querySelectorAll('.stat-number[data-target]');
  let countersAnimated = false;
  function animateCounters() {
    if (countersAnimated) return;
    countersAnimated = true;
    counters.forEach(el => {
      const target = parseInt(el.dataset.target, 10);
      const suffix = el.dataset.suffix || '';
      const duration = 1400;
      const start = performance.now();
      const startVal = Math.floor(target * 0.55);
      el.textContent = startVal + suffix;
      const update = (now) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = startVal + Math.floor(eased * (target - startVal));
        el.textContent = current + suffix;
        if (progress < 1) requestAnimationFrame(update);
        else el.textContent = target + suffix;
      };
      requestAnimationFrame(update);
    });
  }
  if (counters.length) {
    // Fire on scroll into view with low threshold
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) animateCounters();
      });
    }, { threshold: 0.1 });
    counters.forEach(el => counterObserver.observe(el));
    // Fire immediately if stats bar is already in viewport on load
    setTimeout(() => {
      const statsBar = document.getElementById('stats-bar');
      if (statsBar) {
        const rect = statsBar.getBoundingClientRect();
        if (rect.top < window.innerHeight) animateCounters();
      } else {
        // Fallback: fire after short delay regardless
        animateCounters();
      }
    }, 400);
    // Final fallback: always fire after 1.2s
    setTimeout(() => animateCounters(), 1200);
  }

  /* ---- FAQ ACCORDION ---- */
  document.querySelectorAll('.faq-item').forEach(item => {
    const trigger = item.querySelector('.faq-question');
    const answer  = item.querySelector('.faq-answer');
    if (!trigger || !answer) return;
    trigger.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item').forEach(i => {
        i.classList.remove('open');
        const a = i.querySelector('.faq-answer');
        if (a) a.style.maxHeight = '0';
      });
      // Open clicked if it was closed
      if (!isOpen) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* ---- PORTFOLIO FILTER ---- */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  portfolioItems.forEach(item => {
    item.style.transition = 'opacity .3s ease, transform .3s ease';
  });

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      portfolioItems.forEach(item => {
        const match = filter === 'all' || item.dataset.category === filter;
        if (match) {
          item.classList.remove('hidden');
          requestAnimationFrame(() => {
            item.style.opacity = '1';
            item.style.transform = 'scale(1)';
          });
        } else {
          item.style.opacity = '0';
          item.style.transform = 'scale(0.92)';
          setTimeout(() => item.classList.add('hidden'), 300);
        }
      });
    });
  });

  /* ---- PORTFOLIO LIGHTBOX ---- */
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const lightboxClose = document.getElementById('lightbox-close');
  const lightboxPrev = document.getElementById('lightbox-prev');
  const lightboxNext = document.getElementById('lightbox-next');
  let currentLightboxIndex = 0;

  function getVisibleItems() {
    return Array.from(portfolioItems).filter(i => !i.classList.contains('hidden'));
  }

  function openLightbox(index) {
    const visible = getVisibleItems();
    currentLightboxIndex = index;
    const item = visible[currentLightboxIndex];
    if (!item || !lightbox) return;
    const img = item.querySelector('img');
    const caption = item.querySelector('.portfolio-overlay-content span');
    if (lightboxImg) {
      lightboxImg.src = img ? img.src : '';
      lightboxImg.alt = img ? img.alt : '';
    }
    if (lightboxCaption) lightboxCaption.textContent = caption ? caption.textContent : '';
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  function navigateLightbox(dir) {
    const visible = getVisibleItems();
    currentLightboxIndex = (currentLightboxIndex + dir + visible.length) % visible.length;
    const item = visible[currentLightboxIndex];
    if (!item || !lightboxImg) return;
    const img = item.querySelector('img');
    const caption = item.querySelector('.portfolio-overlay-content span');
    lightboxImg.style.opacity = '0';
    setTimeout(() => {
      lightboxImg.src = img ? img.src : '';
      lightboxImg.alt = img ? img.alt : '';
      if (lightboxCaption) lightboxCaption.textContent = caption ? caption.textContent : '';
      lightboxImg.style.opacity = '1';
    }, 150);
  }

  if (lightboxImg) lightboxImg.style.transition = 'opacity .15s ease';

  portfolioItems.forEach(item => {
    item.addEventListener('click', () => {
      const visible = getVisibleItems();
      const idx = visible.indexOf(item);
      if (idx >= 0) openLightbox(idx);
    });
  });

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightboxPrev) lightboxPrev.addEventListener('click', () => navigateLightbox(-1));
  if (lightboxNext) lightboxNext.addEventListener('click', () => navigateLightbox(1));
  if (lightbox) {
    lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
  }
  document.addEventListener('keydown', e => {
    if (!lightbox || !lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
  });

  /* ---- TESTIMONIALS CAROUSEL ---- */
  const track = document.getElementById('testimonials-track');
  const dotsContainer = document.getElementById('carousel-dots');
  const prevBtn = document.getElementById('carousel-prev');
  const nextBtn = document.getElementById('carousel-next');

  if (track) {
    const cards = Array.from(track.querySelectorAll('.testimonial-card'));
    let currentSlide = 0;
    let autoplayTimer = null;

    function getCardsPerView() {
      if (window.innerWidth <= 768) return 1;
      if (window.innerWidth <= 1024) return 2;
      return 3;
    }

    function getTotalSlides() {
      const cpv = getCardsPerView();
      return Math.max(1, cards.length - cpv + 1);
    }

    function buildDots() {
      if (!dotsContainer) return;
      dotsContainer.innerHTML = '';
      const total = getTotalSlides();
      for (let i = 0; i < total; i++) {
        const dot = document.createElement('button');
        dot.className = 'carousel-dot' + (i === currentSlide ? ' active' : '');
        dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
        dot.addEventListener('click', () => { goToSlide(i); startAutoplay(); });
        dotsContainer.appendChild(dot);
      }
    }

    function updateDots() {
      if (!dotsContainer) return;
      dotsContainer.querySelectorAll('.carousel-dot').forEach((d, i) => {
        d.classList.toggle('active', i === currentSlide);
      });
    }

    function goToSlide(index) {
      const total = getTotalSlides();
      currentSlide = ((index % total) + total) % total;
      const cardWidth = cards[0] ? cards[0].offsetWidth + 24 : 0;
      track.style.transform = `translateX(-${currentSlide * cardWidth}px)`;
      updateDots();
    }

    function nextSlide() { goToSlide(currentSlide + 1); }
    function prevSlide() { goToSlide(currentSlide - 1); }

    function startAutoplay() {
      stopAutoplay();
      autoplayTimer = setInterval(nextSlide, 4500);
    }
    function stopAutoplay() {
      if (autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; }
    }

    if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); startAutoplay(); });
    if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); startAutoplay(); });

    track.addEventListener('mouseenter', stopAutoplay);
    track.addEventListener('mouseleave', startAutoplay);

    // Touch swipe
    let touchStartX = 0;
    track.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', e => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) {
        if (diff > 0) nextSlide(); else prevSlide();
        startAutoplay();
      }
    });

    buildDots();
    startAutoplay();

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        buildDots();
        goToSlide(0);
      }, 200);
    });
  }

  /* ---- CLIENT LOGO FALLBACK ---- */
  document.querySelectorAll('.marquee-item img').forEach(img => {
    img.addEventListener('error', function() {
      const alt = this.alt || 'Client';
      const parent = this.parentElement;
      parent.innerHTML = `<span style="font-size:.72rem;font-weight:700;color:#9ca3af;letter-spacing:.06em;text-transform:uppercase;text-align:center;">${alt}</span>`;
    });
  });

  /* ---- CONTACT FORM ---- */
  const form = document.getElementById('contact-form');
  const submitBtn = form ? form.querySelector('[type="submit"]') : null;
  const successMsg = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const nameVal = form.querySelector('#name') ? form.querySelector('#name').value.trim() : '';
      const emailVal = form.querySelector('#email') ? form.querySelector('#email').value.trim() : '';
      const msgVal = form.querySelector('#message') ? form.querySelector('#message').value.trim() : '';
      if (!nameVal || !emailVal || !msgVal) { alert('Please fill in all required fields.'); return; }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailVal)) { alert('Please enter a valid email address.'); return; }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
      }
      try {
        const formData = new FormData(form);
        await fetch('/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams(formData).toString()
        });
      } catch (err) { /* Netlify handles it */ }
      form.reset();
      if (successMsg) {
        successMsg.style.display = 'flex';
        successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      if (submitBtn) submitBtn.innerHTML = '<i class="fas fa-check"></i> Sent!';
      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Enquiry';
        }
        if (successMsg) successMsg.style.display = 'none';
      }, 5000);
    });
  }

  /* ---- FOOTER YEAR ---- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

});

/* ============================================================
   PRINT PRO SG — v24 NEW FEATURES JS
   All 13 GoGoPrint-inspired interactive features
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. PRODUCT CATALOGUE FILTER ─────────────────────────── */
  const prodCatBtns = document.querySelectorAll('.prod-cat-btn');
  const prodCards   = document.querySelectorAll('.prod-card');

  prodCatBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      prodCatBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      prodCards.forEach(card => {
        // data-cat may contain multiple space-separated categories e.g. "popular name-cards"
        const cardCats = (card.dataset.cat || '').split(/\s+/);
        const match = cat === 'all' || cardCats.includes(cat);
        card.classList.toggle('hidden', !match);
      });
    });
  });

  /* ── 2. REVIEWS CAROUSEL ──────────────────────────────────── */
  const reviewsTrack = document.getElementById('reviews-track');
  const reviewsBtns  = document.querySelectorAll('.reviews-btn');
  const reviewsDots  = document.querySelectorAll('.reviews-dot');

  if (reviewsTrack) {
    const reviewCards = Array.from(reviewsTrack.querySelectorAll('.review-card'));
    let reviewIdx = 0;
    let reviewTimer = null;

    function getReviewsPerView() {
      if (window.innerWidth <= 600) return 1;
      if (window.innerWidth <= 900) return 2;
      return 3;
    }

    function scrollReviews(idx) {
      const perView = getReviewsPerView();
      const maxIdx  = Math.max(0, reviewCards.length - perView);
      reviewIdx = Math.max(0, Math.min(idx, maxIdx));
      const cardW = reviewCards[0] ? reviewCards[0].offsetWidth + 24 : 0;
      reviewsTrack.style.transform = `translateX(-${reviewIdx * cardW}px)`;
      reviewsDots.forEach((d, i) => d.classList.toggle('active', i === reviewIdx));
    }

    function startReviewAuto() {
      stopReviewAuto();
      reviewTimer = setInterval(() => {
        const perView = getReviewsPerView();
        const maxIdx  = Math.max(0, reviewCards.length - perView);
        scrollReviews(reviewIdx >= maxIdx ? 0 : reviewIdx + 1);
      }, 4000);
    }
    function stopReviewAuto() {
      if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
    }

    reviewsBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const dir = btn.dataset.dir === 'prev' ? -1 : 1;
        scrollReviews(reviewIdx + dir);
        startReviewAuto();
      });
    });
    reviewsDots.forEach((dot, i) => {
      dot.addEventListener('click', () => { scrollReviews(i); startReviewAuto(); });
    });

    // Touch swipe
    let revTouchX = 0;
    reviewsTrack.addEventListener('touchstart', e => { revTouchX = e.touches[0].clientX; }, { passive: true });
    reviewsTrack.addEventListener('touchend', e => {
      const diff = revTouchX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) { scrollReviews(reviewIdx + (diff > 0 ? 1 : -1)); startReviewAuto(); }
    });

    reviewsTrack.addEventListener('mouseenter', stopReviewAuto);
    reviewsTrack.addEventListener('mouseleave', startReviewAuto);
    startReviewAuto();

    window.addEventListener('resize', () => scrollReviews(0), { passive: true });
  }

  /* ── 3. DESIGN SERVICES TABS ──────────────────────────────── */
  const dsTabs    = document.querySelectorAll('.ds-tab');
  const dsContent = document.querySelectorAll('.ds-tab-content');

  dsTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      dsTabs.forEach(t => t.classList.remove('active'));
      dsContent.forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      const target = document.getElementById(tab.dataset.tab);
      if (target) target.classList.add('active');
    });
  });

  /* ── 4. HELP WIDGET TOGGLE ────────────────────────────────── */
  const helpWidget = document.getElementById('help-widget');
  const helpToggle = document.getElementById('help-widget-toggle');

  if (helpWidget) {
    // Toggle collapse when header is clicked
    if (helpToggle) {
      helpToggle.addEventListener('click', (e) => {
        // Don't collapse if close button was clicked
        if (e.target.closest('.help-widget-close')) {
          helpWidget.classList.add('hidden');
          return;
        }
        helpWidget.classList.toggle('collapsed');
      });
    }
    // Show widget after 20 seconds
    setTimeout(() => {
      helpWidget.classList.remove('hidden');
    }, 20000);
  }

  /* ── 5. NEWSLETTER FORM ───────────────────────────────────── */
  const newsletterForm = document.getElementById('newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', e => {
      e.preventDefault();
      const input = newsletterForm.querySelector('input[type="email"]');
      if (input && input.value.trim()) {
        const btn = newsletterForm.querySelector('button');
        if (btn) {
          btn.innerHTML = '<i class="fas fa-check"></i> Subscribed!';
          btn.disabled = true;
          setTimeout(() => {
            btn.innerHTML = 'Subscribe';
            btn.disabled = false;
            input.value = '';
          }, 3000);
        }
      }
    });
  }

  /* ── 6. CART BADGE ANIMATION ──────────────────────────────── */
  // NOTE: e.preventDefault() removed so .prod-cta links navigate to product pages
  const cartBadge = document.getElementById('cart-badge');
  document.querySelectorAll('.prod-cta').forEach(btn => {
    btn.addEventListener('click', () => {
      if (cartBadge) {
        cartBadge.style.transform = 'scale(1.4)';
        setTimeout(() => { cartBadge.style.transform = 'scale(1)'; }, 200);
      }
    });
  });

  /* ── 7. PROMO BANNER COUNTDOWN TIMER ─────────────────────── */
  const countdownEls = document.querySelectorAll('[data-countdown]');
  countdownEls.forEach(el => {
    const endTime = new Date().getTime() + (parseInt(el.dataset.countdown, 10) || 86400) * 1000;
    function updateTimer() {
      const now  = new Date().getTime();
      const diff = endTime - now;
      if (diff <= 0) { el.textContent = 'EXPIRED'; return; }
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      el.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    }
    updateTimer();
    setInterval(updateTimer, 1000);
  });

  /* ── 8. SMOOTH ANCHOR SCROLL (catch new anchors) ─────────── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    if (anchor._v24) return;
    anchor._v24 = true;
    anchor.addEventListener('click', e => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const navbar = document.getElementById('navbar');
      const navH = navbar ? navbar.offsetHeight : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - navH;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ── 9. BANNERS SHOWCASE PARALLAX TILT ───────────────────── */
  const showcaseImgs = document.querySelectorAll('.banners-showcase-images img');
  if (showcaseImgs.length) {
    const showcaseWrap = document.querySelector('.banners-showcase-images');
    if (showcaseWrap) {
      showcaseWrap.addEventListener('mousemove', e => {
        const rect = showcaseWrap.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        showcaseImgs[0] && (showcaseImgs[0].style.transform = `rotate(-2deg) translate(${x * 8}px, ${y * 8}px)`);
        showcaseImgs[1] && (showcaseImgs[1].style.transform = `rotate(2deg) translateY(16px) translate(${x * -8}px, ${y * -8}px)`);
      });
      showcaseWrap.addEventListener('mouseleave', () => {
        showcaseImgs[0] && (showcaseImgs[0].style.transform = 'rotate(-2deg)');
        showcaseImgs[1] && (showcaseImgs[1].style.transform = 'rotate(2deg) translateY(16px)');
      });
    }
  }

  /* ── 10. STICKY PRICE STRIP VISIBILITY ───────────────────── */
  const priceStrip = document.querySelector('.price-strip');
  if (priceStrip) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        priceStrip.style.opacity = entry.isIntersecting ? '1' : '0.6';
      });
    }, { threshold: 0.2 });
    observer.observe(priceStrip);
  }

  /* ── 11. ABOUT STATS COUNTER (new section) ────────────────── */
  const aboutStatNums = document.querySelectorAll('.about-stat-num[data-target]');
  if (aboutStatNums.length) {
    const aboutObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.dataset.target, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 1200;
        const start = performance.now();
        const from = 0;
        const update = now => {
          const t = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - t, 3);
          el.textContent = Math.floor(from + eased * (target - from)) + suffix;
          if (t < 1) requestAnimationFrame(update);
          else el.textContent = target + suffix;
        };
        requestAnimationFrame(update);
        aboutObserver.unobserve(el);
      });
    }, { threshold: 0.3 });
    aboutStatNums.forEach(el => aboutObserver.observe(el));
  }

  /* ── 12. BLOG CARD HOVER ELEVATION ───────────────────────── */
  document.querySelectorAll('.blog-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.boxShadow = '0 16px 48px rgba(0,0,0,.12)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.boxShadow = '';
    });
  });

  /* ── 13. MOBILE BOTTOM NAV ACTIVE STATE ──────────────────── */
  const mobileNavBtns = document.querySelectorAll('.mobile-cta-bar a, .mobile-cta-bar button');
  mobileNavBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      mobileNavBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

});

/* ── COOKIE BANNER ────────────────────────────────────────────── */
(function() {
  const banner = document.getElementById('cookie-banner');
  if (!banner) return;
  if (localStorage.getItem('cookieConsent')) return;

  // Show after 1.5 seconds
  setTimeout(() => banner.classList.add('visible'), 1500);

  const acceptBtn = document.getElementById('cookie-accept');
  const declineBtn = document.getElementById('cookie-decline');

  function dismissCookie(accepted) {
    banner.classList.remove('visible');
    localStorage.setItem('cookieConsent', accepted ? 'accepted' : 'declined');
    setTimeout(() => banner.remove(), 400);
  }

  if (acceptBtn) acceptBtn.addEventListener('click', () => dismissCookie(true));
  if (declineBtn) declineBtn.addEventListener('click', () => dismissCookie(false));
})();

/* ── PROMO CAROUSEL (mobile scroll) ──────────────────────────── */
(function() {
  const promoCarousel = document.getElementById('promo-carousel');
  const promoPrev = document.getElementById('promo-prev');
  const promoNext = document.getElementById('promo-next');

  if (!promoCarousel) return;

  const promoBanners = Array.from(promoCarousel.querySelectorAll('.promo-banner'));
  let promoIdx = 0;

  function scrollPromo(idx) {
    if (window.innerWidth > 900) return; // Desktop uses grid
    const maxIdx = promoBanners.length - 1;
    promoIdx = Math.max(0, Math.min(idx, maxIdx));
    const bannerW = promoBanners[0] ? promoBanners[0].offsetWidth + 20 : 0;
    promoCarousel.style.transform = `translateX(-${promoIdx * bannerW}px)`;
  }

  if (promoPrev) promoPrev.addEventListener('click', () => scrollPromo(promoIdx - 1));
  if (promoNext) promoNext.addEventListener('click', () => scrollPromo(promoIdx + 1));

  // Touch swipe for promo
  let promoTouchX = 0;
  promoCarousel.addEventListener('touchstart', e => { promoTouchX = e.touches[0].clientX; }, { passive: true });
  promoCarousel.addEventListener('touchend', e => {
    const diff = promoTouchX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) scrollPromo(promoIdx + (diff > 0 ? 1 : -1));
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) {
      promoCarousel.style.transform = '';
      promoIdx = 0;
    }
  }, { passive: true });
})();

/* ============================================================
   DARK MODE TOGGLE — v1
   ============================================================ */

/* ── MAKE ENTIRE PROD-CARD CLICKABLE ─────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.prod-card').forEach(card => {
    const ctaLink = card.querySelector('.prod-cta');
    if (!ctaLink) return;
    const href = ctaLink.getAttribute('href');
    if (!href) return;
    card.style.cursor = 'pointer';
    card.addEventListener('click', e => {
      // Only navigate if the click wasn't on the cta link itself (avoid double navigation)
      if (!e.target.closest('.prod-cta')) {
        window.location.href = href;
      }
    });
  });
});

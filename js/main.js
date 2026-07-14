/* ==========================================================================
   Ramos Roofing Plus - Main Javascript Logic
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Header
  const header = document.querySelector('.main-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // 2. Mobile Menu Toggle
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  function closeMobileMenu() {
    if (navMenu && navMenu.classList.contains('mobile-active')) {
      navMenu.classList.remove('mobile-active');
      if (hamburger) {
        hamburger.innerHTML = '<i class="fas fa-bars"></i>';
      }
    }
  }

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      // Toggle menu visibility (class active)
      navMenu.classList.toggle('mobile-active');
      const isExpanded = navMenu.classList.contains('mobile-active');
      hamburger.innerHTML = isExpanded ? '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
    });

    // Mobile dropdown toggle logic
    const dropdowns = navMenu.querySelectorAll('.dropdown, .mega-dropdown');
    dropdowns.forEach(dropdown => {
      const link = dropdown.querySelector('.nav-link');
      if (link) {
        link.addEventListener('click', (e) => {
          if (window.innerWidth <= 1150) {
            e.preventDefault(); // prevent navigation on top level
            dropdown.classList.toggle('mobile-active');
          }
        });
      }
    });

    // Close mobile menu when clicking any nav link (excluding dropdown toggles)
    const navLinks = navMenu.querySelectorAll('.nav-link, .dropdown-item, .mega-menu a');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        const isDropdownToggle = link.classList.contains('nav-link') && 
          (link.parentElement.classList.contains('dropdown') || link.parentElement.classList.contains('mega-dropdown')) && 
          (href === '#' || !href);
        
        if (!isDropdownToggle) {
          closeMobileMenu();
        }
      });
    });
  }

  // Close mobile menu AND scroll directly to form card on mobile
  const requestButtons = document.querySelectorAll('.btn-request');
  requestButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      closeMobileMenu();
      // On mobile, the layout stacks: text panel comes before the form card.
      // So we scroll directly to the form card instead of the section top.
      if (window.innerWidth <= 992) {
        const formCard = document.getElementById('form-card');
        if (formCard) {
          e.preventDefault();
          const headerHeight = document.querySelector('.main-header')?.offsetHeight || 75;
          const top = formCard.getBoundingClientRect().top + window.scrollY - headerHeight - 12;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      }
    });
  });

  // 3. SMS Chat Widget Toggle & Submission
  const widgetTrigger = document.querySelector('.sms-widget-trigger');
  const widgetBox = document.querySelector('.sms-widget-box');
  const widgetClose = document.querySelector('.sms-widget-close');
  const smsForm = document.querySelector('.sms-widget-form');

  if (widgetTrigger && widgetBox) {
    widgetTrigger.addEventListener('click', () => {
      widgetBox.classList.add('active');
    });
  }

  if (widgetClose && widgetBox) {
    widgetClose.addEventListener('click', () => {
      widgetBox.classList.remove('active');
    });
  }

  if (smsForm) {
    smsForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('sms-name').value;
      const phone = document.getElementById('sms-phone').value;
      const message = document.getElementById('sms-message').value;

      console.log(`[SMS LEAD CAPTURE] Routing lead to Brandon @ (479) 652-1424`);
      console.log(`Lead Details - Name: ${name}, Phone: ${phone}, Inquiry: ${message}`);

      // AJAX submission to Netlify Forms
      const formData = new URLSearchParams();
      formData.append("form-name", "sms-widget");
      formData.append("name", name);
      formData.append("phone", phone);
      formData.append("message", message);
      
      // Add honeypot value if filled (usually blank)
      const botField = smsForm.querySelector('input[name="bot-field"]');
      if (botField && botField.value) {
        formData.append("bot-field", botField.value);
      }

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString()
      })
      .then(() => {
        console.log("Successfully submitted SMS chat lead to Netlify Forms.");
      })
      .catch((error) => {
        console.error("Netlify Form submission failed:", error);
      });

      // Show success bubble in chat widget
      const body = document.querySelector('.sms-widget-body');
      body.innerHTML = `
        <div class="sms-bubble" style="border-radius: 16px; background-color: rgba(197,160,89,0.1); border-color: var(--accent-primary);">
          <p style="color: #fff; font-weight: 600;">Thank you, ${name}!</p>
          <p style="margin-top: 8px; font-size: 0.85rem;">Your message has been sent directly to our operations rep Brandon. We'll text or call you back shortly!</p>
        </div>
      `;
      smsForm.style.display = 'none';
    });
  }

  // 3b. Estimate Request Form -> GoHighLevel (via secure Netlify function)
  const estimateForm = document.getElementById('estimate-request-form');
  if (estimateForm) {
    estimateForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const submitBtn = estimateForm.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'SENDING...';
      }

      const honeypot = estimateForm.querySelector('input[name="company"]');
      const payload = {
        name: document.getElementById('est-name').value,
        phone: document.getElementById('est-phone').value,
        email: document.getElementById('est-email').value,
        message: document.getElementById('est-details').value,
        company: honeypot ? honeypot.value : ''
      };

      fetch('/.netlify/functions/ghl-lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then((res) => {
        if (!res.ok) throw new Error('Request failed');
        return res.json();
      })
      .then(() => {
        const card = estimateForm.closest('.rating-widget-card');
        if (card) {
          card.innerHTML = `
            <div style="padding: 30px 10px; text-align: center;">
              <i class="fas fa-check-circle" style="font-size: 3.5rem; color: var(--accent-hover); margin-bottom: 20px;"></i>
              <h3 style="font-size: 1.8rem; margin-bottom: 12px; font-family: var(--font-headings);">Request Received</h3>
              <p style="color: var(--text-secondary); max-width: 420px; margin: 0 auto;">
                Thanks, ${payload.name}! Brandon Ramos will personally reach out within 24 hours to schedule your free inspection.
              </p>
            </div>
          `;
        } else {
          estimateForm.reset();
        }
      })
      .catch((error) => {
        console.error('Lead submission failed:', error);
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }
        alert("Sorry, something went wrong sending your request. Please call us at (479) 652-1424 or try again.");
      });
    });
  }

  // 4. FAQ Accordion Logic
  const faqQuestions = document.querySelectorAll('.faq-question');
  faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
      const card = question.parentElement;
      const isActive = card.classList.contains('active');

      // Close all other FAQs
      document.querySelectorAll('.faq-card').forEach(otherCard => {
        otherCard.classList.remove('active');
      });

      // Toggle current
      if (!isActive) {
        card.classList.add('active');
      }
    });
  });

  // 5. Star Rating Redirect Logic (Review Page)
  const starBtns = document.querySelectorAll('.star-input-btn');
  const ratingValueInput = document.getElementById('rating-value');
  const feedbackForm = document.querySelector('.review-form-container');
  const redirectBox = document.querySelector('.rating-redirect-box');
  const actualForm = document.querySelector('.feedback-direct-form');

  if (starBtns.length > 0) {
    starBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const rating = parseInt(btn.getAttribute('data-val'), 10);
        
        // Reset stars styling
        starBtns.forEach(s => s.classList.remove('active'));
        for (let i = 0; i < rating; i++) {
          starBtns[i].classList.add('active');
        }

        if (ratingValueInput) ratingValueInput.value = rating;

        // Routing logic
        if (rating >= 4) {
          // Positive reviews (4-5 stars) -> Show Google Redirect link
          feedbackForm.classList.remove('active');
          redirectBox.classList.add('active');
        } else {
          // Negative/Neutral reviews (1-3 stars) -> Show private feedback form
          redirectBox.classList.remove('active');
          feedbackForm.classList.add('active');
        }
      });
    });
  }

  if (actualForm) {
    actualForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('feedback-name').value;
      const phone = document.getElementById('feedback-phone').value;
      const comments = document.getElementById('feedback-comments').value;
      const rating = ratingValueInput ? ratingValueInput.value : 'unknown';

      console.log(`[PRIVATE FEEDBACK CAPTURE] Routing low rating alert (Rating: ${rating}/5) to Austin @ (479) 652-1169`);
      console.log(`Feedback Details - Name: ${name}, Phone: ${phone}, Comments: ${comments}`);

      // AJAX submission to FormSubmit.co
      fetch("https://formsubmit.co/ajax/ramosroofing.ar@icloud.com", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          "Form Name": "Customer Feedback (Low Rating)",
          "Name": name,
          "Phone": phone,
          "Comments": comments,
          "Rating": rating,
          "_subject": "Alert: New Low Rating Private Feedback - Ramos Roofing Plus"
        })
      })
      .then(() => {
        console.log("Successfully submitted customer feedback to FormSubmit.");
      })
      .catch((error) => {
        console.error("FormSubmit submission failed:", error);
      });

      const widgetCard = document.querySelector('.rating-widget-card');
      widgetCard.innerHTML = `
        <div style="padding: 20px; text-align: center;">
          <i class="fas fa-check-circle" style="font-size: 3.5rem; color: var(--accent-hover); margin-bottom: 20px;"></i>
          <h3 style="font-size: 1.8rem; margin-bottom: 12px; font-family: var(--font-headings);">Thank You for Your Feedback</h3>
          <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 30px auto;">
            We appreciate your feedback. Austin Ramos (Owner) has been notified directly at his office. We will call you back to resolve any issues.
          </p>
        </div>
      `;
    });
  }

  // 6. Fix "Request Service" button on non-home pages
  const requestButtons = document.querySelectorAll('.btn-request');
  requestButtons.forEach(btn => {
    const path = window.location.pathname;
    const isHome = path === '/' || path.endsWith('/index.html') || path.endsWith('/') || path === '';
    if (!isHome) {
      if (path.includes('/services/') || path.includes('/locations/') || path.includes('/resources/')) {
        btn.href = '../index.html#quote-form';
      } else {
        btn.href = 'index.html#quote-form';
      }
    }
  });
});

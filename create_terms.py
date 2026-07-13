import re

def create_terms_page():
    # 1. Read about.html to use as template
    with open('r:\\AI Website Development\\Professional\\RamosRoofing-main\\RamosRoofing-main\\about.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split the file to extract header and footer
    # Find the start of Inner Page Hero
    header_end = content.find('<!-- Inner Page Hero -->')
    # Find the start of Footer Section
    footer_start = content.find('<!-- Footer Section -->')
    
    if header_end == -1 or footer_start == -1:
        print("Could not find sections to split.")
        return
        
    header_part = content[:header_end]
    footer_part = content[footer_start:]
    
    # Modify header title and meta
    header_part = header_part.replace('<title>About Ramos Roofing Plus | 25 Years of Family-Owned Excellence</title>', '<title>Terms & Conditions | Ramos Roofing Plus</title>')
    header_part = header_part.replace('<meta property="og:title" content="Our Story | Ramos Roofing Plus">', '<meta property="og:title" content="Terms & Conditions | Ramos Roofing Plus">')
    header_part = header_part.replace('about.html', 'terms-and-conditions.html')
    
    terms_content = """
  <!-- Inner Page Hero -->
  <section class="section section-bg-alt inner-page-hero" style="position: relative; overflow: hidden; padding: 60px 0; text-align: center; border-bottom: 1px solid var(--glass-border);">
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; opacity: 0.8;">
      <img src="./Images/compressed/IMG_0547.webp" alt="Hero Background" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top:0; left:0; filter: brightness(0.6);">
    </div>

    <div class="container" style="position: relative; z-index: 2;">
      <span class="hero-tagline">Legal</span>
      <h1 style="font-size: 3rem; margin-bottom: 0;">Terms & <span>Conditions</span></h1>
    </div>
  </section>

  <!-- Terms Content Section -->
  <section class="section" id="terms-content">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-bottom: 20px;">SMS & Messaging Agreement</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        By engaging with Ramos Roofing Plus and opting into our communication services, you agree to the following terms regarding text messaging and general communications.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">1. Consent to Communicate</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        By submitting your contact information through our website, you expressly authorize Ramos Roofing Plus to send you text messages (SMS) and emails. These messages are used primarily to provide estimates, coordinate service appointments, and follow up on your requests.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">2. Purpose and Frequency</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        Our messaging service is strictly used for transactional and customer service purposes related to your inquiry. We do not engage in aggressive marketing campaigns. Message frequency varies based entirely on the scope of your project and your direct communication with our team.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">3. Opting Out</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        You have the right to revoke your consent at any time. To immediately stop receiving text messages from us, simply reply with the word STOP. Once processed, you will no longer receive SMS communications from our business.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">4. Standard Rates</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        Ramos Roofing Plus does not charge any fees for our text messaging services. However, standard message and data rates applied by your mobile phone carrier may still apply. Please contact your mobile service provider for details on your specific plan.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">5. Commitment to Privacy</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        We deeply respect your privacy. Your phone number, email address, and project details are kept strictly confidential. We will never sell, rent, or distribute your personal contact information to external third parties or marketing affiliates.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">6. Service Reliability</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        While we strive for prompt communication, the delivery of SMS messages relies on external telecommunication networks. Ramos Roofing Plus cannot be held liable for delayed, undelivered, or misrouted messages caused by carrier outages or signal issues.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px;">7. Policy Updates</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px;">
        We may periodically update these messaging terms to comply with new regulations. Any changes will be posted on this page. Your continued use of our communication services constitutes acceptance of those changes.
      </p>

      <h3 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 40px; margin-bottom: 10px;">Questions?</h3>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 60px;">
        If you need help or have questions about our terms, please feel free to email us directly at <a href="mailto:info@ramosroofingplus.com" style="color: var(--accent-primary); text-decoration: underline;">info@ramosroofingplus.com</a>.
      </p>
    </div>
  </section>
"""
    
    final_content = header_part + terms_content + footer_part
    
    with open('r:\\AI Website Development\\Professional\\RamosRoofing-main\\RamosRoofing-main\\terms-and-conditions.html', 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print("terms-and-conditions.html created successfully.")

if __name__ == '__main__':
    create_terms_page()

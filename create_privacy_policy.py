import os

def create_privacy_page():
    # 1. Read about.html to use as template
    with open(r'r:\AI Website Development\Professional\RamosRoofing-main\RamosRoofing-main\about.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split the file to extract header and footer
    header_end = content.find('<!-- Inner Page Hero -->')
    footer_start = content.find('<!-- Footer Section -->')
    
    if header_end == -1 or footer_start == -1:
        print("Could not find sections to split.")
        return
        
    header_part = content[:header_end]
    footer_part = content[footer_start:]
    
    # Modify header title and meta
    header_part = header_part.replace('<title>About Ramos Roofing Plus | 25 Years of Family-Owned Excellence</title>', '<title>Privacy Policy | Ramos Roofing Plus</title>')
    header_part = header_part.replace('<meta property="og:title" content="Our Story | Ramos Roofing Plus">', '<meta property="og:title" content="Privacy Policy | Ramos Roofing Plus">')
    header_part = header_part.replace('about.html', 'privacy-policy.html')
    
    privacy_content = """
  <!-- Inner Page Hero -->
  <section class="section section-bg-alt inner-page-hero" style="position: relative; overflow: hidden; padding: 60px 0; text-align: center; border-bottom: 1px solid var(--glass-border);">
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; opacity: 0.8;">
      <img src="./Images/compressed/IMG_0547.webp" alt="Hero Background" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top:0; left:0; filter: brightness(0.6);">
    </div>

    <div class="container" style="position: relative; z-index: 2;">
      <span class="hero-tagline">Legal</span>
      <h1 style="font-size: 3rem; margin-bottom: 0;">Privacy <span>Policy</span></h1>
    </div>
  </section>

  <!-- Privacy Content Section -->
  <section class="section" id="privacy-content">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        <strong>Effective Date:</strong> July 13, 2026
      </p>

      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        At <strong>Ramos Roofing</strong>, we value your privacy and are committed to protecting your personal information. This Privacy Policy explains how we collect, use, and protect the information you provide when you visit our website or contact us.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Information We Collect</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 15px;">
        We may collect personal information that you voluntarily provide, including:
      </p>
      <ul style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 20px; padding-left: 20px;">
        <li>Name</li>
        <li>Phone number</li>
        <li>Email address</li>
        <li>Property address</li>
        <li>Any information you include in contact forms or service requests</li>
      </ul>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        We may also collect non-personal information such as your IP address, browser type, device information, and website usage data to help improve our website and services.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">How We Use Your Information</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 15px;">
        We use your information to:
      </p>
      <ul style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px; padding-left: 20px;">
        <li>Respond to your inquiries</li>
        <li>Provide roofing inspections, estimates, and services</li>
        <li>Schedule appointments</li>
        <li>Improve our website and customer experience</li>
        <li>Send service updates or follow up regarding your request</li>
        <li>Comply with applicable legal obligations</li>
      </ul>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Information Sharing</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        Ramos Roofing does not sell, rent, or trade your personal information. We may share your information with trusted third-party service providers who help us operate our business or when required by law.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Cookies</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        Our website may use cookies and similar technologies to improve your browsing experience and analyze website traffic. You can modify your browser settings to refuse cookies if you prefer.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Data Security</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        We take reasonable administrative, technical, and physical measures to protect your personal information from unauthorized access, disclosure, or misuse. However, no method of transmitting information over the internet or storing electronic data is completely secure.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Third-Party Links</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        Our website may contain links to third-party websites. We are not responsible for the privacy practices or content of those websites.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Your Rights</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        You may contact us at any time to request access to, correction of, or deletion of your personal information, subject to applicable laws.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Changes to This Privacy Policy</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 30px;">
        We may update this Privacy Policy from time to time. Any changes will be posted on this page along with the revised effective date.
      </p>

      <h2 style="font-family: var(--font-headings); color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; font-size: 1.8rem;">Contact Us</h2>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 15px;">
        If you have any questions regarding this Privacy Policy or how we handle your information, please contact us:
      </p>
      
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 5px;"><strong>Ramos Roofing</strong></p>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 5px;"><strong>Email:</strong> <a href="mailto:info@ramosroofingplus.com" style="color: var(--accent-primary); text-decoration: underline;">info@ramosroofingplus.com</a></p>
      <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 5px;"><strong>Phone:</strong></p>
      <ul style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 60px; padding-left: 20px;">
        <li>Brandon: (479) 652-1424</li>
        <li>Austin: (479) 221-8420</li>
      </ul>
    </div>
  </section>
"""
    
    final_content = header_part + privacy_content + footer_part
    
    with open(r'r:\AI Website Development\Professional\RamosRoofing-main\RamosRoofing-main\privacy-policy.html', 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print("privacy-policy.html created successfully.")
    
def update_footer_links():
    directory = r'r:\AI Website Development\Professional\RamosRoofing-main\RamosRoofing-main'
    
    files_updated = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace root level links
                new_content = content.replace(
                    '<a href="about.html">Privacy Policy</a>', 
                    '<a href="privacy-policy.html">Privacy Policy</a>'
                )
                
                # Replace sub-directory links
                new_content = new_content.replace(
                    '<a href="../about.html">Privacy Policy</a>', 
                    '<a href="../privacy-policy.html">Privacy Policy</a>'
                )
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_updated += 1
                    
    print(f"Updated {files_updated} footer links successfully.")

if __name__ == '__main__':
    create_privacy_page()
    update_footer_links()

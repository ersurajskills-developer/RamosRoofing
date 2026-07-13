import os, re

# Matches hero section
hero_section_pattern = re.compile(
    r'(<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*>)(.*?)(</section>)',
    re.DOTALL
)

files_changed = 0

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            match = hero_section_pattern.search(content)
            if not match:
                continue

            section_open = match.group(1)
            inner_html = match.group(2)
            section_close = match.group(3)

            # Change rgba(0, 0, 0, 0.8) to rgba(0, 0, 0, 0.6)
            new_inner, count = re.subn(r'rgba\(0,\s*0,\s*0,\s*0\.8\)', 'rgba(0, 0, 0, 0.6)', inner_html)
            
            if count > 0:
                new_section = section_open + new_inner + section_close
                new_content = content[:match.start()] + new_section + content[match.end():]
                with open(filepath, 'w', encoding='utf-8') as out:
                    out.write(new_content)
                print(f"Updated overlay opacity to 0.6: {filepath}")
                files_changed += 1

print(f"\nTotal files updated: {files_changed}")

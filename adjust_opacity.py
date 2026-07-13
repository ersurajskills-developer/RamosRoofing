import os, re

hero_pattern = re.compile(r'(<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*>)(.*?)</section>', re.DOTALL)
opacity_pattern = re.compile(r'opacity:\s*0\.\d+;')

files_changed = 0

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
            match = hero_pattern.search(content)
            if match:
                section_tag = match.group(1)
                inner_html = match.group(2)
                
                # Check for opacity in the inner HTML
                new_inner, count = opacity_pattern.subn('opacity: 0.8;', inner_html)
                if count > 0:
                    new_section = section_tag + new_inner + "</section>"
                    new_content = content[:match.start()] + new_section + content[match.end():]
                    with open(filepath, 'w', encoding='utf-8') as out_file:
                        out_file.write(new_content)
                    print(f"Updated {filepath} (replaced {count} opacity properties)")
                    files_changed += 1

print(f"Total files updated: {files_changed}")

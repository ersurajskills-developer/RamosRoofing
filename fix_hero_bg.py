import os, re

# Matches hero section opening tag that has a background-color inline style
hero_open_pattern = re.compile(
    r'(<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*style=")([^"]*?)(")',
)

files_changed = 0

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            # Only process if there's a video in the file
            if '<video' not in content:
                continue

            def fix_bg(m):
                style = m.group(2)
                # Remove any solid background-color from section so video shows through
                style = re.sub(r'background-color:\s*[^;]+;?\s*', '', style)
                style = re.sub(r'background:\s*(?!transparent)[^;]+;?\s*', '', style)
                # Add transparent background
                style = style.rstrip('; ') + '; background: transparent !important;'
                return m.group(1) + style + m.group(3)

            new_content, n = hero_open_pattern.subn(fix_bg, content)

            if n > 0 and new_content != content:
                with open(filepath, 'w', encoding='utf-8') as out:
                    out.write(new_content)
                print(f"Fixed background on {filepath}")
                files_changed += 1

print(f"\nTotal files fixed: {files_changed}")

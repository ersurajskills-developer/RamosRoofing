import os, re

# Matches hero section
hero_section_pattern = re.compile(
    r'(<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*>)(.*?)(</section>)',
    re.DOTALL
)

# The overlay HTML to inject (z-index: 2 sits above video at z-index 1, container must be at z-index 3)
OVERLAY = '    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); z-index: 2;"></div>\n'

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

            # Only process pages with a video in hero
            if '<video' not in inner_html:
                continue

            # Skip if overlay already exists
            if 'rgba(0, 0, 0, 0.8)' in inner_html or 'rgba(0,0,0,0.8)' in inner_html:
                print(f"Skipped (already has overlay): {filepath}")
                continue

            # Ensure container has z-index: 3 so it sits above the overlay (z-index: 2)
            inner_html = re.sub(
                r'(class="[^"]*container[^"]*"[^>]*style=")([^"]*z-index:\s*)(\d+)',
                lambda m: m.group(1) + m.group(2) + '3',
                inner_html
            )

            # Find the end of the video wrapper </div> and inject overlay right after it
            # Video wrapper pattern: <div ...><video ...></video></div>
            video_wrapper_end = re.search(r'(</video>\s*</div>)', inner_html, re.DOTALL)
            if video_wrapper_end:
                insert_pos = video_wrapper_end.end()
                inner_html = inner_html[:insert_pos] + '\n' + OVERLAY + inner_html[insert_pos:]
                changed = True
            else:
                # Fallback: inject after </video>
                video_end = re.search(r'(</video>)', inner_html, re.DOTALL)
                if video_end:
                    insert_pos = video_end.end()
                    inner_html = inner_html[:insert_pos] + '\n' + OVERLAY + inner_html[insert_pos:]
                    changed = True
                else:
                    changed = False

            if changed:
                new_section = section_open + inner_html + section_close
                new_content = content[:match.start()] + new_section + content[match.end():]
                with open(filepath, 'w', encoding='utf-8') as out:
                    out.write(new_content)
                print(f"Added overlay: {filepath}")
                files_changed += 1

print(f"\nTotal files updated: {files_changed}")

import os, re

# Matches the hero section
hero_section_pattern = re.compile(
    r'(<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*>)(.*?)(</section>)',
    re.DOTALL
)

# Case 1: Video wrapped in a div — update the opacity on that div
# e.g.: <div style="... opacity: 0.X; ..."><video ...>
video_in_div_opacity = re.compile(
    r'(<div[^>]*style="[^"]*)(opacity:\s*[\d.]+)(;[^"]*"[^>]*>\s*<video)',
    re.DOTALL
)

# Case 2: Video directly in section (no wrapper div with opacity)
# e.g.: <video autoplay ... style="position: absolute; ...">
bare_video_pattern = re.compile(
    r'(<video\b[^>]*style=")(.*?)(")',
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

            # Only process if a video exists
            if '<video' not in inner_html:
                continue

            changed = False

            # Case 1: video is inside a wrapper div that has opacity
            if video_in_div_opacity.search(inner_html):
                new_inner, n = video_in_div_opacity.subn(
                    lambda m: m.group(1) + 'opacity: 0.8' + m.group(3),
                    inner_html
                )
                if n > 0:
                    inner_html = new_inner
                    changed = True
                    print(f"[Case 1 - wrapper div] Updated {filepath}")

            # Case 2: video tag is direct child of section (no wrapper div opacity)
            # Add opacity: 0.8 to the video's own style
            elif bare_video_pattern.search(inner_html):
                def add_opacity(m):
                    style = m.group(2)
                    if 'opacity' in style:
                        style = re.sub(r'opacity:\s*[\d.]+', 'opacity: 0.8', style)
                    else:
                        style = style.rstrip('; ') + '; opacity: 0.8;'
                    return m.group(1) + style + m.group(3)

                new_inner = bare_video_pattern.sub(add_opacity, inner_html)
                if new_inner != inner_html:
                    inner_html = new_inner
                    changed = True
                    print(f"[Case 2 - bare video] Updated {filepath}")

            if changed:
                new_section = section_open + inner_html + section_close
                new_content = content[:match.start()] + new_section + content[match.end():]
                with open(filepath, 'w', encoding='utf-8') as out:
                    out.write(new_content)
                files_changed += 1

print(f"\nTotal files updated: {files_changed}")

import os, re

hero_pattern = re.compile(r'(<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*>)(.*?)</section>', re.DOTALL)
container_pattern = re.compile(r'(<div[^>]*class="[^"]*container[^"]*"[^>]*>)')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = hero_pattern.search(content)
    if not match:
        return

    section_tag = match.group(1)
    inner_html = match.group(2)

    # Check if media already exists
    if re.search(r'<(img|video)\b', inner_html, re.IGNORECASE):
        return

    # Determine image path based on directory depth
    depth = filepath.count(os.sep)
    if depth == 1:
        img_src = "./Images/compressed/IMG_0547.webp"
    else:
        img_src = "../" * (depth - 1) + "Images/compressed/IMG_0547.webp"

    # Fix section tag to have relative positioning and overflow hidden
    if 'style="' in section_tag:
        if 'position: relative' not in section_tag:
            section_tag = section_tag.replace('style="', 'style="position: relative; overflow: hidden; ')
    else:
        section_tag = section_tag[:-1] + ' style="position: relative; overflow: hidden;">'
        
    # Ensure background color is transparent so it doesn't block the image
    if 'background' in section_tag and 'transparent' not in section_tag:
        section_tag = re.sub(r'background(?:-color)?:\s*[^;]+;', 'background: transparent !important;', section_tag)

    media_html = f"""
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; opacity: 0.6;">
      <img src="{img_src}" alt="Hero Background" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top:0; left:0; filter: brightness(0.6);">
    </div>
"""

    # Add z-index to container
    container_match = container_pattern.search(inner_html)
    if container_match:
        container_tag = container_match.group(1)
        if 'style="' in container_tag:
            if 'position: relative' not in container_tag:
                new_container = container_tag.replace('style="', 'style="position: relative; z-index: 2; ')
            else:
                new_container = container_tag.replace('style="', 'style="z-index: 2; ')
        else:
            new_container = container_tag[:-1] + ' style="position: relative; z-index: 2;">'
        inner_html = inner_html.replace(container_tag, new_container, 1)

    new_section = section_tag + media_html + inner_html + "</section>"
    
    new_content = content[:match.start()] + new_section + content[match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            process_file(os.path.join(root, f))

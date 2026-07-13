import os, re

hero_pattern = re.compile(r'<section[^>]*class="[^"]*inner-page-hero[^"]*"[^>]*>(.*?)</section>', re.DOTALL)
media_pattern = re.compile(r'<(img|video)\b', re.IGNORECASE)

missing_media = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                match = hero_pattern.search(content)
                if match:
                    hero_content = match.group(1)
                    if not media_pattern.search(hero_content):
                        missing_media.append(path)

print(f'Found {len(missing_media)} files missing hero media:')
for m in missing_media:
    print(m)

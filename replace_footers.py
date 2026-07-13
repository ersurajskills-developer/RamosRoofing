import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

footer_match = re.search(r'<footer class="main-footer">.*?</footer>', index_content, re.DOTALL)
if not footer_match:
    print("Could not find footer in index.html")
    exit(1)

base_footer = footer_match.group(0)

def adjust_footer_for_depth(footer_html, depth):
    if depth == 0:
        return footer_html
    
    prefix = '../' * depth
    
    def repl(m):
        url = m.group(1)
        if url.startswith('http') or url.startswith('tel:') or url.startswith('mailto:') or url.startswith('#') or url.startswith('/'):
            return f'href="{url}"'
        return f'href="{prefix}{url}"'
    
    return re.sub(r'href="([^"]+)"', repl, footer_html)

for root, dirs, files in os.walk('.'):
    # skip .git or other hidden dirs
    if '.git' in root:
        continue
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            filepath = os.path.join(root, file)
            # Calculate depth: '.' is root, './services' is depth 1
            # Using os.path.relpath
            relpath = os.path.relpath(filepath, '.')
            parts = relpath.split(os.sep)
            depth = len(parts) - 1
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_footer = adjust_footer_for_depth(base_footer, depth)
            
            new_content = re.sub(r'<footer[^>]*>.*?</footer>', new_footer, content, flags=re.DOTALL)
            
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated footer in {filepath}")

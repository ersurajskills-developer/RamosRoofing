import os
import re

def get_home_header(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match top-bar and header
    # The header in index.html starts with <div class="top-bar"> and ends with </header>
    pattern = re.compile(
        r'(<div class="top-bar">.*?</header>)',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not find top-bar and header in index.html")

def adjust_links_for_subdirectories(header_html):
    # This function adjusts links in the header for files that are exactly 1 directory deep
    # (e.g., services/, locations/, resources/)
    
    # Links to index.html
    header_html = re.sub(r'href="index\.html"', 'href="../index.html"', header_html)
    # Links to about.html
    header_html = re.sub(r'href="about\.html"', 'href="../about.html"', header_html)
    # Links to before-after.html
    header_html = re.sub(r'href="before-after\.html"', 'href="../before-after.html"', header_html)
    # Links to reviews.html
    header_html = re.sub(r'href="reviews\.html"', 'href="../reviews.html"', header_html)
    
    # Links to directories
    header_html = re.sub(r'href="services/', 'href="../services/', header_html)
    header_html = re.sub(r'href="locations/', 'href="../locations/', header_html)
    header_html = re.sub(r'href="resources/', 'href="../resources/', header_html)
    
    # In case there are images inside the header
    header_html = re.sub(r'src="Images/', 'src="../Images/', header_html)
    header_html = re.sub(r'src="images/', 'src="../images/', header_html)

    return header_html

def process_files(directory):
    index_path = os.path.join(directory, 'index.html')
    home_header = get_home_header(index_path)
    sub_header = adjust_links_for_subdirectories(home_header)
    
    header_pattern = re.compile(
        r'(<!-- Top Bar -->|<div class="top-bar">).*?(</header>)',
        re.DOTALL
    )

    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                
                # Check depth
                rel_path = os.path.relpath(filepath, directory)
                depth = rel_path.count(os.sep)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                match = header_pattern.search(content)
                if not match:
                    # Some files might not have top-bar, try just header
                    alt_pattern = re.compile(r'<header[^>]*>.*?</header>', re.DOTALL)
                    match = alt_pattern.search(content)
                
                if match:
                    header_to_use = home_header if depth == 0 else sub_header
                    
                    new_content = content[:match.start()] + header_to_use + content[match.end():]
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated header in: {rel_path}")
                    count += 1
                else:
                    print(f"Could not find header in: {rel_path}")
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    process_files('.')

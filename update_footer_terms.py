import os

def update_terms():
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
                    '<a href="about.html">Terms of Use</a>', 
                    '<a href="terms-and-conditions.html">Terms &amp; Conditions</a>'
                )
                
                # Replace sub-directory links
                new_content = new_content.replace(
                    '<a href="../about.html">Terms of Use</a>', 
                    '<a href="../terms-and-conditions.html">Terms &amp; Conditions</a>'
                )
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_updated += 1
                    
    print(f"Updated {files_updated} files successfully.")

if __name__ == '__main__':
    update_terms()

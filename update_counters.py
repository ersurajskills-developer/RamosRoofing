import os

files_to_update = [
    'services/emergency-tarping.html',
    'services/roof-repair.html',
    'services/siding-replacement.html'
]

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Interactive counters replacements
        content = content.replace('<section class="section section-bg-alt" style="padding: 80px 0; text-align: center;">', 
                                  '<section class="section" style="padding: 80px 0; text-align: center; background-color: #000000;">')
        
        # In these counters, numbers are var(--accent-primary) which is gold, let's strictly set #D4AF37
        content = content.replace('color: var(--accent-primary);', 'color: #D4AF37;')
        
        # Texts are var(--text-primary), let's set to white
        content = content.replace('color: var(--text-primary);', 'color: #ffffff;')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')

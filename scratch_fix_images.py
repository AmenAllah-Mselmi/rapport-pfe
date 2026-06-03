import os, re, glob

existing_images = set(os.listdir('images'))

for tex_file in glob.glob('*.tex'):
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def repl(match):
        img_filename = match.group(1)
        if img_filename not in existing_images:
            print(f"Commenting out missing image {img_filename} in {tex_file}")
            return "% " + match.group(0)
        return match.group(0)
    
    new_content = re.sub(r'\\includegraphics(?:\[.*?\])?\{images/([^}]+)\}', repl, content)
    if new_content != content:
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

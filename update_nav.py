import glob
import re

files = ['index.html', '404.html', 'about.html', 'contact.html', 'disclaimer.html', 'privacy.html', 'terms.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # We want to replace the exact block of nav elements
    old_nav_block = '''<nav class="nav" id="site-nav">
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </nav>'''
      
    # It might have active states, so let's do a regex replacement on the contents of the nav
    # The block starts with <nav class="nav" id="site-nav"> and ends with </nav>
    
    def replacer(match):
        inner = match.group(1)
        if 'budget-calculator.html' in inner:
            return match.group(0) # Already updated
        
        # Determine active states based on filename
        is_home = 'class="active"' if f == 'index.html' else ''
        is_about = 'class="active"' if f == 'about.html' else ''
        is_contact = 'class="active"' if f == 'contact.html' else ''
        
        new_nav = f'''<nav class="nav" id="site-nav">
        <a href="/index.html" {is_home}>Home</a>
        <a href="/budget-calculator.html">Tools</a>
        <a href="/about.html" {is_about}>About</a>
        <a href="/contact.html" {is_contact}>Contact</a>
      </nav>'''
        
        # Since 404 has absolute paths like href="/index.html", we need to accommodate that.
        prefix = '/' if f == '404.html' else ''
        new_nav = f'''<nav class="nav" id="site-nav">
        <a href="{prefix}index.html" {is_home}>Home</a>
        <a href="{prefix}budget-calculator.html">Tools</a>
        <a href="{prefix}about.html" {is_about}>About</a>
        <a href="{prefix}contact.html" {is_contact}>Contact</a>
      </nav>'''
        
        # Wait, if we just use string replace on the actual links it's easier.
        return new_nav.replace('  ', ' ')
        
    # Better approach: Regex to find the <nav> block
    pattern = re.compile(r'<nav class="nav" id="site-nav">(.*?)</nav>', re.DOTALL)
    
    def replace_nav(match):
        inner = match.group(1)
        if 'budget-calculator.html' in inner:
            return match.group(0)
            
        # Keep existing active classes on Home/About/Contact
        lines = inner.split('\n')
        new_lines = []
        for line in lines:
            if 'index.html' in line:
                new_lines.append(line)
                prefix = '/' if 'href="/index.html"' in line else ''
                new_lines.append(f'        <a href="{prefix}budget-calculator.html">Tools</a>')
            else:
                new_lines.append(line)
                
        return '<nav class="nav" id="site-nav">' + '\n'.join(new_lines) + '</nav>'
        
    new_content = pattern.sub(replace_nav, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
    print(f"Updated nav in {f}")

import glob
import re

files = glob.glob('*.html')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the Tools link with a Dropdown-style text (or just add the second tool if we don't have a real CSS dropdown)
    # Since we don't want to mess with CSS, we will just add the second tool link next to the first one in the Nav.
    
    pattern = re.compile(r'<a href="([^"]*)budget-calculator\.html"(.*?)>Tools</a>')
    
    def replacer(match):
        prefix = match.group(1)
        # If we are on hotel-compare, make it active
        compare_active = ' class="active"' if f == 'hotel-compare.html' else ''
        calc_active = ' class="active"' if f == 'budget-calculator.html' else ''
        
        return f'<a href="{prefix}budget-calculator.html"{calc_active}>Budget Calc</a>\n        <a href="{prefix}hotel-compare.html"{compare_active}>Rate Compare</a>'
        
    new_content = pattern.sub(replacer, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
        
print("Updated all navs")

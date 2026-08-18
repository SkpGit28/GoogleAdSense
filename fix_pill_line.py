import re

with open('tools.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to target the Most Popular header inside tools.html
old_div = '''<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: var(--s-2);">
                <h2 style="margin: 0; line-height: 1.2;">Hotel Rate & Hidden Cost Comparator</h2>
                <div style="background: var(--signal); color: var(--ink); padding: 4px 10px; border-radius: 12px; font-weight: bold; font-family: var(--font-ui); font-size: 11px; white-space: nowrap; flex-shrink: 0; margin-top: 4px;">Most Popular</div>
            </div>'''

# Add the bottom border to the flex container and pull it out to full bleed using negative margins
new_div = '''<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; border-bottom: 2px solid var(--signal); padding: 0 var(--s-5) 12px; margin: 0 calc(-1 * var(--s-5)) var(--s-4);">
                <h2 style="margin: 0; line-height: 1.2;">Hotel Rate & Hidden Cost Comparator</h2>
                <div style="background: var(--signal); color: var(--ink); padding: 4px 10px; border-radius: 12px; font-weight: bold; font-family: var(--font-ui); font-size: 11px; white-space: nowrap; flex-shrink: 0; margin-top: 4px;">Most Popular</div>
            </div>'''

html = html.replace(old_div, new_div)

with open('tools.html', 'w', encoding='utf-8') as f:
    f.write(html)

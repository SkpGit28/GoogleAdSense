import re

with open('tools.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The old HTML layout for the card header
old_html = '''<div style="background: var(--signal); color: var(--ink); display: inline-block; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-family: var(--font-ui); font-size: var(--t-xs); margin-bottom: var(--s-3);">Most Popular</div>
            <h2 style="margin-top: 0; margin-bottom: var(--s-2);">Hotel Rate & Hidden Cost Comparator</h2>'''

# The new HTML layout using flexbox to align them horizontally
new_html = '''<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: var(--s-2);">
                <h2 style="margin: 0; line-height: 1.2;">Hotel Rate & Hidden Cost Comparator</h2>
                <div style="background: var(--signal); color: var(--ink); padding: 4px 10px; border-radius: 12px; font-weight: bold; font-family: var(--font-ui); font-size: 11px; white-space: nowrap; flex-shrink: 0; margin-top: 4px;">Most Popular</div>
            </div>'''

html = html.replace(old_html, new_html)

with open('tools.html', 'w', encoding='utf-8') as f:
    f.write(html)

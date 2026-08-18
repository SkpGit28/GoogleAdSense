import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Instead of border-bottom on the text tag, let's wrap the column content properly 
# so the border spans the full width of the padded container.

# Replace Hotel A Header
old_a = '<h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--signal); padding-bottom: 8px; width: 100%; display: block; box-sizing: border-box;">Hotel A</h3>'
new_a = '<div style="border-bottom: 2px solid var(--signal); padding-bottom: 8px; margin-bottom: var(--s-4); width: 100%;"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'
html = html.replace(old_a, new_a)

# Replace Hotel B Header
old_b = '<h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--ink-muted); padding-bottom: 8px; width: 100%; display: block; box-sizing: border-box;">Hotel B</h3>'
new_b = '<div style="border-bottom: 2px solid var(--ink-muted); padding-bottom: 8px; margin-bottom: var(--s-4); width: 100%;"><h3 style="margin: 0; color: var(--ink);">Hotel B</h3></div>'
html = html.replace(old_b, new_b)

# Clean up the extra margin-top we don't need anymore
html = html.replace('<div style="display: flex; flex-direction: column; gap: var(--s-3); margin-top: var(--s-4);">', '<div style="display: flex; flex-direction: column; gap: var(--s-3);">')

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

import re

with open('tools.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the border, padding, and negative margins entirely so it matches the Trip Budget Calculator
old_div = '<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; border-bottom: 2px solid var(--rule); padding: 0 var(--s-5) 12px; margin: 0 calc(-1 * var(--s-5)) var(--s-4);">'
new_div = '<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: var(--s-2);">'

html = html.replace(old_div, new_div)

with open('tools.html', 'w', encoding='utf-8') as f:
    f.write(html)

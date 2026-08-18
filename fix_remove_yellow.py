import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the yellow (var(--signal)) line under Hotel A with the exact same black/grey (var(--ink-muted)) line used for Hotel B
old_a = '<div style="border-bottom: 2px solid var(--signal); padding: 0 var(--s-4) 12px; margin-left: calc(-1 * var(--s-4)); margin-right: calc(-1 * var(--s-4)); margin-bottom: var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'
new_a = '<div style="border-bottom: 2px solid var(--ink-muted); padding: 0 var(--s-4) 12px; margin-left: calc(-1 * var(--s-4)); margin-right: calc(-1 * var(--s-4)); margin-bottom: var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'

html = html.replace(old_a, new_a)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

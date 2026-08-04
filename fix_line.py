import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Hotel A Column header line
html = html.replace(
    '<h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--signal); padding-bottom: 8px;">Hotel A</h3>',
    '<h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--signal); padding-bottom: 8px; width: 100%; display: block; box-sizing: border-box;">Hotel A</h3>'
)

# Fix Hotel B Column header line
html = html.replace(
    '<h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--ink-muted); padding-bottom: 8px;">Hotel B</h3>',
    '<h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--ink-muted); padding-bottom: 8px; width: 100%; display: block; box-sizing: border-box;">Hotel B</h3>'
)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

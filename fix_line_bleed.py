import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# To achieve true full bleed, we have to pull the border out of the padding 
# of the parent container by using negative margins on the wrapping div.
# var(--s-4) in your CSS usually maps to 1rem or 1.5rem (approx 16-24px padding).

old_a_div = '<div style="border-bottom: 2px solid var(--signal); padding-bottom: 8px; margin-bottom: var(--s-4); width: 100%;"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'
new_a_div = '<div style="border-bottom: 2px solid var(--signal); padding: 0 var(--s-4) 12px; margin: 0 calc(-1 * var(--s-4)) var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'
html = html.replace(old_a_div, new_a_div)

old_b_div = '<div style="border-bottom: 2px solid var(--ink-muted); padding-bottom: 8px; margin-bottom: var(--s-4); width: 100%;"><h3 style="margin: 0; color: var(--ink);">Hotel B</h3></div>'
new_b_div = '<div style="border-bottom: 2px solid var(--ink-muted); padding: 0 var(--s-4) 12px; margin: 0 calc(-1 * var(--s-4)) var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel B</h3></div>'
html = html.replace(old_b_div, new_b_div)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's check Hotel A's header in hotel-compare.html. 
# In the image you sent previously, Hotel A had a yellow line, but the yellow line WAS NOT full bleed. 
# Hotel B had a black line, and the black line WAS full bleed. 
# Ah! I see! In my previous fix, Hotel A's yellow line must not be rendering as full bleed for some reason, 
# or I missed it, while Hotel B's line IS full bleed.

# Let's explicitly force BOTH Hotel A and Hotel B headers to use absolute negative margins that match exactly.

# Find Hotel A's header div and replace it with a foolproof full-bleed implementation.
# In CSS, if padding is var(--s-4), we do margin-left: calc(-1 * var(--s-4)); margin-right: calc(-1 * var(--s-4));

old_a = '<div style="border-bottom: 2px solid var(--signal); padding: 0 var(--s-4) 12px; margin: 0 calc(-1 * var(--s-4)) var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'
new_a = '<div style="border-bottom: 2px solid var(--signal); padding: 0 var(--s-4) 12px; margin-left: calc(-1 * var(--s-4)); margin-right: calc(-1 * var(--s-4)); margin-bottom: var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel A</h3></div>'
html = html.replace(old_a, new_a)

old_b = '<div style="border-bottom: 2px solid var(--ink-muted); padding: 0 var(--s-4) 12px; margin: 0 calc(-1 * var(--s-4)) var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel B</h3></div>'
new_b = '<div style="border-bottom: 2px solid var(--ink-muted); padding: 0 var(--s-4) 12px; margin-left: calc(-1 * var(--s-4)); margin-right: calc(-1 * var(--s-4)); margin-bottom: var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel B</h3></div>'
html = html.replace(old_b, new_b)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

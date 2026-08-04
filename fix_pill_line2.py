import re

with open('tools.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First, revert the yellow full bleed line I just added back to the standard flexbox without a bottom border
wrong_div = '''<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; border-bottom: 2px solid var(--signal); padding: 0 var(--s-5) 12px; margin: 0 calc(-1 * var(--s-5)) var(--s-4);">
                <h2 style="margin: 0; line-height: 1.2;">Hotel Rate & Hidden Cost Comparator</h2>
                <div style="background: var(--signal); color: var(--ink); padding: 4px 10px; border-radius: 12px; font-weight: bold; font-family: var(--font-ui); font-size: 11px; white-space: nowrap; flex-shrink: 0; margin-top: 4px;">Most Popular</div>
            </div>'''

correct_no_border = '''<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: var(--s-2);">
                <h2 style="margin: 0; line-height: 1.2;">Hotel Rate & Hidden Cost Comparator</h2>
                <div style="background: var(--signal); color: var(--ink); padding: 4px 10px; border-radius: 12px; font-weight: bold; font-family: var(--font-ui); font-size: 11px; white-space: nowrap; flex-shrink: 0; margin-top: 4px;">Most Popular</div>
            </div>'''
            
html = html.replace(wrong_div, correct_no_border)

# NOW, address what you actually meant: The black line under the "True Cost Breakdown" heading in hotel-compare.html
# Oh wait, let's check what the user meant by "the black underline under the heading to be full widht of the parent container as the other component does".
# Let's open hotel-compare.html and fix the True Cost Breakdown heading.
with open('hotel-compare.html', 'r', encoding='utf-8') as f2:
    html2 = f2.read()

# The True Cost Breakdown header is currently inside a div with background: var(--ink) 
# Wait, "the black underline under the heading" - in tools.html there is no black underline. 
# In hotel-compare.html, Hotel A has a yellow line, Hotel B has a black/ink-muted line.
# Let's look at the True Cost Breakdown section.
# <div style="background: var(--ink); color: #fff; padding: 12px var(--s-4); font-weight: bold; font-family: var(--font-ui);">True Cost Breakdown</div>

# Or maybe the user meant the "Most Popular" pill in tools.html SHOULD NOT have an underline, but something else should?
# Let's read the user message carefully: "removev that yellow underline i was talking about the black underline under the heading to be full widht of the parent container as the other component does"

# "the black underline under the heading"
# Let's look at tools.html again. Does it have a black underline? No.
# Does budget-calculator.html have a black underline? 
with open('budget-calculator.html', 'r', encoding='utf-8') as f3:
    html3 = f3.read()
#  <h3 style="margin-top: 0;">Suggested Allocation</h3>
# <div id="results" style="display: none; margin-top: var(--s-6); padding-top: var(--s-6); border-top: 1px solid #ccc;">

# Let's look at hotel-compare.html. 
# Hotel B has <div style="border-bottom: 2px solid var(--ink-muted); padding: 0 var(--s-4) 12px; margin: 0 calc(-1 * var(--s-4)) var(--s-4);"><h3 style="margin: 0; color: var(--ink);">Hotel B</h3></div>
# This is a grey/black line under Hotel B. It is ALREADY full bleed because we fixed it in the previous step.

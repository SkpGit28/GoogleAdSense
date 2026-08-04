import re

# 1. Optimize hotel-compare.html
with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add responsive CSS to the head
css = '''
  <style>
    @media (max-width: 768px) {
      .responsive-grid { grid-template-columns: 1fr !important; }
      .table-wrapper { overflow-x: auto !important; }
    }
  </style>
</head>'''
html = html.replace('</head>', css)

# Make the 2-column layout stack on mobile
html = html.replace('style="display: grid; grid-template-columns: 1fr 1fr;', 'class="responsive-grid" style="display: grid; grid-template-columns: 1fr 1fr;')

# Add horizontal scrolling to the True Cost Breakdown table wrapper
html = html.replace('overflow: hidden;">', 'overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch;" class="table-wrapper">')

# Add a min-width to the table so it actually triggers the scrollbar instead of squishing the text into unreadable vertical columns
html = html.replace('<table style="width: 100%;', '<table style="width: 100%; min-width: 500px;')

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Optimize budget-calculator.html
with open('budget-calculator.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('</head>', css)
html = html.replace('style="display: grid; grid-template-columns: 1fr 1fr;', 'class="responsive-grid" style="display: grid; grid-template-columns: 1fr 1fr;')

with open('budget-calculator.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 3. Optimize price-inflator.html
with open('price-inflator.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('</head>', css)
# The price inflator has the style tags mixed up, we will just use regex to insert the class
html = re.sub(r'(display:\s*grid;\s*grid-template-columns:\s*1fr 1fr;)', r'\1" class="responsive-grid', html)
# Wait, actually it's easier to inject the class right into the div
html = html.replace('<div style="background: var(--paper-sunk); padding: var(--s-5); border: 1px solid var(--rule); border-radius: 8px; margin-top: var(--s-5); display: grid; grid-template-columns: 1fr 1fr;', '<div class="responsive-grid" style="background: var(--paper-sunk); padding: var(--s-5); border: 1px solid var(--rule); border-radius: 8px; margin-top: var(--s-5); display: grid; grid-template-columns: 1fr 1fr;')

with open('price-inflator.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Mobile optimizations applied!")

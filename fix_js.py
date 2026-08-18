import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken template literals from the powershell string escaping issue
broken1 = 'verdictEl.innerHTML = ?? <strong>Trap Avoided:</strong> The advertised rate for the cheaper hotel was a lie due to taxes/fees. <strong></strong> is actually cheaper by  overall.;'
fixed1 = 'verdictEl.innerHTML = 🚨 <strong>Trap Avoided:</strong> The advertised rate for the cheaper hotel was a lie due to taxes/fees. <strong></strong> is actually cheaper by  overall.;'

broken2 = 'verdictEl.innerHTML = ?? <strong></strong> is cheaper by  for the total stay.;'
fixed2 = 'verdictEl.innerHTML = 💡 <strong></strong> is cheaper by  for the total stay.;'

broken3 = 'verdictEl.innerHTML = Enter rates for both hotels to see the comparison.;'
fixed3 = 'verdictEl.innerHTML = Enter rates for both hotels to see the comparison.;'

html = html.replace(broken1, fixed1)
html = html.replace(broken2, fixed2)
html = html.replace(broken3, fixed3)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

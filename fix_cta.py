import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add a CTA button just above the Results Section
cta_button = '''
        <div style="margin-top: var(--s-5); text-align: center;">
            <button onclick="calcCompare()" style="background: var(--ink); color: #fff; border: none; padding: 14px 32px; font-size: var(--t-md); font-weight: 700; border-radius: 6px; cursor: pointer; font-family: var(--font-ui); transition: transform 0.1s, opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'" onmousedown="this.style.transform='scale(0.98)'" onmouseup="this.style.transform='scale(1)'">Calculate True Cost</button>
        </div>

        <!-- Results Section -->
'''
html = html.replace('<!-- Results Section -->', cta_button)

# Also fix the initial load state so if a user pastes numbers without typing, it calculates
script_fix = '''
    function calcCompare() {
'''
script_fixed = '''
    // Auto-calculate on load just in case values are pre-filled by browser
    document.addEventListener('DOMContentLoaded', calcCompare);

    function calcCompare() {
'''
html = html.replace(script_fix, script_fixed)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

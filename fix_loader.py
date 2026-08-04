import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add standard CSS keyframes for rotation in the head
spin_css = '''  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6151386626480770" crossorigin="anonymous"></script>
  <style>
    @keyframes spin {
      100% { transform: rotate(360deg); }
    }
  </style>'''
html = html.replace('  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6151386626480770" crossorigin="anonymous"></script>', spin_css)

# Update the button HTML to give it an ID and a span for the text and SVG
button_old = '<button onclick="scrollToResults()" style="background: var(--ink); color: #fff; border: none; padding: 14px 32px; font-size: var(--t-md); font-weight: 700; border-radius: 6px; cursor: pointer; font-family: var(--font-ui); transition: transform 0.1s, opacity 0.2s;" onmouseover="this.style.opacity=\'0.9\'" onmouseout="this.style.opacity=\'1\'" onmousedown="this.style.transform=\'scale(0.98)\'" onmouseup="this.style.transform=\'scale(1)\'">Calculate True Cost</button>'
button_new = '''<button id="calcBtn" onclick="simulateCalculation()" style="background: var(--ink); color: #fff; border: none; padding: 14px 32px; font-size: var(--t-md); font-weight: 700; border-radius: 6px; cursor: pointer; font-family: var(--font-ui); transition: transform 0.1s, opacity 0.2s; display: inline-flex; align-items: center; justify-content: center; gap: 8px;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'" onmousedown="this.style.transform='scale(0.98)'" onmouseup="this.style.transform='scale(1)'">
                <svg id="calcSpinner" style="display: none; animation: spin 1.2s linear infinite;" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>
                <span id="calcBtnText">Calculate True Cost</span>
            </button>'''
html = html.replace(button_old, button_new)

# Update the JavaScript block to include the loader logic
new_script = '''
    document.addEventListener('DOMContentLoaded', calcCompare);

    function simulateCalculation() {
        const btn = document.getElementById('calcBtn');
        const spinner = document.getElementById('calcSpinner');
        const text = document.getElementById('calcBtnText');
        
        // Prevent double clicking
        if (btn.disabled) return;
        
        // Step 1: Change to Loading State
        btn.disabled = true;
        btn.style.opacity = "0.7";
        btn.style.cursor = "wait";
        spinner.style.display = "block";
        text.innerText = "Calculating...";
        
        // Step 2: Wait 800ms to simulate complex calculation
        setTimeout(() => {
            // Restore button state
            btn.disabled = false;
            btn.style.opacity = "1";
            btn.style.cursor = "pointer";
            spinner.style.display = "none";
            text.innerText = "Calculate True Cost";
            
            // Execute actual calc and scroll
            scrollToResults();
        }, 800);
    }

    function scrollToResults() {
        calcCompare();
        document.getElementById('res_a_total').scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Add a little highlight flash animation to the total rows
        const a_row = document.getElementById('res_a_total');
        const b_row = document.getElementById('res_b_total');
        
        a_row.style.transition = 'background-color 0.5s';
        b_row.style.transition = 'background-color 0.5s';
        
        const origColor = a_row.style.backgroundColor;
        a_row.style.backgroundColor = '#fff3e0';
        b_row.style.backgroundColor = '#fff3e0';
        
        setTimeout(() => {
            a_row.style.backgroundColor = origColor;
            b_row.style.backgroundColor = origColor;
        }, 800);
    }

    function calcCompare() {
        const a_rate = parseFloat(document.getElementById('a_rate').value) || 0;
        const a_nights = parseInt(document.getElementById('a_nights').value) || 1;
        const a_gst_rate = parseFloat(document.getElementById('a_gst').value);
        const a_fees = parseFloat(document.getElementById('a_fees').value) || 0;

        const b_rate = parseFloat(document.getElementById('b_rate').value) || 0;
        const b_nights = parseInt(document.getElementById('b_nights').value) || 1;
        const b_gst_rate = parseFloat(document.getElementById('b_gst').value);
        const b_fees = parseFloat(document.getElementById('b_fees').value) || 0;

        if (a_rate === 0 && b_rate === 0) {
            document.getElementById('verdict').style.display = 'none';
            return;
        }

        // Auto-update GST brackets based on input rate
        if(a_rate >= 7500) document.getElementById('a_gst').value = "0.18";
        if(a_rate > 0 && a_rate < 7500) document.getElementById('a_gst').value = "0.12";
        if(b_rate >= 7500) document.getElementById('b_gst').value = "0.18";
        if(b_rate > 0 && b_rate < 7500) document.getElementById('b_gst').value = "0.12";

        // Calc A
        const a_base = a_rate * a_nights;
        const a_tax = a_base * parseFloat(document.getElementById('a_gst').value);
        const a_total_fees = a_fees * a_nights;
        const a_total = a_base + a_tax + a_total_fees;

        // Calc B
        const b_base = b_rate * b_nights;
        const b_tax = b_base * parseFloat(document.getElementById('b_gst').value);
        const b_total_fees = b_fees * b_nights;
        const b_total = b_base + b_tax + b_total_fees;

        // Update DOM
        const fmt = (num) => '₹' + Math.round(num).toLocaleString('en-IN');
        
        document.getElementById('res_a_base').innerText = fmt(a_base);
        document.getElementById('res_a_tax').innerText = '+' + fmt(a_tax);
        document.getElementById('res_a_fees').innerText = '+' + fmt(a_total_fees);
        document.getElementById('res_a_total').innerText = fmt(a_total);

        document.getElementById('res_b_base').innerText = fmt(b_base);
        document.getElementById('res_b_tax').innerText = '+' + fmt(b_tax);
        document.getElementById('res_b_fees').innerText = '+' + fmt(b_total_fees);
        document.getElementById('res_b_total').innerText = fmt(b_total);

        // Verdict
        const verdictEl = document.getElementById('verdict');
        verdictEl.style.display = 'block';
        
        if (a_total > 0 && b_total > 0) {
            const diff = Math.abs(a_total - b_total);
            const cheaper = a_total < b_total ? 'Hotel A' : 'Hotel B';
            
            const a_base_cheaper = a_base < b_base;
            const a_total_cheaper = a_total < b_total;
            
            if (a_base_cheaper != a_total_cheaper) {
                verdictEl.innerHTML = "🚨 <strong>Trap Avoided:</strong> The advertised rate for the cheaper hotel was a lie due to taxes/fees. <strong>" + cheaper + "</strong> is actually cheaper by " + fmt(diff) + " overall.";
                verdictEl.style.background = '#fff3e0';
                verdictEl.style.borderLeftColor = '#e65100';
            } else {
                verdictEl.innerHTML = "💡 <strong>" + cheaper + "</strong> is cheaper by " + fmt(diff) + " for the total stay.";
                verdictEl.style.background = '#e8f5e9';
                verdictEl.style.borderLeftColor = '#2e7d32';
            }
        } else {
             verdictEl.innerHTML = "Enter rates for both hotels to see the comparison.";
             verdictEl.style.background = '#f5f5f5';
             verdictEl.style.borderLeftColor = '#9e9e9e';
        }
    }
'''

pattern = re.compile(r'<script>.*?</script>', re.DOTALL)
html = pattern.sub('<script>\n' + new_script + '\n</script>', html)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

import re

with open('hotel-compare.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I am completely overriding the script block using base64 decoding so PowerShell CANNOT mess up backticks or interpolation variables.
import base64

js_code = '''
    // Auto-calculate on load just in case values are pre-filled by browser
    document.addEventListener('DOMContentLoaded', calcCompare);

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

# Update the button to use scrollToResults()
html = html.replace('onclick="calcCompare()"', 'onclick="scrollToResults()"')

pattern = re.compile(r'<script>.*?</script>', re.DOTALL)
html = pattern.sub('<script>' + js_code + '</script>', html)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)


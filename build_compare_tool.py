import re

with open('budget-calculator.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace titles
html = html.replace('India Trip Budget Calculator', 'Hotel Rate & Hidden Cost Comparator')
html = html.replace('Calculate your total India trip budget, including suggested hotel per-night spend based on your travel style.', 'Compare Indian hotels across multiple booking platforms and uncover hidden costs like taxes, resort fees, and mandatory meal plans.')
html = html.replace('budget-calculator.html', 'hotel-compare.html')
html = html.replace('<a href="hotel-compare.html">Tools</a>', '<a href="/budget-calculator.html">Tools</a>\n        <a href="/hotel-compare.html" class="active">Compare</a>')

# Replace the main content
main_content = '''
  <div class="article-header">
    <div class="article-header__inner">
      <h1 class="marker">Hotel Rate & Hidden Cost Comparator</h1>
      <div class="article-meta-bar">
        <span>Interactive Tool</span>
        <span class="badge badge--sourced">Real-time Calculation</span>
      </div>
    </div>
  </div>

  <main id="main" class="legal-page">
    <p>Indian hotel rates advertised on booking platforms rarely show the final price. Use this tool to compare two hotels side-by-side, adding in standard 12-18% GST, resort fees, and mandatory meal plans to reveal the true cost of your stay.</p>

    <div style="background: var(--paper); padding: var(--s-6); border-radius: 8px; border: 1px solid var(--rule); margin-top: var(--s-6); box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--s-6); align-items: start;">
            
            <!-- Hotel A Column -->
            <div style="background: var(--paper-sunk); padding: var(--s-4); border: 1px solid var(--rule); border-radius: 6px;">
                <h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--signal); padding-bottom: 8px;">Hotel A</h3>
                <div style="display: flex; flex-direction: column; gap: var(--s-3); margin-top: var(--s-4);">
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">Advertised Nightly Rate (₹)</label>
                        <input type="number" id="a_rate" placeholder="e.g. 4500" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" oninput="calcCompare()">
                    </div>
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">Nights</label>
                        <input type="number" id="a_nights" value="1" min="1" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" oninput="calcCompare()">
                    </div>
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">GST Bracket</label>
                        <select id="a_gst" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" onchange="calcCompare()">
                            <option value="0.12">12% (Under ₹7,500/night)</option>
                            <option value="0.18">18% (Over ₹7,500/night)</option>
                        </select>
                    </div>
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">Mandatory Fees / Meals (₹ per day)</label>
                        <input type="number" id="a_fees" placeholder="e.g. 1500 for Gala Dinner" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" oninput="calcCompare()">
                    </div>
                </div>
            </div>

            <!-- Hotel B Column -->
            <div style="background: var(--paper-sunk); padding: var(--s-4); border: 1px solid var(--rule); border-radius: 6px;">
                <h3 style="margin-top: 0; color: var(--ink); border-bottom: 2px solid var(--ink-muted); padding-bottom: 8px;">Hotel B</h3>
                <div style="display: flex; flex-direction: column; gap: var(--s-3); margin-top: var(--s-4);">
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">Advertised Nightly Rate (₹)</label>
                        <input type="number" id="b_rate" placeholder="e.g. 5200" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" oninput="calcCompare()">
                    </div>
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">Nights</label>
                        <input type="number" id="b_nights" value="1" min="1" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" oninput="calcCompare()">
                    </div>
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">GST Bracket</label>
                        <select id="b_gst" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" onchange="calcCompare()">
                            <option value="0.12">12% (Under ₹7,500/night)</option>
                            <option value="0.18">18% (Over ₹7,500/night)</option>
                        </select>
                    </div>
                    <div>
                        <label style="display:block; font-weight: 600; font-size: var(--t-sm);">Mandatory Fees / Meals (₹ per day)</label>
                        <input type="number" id="b_fees" placeholder="e.g. 0" style="width: 100%; padding: 8px; border: 1px solid #ccc; font-family: var(--font-ui);" oninput="calcCompare()">
                    </div>
                </div>
            </div>

        </div>

        <!-- Results Section -->
        <div style="margin-top: var(--s-6); border: 2px solid var(--ink); border-radius: 8px; overflow: hidden;">
            <div style="background: var(--ink); color: #fff; padding: 12px var(--s-4); font-weight: bold; font-family: var(--font-ui);">True Cost Breakdown</div>
            
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-family: var(--font-ui);">
                <thead>
                    <tr style="background: var(--paper-sunk); border-bottom: 1px solid var(--rule);">
                        <th style="padding: 12px var(--s-4);">Metric</th>
                        <th style="padding: 12px var(--s-4); border-left: 1px solid var(--rule);">Hotel A</th>
                        <th style="padding: 12px var(--s-4); border-left: 1px solid var(--rule);">Hotel B</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid var(--rule);">
                        <td style="padding: 12px var(--s-4); color: var(--ink-muted);">Base Room Total</td>
                        <td id="res_a_base" style="padding: 12px var(--s-4); border-left: 1px solid var(--rule);">₹0</td>
                        <td id="res_b_base" style="padding: 12px var(--s-4); border-left: 1px solid var(--rule);">₹0</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--rule);">
                        <td style="padding: 12px var(--s-4); color: var(--ink-muted);">Hidden GST Tax</td>
                        <td id="res_a_tax" style="padding: 12px var(--s-4); border-left: 1px solid var(--rule); color: #d32f2f;">+₹0</td>
                        <td id="res_b_tax" style="padding: 12px var(--s-4); border-left: 1px solid var(--rule); color: #d32f2f;">+₹0</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--rule);">
                        <td style="padding: 12px var(--s-4); color: var(--ink-muted);">Total Extra Fees</td>
                        <td id="res_a_fees" style="padding: 12px var(--s-4); border-left: 1px solid var(--rule); color: #d32f2f;">+₹0</td>
                        <td id="res_b_fees" style="padding: 12px var(--s-4); border-left: 1px solid var(--rule); color: #d32f2f;">+₹0</td>
                    </tr>
                    <tr style="background: var(--signal); color: var(--ink);">
                        <td style="padding: 16px var(--s-4); font-weight: bold; font-size: var(--t-lg);">Final Checkout Price</td>
                        <td id="res_a_total" style="padding: 16px var(--s-4); border-left: 1px solid var(--ink); font-weight: bold; font-size: var(--t-lg);">₹0</td>
                        <td id="res_b_total" style="padding: 16px var(--s-4); border-left: 1px solid var(--ink); font-weight: bold; font-size: var(--t-lg);">₹0</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div id="verdict" style="margin-top: var(--s-4); padding: var(--s-4); background: #e8f5e9; border-left: 4px solid #2e7d32; font-weight: 600; display: none; font-family: var(--font-ui);">
            Waiting for input...
        </div>

    </div>
    
    <script>
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
            
            // Check if the visually cheaper hotel is actually more expensive
            const a_base_cheaper = a_base < b_base;
            const a_total_cheaper = a_total < b_total;
            
            if (a_base_cheaper != a_total_cheaper) {
                verdictEl.innerHTML = 🚨 <strong>Trap Avoided:</strong> The advertised rate for the cheaper hotel was a lie due to taxes/fees. <strong></strong> is actually cheaper by  overall.;
                verdictEl.style.background = '#fff3e0';
                verdictEl.style.borderLeftColor = '#e65100';
            } else {
                verdictEl.innerHTML = 💡 <strong></strong> is cheaper by  for the total stay.;
                verdictEl.style.background = '#e8f5e9';
                verdictEl.style.borderLeftColor = '#2e7d32';
            }
        } else {
             verdictEl.innerHTML = Enter rates for both hotels to see the comparison.;
             verdictEl.style.background = '#f5f5f5';
             verdictEl.style.borderLeftColor = '#9e9e9e';
        }
    }
    </script>
  </main>
'''
html = re.sub(r'<div class="article-header">.*?</main>', main_content, html, flags=re.DOTALL)

with open('hotel-compare.html', 'w', encoding='utf-8') as f:
    f.write(html)

import re

with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace meta tags
html = html.replace('Who writes Prime Hotel Picks, how the hotel research is actually done, and what we do not claim. Written and edited by Sushant Kumar.', 'Calculate your total India trip budget, including suggested hotel per-night spend based on your travel style.')
html = html.replace('About and how we research - Prime Hotel Picks', 'India Trip Budget Calculator - Prime Hotel Picks')
html = html.replace('https://primehotelpicks.com/about.html', 'https://primehotelpicks.com/budget-calculator.html')

# Remove JSON LD scripts
html = re.sub(r'<script type=\"application/ld\+json\">.*?</script>', '', html, flags=re.DOTALL)

# Update nav (remove active from about, add Tools)
nav_old = '''      <nav class="nav" id="site-nav">
        <a href="index.html">Home</a>
        <a href="about.html" class="active">About</a>
        <a href="contact.html">Contact</a>
      </nav>'''
nav_new = '''      <nav class="nav" id="site-nav">
        <a href="index.html">Home</a>
        <a href="budget-calculator.html" class="active">Tools</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </nav>'''
html = html.replace(nav_old, nav_new)

# Replace main content
main_content = '''
  <div class="article-header">
    <div class="article-header__inner">
      <h1 class="marker">India Trip Budget Calculator</h1>
      <div class="article-meta-bar">
        <span>Interactive Tool</span>
        <span class="badge badge--sourced">Instant Calculation</span>
      </div>
    </div>
  </div>

  <main id="main" class="legal-page">
    <p>Use this calculator to determine how much you should allocate for hotels per night based on your overall trip budget, duration, and travel style.</p>

    <div style="background: var(--bg-card, #f9f9f9); padding: var(--s-6); border-radius: 8px; border: 1px solid var(--rule); margin-top: var(--s-6);">
        <form id="budgetForm" onsubmit="event.preventDefault(); calculateBudget();" style="display: flex; flex-direction: column; gap: var(--s-4);">
            <div>
                <label for="totalBudget" style="display:block; font-weight: 600; margin-bottom: var(--s-2);">Total Trip Budget (₹)</label>
                <input type="number" id="totalBudget" required min="1000" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: var(--font-ui);">
            </div>
            <div>
                <label for="days" style="display:block; font-weight: 600; margin-bottom: var(--s-2);">Duration (Days)</label>
                <input type="number" id="days" required min="1" max="90" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: var(--font-ui);">
            </div>
            <div>
                <label for="style" style="display:block; font-weight: 600; margin-bottom: var(--s-2);">Travel Style</label>
                <select id="style" required style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: var(--font-ui);">
                    <option value="budget">Budget (Hostels / Cheap Eats / Local Transport)</option>
                    <option value="standard" selected>Standard (3-4 Star Hotels / Mixed Dining / Cabs)</option>
                    <option value="luxury">Luxury (5 Star Hotels / Fine Dining / Private Cars)</option>
                </select>
            </div>
            <button type="submit" style="background: var(--ink); color: #fff; border: none; padding: 12px; font-weight: 600; border-radius: 4px; cursor: pointer; font-family: var(--font-ui);">Calculate</button>
        </form>

        <div id="results" style="display: none; margin-top: var(--s-6); padding-top: var(--s-6); border-top: 1px solid #ccc;">
            <h3 style="margin-top: 0;">Suggested Allocation</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--s-4); margin-top: var(--s-4);">
                <div style="background: #fff; padding: var(--s-4); border-radius: 6px; border: 1px solid var(--rule);">
                    <div style="font-size: var(--t-sm); color: var(--ink-muted);">Max Hotel Spend (Per Night)</div>
                    <div id="resHotel" style="font-size: var(--t-xl); font-weight: 700; color: var(--ink); font-family: var(--font-ui);">₹0</div>
                </div>
                <div style="background: #fff; padding: var(--s-4); border-radius: 6px; border: 1px solid var(--rule);">
                    <div style="font-size: var(--t-sm); color: var(--ink-muted);">Daily Food & Local Travel</div>
                    <div id="resDaily" style="font-size: var(--t-xl); font-weight: 700; color: var(--ink); font-family: var(--font-ui);">₹0</div>
                </div>
                <div style="grid-column: 1 / -1; background: #fff; padding: var(--s-4); border-radius: 6px; border: 1px solid var(--rule);">
                    <div style="font-size: var(--t-sm); color: var(--ink-muted);">Flights & Intercity Transport Buffer (Total)</div>
                    <div id="resTransport" style="font-size: var(--t-xl); font-weight: 700; color: var(--ink); font-family: var(--font-ui);">₹0</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function calculateBudget() {
        const budget = parseFloat(document.getElementById('totalBudget').value);
        const days = parseInt(document.getElementById('days').value);
        const style = document.getElementById('style').value;
        
        let hotelPct, foodPct, transportPct;
        
        if (style === 'budget') {
            hotelPct = 0.30;
            foodPct = 0.40;
            transportPct = 0.30;
        } else if (style === 'luxury') {
            hotelPct = 0.55;
            foodPct = 0.25;
            transportPct = 0.20;
        } else {
            hotelPct = 0.40;
            foodPct = 0.35;
            transportPct = 0.25;
        }
        
        const totalHotel = budget * hotelPct;
        const totalFood = budget * foodPct;
        const transportBuffer = budget * transportPct;
        
        const perNightHotel = totalHotel / Math.max(1, (days - 1));
        const dailyFood = totalFood / days;
        
        document.getElementById('resHotel').innerText = '₹' + Math.round(perNightHotel).toLocaleString('en-IN');
        document.getElementById('resDaily').innerText = '₹' + Math.round(dailyFood).toLocaleString('en-IN');
        document.getElementById('resTransport').innerText = '₹' + Math.round(transportBuffer).toLocaleString('en-IN');
        
        document.getElementById('results').style.display = 'block';
    }
    </script>
  </main>
'''
html = re.sub(r'<div class="article-header">.*?</main>', main_content, html, flags=re.DOTALL)

with open('budget-calculator.html', 'w', encoding='utf-8') as f:
    f.write(html)

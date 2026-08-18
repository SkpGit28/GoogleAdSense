import glob
import re

# Step 1: Create a central Tools hub page
with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace metadata
html = html.replace('About and how we research', 'Travel Tools')
html = html.replace('Who writes Prime Hotel Picks, how the hotel research is actually done, and what we do not claim. Written and edited by Sushant Kumar.', 'Interactive tools for calculating travel budgets and revealing hidden hotel taxes in India.')
html = html.replace('about.html', 'tools.html')

# Remove schema scripts
html = re.sub(r'<script type=\"application/ld\+json\">.*?</script>', '', html, flags=re.DOTALL)

# Main content block for the Hub
hub_content = '''
  <div class="article-header">
    <div class="article-header__inner">
      <h1 class="marker">Travel Tools</h1>
      <div class="article-meta-bar">
        <span>Interactive Utilities</span>
        <span class="badge badge--sourced">Real-time Data</span>
      </div>
    </div>
  </div>

  <main id="main" class="legal-page">
    <p>Indian hotel pricing can be highly deceptive, and planning a budget requires factoring in hidden costs, taxes, and domestic travel. Use the free tools below to plan your trip.</p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--s-6); margin-top: var(--s-6);">
        
        <!-- Tool 1 -->
        <a href="hotel-compare.html" style="display: block; background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: var(--s-5); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.08)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
            <div style="background: var(--signal); color: var(--ink); display: inline-block; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-family: var(--font-ui); font-size: var(--t-xs); margin-bottom: var(--s-3);">Most Popular</div>
            <h2 style="margin-top: 0; margin-bottom: var(--s-2);">Hotel Rate & Hidden Cost Comparator</h2>
            <p style="color: var(--ink-muted); line-height: 1.5; margin-bottom: 0;">Compare two hotels side-by-side. Automatically calculates 12% vs 18% GST brackets and adds mandatory resort/gala fees to reveal which hotel is actually cheaper at checkout.</p>
        </a>

        <!-- Tool 2 -->
        <a href="budget-calculator.html" style="display: block; background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: var(--s-5); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.08)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
            <h2 style="margin-top: 0; margin-bottom: var(--s-2);">Trip Budget Calculator</h2>
            <p style="color: var(--ink-muted); line-height: 1.5; margin-bottom: 0;">Enter your total budget, duration, and travel style (Budget/Standard/Luxury). Instantly generates a realistic daily allowance for food and sets your maximum nightly hotel limit.</p>
        </a>

    </div>
  </main>
'''
html = re.sub(r'<div class="article-header">.*?</main>', hub_content, html, flags=re.DOTALL)

with open('tools.html', 'w', encoding='utf-8') as f:
    f.write(html)


# Step 2: Clean up all navs across the site
files = glob.glob('*.html')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # We want to replace any combination of Budget Calc and Rate Compare links
    # with a single "Tools" link pointing to tools.html
    
    def replacer(match):
        prefix = match.group(1)
        # If we are on tools.html, hotel-compare, or budget-calc, mark Tools as active
        active = ' class="active"' if f in ['tools.html', 'hotel-compare.html', 'budget-calculator.html'] else ''
        return f'<a href="{prefix}tools.html"{active}>Tools</a>'
        
    # Catch both versions of the old nav (with active states or without)
    pattern = re.compile(r'<a href="([^"]*)budget-calculator\.html"[^>]*>Budget Calc</a>\s*<a href="[^"]*hotel-compare\.html"[^>]*>Rate Compare</a>')
    
    new_content = pattern.sub(replacer, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
        
print("Created tools.html hub and updated all navs")

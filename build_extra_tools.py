import re

with open('budget-calculator.html', 'r', encoding='utf-8') as f:
    template = f.read()

top_part = template.split('<div class="article-header">')[0]
bottom_part = template.split('</main>')[1]

def create_page(filename, title, desc, h1, badge, content):
    html = top_part
    html = re.sub(r'<title>.*?</title>', f'<title>{title} - Prime Hotel Picks</title>', html)
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', html)
    
    # fix the active class on nav just in case
    html = html.replace('class="active"', '')
    html = html.replace('href="/tools.html"', 'href="/tools.html" class="active"')
    
    main_sec = f'''
  <div class="article-header">
    <div class="article-header__inner">
      <h1 class="marker">{h1}</h1>
      <div class="article-meta-bar">
        <span>Interactive Tool</span>
        <span class="badge badge--sourced">{badge}</span>
      </div>
    </div>
  </div>
  <main id="main" class="legal-page">
{content}
  </main>
'''
    with open(filename, 'w', encoding='utf-8') as out:
        out.write(html + main_sec + bottom_part)


# ---------------------------------------------------------
# TOOL 1: JARGON TRANSLATOR
# ---------------------------------------------------------
jargon_content = '''
    <p>Booking sites are full of deceptive marketing speak. Paste a hotel's description below, and our B.S. Detector will highlight the jargon and translate it into what you will actually experience.</p>
    
    <div style="margin-top: var(--s-5);">
        <textarea id="jargonInput" rows="6" placeholder="Paste the hotel description here (e.g. 'Enjoy our cozy, vibrant rooms located steps from the beach with a rustic heritage feel...')" style="width: 100%; padding: 16px; border: 1px solid var(--rule); border-radius: 8px; font-family: var(--font-ui); font-size: var(--t-md); resize: vertical; box-sizing: border-box;"></textarea>
        
        <div style="margin-top: var(--s-4); text-align: right;">
            <button onclick="translateJargon()" style="background: var(--ink); color: #fff; border: none; padding: 12px 24px; font-size: var(--t-md); font-weight: 700; border-radius: 6px; cursor: pointer; font-family: var(--font-ui);">Detect Jargon</button>
        </div>
    </div>

    <div id="jargonResults" style="margin-top: var(--s-6); display: none;">
        <h3 style="border-bottom: 2px solid var(--ink); padding-bottom: 8px; margin-bottom: var(--s-4);">Honest Translation</h3>
        <div id="jargonOutput" style="display: flex; flex-direction: column; gap: var(--s-3);"></div>
    </div>

    <script>
    const jargonDict = [
        { word: "cozy", truth: "Extremely small. You will likely bump your knees on the bed." },
        { word: "vibrant", truth: "Loud. Usually means the hotel is above a nightclub, busy street, or active bar." },
        { word: "rustic", truth: "Old and unrenovated. Expect creaky furniture and dated plumbing." },
        { word: "steps from", truth: "Technically true, but those steps might involve crossing a dangerous 4-lane highway." },
        { word: "partial sea view", truth: "You can see a sliver of water if you lean dangerously over the balcony railing." },
        { word: "heritage feel", truth: "The building is very old, and so is the air conditioning." },
        { word: "up and coming", truth: "Surrounded by active, noisy construction sites." },
        { word: "tropical", truth: "Lots of mosquitoes and bugs. Do not leave your window open." },
        { word: "bustling", truth: "Chaotic, crowded, and guaranteed traffic jams outside the lobby." },
        { word: "intimate", truth: "Zero privacy. You will hear your neighbors whispering." }
    ];

    function translateJargon() {
        const text = document.getElementById('jargonInput').value.toLowerCase();
        const output = document.getElementById('jargonOutput');
        output.innerHTML = '';
        
        let foundAny = false;

        jargonDict.forEach(item => {
            if (text.includes(item.word)) {
                foundAny = true;
                output.innerHTML += `
                    <div style="background: var(--paper-sunk); border-left: 4px solid #d32f2f; padding: var(--s-4); border-radius: 4px;">
                        <div style="color: #d32f2f; font-weight: bold; font-family: var(--font-ui); text-transform: uppercase; font-size: var(--t-xs); margin-bottom: 4px;">Detected: "${item.word}"</div>
                        <div style="font-weight: 600; color: var(--ink);">${item.truth}</div>
                    </div>
                `;
            }
        });

        if (!foundAny && text.trim().length > 0) {
            output.innerHTML = '<div style="background: #e8f5e9; border-left: 4px solid #2e7d32; padding: var(--s-4); border-radius: 4px; font-weight: 600;">No standard BS keywords detected! But still read the bulk 1-star reviews to be safe.</div>';
        } else if (text.trim().length === 0) {
            output.innerHTML = '<div style="color: var(--ink-muted);">Please paste some text first.</div>';
        }

        document.getElementById('jargonResults').style.display = 'block';
    }
    </script>
'''
create_page('jargon-translator.html', 'Hotel Jargon Translator', 'Paste a hotel description and translate the deceptive marketing jargon into brutal honesty.', 'Hotel Jargon Translator', 'B.S. Detector', jargon_content)


# ---------------------------------------------------------
# TOOL 2: PRICE INFLATOR MATRIX
# ---------------------------------------------------------
inflator_content = '''
    <p>Indian hotel prices are heavily manipulated by local wedding dates, regional festivals, and monsoons. Select your destination and month to see if you are stepping into a pricing trap.</p>
    
    <div style="background: var(--paper-sunk); padding: var(--s-5); border: 1px solid var(--rule); border-radius: 8px; margin-top: var(--s-5); display: grid; grid-template-columns: 1fr 1fr; gap: var(--s-4);">
        <div>
            <label style="display:block; font-weight: 600; margin-bottom: 8px;">Region</label>
            <select id="infRegion" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: var(--font-ui);">
                <option value="Rajasthan">Rajasthan (Jaipur, Udaipur, Jodhpur)</option>
                <option value="Goa">Goa</option>
                <option value="Kerala">Kerala (Backwaters, Munnar)</option>
                <option value="Himachal">Himachal Pradesh (Shimla, Manali)</option>
            </select>
        </div>
        <div>
            <label style="display:block; font-weight: 600; margin-bottom: 8px;">Month of Travel</label>
            <select id="infMonth" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: var(--font-ui);">
                <option value="Jan">January</option>
                <option value="May">May</option>
                <option value="Jul">July</option>
                <option value="Nov">November</option>
                <option value="Dec">December</option>
            </select>
        </div>
        <div style="grid-column: 1 / -1; margin-top: var(--s-3);">
            <button onclick="checkMatrix()" style="width: 100%; background: var(--ink); color: #fff; border: none; padding: 14px; font-size: var(--t-md); font-weight: 700; border-radius: 6px; cursor: pointer; font-family: var(--font-ui);">Analyze Risk</button>
        </div>
    </div>

    <div id="infResults" style="margin-top: var(--s-6); display: none; padding: var(--s-5); border-radius: 8px;">
        <div style="font-size: var(--t-xs); font-family: var(--font-ui); text-transform: uppercase; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px;" id="infBadge">Status</div>
        <h2 id="infTitle" style="margin-top: 0; margin-bottom: var(--s-3);">Title</h2>
        <p id="infDesc" style="font-size: var(--t-md); margin-bottom: 0;"></p>
    </div>

    <script>
    function checkMatrix() {
        const region = document.getElementById('infRegion').value;
        const month = document.getElementById('infMonth').value;
        const res = document.getElementById('infResults');
        const badge = document.getElementById('infBadge');
        const title = document.getElementById('infTitle');
        const desc = document.getElementById('infDesc');
        
        res.style.display = 'block';
        
        let danger = "Low Risk";
        let color = "#2e7d32";
        let bg = "#e8f5e9";
        let t = "";
        let d = "";

        if (region === "Rajasthan" && (month === "Nov" || month === "Dec" || month === "Jan")) {
            danger = "Extreme Danger"; color = "#c62828"; bg = "#ffebee";
            t = "Peak Wedding & Tourist Season";
            d = "Rates are inflated by up to 300%. Expect loud Baraat (wedding) processions late into the night at major heritage hotels, making sleep difficult.";
        } else if (region === "Rajasthan" && month === "May") {
            danger = "Heat Warning"; color = "#e65100"; bg = "#fff3e0";
            t = "Severe Summer Heat";
            d = "Rates are very cheap, but temperatures exceed 40°C. Sightseeing is impossible during the day.";
        } else if (region === "Goa" && (month === "Dec" || month === "Jan")) {
            danger = "Extreme Danger"; color = "#c62828"; bg = "#ffebee";
            t = "Peak Holiday Surge";
            d = "Every resort enforces mandatory 'Gala Dinner' charges (₹5k-₹15k per person). Taxis and flights are at their absolute most expensive.";
        } else if (region === "Goa" && month === "Jul") {
            danger = "Weather Warning"; color = "#1565c0"; bg = "#e3f2fd";
            t = "Heavy Monsoons";
            d = "Rates drop significantly, but many beach shacks are dismantled and swimming is strictly prohibited due to dangerous currents.";
        } else if (region === "Kerala" && month === "Jul") {
            danger = "Weather Warning"; color = "#1565c0"; bg = "#e3f2fd";
            t = "Active Monsoons";
            d = "Houseboat experiences are miserable in heavy rain. Leech and mosquito populations spike at nature resorts.";
        } else if (region === "Himachal" && month === "May") {
            danger = "High Risk"; color = "#e65100"; bg = "#fff3e0";
            t = "Summer Vacation Chaos";
            d = "Massive influx of domestic tourists escaping the heat. Expect 3-hour traffic jams just to cross Shimla or Manali.";
        } else if (region === "Himachal" && month === "Jan") {
            danger = "Variable Risk"; color = "#1565c0"; bg = "#e3f2fd";
            t = "Snow Risk";
            d = "Beautiful views, but many budget hotels lack central heating. Roads frequently close due to snow, trapping you in your hotel.";
        } else {
            danger = "Sweet Spot"; color = "#2e7d32"; bg = "#e8f5e9";
            t = "Good Value Window";
            d = "You have selected a shoulder season or off-peak window with acceptable weather. Hotel rates should be negotiable and crowds minimal.";
        }

        res.style.backgroundColor = bg;
        res.style.border = `1px solid ${color}`;
        badge.style.color = color;
        badge.innerText = danger;
        title.innerText = t;
        title.style.color = color;
        desc.innerText = d;
    }
    </script>
'''
create_page('price-inflator.html', 'Monsoon & Wedding Price Inflator', 'Check if your travel dates collide with local monsoons or peak wedding seasons that inflate rates.', 'Monsoon & Wedding Price Matrix', 'Live Analysis', inflator_content)


# ---------------------------------------------------------
# TOOL 3: DEALBREAKER QUIZ
# ---------------------------------------------------------
quiz_content = '''
    <p>Skip the endless scrolling. Tell us your absolute dealbreakers, and we will route you to the exact honest hotel guide that fits your needs.</p>
    
    <div id="quizContainer" style="background: var(--paper-sunk); padding: var(--s-6); border: 1px solid var(--rule); border-radius: 8px; margin-top: var(--s-5);">
        
        <div id="q1">
            <h3 style="margin-top: 0;">1. What is your absolute maximum budget per night?</h3>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 16px;">
                <button onclick="nextQ(1, 'budget')" class="quiz-btn">Under ₹1,500 (Hostels & Backpacking)</button>
                <button onclick="nextQ(1, 'mid')" class="quiz-btn">₹3,000 - ₹8,000 (Standard Comfort)</button>
                <button onclick="nextQ(1, 'luxury')" class="quiz-btn">Money is no object (Palaces & 5-Stars)</button>
            </div>
        </div>

        <div id="q2" style="display: none;">
            <h3 style="margin-top: 0;">2. What is your biggest dealbreaker?</h3>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 16px;">
                <button onclick="nextQ(2, 'noise')" class="quiz-btn">I hate loud traffic and honking</button>
                <button onclick="nextQ(2, 'scams')" class="quiz-btn">I hate being scammed by "Hidden Fees"</button>
                <button onclick="nextQ(2, 'fake')" class="quiz-btn">I hate fake "Wellness" or "Eco" marketing</button>
            </div>
        </div>

        <div id="q3" style="display: none;">
            <h3 style="margin-top: 0;">3. What is the vibe of your trip?</h3>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 16px;">
                <button onclick="finishQuiz('rajasthan-palace-hotels.html')" class="quiz-btn">Royal & Historic (Heritage)</button>
                <button onclick="finishQuiz('beach-resorts-goa.html')" class="quiz-btn">Beaches & Pools</button>
                <button onclick="finishQuiz('bengaluru-business-hotels.html')" class="quiz-btn">Strictly Business (Wi-Fi is life)</button>
                <button onclick="finishQuiz('rishikesh-wellness-retreats.html')" class="quiz-btn">Nature & Peace</button>
            </div>
        </div>

    </div>
    
    <style>
        .quiz-btn {
            background: var(--paper); border: 2px solid var(--ink); color: var(--ink); padding: 14px; text-align: left; font-size: var(--t-md); font-weight: 600; border-radius: 6px; cursor: pointer; font-family: var(--font-ui); transition: all 0.1s;
        }
        .quiz-btn:hover { background: var(--ink); color: #fff; }
    </style>

    <script>
    let answers = {};
    
    function nextQ(current, answer) {
        answers['q' + current] = answer;
        document.getElementById('q' + current).style.display = 'none';
        
        // Fast-track logic for extreme budgets
        if (current === 1 && answer === 'budget') {
            finishQuiz('budget-hostels-india.html');
            return;
        }
        
        // Fast-track logic for specific dealbreakers
        if (current === 2 && answer === 'fake') {
            finishQuiz('eco-stays-india.html');
            return;
        }
        
        document.getElementById('q' + (current + 1)).style.display = 'block';
    }

    function finishQuiz(url) {
        document.getElementById('quizContainer').innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <h2 style="margin-top: 0; color: #2e7d32;">Match Found!</h2>
                <p>Based on your brutal honesty, we found the perfect guide for you to read.</p>
                <a href="/articles/${url}" style="display: inline-block; background: var(--ink); color: #fff; padding: 14px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 16px;">Read Your Custom Guide</a>
            </div>
        `;
    }
    </script>
'''
create_page('dealbreaker-quiz.html', 'The Dealbreaker Matchmaker', 'Take a 3-question quiz to find the exact honest hotel guide that fits your travel style.', 'The Dealbreaker Matchmaker', 'Quiz', quiz_content)


# ---------------------------------------------------------
# UPDATE TOOLS.HTML HUB
# ---------------------------------------------------------
with open('tools.html', 'r', encoding='utf-8') as f:
    hub = f.read()

new_tools = '''
        <!-- Tool 3 -->
        <a href="jargon-translator.html" style="display: block; background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: var(--s-5); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.08)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
            <div style="background: #ffebee; color: #c62828; display: inline-block; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-family: var(--font-ui); font-size: 11px; margin-bottom: var(--s-2);">B.S. Detector</div>
            <h2 style="margin-top: 0; margin-bottom: var(--s-2);">Hotel Jargon Translator</h2>
            <p style="color: var(--ink-muted); line-height: 1.5; margin-bottom: 0;">Paste a hotel's description from Agoda or Booking.com, and we will highlight the marketing jargon and translate it into brutal honesty.</p>
        </a>

        <!-- Tool 4 -->
        <a href="price-inflator.html" style="display: block; background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: var(--s-5); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.08)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
            <h2 style="margin-top: 0; margin-bottom: var(--s-2);">Monsoon & Wedding Price Matrix</h2>
            <p style="color: var(--ink-muted); line-height: 1.5; margin-bottom: 0;">Check if your travel dates collide with local monsoons, regional festivals, or peak wedding seasons that silently inflate rates by up to 300%.</p>
        </a>

        <!-- Tool 5 -->
        <a href="dealbreaker-quiz.html" style="display: block; background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: var(--s-5); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.08)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
            <h2 style="margin-top: 0; margin-bottom: var(--s-2);">The Dealbreaker Matchmaker</h2>
            <p style="color: var(--ink-muted); line-height: 1.5; margin-bottom: 0;">Take a rapid-fire quiz about your absolute dealbreakers, and we will instantly route you to the exact honest hotel guide you need.</p>
        </a>
    </div>
'''

hub = re.sub(r'    </div>\s*</main>', new_tools + '  </main>', hub)
with open('tools.html', 'w', encoding='utf-8') as f:
    f.write(hub)

print("Generated all 3 new tools and updated tools.html")

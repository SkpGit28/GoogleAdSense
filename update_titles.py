import json

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for article in data['articles']:
        slug = article['slug']
        if slug == 'rajasthan-palace-hotels':
            article['title'] = 'Where NOT to Stay in Rajasthan (And 3 Palace Hotels That Are Worth It)'
            article['h1'] = 'Where NOT to stay in Rajasthan (and 3 palace hotels that are worth it)'
        elif slug == 'best-hotels-udaipur':
            article['title'] = 'Udaipur Hotels: Taj Lake Palace vs Oberoi Udaivilas (Honest Review)'
            article['h1'] = 'Taj Lake Palace vs Oberoi Udaivilas: The honest truth about Udaipur''s top hotels'
        elif slug == 'heritage-hotels-mumbai':
            article['title'] = 'I Compared Mumbai Harbour Hotels: Taj Mahal Palace vs Trident vs Oberoi'
            article['h1'] = 'I compared Mumbai Harbour hotels: Taj Mahal Palace vs Trident vs Oberoi'
        elif slug == 'kerala-backwater-resorts':
            article['title'] = 'Kerala Backwater Stays: Are Houseboats Actually a Scam?'
            article['h1'] = 'Kerala backwater stays: Are houseboats actually a scam?'
        elif slug == 'varanasi-ghat-hotels':
            article['title'] = 'Where to Stay in Varanasi (And Which Ghat Hotels to Avoid)'
            article['h1'] = 'Where to stay in Varanasi (and which ghat hotels to avoid)'
        elif slug == 'bengaluru-business-hotels':
            article['title'] = 'Bengaluru Business Hotels: The Only 5 With Fast Wi-Fi and No Traffic Pain'
            article['h1'] = 'Bengaluru business hotels: The only 5 with fast Wi-Fi and no traffic pain'
        elif slug == 'best-hotels-new-delhi':
            article['title'] = 'Delhi Hotels: Where to Stay (And 2 Overpriced Hotels to Skip)'
            article['h1'] = 'Delhi hotels: Where to stay (and 2 overpriced hotels to skip)'
        elif slug == 'beach-resorts-goa':
            article['title'] = '10 Goa Beach Resorts With Private Pools (Photos + Honest Pros & Cons)'
            article['h1'] = '10 Goa beach resorts with private pools (photos + honest pros & cons)'
        elif slug == 'hotels-near-taj-mahal-agra':
            article['title'] = 'Hotels Near the Taj Mahal That Actually Have the View (And Which Lie)'
            article['h1'] = 'Hotels near the Taj Mahal that actually have the view (and which lie)'
        elif slug == 'himachal-hill-station-hotels':
            article['title'] = 'Shimla vs Manali Hotels: The Brutal Truth About Hill Station Stays'
            article['h1'] = 'Shimla vs Manali hotels: The brutal truth about hill station stays'
        elif slug == 'rishikesh-wellness-retreats':
            article['title'] = 'Rishikesh Retreats: 4 Real Wellness Stays (And 3 Spa Menus in Disguise)'
            article['h1'] = 'Rishikesh retreats: 4 real wellness stays (and 3 spa menus in disguise)'
        elif slug == 'wildlife-lodges-ranthambore':
            article['title'] = 'Ranthambore Lodges: The Real Cost of Safari Access (Honest Breakdown)'
            article['h1'] = 'Ranthambore lodges: The real cost of safari access (honest breakdown)'
        elif slug == 'hyderabad-luxury-hotels':
            article['title'] = 'Hyderabad Luxury Hotels: Falaknuma vs Banjara Hills vs HITEC City'
            article['h1'] = 'Hyderabad luxury hotels: Falaknuma vs Banjara Hills vs HITEC City'
        elif slug == 'kolkata-heritage-hotels':
            article['title'] = 'Kolkata Heritage Hotels: Is The Oberoi Grand Still the Best?'
            article['h1'] = 'Kolkata heritage hotels: Is The Oberoi Grand still the best?'
        elif slug == 'andaman-island-resorts':
            article['title'] = 'Andaman Resorts: Havelock vs Neil Island (And 1 Resort to Skip)'
            article['h1'] = 'Andaman resorts: Havelock vs Neil Island (and 1 resort to skip)'
        elif slug == 'ladakh-hotels-leh':
            article['title'] = 'Leh Ladakh Stays: The 5 Hotels You Need for Altitude Adjustment'
            article['h1'] = 'Leh Ladakh stays: The 5 hotels you need for altitude adjustment'
        elif slug == 'darjeeling-tea-estate-stays':
            article['title'] = 'Darjeeling Tea Estate Stays: 4 Bungalows Worth the Money'
            article['h1'] = 'Darjeeling tea estate stays: 4 bungalows worth the money'
        elif slug == 'amritsar-hotels-golden-temple':
            article['title'] = 'Best Hotels Under 3000 Near the Golden Temple, Amritsar'
            article['h1'] = 'Best hotels under 3000 near the Golden Temple, Amritsar'
        elif slug == 'budget-hostels-india':
            article['title'] = 'What 700/Night Actually Gets You in Indian Hostels (Honest Photos)'
            article['h1'] = 'What 700/night actually gets you in Indian hostels (honest photos)'
        elif slug == 'eco-stays-india':
            article['title'] = 'Eco Stays in India: 6 Real Eco Lodges (And 3 Greenwashed Scams)'
            article['h1'] = 'Eco stays in India: 6 real eco lodges (and 3 greenwashed scams)'
            
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {filename}")

update_file('_build/articles.json')
update_file('_build/articles2.json')

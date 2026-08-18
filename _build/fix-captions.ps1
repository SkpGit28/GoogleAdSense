$ErrorActionPreference = "Stop"
$manifest = Get-Content "_build\image-manifest.json" -Raw | ConvertFrom-Json
$imgDict = @{}
foreach ($m in $manifest) { $imgDict[$m.key] = $m }

$descDict = @{}
$descDict["rambagh-palace"] = "The lobby courtyard colonnade at Rambagh Palace."
$descDict["umaid-bhawan"] = "An elevated view of Umaid Bhawan Palace in Jodhpur."
$descDict["samode-palace"] = "The historic inner courtyard at Samode Haveli."
$descDict["taj-lake-palace"] = "Taj Lake Palace resting in the middle of Lake Pichola."
$descDict["oberoi-udaivilas"] = "The sprawling inner courtyard gardens at The Oberoi Udaivilas."
$descDict["taj-mahal-palace-mumbai"] = "The iconic heritage Palace wing of the Taj Mahal Palace viewed from Apollo Bunder."
$descDict["oberoi-mumbai"] = "The modern exterior of The Oberoi Trident complex at Nariman Point."
$descDict["trident-nariman"] = "The Marine Drive skyline at Nariman Point, where the Trident and Oberoi share a sweeping bay view."
$descDict["imperial-delhi"] = "The stately colonial entrance of The Imperial Hotel in central Delhi."
$descDict["taj-fort-aguada"] = "Terraced lawns looking out over the Arabian Sea from Taj Fort Aguada."
$descDict["alila-diwa-goa"] = "Traditional Goan courtyard architecture surrounded by green paddy fields at Alila Diwa."
$descDict["kumarakom-lake"] = "Kumarakom Lake Resort looking out over the expansive Vembanad Lake."
$descDict["coconut-lagoon"] = "A peaceful inland canal approaching Coconut Lagoon."
$descDict["itc-mughal"] = "A historical map showing the Agra Subah. This illustrates the Mughal administrative region rather than the ITC Mughal property itself."
$descDict["taj-convention-agra"] = "The modern glass facade of the Taj Hotel and Convention Centre."
$descDict["brijrama-palace"] = "The imposing riverfront elevation of BrijRama Palace standing tall above Darbhanga Ghat."
$descDict["varanasi-ghats"] = "The Ganges riverfront illuminated by lamps. This illustrates the general ghat atmosphere at night, not a specific hotel."
$descDict["oberoi-cecil"] = "The classic British-era facade of The Oberoi Cecil in Shimla."
$descDict["manali-hotel"] = "Traditional cedar timber architecture typical of mountain lodges in the Manali valleys."
$descDict["taj-rishikesh"] = "Himalayan stone villas stepping down the hillside at Taj Rishikesh."
$descDict["aman-i-khas"] = "A chital deer grazing in the brush. This shows the wildlife found in Ranthambore rather than the Aman-i-Khas camp itself."
$descDict["itc-kohenur"] = "The striking angular glass architecture of ITC Kohenur dominating the HITEC City skyline."
$descDict["leela-bengaluru"] = "The opulent palace-style architecture of The Leela Palace Bengaluru."
$descDict["taj-west-end"] = "Lush heritage gardens and colonial buildings at the Taj West End."
$descDict["oberoi-grand-kolkata"] = "The grand neoclassical entrance to The Oberoi Grand on Chowringhee Road."
$descDict["itc-royal-bengal"] = "The towering palatial profile of ITC Royal Bengal along the EM Bypass."
$descDict["taj-exotica-havelock"] = "A wooden stilt villa tucked beneath native mahua trees at Taj Exotica."
$descDict["barefoot-havelock"] = "A rustic eco-cottage built from bamboo and thatch at Barefoot at Havelock."
$descDict["seashell-havelock"] = "Timber chalets arranged among dense coconut palms at SeaShell Havelock."
$descDict["nimmu-house"] = "The restored Ladakhi noble estate of Nimmu House set against rugged mountains."
$descDict["stok-palace"] = "The prayer hall entrance at Stok Gompa. This shows the neighbouring monastery rather than the Stok Palace heritage hotel itself."
$descDict["glenburn-tea-estate"] = "A colonial planter's bungalow looking across the tea garden slopes at Glenburn."
$descDict["mayfair-darjeeling"] = "The open-air breakfast terrace at Keventer's on Nehru Road, illustrating central Darjeeling town rather than the Mayfair resort."
$descDict["taj-swarna-amritsar"] = "The Golden Temple illuminated at night. This shows the shrine itself rather than the Taj Swarna hotel located on the outer ring road."
$descDict["hyatt-amritsar"] = "The brick facades along Heritage Street, illustrating the pedestrian precinct near the Golden Temple rather than a specific hotel."
$descDict["spice-village-thekkady"] = "The Edapalayam Palace across Periyar Lake, showing the surrounding forest reserve context rather than the Spice Village tribal cottages."
$descDict["diphlu-river-lodge"] = "A bamboo stilt cottage facing the Diphlu River and Kaziranga National Park."
$descDict["delhi-old-city"] = "A bustling street scene in Old Delhi, capturing the dense urban fabric of the walled city rather than a specific central hotel."
$descDict["goa-candolim"] = "The public access pathway leading down to Candolim Beach, showing the immediate neighborhood rather than a private resort."
$descDict["rishikesh-bridge"] = "The iconic Lakshman Jhula suspension bridge over the Ganges, representing the town center rather than the upriver wellness retreats."
$descDict["agra-taj-view"] = "The Taj Mahal viewed from across the Yamuna River at Mehtab Bagh. This shows the monument's rear elevation rather than a hotel room view."
$descDict["shimla-mall"] = "The historic Town Hall building on Mall Road, showing central Shimla's pedestrian zone rather than a specific budget property."
$descDict["leh-market"] = "The pedestrianized Main Bazaar in Leh framed by mountain peaks, illustrating the town center where family guesthouses are located."
$descDict["kolkata-park-street"] = "Historic tombs inside the South Park Street Cemetery, representing the heritage neighborhood near Park Street rather than a modern hotel."

$files = Get-ChildItem -Path "_build\bodies\*.html"
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    
    $regex = '(?s)<figure class="article-image">\s*<img src="\.\./images/hotels/([^"]+)-800\.jpg"[^>]+>\s*<figcaption>.*?</figcaption>\s*</figure>'
    
    $newContent = [regex]::Replace($content, $regex, {
        param($m)
        $key = $m.Groups[1].Value
        $img = $imgDict[$key]
        
        $desc = $descDict[$key]
        if (-not $desc) { $desc = "A view related to $key." }

        $artist = $img.artist
        $license = $img.license
        $licenseUrl = $img.licenseUrl

        if ([string]::IsNullOrWhiteSpace($licenseUrl)) {
            $licHtml = $license
        } else {
            $licHtml = "<a href=""$licenseUrl"" rel=""nofollow noopener"">$license</a>"
        }

        $caption = "<figcaption>$desc Photo: $artist, $licHtml, via Wikimedia Commons.</figcaption>"
        
        return $m.Value -replace '(?s)<figcaption>.*?</figcaption>', $caption
    })

    [System.IO.File]::WriteAllText($file.FullName, $newContent, (New-Object System.Text.UTF8Encoding $false))
}
Write-Host "Caption audit complete." -ForegroundColor Green
$descDict["oberoi-vanyavilas"] = "A langur monkey observing from a tree branch, representing the native park wildlife rather than the Oberoi Vanyavilas property."
$descDict["taj-falaknuma"] = "The magnificent marble staircase and entrance facade of Taj Falaknuma Palace."
$descDict["park-hyatt-hyderabad"] = "The Lamakaan cultural space in Banjara Hills, showing the neighbourhood's arts scene rather than the Park Hyatt hotel."

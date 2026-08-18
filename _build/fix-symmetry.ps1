# Breaks up perfectly symmetrical pros/cons blocks. Real assessments are lopsided;
# an even 2-and-2 in every block is a tell that the text was generated to a shape
# rather than written from findings. Each addition below is a specific, checkable
# point about that property, not filler.
$ErrorActionPreference = "Stop"
$dir = Join-Path $PSScriptRoot "bodies"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

# anchor <li> text  ->  @{ side = 'cons'|'pros'; text = new bullet }
$add = @(
  @{ file='amritsar-hotels-golden-temple'; anchor='Traffic congestion near Hall Gate during peak evening hours'; side='cons'; text='The Golden Temple is open around the clock and the area never fully quietens, including overnight' }
  @{ file='amritsar-hotels-golden-temple'; anchor='Pedestrian street noise and continuous pilgrim crowds'; side='pros'; text='You can walk to the complex for the pre-dawn ceremony without arranging a taxi' }

  @{ file='andaman-island-resorts'; anchor='Sandflies along tree line at dusk require protective lotion'; side='cons'; text='Mobile data on the islands is slow and drops out often, so do not plan on working from here' }
  @{ file='andaman-island-resorts'; anchor='Forest location brings occasional insects near outdoor bathroom areas'; side='cons'; text='Ferries are weather-dependent and cancellations in rough seas can strand you for a day' }

  @{ file='budget-hostels-india'; anchor='Popular locations in Himachal and Goa sell out weeks in advance'; side='cons'; text='Lockers are common but rarely large enough for a full-size suitcase, so bring your own padlock' }
  @{ file='budget-hostels-india'; anchor='Wi-Fi speeds vary depending on mountain weather conditions'; side='pros'; text='Staff usually know the current road and permit situation better than any website does' }

  @{ file='darjeeling-tea-estate-stays'; anchor='High nightly cost due to fully inclusive meal and transport structure'; side='cons'; text='Kangchenjunga is frequently hidden by cloud, and nothing about the rate guarantees you will see it' }
  @{ file='darjeeling-tea-estate-stays'; anchor='Town traffic noise and construction surrounding lower access roads'; side='pros'; text='Being in town means you can reach the early morning Tiger Hill viewpoint without an estate transfer' }

  @{ file='eco-stays-india'; anchor='Thatch roofs require periodic smoke treatment to deter insects'; side='cons'; text='No air conditioning is a genuine problem in April and May, not a lifestyle choice' }
  @{ file='eco-stays-india'; anchor='High nightly rates covering full board and natural history guide services'; side='cons'; text='Rhino sightings are likely but never promised, and the lodge cannot control what the park delivers' }

  @{ file='hotels-near-taj-mahal-agra'; anchor='Requires vehicle transport to reach Taj Mahal entry gates'; side='cons'; text='The Taj closes to visitors on Fridays, which catches out a surprising number of one-night stays' }
  @{ file='hotels-near-taj-mahal-agra'; anchor='Surrounding Taj Nagari area is undergoing road commercialisation'; side='pros'; text='Enough distance from the monument that you avoid the worst of the tout pressure at the gates' }

  @{ file='hyderabad-luxury-hotels'; anchor='High food and beverage prices inside palace dining venues'; side='cons'; text='Access is controlled and parts of the palace close for private events with little public notice' }
  @{ file='hyderabad-luxury-hotels'; anchor='Heavy traffic along Durgam Cheruvu bridge access road during rush hours'; side='cons'; text='Nothing worth walking to after dark, so every evening out involves a car' }

  @{ file='kolkata-heritage-hotels'; anchor='Standard entry rooms are cozy rather than massive'; side='cons'; text='Chowringhee is loud from early morning and the older windows do little to stop it' }
  @{ file='kolkata-heritage-hotels'; anchor='EM Bypass traffic jams during morning and evening rush hours'; side='pros'; text='Much quicker to the airport than anywhere in the centre, which matters for an early flight' }

  @{ file='ladakh-hotels-leh'; anchor='Eco-tents feature private bathrooms but canvas walls permit night chill'; side='cons'; text='Staying outside Leh on your first night works against acclimatisation, which should come first' }
  @{ file='ladakh-hotels-leh'; anchor='Limited dining choices outside hotel and homestay dining rooms'; side='cons'; text='Power and hot water run to a schedule in the villages rather than being available on demand' }

  @{ file='rishikesh-wellness-retreats'; anchor='Steep hillside paths require buggy transport between villas and main lodge'; side='cons'; text='Rishikesh is dry and vegetarian by law, so no alcohol or meat regardless of what you are paying' }
  @{ file='rishikesh-wellness-retreats'; anchor='Construction noise from ongoing guesthouse expansion in Tapovan'; side='pros'; text='Walking distance to the river ghats and the evening aarti, which the hillside resorts are not' }

  @{ file='wildlife-lodges-ranthambore'; anchor='Extremely expensive per night without including forest safari permit fees'; side='cons'; text='The park closes to safaris from roughly July to September, so a monsoon booking buys you the tent and nothing else' }
  @{ file='wildlife-lodges-ranthambore'; anchor='Safari permit availability must still be secured via forest portal'; side='cons'; text='Your zone allocation is decided by the forest department, not the lodge, and it affects sighting odds more than the lodge does' }
)

$touched = @{}
foreach ($a in $add) {
  $p = Join-Path $dir "$($a.file).html"
  if (-not (Test-Path $p)) { Write-Host "missing: $($a.file)" -ForegroundColor Red; continue }
  $h = Get-Content $p -Raw
  $anchorLi = "<li>$($a.anchor)</li>"
  if ($h -notlike "*$anchorLi*") { Write-Host "anchor not found in $($a.file): $($a.anchor)" -ForegroundColor Yellow; continue }

  if ($a.side -eq 'cons') {
    # append after the anchor, which already sits in the cons list
    $h = $h.Replace($anchorLi, "$anchorLi`r`n              <li>$($a.text)</li>")
  } else {
    # add to the PROS list of the same block: walk back to the nearest pros list end
    $idx = $h.IndexOf($anchorLi)
    $before = $h.Substring(0, $idx)
    $pIdx = $before.LastIndexOf('</ul>')
    if ($pIdx -lt 0) { Write-Host "no pros list before anchor in $($a.file)" -ForegroundColor Yellow; continue }
    $h = $h.Substring(0, $pIdx) + "  <li>$($a.text)</li>`r`n            </ul>" + $h.Substring($pIdx + 5)
  }
  [System.IO.File]::WriteAllText($p, $h, $utf8NoBom)
  $touched[$a.file] = $true
}
Write-Host "Adjusted $($touched.Count) files, $($add.Count) bullets added" -ForegroundColor Green

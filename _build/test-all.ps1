$ErrorActionPreference = "Continue"

Write-Host "=== CHECK A: Banned Phrases in New Articles ===" -ForegroundColor Yellow
$newSlugs = @('beach-resorts-goa', 'hotels-near-taj-mahal-agra', 'himachal-hill-station-hotels', 'rishikesh-wellness-retreats', 'wildlife-lodges-ranthambore', 'hyderabad-luxury-hotels', 'kolkata-heritage-hotels', 'andaman-island-resorts', 'ladakh-hotels-leh', 'darjeeling-tea-estate-stays', 'amritsar-hotels-golden-temple', 'budget-hostels-india', 'eco-stays-india')
$banned = @('\bworld-class\b', '\bnestled\b', '\bhidden gem\b', '\bmust-visit\b', '\bboasts\b', '\bcurated\b', '\bseamless\b', '\belevate\b', '\bunparalleled\b', '\btestament to\b', '\bbreathtaking\b', '\bvibrant tapestry\b', 'Here''s what I found', 'Let''s dive in', 'It''s worth noting that', 'Whether you''re', 'not just', 'Final Thoughts', 'Verified Stay', 'I stayed', 'during my stay', 'Fact-Checked', 'reviewCount')
$aFails = 0
foreach ($slug in $newSlugs) {
  $fPath = "articles\$slug.html"
  if (Test-Path $fPath) {
    $txt = [System.IO.File]::ReadAllText($fPath)
    foreach ($b in $banned) {
      if ($txt -match $b) {
        Write-Host "FAIL A: $fPath contains '$b'" -ForegroundColor Red
        $aFails++
      }
    }
  }
}
if ($aFails -eq 0) { Write-Host "CHECK A PASSED: 0 banned phrases found across all 13 new articles!" -ForegroundColor Green }

Write-Host "`n=== CHECK B: Em Dash ===" -ForegroundColor Yellow
$bFails = 0
foreach ($f in $htmlFiles) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  if ($txt -match '—') {
    Write-Host "FAIL B: Em dash found in $($f.FullName)" -ForegroundColor Red
    $bFails++
  }
}
if ($bFails -eq 0) { Write-Host "CHECK B PASSED: 0 em dashes found!" -ForegroundColor Green }

Write-Host "`n=== CHECK C: aggregateRating in articles/ ===" -ForegroundColor Yellow
$cFiles = Get-ChildItem -Path 'articles' -Filter '*.html'
$cFails = 0
foreach ($f in $cFiles) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  if ($txt -match 'aggregateRating') {
    Write-Host "FAIL C: aggregateRating in $($f.FullName)" -ForegroundColor Red
    $cFails++
  }
}
if ($cFails -eq 0) { Write-Host "CHECK C PASSED: 0 aggregateRating found in articles/" -ForegroundColor Green }

Write-Host "`n=== CHECK D: Local href/src Links Resolution ===" -ForegroundColor Yellow
$dFails = 0
$rootPath = (Get-Item '.').FullName
foreach ($f in $htmlFiles) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  $dir = $f.DirectoryName
  # matches href="..." and src="..."
  $matches = [regex]::Matches($txt, '(?:href|src)="([^"#:]+)(?:#[^"]*)?"')
  foreach ($m in $matches) {
    $target = $m.Groups[1].Value
    if ($target -like 'http*' -or $target -like 'mailto*' -or $target -like 'tel*' -or $target -eq '') { continue }
    if ($target.StartsWith('/')) {
      $resolved = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($rootPath, $target.TrimStart('/')))
    } else {
      $resolved = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($dir, $target))
    }
    if (-not (Test-Path $resolved)) {
      Write-Host "FAIL D: In $($f.Name), link target does not exist: $target -> $resolved" -ForegroundColor Red
      $dFails++
    }
  }
}
if ($dFails -eq 0) { Write-Host "CHECK D PASSED: All local href/src targets resolve successfully!" -ForegroundColor Green }

Write-Host "`n=== CHECK E: XML / JSON-LD Validation ===" -ForegroundColor Yellow
try {
  [xml]$sm = [System.IO.File]::ReadAllText('sitemap.xml')
  Write-Host "CHECK E PASSED: sitemap.xml parsed as valid XML ($($sm.urlset.url.Count) URLs)" -ForegroundColor Green
} catch {
  Write-Host "FAIL E: sitemap.xml XML parse error: $_" -ForegroundColor Red
}
$eFails = 0
foreach ($f in $htmlFiles) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  $matches = [regex]::Matches($txt, '(?s)<script type="application/ld\+json">(.*?)</script>')
  foreach ($m in $matches) {
    try {
      $null = $m.Groups[1].Value | ConvertFrom-Json
    } catch {
      Write-Host "FAIL E: JSON-LD parse error in $($f.Name): $_" -ForegroundColor Red
      $eFails++
    }
  }
}
if ($eFails -eq 0) { Write-Host "CHECK E PASSED: All JSON-LD blocks parsed successfully!" -ForegroundColor Green }

Write-Host "`n=== CHECK F: BOM Check ===" -ForegroundColor Yellow
$allSiteFiles = Get-ChildItem -Path '.' -Include '*.html','*.xml','*.txt','*.css','*.js' -Recurse | Where-Object { $_.FullName -notmatch '\\_build\\' }
$fFails = 0
foreach ($f in $allSiteFiles) {
  $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
  if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "FAIL F: UTF-8 BOM present in $($f.FullName)" -ForegroundColor Red
    $fFails++
  }
}
if ($fFails -eq 0) { Write-Host "CHECK F PASSED: 0 BOMs found across all site files!" -ForegroundColor Green }

Write-Host "`n=== CHECK H: Word Count for Articles ===" -ForegroundColor Yellow
$hFails = 0
foreach ($f in $cFiles) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  # Strip HTML tags to approximate innerText word count
  $bodyOnly = [regex]::Replace($txt, '(?s)<script.*?</script>|<style.*?</style>|<.*?>', ' ')
  $words = ($bodyOnly -split '\s+' | Where-Object { $_ -match '\w+' }).Count
  if ($words -lt 1200) {
    Write-Host "FAIL H: $($f.Name) has $words words (under 1,200)" -ForegroundColor Red
    $hFails++
  } else {
    Write-Host "PASS H: $($f.Name) has $words words" -ForegroundColor Green
  }
}
if ($hFails -eq 0) { Write-Host "CHECK H PASSED: All 20 articles meet or exceed 1,200 words!" -ForegroundColor Green }

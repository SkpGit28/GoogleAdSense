param([string]$Key)
$ErrorActionPreference = "Stop"
$pwd = (Get-Item .).FullName
$Manifest = "$pwd\_build\manifest3.json"
. "$pwd\_build\img-util.ps1"
$j = Get-Content "$pwd\_build\candidates3.json" -Raw | ConvertFrom-Json
$cands = $j.$Key
$best = $cands[0] # Just take the first for speed, or we can sort
$slug = $Key
$wide = "$pwd\images\hotels\$slug-1200.jpg"
$fig  = "$pwd\images\hotels\$slug-800.jpg"
$tmp  = "$pwd\commons-$slug.tmp"
$ua = "PrimeHotelPicks-ImageSourcing/1.0 (skponpurpose@gmail.com)"

Invoke-WebRequest -Uri $best.url -Headers @{ "User-Agent" = $ua } -OutFile $tmp -TimeoutSec 90
Convert-Image -In $tmp -Out $fig  -W 800  -H 533 -Quality 80
Convert-Image -In $tmp -Out $wide -W 1200 -H 630 -Quality 78
Remove-Item $tmp -Force

$entry = [ordered]@{
  key         = $key
  file800     = "images/hotels/$slug-800.jpg"
  file1200    = "images/hotels/$slug-1200.jpg"
  commonsFile = $best.title
  descpage    = $best.descpage
  artist      = $best.artist
  license     = $best.license
  licenseUrl  = $best.licenseUrl
  description = $best.description
}
$entry | ConvertTo-Json -Depth 6 | Out-File -FilePath "$pwd\_build\manifest3-$key.json" -Encoding utf8


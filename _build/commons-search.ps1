# Discover candidate Wikimedia Commons images for each hotel.
# Emits JSON: for each query, up to N candidates with title, url, size, artist, license.
param(
  [Parameter(Mandatory=$true)][string]$QueryFile,   # text file: one "key|search terms" per line
  [string]$Out = "commons-candidates.json",
  [int]$Limit = 8
)
$ErrorActionPreference = "Stop"
$ua = "PrimeHotelPicks-ImageSourcing/1.0 (skponpurpose@gmail.com)"
$api = "https://commons.wikimedia.org/w/api.php"

function Strip-Html([string]$s) {
  if ([string]::IsNullOrWhiteSpace($s)) { return "" }
  $t = [regex]::Replace($s, '<[^>]+>', '')
  $t = [System.Net.WebUtility]::HtmlDecode($t)
  return ($t -replace '\s+', ' ').Trim()
}

$results = [ordered]@{}
foreach ($line in (Get-Content $QueryFile | Where-Object { $_.Trim() -ne "" -and -not $_.StartsWith("#") })) {
  $parts = $line -split '\|', 2
  $key = $parts[0].Trim()
  $q   = $parts[1].Trim()
  Write-Host "[$key] searching: $q" -ForegroundColor Cyan

  # NB: pipes in iiprop MUST be percent-encoded or MediaWiki silently returns empty imageinfo
  $uri = "$api" + "?action=query&format=json&generator=search&gsrsearch=" +
         [uri]::EscapeDataString($q) +
         "&gsrnamespace=6&gsrlimit=$Limit&prop=imageinfo&iiprop=url%7Csize%7Cmime%7Cextmetadata&iiurlwidth=1600"
  try {
    $r = Invoke-RestMethod -Uri $uri -Headers @{ "User-Agent" = $ua } -TimeoutSec 40
  } catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
    $results[$key] = @(); continue
  }

  $cands = @()
  if ($r.query -and $r.query.pages) {
    foreach ($p in $r.query.pages.PSObject.Properties.Value) {
      $ii = $p.imageinfo[0]
      if (-not $ii) { continue }
      $ext = $ii.extmetadata
      $ext_ = { param($n) if ($ext.PSObject.Properties[$n]) { Strip-Html $ext.$n.value } else { "" } }
      if ($p.title -notmatch '\.(jpg|jpeg|png|webp)$') { continue }
      if ($ii.width -lt 900) { continue }
      # landscape-ish only; portraits crop badly into 3:2 article figures
      if ($ii.height -gt 0 -and ($ii.width / $ii.height) -lt 1.05) { continue }
      $mime = $ii.mime
      $cands += [ordered]@{
        title       = $p.title
        descpage    = $ii.descriptionurl
        url         = $ii.url
        thumb       = $ii.thumburl
        width       = $ii.width
        height      = $ii.height
        mime        = $mime
        artist      = (& $ext_ 'Artist')
        credit      = (& $ext_ 'Credit')
        license     = (& $ext_ 'LicenseShortName')
        licenseUrl  = (& $ext_ 'LicenseUrl')
        usageTerms  = (& $ext_ 'UsageTerms')
        description = (& $ext_ 'ImageDescription')
      }
    }
  }
  Write-Host "  -> $($cands.Count) usable candidates" -ForegroundColor DarkGray
  $results[$key] = $cands
  Start-Sleep -Milliseconds 400
}

$results | ConvertTo-Json -Depth 8 | Set-Content -Path $Out -Encoding utf8
Write-Host "Wrote $Out" -ForegroundColor Green

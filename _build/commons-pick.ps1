# Pick the best Commons candidate per key, download, resize, and write a credits manifest.
param(
  [Parameter(Mandatory=$true)][string]$CandidatesJson,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [Parameter(Mandatory=$true)][string]$Manifest,
  [string]$HintFile = ""
)
$ErrorActionPreference = "Stop"
. "$PSScriptRoot\img-util.ps1"
$ua = "PrimeHotelPicks-ImageSourcing/1.0 (skponpurpose@gmail.com)"

# optional "key|must-contain-word" hints to bias selection toward the right subject
$hints = @{}
if ($HintFile -and (Test-Path $HintFile)) {
  foreach ($l in (Get-Content $HintFile | Where-Object { $_.Trim() -and -not $_.StartsWith("#") })) {
    $p = $l -split '\|', 2
    $hints[$p[0].Trim()] = @($p[1] -split ',' | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ })
  }
}

# reject obvious non-subject shots
$badWords = @('map','logo','coat of arms','plaque','signboard','sign board','stamp','coin','diagram','chart','graph','portrait of','statue of','bust of')

$j = Get-Content $CandidatesJson -Raw | ConvertFrom-Json
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
$picked = @()

foreach ($prop in $j.PSObject.Properties) {
  $key = $prop.Name
  $cands = @($prop.Value)
  if ($cands.Count -eq 0) { Write-Host "[$key] no candidates" -ForegroundColor Yellow; continue }

  $want = if ($hints.ContainsKey($key)) { $hints[$key] } else { @() }

  $scored = foreach ($c in $cands) {
    $t = ("$($c.title) $($c.description)").ToLower()
    $score = 0
    foreach ($w in $want) { if ($t -like "*$w*") { $score += 10 } }
    foreach ($b in $badWords) { if ($t -like "*$b*") { $score -= 25 } }
    # prefer big, prefer landscape near 3:2
    $ar = if ($c.height -gt 0) { $c.width / $c.height } else { 1.5 }
    $score += [Math]::Min(6, [int]($c.width / 800))
    $score -= [Math]::Abs($ar - 1.5) * 4
    if ($c.license -match 'CC0|public domain') { $score += 2 }
    [pscustomobject]@{ c = $c; score = $score }
  }

  $best = ($scored | Sort-Object score -Descending | Select-Object -First 1).c
  $slug = $key
  $wide = Join-Path $OutDir "$slug-1200.jpg"
  $fig  = Join-Path $OutDir "$slug-800.jpg"
  $tmp  = Join-Path $env:TEMP "commons-$slug.tmp"

  try {
    Write-Host "[$key] $($best.title)" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $best.url -Headers @{ "User-Agent" = $ua } -OutFile $tmp -TimeoutSec 90
    Convert-Image -In $tmp -Out $fig  -W 800  -H 533 -Quality 80
    Convert-Image -In $tmp -Out $wide -W 1200 -H 630 -Quality 78
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue

    $picked += [ordered]@{
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
  } catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
  }
  Start-Sleep -Milliseconds 250
}

$picked | ConvertTo-Json -Depth 6 | Set-Content -Path $Manifest -Encoding utf8
Write-Host "`nPicked $($picked.Count) images -> $Manifest" -ForegroundColor Green

# Assembles dist/ containing ONLY the files that belong on the public web.
#
# Why this exists: .vercelignore is understood by Vercel and nothing else. Deploy
# this repo to Cloudflare Pages, Netlify, GitHub Pages or anything similar and
# _build/ ships with it -- which republishes 20 unstyled, title-less duplicates
# of every article at /_build/bodies/*.html. That was the strongest single match
# for the original "low value content" rejection.
#
# Allow-list, not deny-list: anything not named here does not ship, so adding a
# new script or scratch folder to the repo cannot silently expose it.
#
# Run:  powershell -File build-dist.ps1
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$dist = Join-Path $root "dist"

if (Test-Path $dist) { Remove-Item $dist -Recurse -Force }
New-Item -ItemType Directory -Path $dist | Out-Null

# Root files that belong on the site.
$rootFiles = @(
  "index.html", "404.html", "about.html", "contact.html", "credits.html",
  "disclaimer.html", "privacy.html", "terms.html", "tools.html",
  "budget-calculator.html", "dealbreaker-quiz.html", "hotel-compare.html",
  "jargon-translator.html", "price-inflator.html",
  "ads.txt", "robots.txt", "sitemap.xml", "favicon.svg"
)

$missing = @()
foreach ($f in $rootFiles) {
  $src = Join-Path $root $f
  if (Test-Path $src) { Copy-Item $src -Destination $dist }
  else { $missing += $f }
}
if ($missing.Count -gt 0) { throw "missing expected files: $($missing -join ', ')" }

# Directories that belong on the site.
foreach ($d in @("articles", "css", "js", "images")) {
  $src = Join-Path $root $d
  if (-not (Test-Path $src)) { throw "missing expected directory: $d" }
  Copy-Item $src -Destination $dist -Recurse
}

# Nothing from the build sources may ever appear in the output.
$leaked = Get-ChildItem $dist -Recurse -Force |
  Where-Object { $_.FullName -match '\\_build\\|\.py$|\.ps1$|\.htaccess$|\\\.git' }
if ($leaked) {
  $leaked | ForEach-Object { Write-Host "  LEAKED: $($_.FullName)" -ForegroundColor Red }
  throw "build sources leaked into dist/ -- refusing to publish"
}

# Security and caching headers, in Cloudflare Pages / Netlify syntax. This is
# the portable equivalent of vercel.json; keep the two in step. 'unsafe-inline'
# in script-src is required -- all five tool pages run on inline scripts.
$headers = @"
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://pagead2.googlesyndication.com https://partner.googleadservices.com https://tpc.googlesyndication.com https://www.googletagservices.com https://googleads.g.doubleclick.net https://adservice.google.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; frame-src https://googleads.g.doubleclick.net https://tpc.googlesyndication.com; connect-src 'self' https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net; base-uri 'self'; form-action 'self'; object-src 'none'; frame-ancestors 'self'

/images/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=2592000

/js/*
  Cache-Control: public, max-age=2592000
"@
[System.IO.File]::WriteAllText((Join-Path $dist "_headers"), $headers, (New-Object System.Text.UTF8Encoding $false))

$files = (Get-ChildItem $dist -Recurse -File).Count
$bytes = (Get-ChildItem $dist -Recurse -File | Measure-Object -Property Length -Sum).Sum
Write-Host ("dist/ built: {0} files, {1:N1} MB" -f $files, ($bytes / 1MB)) -ForegroundColor Green
Write-Host "  verified: no _build/, no .py, no .ps1, no .htaccess" -ForegroundColor Green

# Verifies the precondition for deindexing: every URL that must disappear from
# Google actually returns 404 on the live site.
#
# This script CANNOT tell you whether Google has dropped a URL from its index --
# scraping Google results is against their terms and gets blocked. The index
# check is manual, in Search Console. What this does check is the thing that
# makes deindexing happen at all: a real 404. If any URL below still returns
# 200, Google will keep it indexed no matter how long you wait.
#
# Run:  powershell -File _build\check-deindex.ps1

$site = "https://primehotelpicks.com"

# Must be GONE (404). Sampled across every category that used to leak.
$mustBeGone = @(
  "/_build/bodies/rajasthan-palace-hotels.html",
  "/_build/bodies/budget-hostels-india.html",
  "/_build/bodies/eco-stays-india.html",
  "/_build/build.ps1",
  "/_build/articles.json",
  "/_build/articles2.json",
  "/_build/image-manifest.json",
  "/_build/candidates2.json",
  "/_build/test-runner.html",
  "/build_extra_tools.py",
  "/fix_js.py",
  "/optimize_mobile.py",
  "/update_nav.py"
)

# Must be PRESENT (200). If one of these 404s, a deploy is incomplete.
$mustExist = @(
  "/",
  "/index.html",
  "/articles/index.html",
  "/articles/rajasthan-palace-hotels.html",
  "/tools.html",
  "/about.html",
  "/contact.html",
  "/privacy.html",
  "/ads.txt",
  "/sitemap.xml",
  "/robots.txt"
)

function Get-Status([string]$url) {
  # HttpWebRequest rather than Invoke-WebRequest: Windows PowerShell 5.1 has no
  # -SkipHttpErrorCheck, so a 404 throws before the status can be read.
  try {
    $req = [System.Net.HttpWebRequest]::Create($url)
    $req.Method = "HEAD"
    $req.AllowAutoRedirect = $false
    $req.Timeout = 20000
    $req.UserAgent = "PrimeHotelPicks-deindex-check/1.0"
    $resp = $req.GetResponse()
    $code = [int]$resp.StatusCode
    $resp.Close()
    return $code
  } catch [System.Net.WebException] {
    if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
    return 0
  } catch {
    return 0
  }
}

$fail = 0

Write-Host ""
Write-Host "Must be GONE (expect 404)" -ForegroundColor Cyan
foreach ($p in $mustBeGone) {
  $code = Get-Status "$site$p"
  $ok = ($code -eq 404 -or $code -eq 410)
  if (-not $ok) { $fail++ }
  $colour = if ($ok) { "Green" } else { "Red" }
  Write-Host ("  {0,-46} {1}" -f $p, $code) -ForegroundColor $colour
}

Write-Host ""
Write-Host "Must EXIST (expect 200)" -ForegroundColor Cyan
foreach ($p in $mustExist) {
  $code = Get-Status "$site$p"
  $ok = ($code -eq 200)
  if (-not $ok) { $fail++ }
  $colour = if ($ok) { "Green" } else { "Red" }
  Write-Host ("  {0,-46} {1}" -f $p, $code) -ForegroundColor $colour
}

Write-Host ""
if ($fail -eq 0) {
  Write-Host "All good. The 404s are live, so Google can now drop these URLs." -ForegroundColor Green
  Write-Host "Next: Search Console > URL Inspection on a _build/ URL. You want" -ForegroundColor Green
  Write-Host "'URL is not on Google'. Until then they are removed from the site" -ForegroundColor Green
  Write-Host "but may still appear in search results." -ForegroundColor Green
} else {
  Write-Host "$fail check(s) failed - see red above. Fix before reapplying to AdSense." -ForegroundColor Red
  exit 1
}

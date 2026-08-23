# Builds articles/*.html, credits.html and sitemap.xml from _build/ sources.
# Run:  powershell -File _build\build.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$site = "https://primehotelpicks.com"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$build = $PSScriptRoot

function HtmlEnc([string]$s) { [System.Net.WebUtility]::HtmlEncode($s) }

# ---------------------------------------------------------------- shared parts
function Head($m, $depth) {
  $up = if ($depth -eq 1) { "../" } else { "" }
  $canonical = "$site/" + $(if ($depth -eq 1) { "articles/" } else { "" }) + $m.slug + ".html"
  $og = "$site/" + $m.ogImage

  $hotelItems = ""
  $pos = 0
  foreach ($h in $m.hotels) {
    $addr = @()
    if ($h.street)   { $addr += '"streetAddress": ' + (ConvertTo-Json $h.street) }
    $addr += '"addressLocality": ' + (ConvertTo-Json $h.locality)
    if ($h.region)   { $addr += '"addressRegion": ' + (ConvertTo-Json $h.region) }
    $addr += '"addressCountry": "IN"'
    # NOTE: deliberately no aggregateRating and no Review. Publishing invented
    # ratings for a third-party business breaks Google's structured data policy.
    $pos++
    $hotelItems += @"
      {
        "@type": "ListItem",
        "position": $pos,
        "item": {
          "@type": "Hotel",
          "name": $(ConvertTo-Json $h.name),
          "address": { "@type": "PostalAddress", $($addr -join ', ') },
          "priceRange": $(ConvertTo-Json $h.priceRange)
        }
      },
"@
  }

  $hotelLd = ""
  if ($hotelItems) {
    $hotelItems = $hotelItems.TrimEnd(",`r`n".ToCharArray())
    # An ItemList of the properties discussed, rather than loose Hotel entities
    # claiming this page *is* each business.
    $hotelLd = @"

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": $(ConvertTo-Json ("Properties covered in: " + $m.title)),
    "itemListOrder": "https://schema.org/ItemListOrderAscending",
    "numberOfItems": $pos,
    "itemListElement": [
$hotelItems
    ]
  }
  </script>
"@
  }

  $kw = ($m.keywords | ForEach-Object { ConvertTo-Json $_ }) -join ', '

  @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" type="image/svg+xml" href="${up}favicon.svg">

  <meta name="description" content="$(HtmlEnc $m.description)">
  <title>$(HtmlEnc $m.title) - Prime Hotel Picks</title>
  <link rel="canonical" href="$canonical">
  <link rel="stylesheet" href="${up}css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">

  <meta property="og:type" content="article">
  <meta property="og:title" content="$(HtmlEnc $m.title)">
  <meta property="og:description" content="$(HtmlEnc $m.description)">
  <meta property="og:url" content="$canonical">
  <meta property="og:image" content="$og">
  <meta property="og:site_name" content="Prime Hotel Picks">
  <meta property="og:locale" content="en_IN">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="$(HtmlEnc $m.title)">
  <meta name="twitter:description" content="$(HtmlEnc $m.description)">
  <meta name="twitter:image" content="$og">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": $(ConvertTo-Json $m.title),
    "description": $(ConvertTo-Json $m.description),
    "author": { "@type": "Person", "name": "Sushant Kumar", "url": "$site/about.html" },
    "publisher": {
      "@type": "Organization",
      "@id": "$site/#organization",
      "name": "Prime Hotel Picks",
      "url": "$site",
      "logo": { "@type": "ImageObject", "url": "$site/images/logo.png", "width": 600, "height": 120 }
    },
    "datePublished": "$($m.published)",
    "dateModified": "$($m.updated)",
    "mainEntityOfPage": { "@type": "WebPage", "@id": "$canonical" },
    "image": ["$og"],
    "keywords": [$kw],
    "articleSection": $(ConvertTo-Json $m.region),
    "inLanguage": "en-IN"
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "$site/" },
      { "@type": "ListItem", "position": 2, "name": $(ConvertTo-Json $m.title), "item": "$canonical" }
    ]
  }
  </script>$hotelLd
  <script>
  /* Must run before the AdSense script below. Declining (or ignoring the
     banner) leaves ads non-personalised; only an explicit Accept turns
     personalisation on. Changing the choice reloads the page so this re-runs. */
  (function () {
    var ok = false;
    try { ok = localStorage.getItem('cookieConsent') === 'accepted'; } catch (e) {}
    (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = ok ? 0 : 1;
  })();
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6151386626480770" crossorigin="anonymous"></script>
</head>
"@
}

function Header($up, $active) {
  $a = { param($p) if ($active -eq $p) { ' class="active"' } else { '' } }
  @"
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="header">
    <div class="header-top">
      <a href="${up}index.html" class="logo">Prime Hotel <span>Picks</span></a>
      <button class="menu-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="site-nav">&#9776;</button>
      <nav class="nav" id="site-nav">
        <a href="${up}index.html"$(& $a 'home')>Home</a>
        <a href="$(if ($up) { "index.html" } else { "articles/index.html" })"$(& $a 'guides')>Guides</a>
        <a href="${up}tools.html"$(& $a 'tools')>Tools</a>
        <a href="${up}about.html"$(& $a 'about')>About</a>
        <a href="${up}contact.html"$(& $a 'contact')>Contact</a>
      </nav>
    </div>
  </header>
"@
}

function Footer($up) {
  @"
  <footer class="footer">
    <div class="footer-grid">
      <div class="footer-col">
        <h2>Prime Hotel Picks</h2>
        <p>Researched guides to where you actually stay in India. Rates, locations and trade-offs, checked and dated.</p>
      </div>
      <div class="footer-col">
        <h2>Site</h2>
        <ul>
          <li><a href="${up}index.html">Home</a></li>
          <li><a href="$(if ($up) { "index.html" } else { "articles/index.html" })">All guides</a></li>
          <li><a href="${up}tools.html">Tools</a></li>
          <li><a href="${up}about.html">About</a></li>
          <li><a href="${up}contact.html">Contact</a></li>
          <li><a href="${up}credits.html">Photo credits</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>Legal</h2>
        <ul>
          <li><a href="${up}privacy.html">Privacy Policy</a></li>
          <li><a href="${up}terms.html">Terms of Service</a></li>
          <li><a href="${up}disclaimer.html">Disclaimer</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Prime Hotel Picks</p>
      <p>Hotel photographs are credited to their photographers on the <a href="${up}credits.html">credits page</a>.</p>
    </div>
  </footer>

  <script src="${up}js/main.js"></script>

  <div class="cookie-consent">
    <div class="cookie-consent__inner">
      <div class="cookie-consent__text">
        This site shows advertising from Google. Accept and you will see personalised ads. Decline,
        or ignore this, and ads stay non-personalised. <a href="${up}privacy.html">Read the privacy policy</a>.
      </div>
      <div class="cookie-consent__buttons">
        <button class="cookie-consent__btn cookie-consent__btn--accept">Accept</button>
        <button class="cookie-consent__btn cookie-consent__btn--decline">Decline</button>
      </div>
    </div>
  </div>
</body>
</html>
"@
}

# ---------------------------------------------------------------- articles
# metadata may be split across articles.json, articles2.json, ... so they stay editable
$all = @()
foreach ($f in (Get-ChildItem "$build\articles*.json" | Sort-Object Name)) {
  $all += (Get-Content $f.FullName -Raw | ConvertFrom-Json).articles
}

# sidebar: 5 most recent other articles + destination list
function Sidebar($current) {
  $others = $all | Where-Object { $_.slug -ne $current } | Select-Object -First 6
  $pop = ""
  $i = 1
  foreach ($o in ($others | Select-Object -First 5)) {
    $pop += "          <li><a href=""$($o.slug).html""><span class=""popular-number"">$('{0:D2}' -f $i)</span>$(HtmlEnc $o.shortTitle)</a></li>`n"
    $i++
  }
  $dest = ""
  $cur = $all | Where-Object { $_.slug -eq $current } | Select-Object -First 1
  $sameGroup = $all | Where-Object { $_.slug -ne $current -and $_.group -eq $cur.group } |
                 Sort-Object itemOrder
  $otherGroup = $all | Where-Object { $_.slug -ne $current -and $_.group -ne $cur.group } |
                 Sort-Object groupOrder, itemOrder
  foreach ($o in (@($sameGroup) + @($otherGroup) | Select-Object -First 6)) {
    $dest += "          <li><a href=""$($o.slug).html"">$(HtmlEnc $o.place)</a></li>`n"
  }
  @"
    <aside class="sidebar">
      <div class="sidebar-widget">
        <h3>More guides</h3>
        <ul>
$pop        </ul>
      </div>
      <div class="sidebar-widget">
        <h3>Destinations</h3>
        <ul>
$dest        </ul>
      </div>
    </aside>
"@
}

# ---------------------------------------------------------------- body checks
# Two defects reached production undetected and read to a crawler as
# auto-generated junk:
#   * budget-hostels-india had whole sections injected inside a <tbody> and a
#     <ul>, which mangled the table that followed.
#   * andaman-island-resorts repeated three entire sections verbatim.
# Both are cheap to detect, so the build now refuses to emit a broken body.
function Test-Body([string]$html) {
  $problems = @()

  # Block-level content must never appear inside a <tbody> or a <ul>.
  foreach ($pair in @(@('<tbody>', '</tbody>'), @('<ul[^>]*>', '</ul>'))) {
    $rx = [regex]::new($pair[0] + '(.*?)' + $pair[1], 'Singleline')
    foreach ($mm in $rx.Matches($html)) {
      if ($mm.Groups[1].Value -match '<h2|<p>') {
        $problems += "block-level content nested inside $($pair[0])"
        break
      }
    }
  }

  # Article-level <h2> headings must be unique. Hotel names use
  # <h2 class="hotel-entry__title"> and are deliberately not matched here.
  $heads = [regex]::Matches($html, '<h2>([^<]*)</h2>') | ForEach-Object { $_.Groups[1].Value.Trim() }
  $dupes = $heads | Group-Object | Where-Object { $_.Count -gt 1 } | ForEach-Object { $_.Name }
  foreach ($d in $dupes) { $problems += "duplicate section heading: '$d'" }

  # Tag balance.
  foreach ($t in @('tbody', 'ul', 'table', 'figure')) {
    $o = ([regex]::Matches($html, "<$t[ >]")).Count
    $c = ([regex]::Matches($html, "</$t>")).Count
    if ($o -ne $c) { $problems += "unbalanced <$t>: $o open, $c close" }
  }

  return $problems
}

$built = 0
$bodyErrors = 0
foreach ($m in $all) {
  $bodyFile = "$build\bodies\$($m.slug).html"
  if (-not (Test-Path $bodyFile)) { Write-Host "skip (no body): $($m.slug)" -ForegroundColor DarkYellow; continue }
  $body = Get-Content $bodyFile -Raw

  $problems = Test-Body $body
  if ($problems.Count -gt 0) {
    $bodyErrors++
    Write-Host "BROKEN BODY: $($m.slug)" -ForegroundColor Red
    foreach ($pr in $problems) { Write-Host "    - $pr" -ForegroundColor Red }
    continue
  }

  $board = ""
  foreach ($f in $m.board) {
    $board += "        <dl><dt>$(HtmlEnc $f.k)</dt><dd>$(HtmlEnc $f.v)</dd></dl>`n"
  }

  $html = (Head $m 1) + (Header "../" "") + @"

  <div class="article-header">
    <div class="article-header__inner">
      <h1>$(HtmlEnc $m.h1)</h1>
      <div class="article-meta-bar">
        <span>Published $($m.publishedLabel)</span>
        <span>Updated $($m.updatedLabel)</span>
        <span class="badge badge--checked">Rates checked $($m.ratesChecked)</span>
      </div>
      <div class="platform-board">
$board      </div>
    </div>
  </div>

  <div class="content-layout">
    <main id="main" class="article-content">
      <div class="ad-slot ad-top"></div>

      <div class="author-card">
        <img src="../images/author-sushant-kumar.jpg" srcset="../images/author-sushant-kumar.jpg 1x, ../images/author-sushant-kumar@2x.jpg 2x" alt="Illustrated portrait of Sushant Kumar" class="author-card__photo" width="64" height="64">
        <div class="author-card__info">
          <div class="author-card__name">Sushant Kumar</div>
          <div class="author-card__title">Founder and Editor</div>
          <div class="author-card__bio">I research and write every guide on this site myself, from published rates, hotel material and guest reviews read in bulk. I have not stayed at every property here and I do not pretend to have.</div>
          <div class="author-card__meta">
            <span>Updated $($m.updatedLabel)</span>
            <span class="badge badge--sourced">Researched, not a paid stay</span>
          </div>
        </div>
      </div>

      <div class="methodology-box">
        <div class="methodology-box__header">
          <h2>How these hotels were researched</h2>
          <span class="methodology-box__toggle">&#9660;</span>
        </div>
        <div class="methodology-box__content">
          <ul>
            <li><strong>Rates:</strong> compared across more than one booking platform on the same day, quoted as a range with the month checked. Not a quote, and they move.</li>
            <li><strong>Guest reviews in bulk:</strong> looking for complaints that repeat across many months, not single bad nights.</li>
            <li><strong>Location:</strong> checked against a map, measured to the thing you actually came for.</li>
            <li><strong>Real cost of entry:</strong> taxes, compulsory meal plans, transfers, and what is not included in the headline rate.</li>
            <li><strong>What I could not confirm</strong> is said plainly in the text rather than filled in.</li>
          </ul>
          <div class="methodology-box__disclosure">Prime Hotel Picks is independently run. Some booking links may earn a commission at no extra cost to you. No hotel pays to be included, and criticism is not removed on request. Photographs are credited to their photographers on the <a href="../credits.html">credits page</a>.</div>
        </div>
      </div>

$body
      <div class="ad-slot ad-bottom"></div>
    </main>
$(Sidebar $m.slug)  </div>

"@ + (Footer "../")

  # WriteAllText with a BOM-less encoder: Set-Content -Encoding utf8 emits a BOM on
  # Windows PowerShell 5.1, which has previously broken XML/HTML parsing on this site.
  [System.IO.File]::WriteAllText("$root\articles\$($m.slug).html", $html, $utf8NoBom)
  $built++
}
Write-Host "Built $built articles" -ForegroundColor Green
if ($bodyErrors -gt 0) {
  throw "$bodyErrors body file(s) failed validation and were NOT built. Fix them and re-run; see the red output above."
}

# ---------------------------------------------------------------- credits.html
$man = Get-Content "$build\image-manifest.json" -Raw | ConvertFrom-Json
$rows = ""
foreach ($e in ($man | Sort-Object key)) {
  $lic = if ($e.licenseUrl) { "<a href=""$($e.licenseUrl)"" rel=""nofollow noopener"">$(HtmlEnc $e.license)</a>" } else { HtmlEnc $e.license }
  $artist = if ($e.artist) { HtmlEnc $e.artist } else { "Not stated on the file page" }
  $rows += @"
      <tr>
        <td><img src="$($e.file800)" alt="" width="80" height="53" loading="lazy" style="width:80px;height:auto;border:1px solid var(--rule);"></td>
        <td>$(HtmlEnc (($e.commonsFile -replace '^File:','')))</td>
        <td>$artist</td>
        <td>$lic</td>
        <td><a href="$($e.descpage)" rel="nofollow noopener">File page</a></td>
      </tr>

"@
}

$credits = (Head @{
  slug='credits'; title='Photo credits and licences'; description='Every photograph on Prime Hotel Picks, with the photographer, the licence it is used under, and a link to the original file.';
  ogImage='images/logo.png'; published='2026-07-27'; updated='2026-07-27'; region='India'; keywords=@('photo credits','image licences'); hotels=@()
} 0)

# Head() emits article schema; for credits we want a plain page, so rebuild minimally
$credits = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <meta name="description" content="Every photograph used on Prime Hotel Picks, with the photographer, the licence, and a link to the original file on Wikimedia Commons.">
  <title>Photo credits and licences - Prime Hotel Picks</title>
  <link rel="canonical" href="$site/credits.html">
  <link rel="stylesheet" href="css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
  <script>
  /* Must run before the AdSense script below. Declining (or ignoring the
     banner) leaves ads non-personalised; only an explicit Accept turns
     personalisation on. Changing the choice reloads the page so this re-runs. */
  (function () {
    var ok = false;
    try { ok = localStorage.getItem('cookieConsent') === 'accepted'; } catch (e) {}
    (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = ok ? 0 : 1;
  })();
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6151386626480770" crossorigin="anonymous"></script>
</head>
"@ + (Header "" "") + @"

  <div class="article-header">
    <div class="article-header__inner">
      <h1 class="marker">Photo credits</h1>
      <div class="article-meta-bar"><span>Last updated: 27 July 2026</span></div>
    </div>
  </div>

  <main id="main" class="legal-page">
    <p>Prime Hotel Picks does not own the hotel photographs on this site and does not claim to
      have taken them. Every image below came from Wikimedia Commons and is used under the
      licence shown against it.</p>

    <p>Most are Creative Commons licences that require attribution, which is what this page is
      for. If you are the photographer of any image here and the credit is wrong or you want the
      photograph removed, email
      <a href="mailto:webmedia263@gmail.com">webmedia263@gmail.com</a> and I will
      correct or remove it.</p>

    <p>A photograph appearing here is not an endorsement by the photographer of anything written
      on this site. Where an image shows a location near a hotel rather than the hotel itself,
      the caption on the page says so.</p>

    <div class="table-scroll">
    <table class="credits-table">
      <thead>
        <tr><th>Image</th><th>File</th><th>Photographer</th><th>Licence</th><th>Source</th></tr>
      </thead>
      <tbody>
$rows      </tbody>
    </table>
    </div>

    <h2>The author portrait</h2>
    <p>The illustrated portrait of Sushant Kumar used on the <a href="about.html">about page</a>
      and on article bylines is a generated illustration, not a photograph of a person. It is
      labelled as an illustration wherever it appears.</p>
  </main>

"@ + (Footer "")

[System.IO.File]::WriteAllText("$root\credits.html", $credits, $utf8NoBom)
Write-Host "Built credits.html ($($man.Count) images)" -ForegroundColor Green

# ---------------------------------------------------------------- articles/index.html
# A real archive. Before this the 20 guides hung off the homepage grid and a
# randomised sidebar, with no topical structure and nothing in the nav.
$groups = $all | Group-Object group | Sort-Object { $_.Group[0].groupOrder }

$sections = ""
foreach ($g in $groups) {
  $cards = ""
  foreach ($o in ($g.Group | Sort-Object itemOrder)) {
    $cards += @"
        <li class="archive-item">
          <a href="$($o.slug).html">
            <span class="archive-item__place">$(HtmlEnc $o.place)</span>
            <span class="archive-item__title">$(HtmlEnc $o.shortTitle)</span>
            <span class="archive-item__desc">$(HtmlEnc $o.description)</span>
            <span class="archive-item__meta">Updated $($o.updatedLabel) &middot; Rates checked $($o.ratesChecked)</span>
          </a>
        </li>

"@
  }
  $sections += @"
      <section class="archive-group">
        <h2>$(HtmlEnc $g.Name)</h2>
        <ul class="archive-list">
$cards        </ul>
      </section>

"@
}

$archiveLd = ""
$i = 1
foreach ($g in $groups) {
  foreach ($o in ($g.Group | Sort-Object itemOrder)) {
    $archiveLd += "      { ""@type"": ""ListItem"", ""position"": $i, ""url"": ""$site/articles/$($o.slug).html"", ""name"": $(ConvertTo-Json $o.title) },`n"
    $i++
  }
}
$archiveLd = $archiveLd.TrimEnd(",`n".ToCharArray())

$archive = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <meta name="description" content="Every hotel guide on Prime Hotel Picks, grouped by where in India it covers. $($all.Count) researched guides, each with the month its rates were checked.">
  <title>All hotel guides - Prime Hotel Picks</title>
  <link rel="canonical" href="$site/articles/index.html">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "All hotel guides",
    "url": "$site/articles/index.html",
    "isPartOf": { "@id": "$site/#organization" },
    "mainEntity": {
      "@type": "ItemList",
      "numberOfItems": $($all.Count),
      "itemListElement": [
$archiveLd
      ]
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "$site/" },
      { "@type": "ListItem", "position": 2, "name": "All guides", "item": "$site/articles/index.html" }
    ]
  }
  </script>
  <script>
  /* Must run before the AdSense script below. Declining (or ignoring the
     banner) leaves ads non-personalised; only an explicit Accept turns
     personalisation on. Changing the choice reloads the page so this re-runs. */
  (function () {
    var ok = false;
    try { ok = localStorage.getItem('cookieConsent') === 'accepted'; } catch (e) {}
    (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = ok ? 0 : 1;
  })();
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6151386626480770" crossorigin="anonymous"></script>
</head>
"@ + (Header "../" "guides") + @"

  <div class="article-header">
    <div class="article-header__inner">
      <h1 class="marker">All guides</h1>
      <div class="article-meta-bar">
        <span>$($all.Count) guides</span>
        <span class="badge badge--sourced">Researched, not paid stays</span>
      </div>
    </div>
  </div>

  <main id="main" class="archive-page">
    <p class="archive-intro">Every guide on the site, grouped by where it covers. Each one states the
      month its rates were checked and says plainly what could not be confirmed. None of them are
      paid placements, and at least one property in most guides is one I suggest you skip. How the
      research is done is set out on the <a href="../about.html">about page</a>.</p>

$sections  </main>

"@ + (Footer "../")

[System.IO.File]::WriteAllText("$root\articles\index.html", $archive, $utf8NoBom)
Write-Host "Built articles/index.html ($($all.Count) guides in $($groups.Count) groups)" -ForegroundColor Green

# ---------------------------------------------------------------- sitemap.xml
# Per-URL lastmod. A sitemap asserting that every page changed on the same
# hardcoded day is both untrue and a weak crawl signal.
function FileStamp([string]$relPath) {
  $full = Join-Path $root $relPath
  if (Test-Path $full) { return (Get-Item $full).LastWriteTime.ToString("yyyy-MM-dd") }
  return (Get-Date).ToString("yyyy-MM-dd")
}
$urls = @(
  @{ loc = "$site/";              pri = "1.0"; freq = "weekly" },
  @{ loc = "$site/articles/index.html"; pri = "0.9"; freq = "weekly" },
  @{ loc = "$site/tools.html"; pri = "0.9"; freq = "monthly" },
  @{ loc = "$site/jargon-translator.html"; pri = "0.8"; freq = "monthly" },
  @{ loc = "$site/price-inflator.html"; pri = "0.8"; freq = "monthly" },
  @{ loc = "$site/dealbreaker-quiz.html"; pri = "0.8"; freq = "monthly" },
  @{ loc = "$site/budget-calculator.html"; pri = "0.8"; freq = "monthly" },
  @{ loc = "$site/hotel-compare.html"; pri = "0.8"; freq = "monthly" },
  @{ loc = "$site/about.html";    pri = "0.6"; freq = "monthly" },
  @{ loc = "$site/contact.html";  pri = "0.4"; freq = "yearly" },
  @{ loc = "$site/credits.html";  pri = "0.3"; freq = "monthly" },
  @{ loc = "$site/privacy.html";  pri = "0.3"; freq = "yearly" },
  @{ loc = "$site/terms.html";    pri = "0.3"; freq = "yearly" },
  @{ loc = "$site/disclaimer.html"; pri = "0.3"; freq = "yearly" }
)
foreach ($m in $all) {
  if (Test-Path "$root\articles\$($m.slug).html") {
    $urls += @{ loc = "$site/articles/$($m.slug).html"; pri = "0.8"; freq = "monthly"; lastmod = $m.updated }
  }
}
$sm = '<?xml version="1.0" encoding="UTF-8"?>' + "`n" + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "`n"
foreach ($u in $urls) {
  $stamp = if ($u.lastmod) { $u.lastmod } else { FileStamp ($u.loc -replace [regex]::Escape("$site/"), "" -replace "^$", "index.html") }
  $sm += "  <url>`n    <loc>$($u.loc)</loc>`n    <lastmod>$stamp</lastmod>`n    <changefreq>$($u.freq)</changefreq>`n    <priority>$($u.pri)</priority>`n  </url>`n"
}
$sm += '</urlset>' + "`n"
# no BOM: a BOM breaks XML parsing for some crawlers
[System.IO.File]::WriteAllText("$root\sitemap.xml", $sm, (New-Object System.Text.UTF8Encoding $false))
Write-Host "Built sitemap.xml ($($urls.Count) urls)" -ForegroundColor Green






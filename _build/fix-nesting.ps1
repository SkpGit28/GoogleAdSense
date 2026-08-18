# Repairs body fragments where the second pros-cons block was never closed, which
# left the third .hotel-entry nested inside a <ul>. Tag COUNTS balanced, so only a
# real DOM parse caught it. Three orphan </div> ended up after the highlight-box,
# and the mid-article ad slot was stranded at the very end of the file.
$ErrorActionPreference = "Stop"
$dir = Join-Path $PSScriptRoot "bodies"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$fixed = @()

foreach ($f in (Get-ChildItem "$dir\*.html" | Sort-Object Name)) {
  $h = Get-Content $f.FullName -Raw
  $orig = $h

  # 1. close the cons section / pros-cons / hotel-entry before the next entry
  $h = [regex]::Replace($h,
    '(?m)^(\s*)</ul>\r?\n(\s*)<div class="hotel-entry">',
    "`$1</ul>`r`n          </div>`r`n        </div>`r`n      </div>`r`n`r`n`$2<div class=`"hotel-entry`">")

  # 2. drop the three orphan closers that ended up after the highlight-box
  $h = [regex]::Replace($h,
    '(?m)^      </div>\r?\n          </div>\r?\n        </div>\r?\n      </div>\r?\n',
    "      </div>`r`n")

  # 3. the mid-article ad slot belongs between entries, not after everything.
  #    build.ps1 already emits ad-top and ad-bottom, so remove any trailing one
  #    and reinsert before the second hotel entry.
  $h = [regex]::Replace($h, '(?s)\r?\n\s*<div class="ad-slot ad-in-content"></div>\s*$', "`r`n")
  if ($h -notmatch 'ad-in-content') {
    $n = 0
    $h = [regex]::Replace($h, '(?m)^(\s*)<div class="hotel-entry">', {
      param($m)
      $script:n++
      if ($script:n -eq 2) { "      <div class=`"ad-slot ad-in-content`"></div>`r`n`r`n$($m.Groups[1].Value)<div class=`"hotel-entry`">" }
      else { $m.Value }
    })
  }

  if ($h -ne $orig) {
    [System.IO.File]::WriteAllText($f.FullName, $h, $utf8NoBom)
    $fixed += $f.BaseName
  }
}
Write-Host "Repaired $($fixed.Count) fragments:" -ForegroundColor Green
$fixed | ForEach-Object { "  $_" }

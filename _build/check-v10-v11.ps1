$files = Get-ChildItem -Path 'articles' -Filter '*.html'
$v10Nested = 0
$v10Invalid = 0
$totalProsCons = 0
$symmetricCount = 0

foreach ($f in $files) {
    $html = New-Object -ComObject "htmlfile"
    $html.IHTMLDocument2_write([System.IO.File]::ReadAllText($f.FullName))
    $html.Close()

    # V10: nested hotel-entry
    $entries = $html.getElementsByTagName("div") | Where-Object { $_.className -match '\bhotel-entry\b' -and $_.className -notmatch '__' }
    foreach ($entry in $entries) {
        $parent = $entry.parentElement
        while ($parent -ne $null) {
            if ($parent.className -match '\bhotel-entry\b' -and $parent.className -notmatch '__') {
                $v10Nested++
                Write-Host "V10 FAIL: Nested hotel-entry in $($f.Name)" -ForegroundColor Red
                break
            }
            $parent = $parent.parentElement
        }
    }

    # V10: invalid UL children
    $uls = $html.getElementsByTagName("ul")
    foreach ($ul in $uls) {
        $children = $ul.children
        foreach ($child in $children) {
            $tag = $child.tagName.ToLower()
            $cls = $child.className
            if ($tag -eq 'table' -or $tag -eq 'figure' -or ($cls -match '\bhotel-entry\b' -and $cls -notmatch '__') -or ($cls -match '\bfacts\b')) {
                $v10Invalid++
                Write-Host "V10 FAIL: Invalid child <$tag class='$cls'> inside UL in $($f.Name)" -ForegroundColor Red
            }
        }
    }

    # V11: Pros/cons symmetry
    $prosCons = $html.getElementsByTagName("div") | Where-Object { $_.className -match '\bpros-cons\b' -and $_.className -notmatch '__' }
    foreach ($pc in $prosCons) {
        $totalProsCons++
        $pros = 0
        $cons = 0
        $sections = $pc.getElementsByTagName("div")
        foreach ($sec in $sections) {
            if ($sec.className -match '\bpros--section\b') {
                $pros = @($sec.getElementsByTagName("li")).Count
            }
            if ($sec.className -match '\bcons--section\b') {
                $cons = @($sec.getElementsByTagName("li")).Count
            }
        }
        if ($pros -gt 0 -and $cons -gt 0 -and $pros -eq $cons) {
            $symmetricCount++
        }
    }
}

Write-Host "`nV10 Results:"
Write-Host "Nested hotel-entry blocks: $v10Nested"
Write-Host "Invalid UL children: $v10Invalid"

if ($totalProsCons -gt 0) {
    $symPct = [Math]::Round(($symmetricCount / $totalProsCons) * 100, 1)
    Write-Host "`nV11 Results:"
    Write-Host "Total pros-cons blocks: $totalProsCons"
    Write-Host "Symmetric blocks: $symmetricCount ($symPct%)"
    if ($symPct -le 35) {
        Write-Host "V11 PASSED: Symmetry is <= 35%" -ForegroundColor Green
    } else {
        Write-Host "V11 FAIL: Symmetry > 35%" -ForegroundColor Red
    }
}


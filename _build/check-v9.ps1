$files = Get-ChildItem -Path 'articles' -Filter '*.html'
$v9Fails = 0
foreach ($f in $files) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  
  if ($txt -notmatch 'could not confirm') { Write-Host "FAIL: $($f.Name) missing 'could not confirm'" -ForegroundColor Red; $v9Fails++ }
  if ($txt -notmatch 'skip') { Write-Host "FAIL: $($f.Name) missing 'skip'" -ForegroundColor Red; $v9Fails++ }
  if ($txt -notmatch 'Rates checked') { Write-Host "FAIL: $($f.Name) missing 'Rates checked'" -ForegroundColor Red; $v9Fails++ }
  
  $photoCount = ([regex]::Matches($txt, 'Photo:')).Count
  $figCount = ([regex]::Matches($txt, '<figcaption')).Count
  if ($photoCount -lt $figCount) { Write-Host "FAIL: $($f.Name) missing 'Photo:' credit in figcaption" -ForegroundColor Red; $v9Fails++ }
}
if ($v9Fails -eq 0) { Write-Host "CHECK V9 PASSED!" -ForegroundColor Green }
$htmlFiles = Get-ChildItem -Path '.' -Filter '*.html' -Recurse | Where-Object { $_.FullName -notmatch '\\_build\\' }
foreach ($f in $htmlFiles) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  $matches = [regex]::Matches($txt, '<img[^>]*>')
  foreach ($m in $matches) {
    if ($m.Value -notmatch 'width=' -or $m.Value -notmatch 'height=') {
      Write-Host "FAIL: $($f.Name) missing width/height: $($m.Value)" -ForegroundColor Red
    }
  }
}
Write-Host "Done checking images."
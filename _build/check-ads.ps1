$files = Get-ChildItem -Path 'articles' -Filter '*.html'
foreach ($f in $files) {
  $txt = [System.IO.File]::ReadAllText($f.FullName)
  $topCount = ([regex]::Matches($txt, 'ad-top')).Count
  $midCount = ([regex]::Matches($txt, 'ad-in-content')).Count
  $botCount = ([regex]::Matches($txt, 'ad-bottom')).Count
  
  if ($topCount -ne 1 -or $midCount -ne 1 -or $botCount -ne 1) {
    Write-Host "FAIL: $($f.Name) has incorrect ad-slot counts: Top $topCount, Mid $midCount, Bot $botCount" -ForegroundColor Red
  }

  $midPos = $txt.IndexOf('ad-in-content')
  $lastEntryPos = $txt.LastIndexOf('<div class="hotel-entry">')
  
  if ($midPos -gt $lastEntryPos) {
    Write-Host "FAIL: $($f.Name) has ad-in-content AFTER the last hotel entry." -ForegroundColor Red
  }
}
Write-Host "Done checking ads."
$html = New-Object -ComObject 'htmlfile'
$html.IHTMLDocument2_write([System.IO.File]::ReadAllText('articles\amritsar-hotels-golden-temple.html'))
$html.Close()
$entries = $html.getElementsByTagName('div') | Where-Object { $_.className -match 'hotel-entry' -and $_.className -notmatch '__' }
Write-Host "Count: $($entries.Count)"
foreach ($e in $entries) {
    Write-Host "Parent class: $($e.parentElement.className)"
}
$ErrorActionPreference = "Stop"
$files = Get-ChildItem -Path 'articles' -Filter '*.html'
$nestedHotelEntry = 0
$invalidUlChildren = 0
$totalBlocks = 0
$symmetricBlocks = 0
$symDistribution = @{}

foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName)
    $html = New-Object -ComObject "htmlfile"
    $html.IHTMLDocument2_write($text)
    $html.Close()
    
    $doc = $html
    $hotelEntries = $doc.body.querySelectorAll('.hotel-entry')
    # wait, htmlfile COM object may not support querySelectorAll fully in old IE modes, but let's try
}

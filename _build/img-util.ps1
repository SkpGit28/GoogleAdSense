# Resize + centre-crop an image to exact WxH, save as JPEG (or PNG) at given quality.
Add-Type -AssemblyName System.Drawing

function Convert-Image {
  param(
    [Parameter(Mandatory=$true)][string]$In,
    [Parameter(Mandatory=$true)][string]$Out,
    [Parameter(Mandatory=$true)][int]$W,
    [Parameter(Mandatory=$true)][int]$H,
    [int]$Quality = 82,
    [switch]$Png
  )
  $src = [System.Drawing.Image]::FromFile((Resolve-Path $In).Path)
  try {
    # scale so the image covers WxH, then centre-crop
    $scale = [Math]::Max($W / $src.Width, $H / $src.Height)
    $sw = [int][Math]::Ceiling($src.Width  * $scale)
    $sh = [int][Math]::Ceiling($src.Height * $scale)
    $ox = [int](($W - $sw) / 2)
    $oy = [int](($H - $sh) / 2)

    $bmp = New-Object System.Drawing.Bitmap($W, $H)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode  = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode    = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.SmoothingMode      = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $g.Clear([System.Drawing.Color]::White)
    $g.DrawImage($src, $ox, $oy, $sw, $sh)
    $g.Dispose()

    $dir = Split-Path $Out -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

    if ($Png) {
      $bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
    } else {
      $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
      $ep = New-Object System.Drawing.Imaging.EncoderParameters(1)
      $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]$Quality)
      $bmp.Save($Out, $codec, $ep)
    }
    $bmp.Dispose()
  } finally { $src.Dispose() }
}

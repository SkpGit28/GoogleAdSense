$ErrorActionPreference = "Stop"
$pwd = (Get-Item .).FullName
$m = Get-Content "$pwd\_build\image-manifest.json" -Raw | ConvertFrom-Json
$u = Get-Content "$pwd\_build\manifest3-umaid-bhawan.json" -Raw | ConvertFrom-Json
$k = Get-Content "$pwd\_build\manifest3-itc-kohenur.json" -Raw | ConvertFrom-Json

for ($i=0; $i -lt $m.Count; $i++) {
  if ($m[$i].key -eq 'umaid-bhawan') { $m[$i] = $u }
  if ($m[$i].key -eq 'itc-kohenur')  { $m[$i] = $k }
}
$m | ConvertTo-Json -Depth 6 | Set-Content -Path "$pwd\_build\image-manifest.json" -Encoding utf8

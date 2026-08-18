$ErrorActionPreference = "Stop"
$pwd = (Get-Item .).FullName
& "$pwd\_build\commons-pick.ps1" -CandidatesJson "$pwd\_build\candidates3.json" -OutDir "$pwd\images\hotels" -Manifest "$pwd\_build\manifest3.json"
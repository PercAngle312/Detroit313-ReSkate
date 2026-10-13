param(
  [Parameter(Mandatory=$true)][string]$SourceZip,
  [Parameter(Mandatory=$true)][string]$StudioZip,
  [Parameter(Mandatory=$true)][string]$BlenderExe,
  [string]$OutputDirectory = "build_output",
  [switch]$Compile,
  [string]$GamePath = ""
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$SourceZip=(Resolve-Path -LiteralPath $SourceZip).Path
$StudioZip=(Resolve-Path -LiteralPath $StudioZip).Path
$BlenderExe=(Resolve-Path -LiteralPath $BlenderExe).Path
$OutputDirectory=[System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$Root=Join-Path $OutputDirectory 'source'
New-Item -ItemType Directory -Force -Path $Root | Out-Null
python scripts/inventory_detroit_assets.py $SourceZip
if ($LASTEXITCODE -ne 0) { throw 'Source inventory failed' }
Expand-Archive -LiteralPath $SourceZip -DestinationPath $Root -Force
$SceneScript=Get-ChildItem -LiteralPath $Root -Recurse -Filter build_detroit_studio_scene.py -File | Select-Object -First 1
if (-not $SceneScript) { throw 'Scene builder missing' }
$SceneRoot=$SceneScript.Directory.FullName
$Blend=Join-Path $OutputDirectory 'Detroit313_CampusMartius.blend'
& $BlenderExe -b --factory-startup --python $SceneScript.FullName -- $StudioZip $SceneRoot $Blend
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Blend)) { throw 'Blender scene generation failed' }
Write-Host "Built scene: $Blend"
if ($Compile) {
  if (-not $GamePath -or -not (Test-Path -LiteralPath $GamePath)) { throw 'Authorized game installation path required for compilation' }
  $CliFolder=Join-Path $OutputDirectory 'studio'
  Expand-Archive -LiteralPath $StudioZip -DestinationPath $CliFolder -Force
  $Cli=Get-ChildItem -LiteralPath $CliFolder -Filter reskate_cli.exe -Recurse | Select-Object -First 1
  if (-not $Cli) { throw 'Studio compiler not found' }
  & $Cli.FullName compile-map $GamePath $Blend (Join-Path $OutputDirectory 'compiled')
  if ($LASTEXITCODE -ne 0) { throw 'ReSkate compilation failed' }
}

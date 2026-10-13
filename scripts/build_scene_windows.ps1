param(
  [Parameter(Mandatory=$true)][string]$SourceZip,
  [Parameter(Mandatory=$true)][string]$StudioZip,
  [Parameter(Mandatory=$true)][string]$BlenderExe,
  [string]$OutputDirectory = "build_output"
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$SourceZip = (Resolve-Path -LiteralPath $SourceZip).Path
$StudioZip = (Resolve-Path -LiteralPath $StudioZip).Path
$BlenderExe = (Resolve-Path -LiteralPath $BlenderExe).Path
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

python scripts/inventory_detroit_assets.py $SourceZip
if ($LASTEXITCODE -ne 0) { throw 'Source inventory failed' }

$Expanded = Join-Path $OutputDirectory 'source'
New-Item -ItemType Directory -Force -Path $Expanded | Out-Null
Expand-Archive -LiteralPath $SourceZip -DestinationPath $Expanded -Force
$Root = Get-ChildItem -Path $Expanded -Recurse -Filter SPAWN_SURVEY_v24.json -File | Select-Object -First 1
if (-not $Root) { throw 'Source data root not found' }
$Root = $Root.Directory.FullName
$OutputBlend = Join-Path $OutputDirectory 'Detroit313_CampusMartius.blend'
$Assembler = Join-Path $PSScriptRoot 'assemble_campus.py'
if (-not (Test-Path -LiteralPath $Assembler)) { throw 'Assembler missing' }

& $BlenderExe -b --factory-startup --python $Assembler -- $Root $StudioZip $OutputBlend
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $OutputBlend)) {
  throw 'Blender scene generation failed; inspect stdout and stderr'
}
Write-Host "Scene created: $OutputBlend"
Write-Host "Compiler is deliberately not invoked here. Native map compilation requires authorized game files and a separately verified Studio runtime."

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OutputRoot,

    [Parameter(Mandatory = $true)]
    [string]$AnalysisRoot,

    [string]$Baseline = 'ST00_BASE_CONTROL',

    [string[]]$SkipDirectory = @('_SMOKE_10yr'),

    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptRoot
$pythonScript = Join-Path $projectRoot 'src\scape_quick_charts.py'

New-Item -ItemType Directory -Force -Path $AnalysisRoot | Out-Null

$skipArgs = @()
foreach ($skip in $SkipDirectory) {
    $skipArgs += @('--skip-directory', $skip)
}

& $Python $pythonScript `
    --output-root $OutputRoot `
    --analysis-root $AnalysisRoot `
    --baseline $Baseline `
    @skipArgs

if ($LASTEXITCODE -ne 0) {
    throw "scape_quick_charts.py failed with exit code $LASTEXITCODE"
}


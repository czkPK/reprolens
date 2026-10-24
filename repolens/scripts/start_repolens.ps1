param(
    [string]$Path
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not $Path) {
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = "Select the repository folder to audit"
    $dialog.ShowNewFolderButton = $false
    $result = $dialog.ShowDialog()
    if ($result -ne [System.Windows.Forms.DialogResult]::OK) {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
    $Path = $dialog.SelectedPath
}

if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    Write-Host "Folder not found: $Path" -ForegroundColor Red
    exit 1
}

$resolved = (Resolve-Path -LiteralPath $Path).Path
$outDir = Join-Path $root "reports\latest"
$env:PYTHONPATH = Join-Path $root "src"

Write-Host ""
Write-Host "ReproLens is auditing:" -ForegroundColor Cyan
Write-Host $resolved
Write-Host ""

python -m repolens audit $resolved --out-dir $outDir --explain --autofix
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Audit failed. Please share the error above." -ForegroundColor Red
    exit $LASTEXITCODE
}

$report = Join-Path $outDir "report.html"
Write-Host ""
Write-Host "Audit complete. Opening the report..." -ForegroundColor Green
Start-Process -FilePath $report

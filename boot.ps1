param (
    [string]$VAR_CONTEXT
)

& ".\venv\Scripts\Activate.ps1"

if ($VAR_CONTEXT -eq "production") {
    $VAR_CONTEXT = "production"
} else {
    $VAR_CONTEXT = "development"
}

Write-Output "environment set to: $VAR_CONTEXT"
$env:FLASK_CONTEXT = $VAR_CONTEXT
python app.py
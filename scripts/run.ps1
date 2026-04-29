$ProjectRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $ProjectRoot "src"

$PythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCommand) {
    $PythonCommand = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $PythonCommand) {
    Write-Error "Python nao foi encontrado. Instale Python 3.10 ou superior."
    exit 1
}

& $PythonCommand.Source -m smart_notepad

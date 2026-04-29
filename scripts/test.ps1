$ProjectRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $ProjectRoot "src"

python -m unittest discover -s tests
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

python -m compileall src tests


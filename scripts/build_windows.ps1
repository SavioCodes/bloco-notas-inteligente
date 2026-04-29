$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$env:PYTHONPATH = Join-Path $ProjectRoot "src"

python -m unittest discover -s tests
python -m smart_notepad --smoke-test

python -m PyInstaller --noconfirm --clean "BlocoNotasInteligente.spec"

$ExePath = Join-Path $ProjectRoot "dist/BlocoNotasInteligente.exe"
if (-not (Test-Path $ExePath)) {
    throw "Executavel nao foi gerado em $ExePath"
}

$SmokeProcess = Start-Process -FilePath $ExePath -ArgumentList "--smoke-test" -Wait -PassThru -WindowStyle Hidden
if ($SmokeProcess.ExitCode -ne 0) {
    throw "Smoke test do executavel falhou com codigo $($SmokeProcess.ExitCode)."
}

$HashPath = "$ExePath.sha256"
$Hash = Get-FileHash -Path $ExePath -Algorithm SHA256
"$($Hash.Hash)  BlocoNotasInteligente.exe" | Set-Content -Path $HashPath -Encoding ASCII

Write-Host "Build Windows OK: $ExePath"
Write-Host "SHA256: $($Hash.Hash)"

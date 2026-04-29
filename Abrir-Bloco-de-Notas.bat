@echo off
setlocal
cd /d "%~dp0"

set "PYTHONPATH=%CD%\src"
set "PY_CMD="

where py >nul 2>nul
if not errorlevel 1 set "PY_CMD=py"

if not defined PY_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PY_CMD=python"
)

if not defined PY_CMD (
    echo Python nao foi encontrado.
    echo Instale Python 3.10 ou superior e marque a opcao "Add Python to PATH".
    pause
    exit /b 1
)

echo Abrindo Bloco de Notas Inteligente...
echo Se a janela do app abriu, esta tela pode ficar em segundo plano.
echo.

%PY_CMD% -m smart_notepad
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo O app fechou com erro. Execute Testar-Instalacao.bat para diagnosticar.
    pause
    exit /b %EXIT_CODE%
)

if /I not "%~1"=="/nopause" pause


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

echo ========================================
echo  Verificador do Bloco de Notas Inteligente
echo ========================================
echo.

if not defined PY_CMD (
    echo [ERRO] Python nao foi encontrado.
    echo Instale Python 3.10 ou superior e marque "Add Python to PATH".
    if /I not "%~1"=="/nopause" pause
    exit /b 1
)

echo [1/4] Python encontrado:
%PY_CMD% --version
if errorlevel 1 goto :erro
echo.

echo [2/4] Testando interface Tkinter...
%PY_CMD% -c "import tkinter as tk; root=tk.Tk(); root.withdraw(); root.update(); root.destroy(); print('Tkinter OK')"
if errorlevel 1 goto :erro
echo.

echo [3/4] Testando importacao do app...
%PY_CMD% -c "import smart_notepad; print('App OK:', smart_notepad.__version__)"
if errorlevel 1 goto :erro
echo.

echo [4/4] Rodando testes automaticos...
%PY_CMD% -m unittest discover -s tests
if errorlevel 1 goto :erro
echo.

echo Tudo certo. Agora abra com:
echo Abrir-Bloco-de-Notas.bat
echo.
if /I not "%~1"=="/nopause" pause
exit /b 0

:erro
echo.
echo Algo falhou acima. A mensagem logo acima mostra o motivo.
if /I not "%~1"=="/nopause" pause
exit /b 1


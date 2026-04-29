# Empacotamento Windows

## Objetivo

Gerar um `.exe` para Windows usando PyInstaller, sem exigir que o usuario final
abra terminal ou configure `PYTHONPATH`.

## Requisitos

- Python 3.10 ou superior.
- PyInstaller instalado.

```powershell
python -m pip install pyinstaller
```

## Gerar executavel

```powershell
.\scripts\build_windows.ps1
```

O arquivo final fica em:

```text
dist\BlocoNotasInteligente.exe
```

O hash SHA256 fica em:

```text
dist\BlocoNotasInteligente.exe.sha256
```

## Validacao feita pelo script

O script executa:

- Testes automatizados com `unittest`.
- Smoke test do fluxo do usuario no codigo fonte.
- Build com PyInstaller.
- Smoke test do proprio `.exe`.
- Geracao de hash SHA256 para anexar na release.

## Fluxo testado

- Criar nota.
- Salvar conteudo e tags.
- Buscar nota.
- Mover para lixeira.
- Restaurar nota.
- Exportar Markdown.

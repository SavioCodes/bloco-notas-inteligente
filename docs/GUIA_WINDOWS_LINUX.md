# Guia Windows e Linux

## Requisitos

- Python 3.10 ou superior.
- Tkinter disponivel na instalacao do Python.

## Windows

Instale Python pelo site oficial e marque a opcao para adicionar ao PATH.
Depois execute:

```powershell
.\scripts\run.ps1
```

Se o comando `python` nao existir, tente:

```powershell
py -m smart_notepad
```

com `PYTHONPATH` apontando para `src`.

## Linux

Em algumas distribuicoes, Tkinter fica em um pacote separado.

Ubuntu/Debian:

```bash
sudo apt install python3-tk
```

Fedora:

```bash
sudo dnf install python3-tkinter
```

Depois execute:

```bash
./scripts/run.sh
```

## Empacotamento futuro

Para distribuir o app sem pedir que o usuario instale Python, a opcao mais
simples sera PyInstaller.

Exemplo futuro:

```bash
pyinstaller --name BlocoNotasInteligente --windowed src/smart_notepad/__main__.py
```


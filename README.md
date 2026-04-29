<p align="center">
  <img src="assets/logo.svg" alt="Bloco de Notas Inteligente" width="760">
</p>

<p align="center">
  <a href="https://github.com/SavioCodes/bloco-notas-inteligente/actions/workflows/tests.yml">
    <img alt="Tests" src="https://github.com/SavioCodes/bloco-notas-inteligente/actions/workflows/tests.yml/badge.svg">
  </a>
  <a href="https://github.com/SavioCodes/bloco-notas-inteligente/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/SavioCodes/bloco-notas-inteligente?include_prereleases&label=release">
  </a>
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-2f6f5e">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-d79a2b">
</p>

# Bloco de Notas Inteligente

Um bloco de notas desktop, local e multiplataforma, feito com Python, Tkinter e
SQLite. A proposta e ser simples de usar, leve de rodar e seguro contra perda
acidental de notas.

## Destaques

- Editor de notas com salvamento local em SQLite.
- Interface organizada com barra de acoes, paineis e atalhos.
- Busca por titulo, conteudo e tags.
- Painel inteligente local com resumo, titulo sugerido, tags, palavras-chave e tarefas.
- Lixeira recuperavel antes de apagar definitivamente.
- Importacao de `.txt` e `.md`.
- Exportacao Markdown.
- Scripts para Windows e Linux.
- Testes automatizados em Windows e Linux via GitHub Actions.

## Comece pelo Windows

1. Clique duas vezes em `Testar-Instalacao.bat`.
2. Se aparecer `Tudo certo`, clique duas vezes em `Abrir-Bloco-de-Notas.bat`.

Pelo terminal:

```powershell
.\scripts\run.ps1
```

## Comece pelo Linux

```bash
chmod +x scripts/run.sh scripts/test.sh
./scripts/run.sh
```

Se faltar Tkinter no Ubuntu/Debian:

```bash
sudo apt install python3-tk
```

## Atalhos

| Atalho | Acao |
| --- | --- |
| `Ctrl+N` | Nova nota |
| `Ctrl+S` | Salvar agora |
| `Ctrl+F` | Buscar |
| `Ctrl+E` | Exportar Markdown |
| `Ctrl+I` | Importar texto |
| `Ctrl+1` | Ver notas |
| `Ctrl+2` | Ver lixeira |
| `Ctrl+Shift+Delete` | Mover para lixeira |
| `Ctrl+Shift+R` | Restaurar nota |
| `F5` | Atualizar |
| `Esc` | Limpar busca |

## Testes

Windows:

```powershell
.\scripts\test.ps1
```

Linux:

```bash
./scripts/test.sh
```

Manual:

```bash
PYTHONPATH="$PWD/src" python -m unittest discover -s tests
PYTHONPATH="$PWD/src" python -m compileall src tests
```

## Onde os dados ficam salvos

- Windows: `%LOCALAPPDATA%\BlocoNotasInteligente\notes.sqlite3`
- Linux: `$XDG_DATA_HOME/bloco-notas-inteligente/notes.sqlite3`
- Fallback Linux: `~/.local/share/bloco-notas-inteligente/notes.sqlite3`

Para usar uma pasta portatil:

```powershell
$env:SMART_NOTEPAD_HOME = "C:\caminho\para\dados"
```

Linux:

```bash
export SMART_NOTEPAD_HOME="/caminho/para/dados"
```

## Estrutura

```text
.
|-- .github/                 # Workflows, templates e configuracao GitHub
|-- assets/                  # Logo e futuros recursos visuais
|-- docs/                    # Planejamento, arquitetura, roadmap e releases
|-- scripts/                 # Scripts Windows/Linux
|-- src/smart_notepad/       # Codigo do app
|-- tests/                   # Testes automatizados
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- README.md
`-- pyproject.toml
```

## Documentacao

- `docs/PLANO_DO_PROJETO.md`
- `docs/ARQUITETURA.md`
- `docs/DECISOES_TECNICAS.md`
- `docs/ATALHOS_E_LIXEIRA.md`
- `docs/GUIA_WINDOWS_LINUX.md`
- `docs/COMO_TESTAR.md`
- `docs/ROADMAP.md`
- `CHANGELOG.md`

## Roadmap curto

- Preview Markdown.
- Backup automatico.
- Empacotamento com PyInstaller.
- Criptografia local opcional.
- Temas configuraveis.
- IA local/API opcional com consentimento do usuario.

## Licenca

Distribuido sob a licenca MIT. Veja `LICENSE`.

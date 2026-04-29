# Changelog

Todas as mudancas importantes deste projeto serao documentadas aqui.

O formato segue a ideia de Keep a Changelog e o versionamento segue SemVer.

## [0.1.1] - 2026-04-29

### Adicionado

- Executavel Windows gerado com PyInstaller.
- Smoke test automatizado do fluxo principal do usuario.
- Comandos `--version` e `--smoke-test`.
- Script `scripts/build_windows.ps1`.
- Documentacao de empacotamento Windows.

## [0.1.0] - 2026-04-29

### Adicionado

- Estrutura inicial do app desktop.
- Interface Tkinter com tema visual organizado.
- Editor de notas com salvamento local em SQLite.
- Busca por titulo, conteudo e tags.
- Analise inteligente local com titulo sugerido, tags, palavras-chave, tarefas e estatisticas.
- Lixeira recuperavel com restauracao e exclusao definitiva.
- Importacao de `.txt` e `.md`.
- Exportacao Markdown.
- Scripts para Windows e Linux.
- Testes automatizados com `unittest`.
- Documentacao inicial, templates GitHub, workflows e release inicial.

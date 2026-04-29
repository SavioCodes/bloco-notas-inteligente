# Changelog

Todas as mudancas importantes deste projeto serao documentadas aqui.

O formato segue a ideia de Keep a Changelog e o versionamento segue SemVer.

## [0.2.0] - 2026-04-29

### Adicionado

- Preview Markdown formatado dentro do app.
- Temas `Papel/caderno`, `Claro` e `Escuro`.
- Backup automatico do banco SQLite com retencao.
- Comando manual para criar backup.
- Pasta de backups acessivel pelo menu.
- Protecao opcional por senha para criptografar notas localmente.
- Testes para backup, Markdown, criptografia e busca em notas criptografadas.
- Smoke test cobrindo preview, tema, backup, lixeira, restauracao, exportacao e senha.

### Observacao de seguranca

- A protecao por senha usa primitivas criptograficas da biblioteca padrao do Python e e pensada como protecao local inicial. Para dados extremamente sensiveis, ainda e recomendado usar tambem uma solucao auditada de criptografia de disco.

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

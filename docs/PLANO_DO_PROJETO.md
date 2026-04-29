# Plano do Projeto

## Objetivo

Criar um bloco de notas inteligente, local, privado e multiplataforma para Windows
e Linux. A primeira versao deve ser simples de executar, facil de manter e pronta
para evoluir para sincronizacao, criptografia, plugins e IA local ou via API.

## Principios

- Privacidade primeiro: as notas ficam no computador do usuario.
- Multiplataforma: usar tecnologias que funcionem bem no Windows e no Linux.
- Baixa friccao: rodar com Python padrao sempre que possivel.
- Evolucao segura: separar interface, banco de dados e inteligencia.
- Documentacao desde o inicio: manter plano, arquitetura e roadmap no repositorio.

## Escopo da versao inicial

- Criar, editar, pesquisar e excluir notas.
- Mover notas para lixeira antes de apagar definitivamente.
- Salvar notas em SQLite.
- Usar interface desktop com Tkinter.
- Melhorar organizacao visual com barra de acoes, paineis e atalhos.
- Mostrar preview Markdown formatada.
- Criar backups automaticos do banco SQLite.
- Permitir temas claro, escuro e papel/caderno.
- Permitir protecao opcional por senha.
- Detectar palavras-chave, tarefas e estatisticas de texto.
- Sugerir titulo e tags com regras locais.
- Exportar nota em Markdown.
- Importar arquivos `.txt` e `.md`.

## Fora do escopo inicial

- Sincronizacao em nuvem.
- Login de usuario.
- Colaboracao em tempo real.
- IA remota por API.
- Editor Markdown avancado com preview visual.

## Estrutura inicial

```text
.
|-- docs/
|   |-- ARQUITETURA.md
|   |-- GUIA_WINDOWS_LINUX.md
|   |-- PLANO_DO_PROJETO.md
|   `-- ROADMAP.md
|-- scripts/
|   |-- run.ps1
|   `-- run.sh
|-- src/
|   `-- smart_notepad/
|       |-- __init__.py
|       |-- __main__.py
|       |-- app.py
|       |-- config.py
|       |-- db.py
|       |-- intelligence.py
|       |-- models.py
|       `-- ui.py
|-- tests/
|   `-- test_intelligence.py
|-- README.md
|-- pyproject.toml
`-- .gitignore
```

## Criterios de sucesso da primeira versao

- O app abre no Windows e no Linux.
- Uma nota criada continua disponivel apos fechar e abrir o app.
- A busca encontra notas por titulo, conteudo ou tags.
- O painel inteligente atualiza enquanto o usuario escreve.
- Excluir uma nota move para a lixeira e permite restaurar.
- Apagar definitivo fica separado e exige confirmacao.
- Preview Markdown renderiza estruturas comuns.
- Backup automatico e backup manual criam copias consistentes.
- Protecao por senha criptografa titulo, conteudo e tags.
- Os testes automatizados passam.

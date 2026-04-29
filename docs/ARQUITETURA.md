# Arquitetura

## Visao geral

O projeto usa uma arquitetura simples em camadas:

- Interface: `ui.py`
- Aplicacao: `app.py`
- Persistencia: `db.py`
- Inteligencia local: `intelligence.py`
- Preview Markdown: `markdown_preview.py`
- Backups: `backup.py`
- Configuracoes: `settings.py`
- Protecao por senha: `security.py`
- Modelo de dados: `models.py`
- Configuracao de caminhos: `config.py`

## Decisao tecnologica

A base usa Python, Tkinter e SQLite.

Essa combinacao foi escolhida porque:

- Python e facil de instalar no Windows e no Linux.
- Tkinter vem com a maioria das instalacoes Python.
- SQLite e local, confiavel e dispensa servidor.
- O empacotamento futuro com PyInstaller e direto.

## Fluxo de dados

```text
Usuario -> Tkinter UI -> NotesRepository -> SQLite
                 |
                 `-> SmartAnalyzer -> painel inteligente
```

## Persistencia

As notas sao salvas em uma tabela SQLite com:

- `id`
- `title`
- `content`
- `tags`
- `created_at`
- `updated_at`
- `deleted_at`

As tags ficam serializadas como JSON para manter o banco simples na primeira
versao.

## Lixeira

A lixeira usa exclusao logica:

- Notas ativas possuem `deleted_at = NULL`.
- Notas na lixeira possuem `deleted_at` preenchido.
- Restaurar limpa `deleted_at`.
- Apagar definitivamente remove a linha do SQLite.

Esse desenho evita perda acidental e mantem compatibilidade com bancos antigos,
porque a coluna `deleted_at` e criada automaticamente quando necessario.

## Inteligencia local

O modulo `intelligence.py` faz analise sem rede:

- Remove palavras comuns.
- Conta frequencia de termos relevantes.
- Sugere palavras-chave.
- Detecta linhas de tarefa.
- Sugere tags.
- Calcula estatisticas.
- Gera uma sugestao de titulo.

## Backups

O modulo `backup.py` cria copias consistentes do SQLite usando a API nativa de
backup do SQLite. Os backups ficam em `backups/` dentro da pasta de dados do app
e seguem uma politica simples de retencao.

## Protecao por senha

Quando ativada, a protecao por senha criptografa titulo, conteudo e tags das
notas no banco SQLite. Antes de ativar ou desativar a protecao, o app cria um
backup do banco.

A implementacao usa PBKDF2-HMAC-SHA256 para derivacao de chave e autenticacao
HMAC para detectar senha incorreta ou alteracao dos dados. E uma protecao local
inicial e nao substitui criptografia de disco auditada para cenarios criticos.

## Evolucao recomendada

Quando o app crescer, os proximos passos arquiteturais devem ser:

- Adicionar migracoes de banco.
- Criar camada de servicos entre UI e repositorio.
- Separar componentes de UI em arquivos menores.
- Adicionar opcao de criptografia local.
- Criar adaptadores para IA local ou provedores externos.

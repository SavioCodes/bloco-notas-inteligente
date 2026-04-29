# Atalhos e Lixeira

## Atalhos

| Atalho | Acao |
| --- | --- |
| `Ctrl+N` | Criar nova nota |
| `Ctrl+S` | Salvar agora |
| `Ctrl+F` | Focar busca |
| `Ctrl+E` | Exportar Markdown |
| `Ctrl+I` | Importar texto |
| `Ctrl+P` | Mostrar ou ocultar preview Markdown |
| `Ctrl+B` | Criar backup agora |
| `Ctrl+1` | Mostrar notas ativas |
| `Ctrl+2` | Mostrar lixeira |
| `Ctrl+L` | Usar titulo sugerido |
| `Ctrl+Shift+T` | Adicionar tags sugeridas |
| `Ctrl+Shift+Delete` | Mover nota para lixeira |
| `Ctrl+Shift+R` | Restaurar nota |
| `F5` | Atualizar lista |
| `Esc` | Limpar busca |

## Como a lixeira funciona

Excluir uma nota nao apaga o conteudo imediatamente. O app preenche o campo
`deleted_at` no banco SQLite e a nota passa a aparecer apenas na lixeira.

Na lixeira, existem duas opcoes:

- Restaurar nota: volta a nota para a lista principal.
- Apagar definitivo: remove a nota do banco e nao pode ser desfeito.

Tambem existe a opcao de esvaziar a lixeira pelo menu `Lixeira`.

## Por que esse fluxo e mais seguro

- Evita perda acidental.
- Permite recuperar notas apagadas por engano.
- Mantem a busca principal limpa.
- Deixa a acao irreversivel separada e com confirmacao.

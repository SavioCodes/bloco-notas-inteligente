# Preview, Backup, Temas e Seguranca

## Preview Markdown

O app mostra uma preview formatada da nota enquanto voce escreve.

Formatos reconhecidos na primeira versao:

- Titulos com `#`, `##`, `###`.
- Listas com `-`, `*` ou numeros.
- Checkboxes com `- [ ]` e `- [x]`.
- Citacoes com `>`.
- Blocos de codigo com crases triplas.
- Linhas horizontais com `---`.

Atalho:

```text
Ctrl+P
```

## Backup automatico

O app cria backups consistentes do banco SQLite na pasta de dados.

Padroes:

- Backup automatico ativado.
- Intervalo: 15 minutos.
- Retencao: 20 backups.
- Backup manual pelo menu `Ferramentas`.

Atalho:

```text
Ctrl+B
```

## Temas

Temas disponiveis:

- Papel/caderno.
- Claro.
- Escuro.

O tema escolhido fica salvo em `settings.json` na pasta de dados do app.

## Protecao opcional por senha

A protecao por senha criptografa localmente:

- Titulo.
- Conteudo.
- Tags.

Antes de ativar ou desativar a protecao, o app cria um backup do banco.

Importante:

- Se a senha for perdida, as notas protegidas nao podem ser recuperadas pelo app.
- Backups criados enquanto a protecao esta ativa tambem ficam com as notas criptografadas.
- Esta protecao e uma camada local inicial. Para dados extremamente sensiveis,
  use tambem criptografia de disco auditada, como BitLocker, VeraCrypt ou LUKS.


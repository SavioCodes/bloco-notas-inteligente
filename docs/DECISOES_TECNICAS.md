# Decisoes Tecnicas

## Python + Tkinter

Escolhido para manter a primeira versao leve, local e simples de executar no
Windows e no Linux.

## SQLite

Escolhido para persistencia local confiavel sem precisar de servidor.

## Inteligencia local primeiro

A primeira versao nao envia notas para APIs externas. Isso reduz custo,
dependencias e risco de privacidade.

## Lixeira com exclusao logica

Notas movidas para a lixeira recebem `deleted_at`. A remocao definitiva fica
separada para evitar perda acidental.


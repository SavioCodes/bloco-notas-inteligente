# Politica de Seguranca

## Versoes suportadas

| Versao | Suporte |
| --- | --- |
| 0.1.x | Sim |

## Reportando problemas

Se encontrar um problema de seguranca, nao publique detalhes sensiveis em uma issue publica.

Entre em contato com o mantenedor do repositorio ou abra uma issue com uma descricao geral, sem dados privados ou payloads perigosos.

## Principios de seguranca

- Notas ficam salvas localmente.
- O app nao envia conteudo para servidores externos.
- Exclusao comum move notas para a lixeira antes de apagar definitivamente.
- A protecao por senha criptografa titulo, conteudo e tags localmente.
- Antes de ativar ou desativar a protecao por senha, o app cria backup do banco.
- Futuras integracoes de IA devem ser opt-in e documentadas.

## Nota sobre criptografia

A protecao por senha e uma camada local inicial criada com primitivas da
biblioteca padrao do Python. Para dados extremamente sensiveis, use tambem uma
solucao auditada de criptografia de disco, como BitLocker, VeraCrypt ou LUKS.

# Como testar sem complicacao

## No Windows

O jeito mais facil e usar os arquivos na pasta principal do projeto.

1. Clique duas vezes em `Testar-Instalacao.bat`.
2. Se aparecer `Tudo certo`, clique duas vezes em `Abrir-Bloco-de-Notas.bat`.
3. Quando a janela abrir, crie uma nota e escreva qualquer texto.
4. Feche o app e abra de novo para confirmar que a nota ficou salva.
5. Teste `Ctrl+Shift+Delete` para mover a nota para a lixeira.
6. Entre na aba `Lixeira` ou use `Ctrl+2` e restaure com `Ctrl+Shift+R`.

## Se aparecer erro

Veja a ultima mensagem que apareceu na janela preta.

Erros comuns:

- `Python nao foi encontrado`: instale Python 3.10 ou superior e marque `Add Python to PATH`.
- Erro com `tkinter`: a instalacao do Python esta sem suporte grafico.
- Erro nos testes: algum arquivo do projeto foi alterado ou apagado.

## Teste rapido da lixeira

1. Crie uma nota chamada `Teste da lixeira`.
2. Clique em `Mover para lixeira`.
3. Abra `Lixeira`.
4. Clique em `Restaurar nota`.
5. Volte para `Notas` e confirme que a nota apareceu de novo.

## No Linux

Execute:

```bash
chmod +x scripts/run.sh
PYTHONPATH="$PWD/src" python3 -m unittest discover -s tests
./scripts/run.sh
```

Se faltar Tkinter no Ubuntu/Debian:

```bash
sudo apt install python3-tk
```

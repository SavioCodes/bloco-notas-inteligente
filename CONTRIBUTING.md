# Contribuindo

Obrigado por querer melhorar o Bloco de Notas Inteligente.

## Como preparar o ambiente

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests
```

No Linux:

```bash
PYTHONPATH="$PWD/src" python3 -m unittest discover -s tests
```

## Padroes do projeto

- Mantenha o app simples, local e multiplataforma.
- Prefira codigo claro a abstracoes grandes demais.
- Proteja as notas do usuario contra perda acidental.
- Atualize testes quando alterar regras de banco, inteligencia ou interface.
- Atualize documentacao quando mudar comportamento visivel.

## Fluxo sugerido

1. Crie uma branch pequena e objetiva.
2. Rode os testes.
3. Atualize documentacao quando necessario.
4. Abra um pull request explicando o que mudou e como testou.


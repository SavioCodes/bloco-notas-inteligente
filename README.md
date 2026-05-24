<p align="center">
  <img src="assets/logo.svg" alt="Bloco de Notas Inteligente" width="760">
</p>

<p align="center">
  <a href="https://github.com/SavioCodes/bloco-notas-inteligente/actions/workflows/tests.yml">
    <img alt="Tests Status" src="https://github.com/SavioCodes/bloco-notas-inteligente/actions/workflows/tests.yml/badge.svg?style=flat-square">
  </a>
  <a href="https://github.com/SavioCodes/bloco-notas-inteligente/releases">
    <img alt="Latest Release" src="https://img.shields.io/github/v/release/SavioCodes/bloco-notas-inteligente?include_prereleases&label=release&style=flat-square&color=007acc">
  </a>
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-2f6f5e?style=flat-square">
  </a>
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.10%2B-d79a2b?style=flat-square">
</p>

# Bloco de Notas Inteligente

Um bloco de notas desktop, local-first e multiplataforma, desenvolvido com Python, Tkinter e SQLite. Projetado com foco em leveza, simplicidade de uso e resiliência contra perda acidental de dados.

---

### 💡 Decisões de Arquitetura & Roteiro

*   **Offline-First & Confiabilidade:** Armazenamento em banco de dados SQLite local, garantindo transações ACID confiáveis e total independência de conexões externas.
*   **Zero Dependências Pesadas:** Interface nativa com Tkinter. O aplicativo inicia instantaneamente e consome recursos mínimos, sem o overhead de runtimes baseados em Electron ou grandes frameworks gráficos.
*   **Privacidade e Segurança:** Criptografia local opcional diretamente no banco de dados para proteger notas confidenciais de acessos não autorizados na máquina física.

---

### ⚡ Recursos Principais

#### 📝 Editor & Visualização
*   **Suporte a Markdown:** Editor limpo com renderização/preview Markdown lado a lado.
*   **Temas Integrados:** Alternância entre os temas `Papel/Caderno`, `Claro` e `Escuro`.
*   **Importação e Exportação:** Suporte nativo para carregar e salvar em formatos `.txt` e `.md`.

#### 🛡️ Resiliência & Segurança
*   **Criptografia Local:** Proteção opcional por senha com criptografia das notas diretamente no SQLite.
*   **Rotina de Backups:** Backup automático do banco de dados SQLite com política automática de retenção.
*   **Lixeira com Duplo Estágio:** Lixeira recuperável para evitar exclusões acidentais.

#### 🔍 Organização & Busca
*   **Busca Avançada:** Filtros inteligentes por título, conteúdo e tags.
*   **Painel Inteligente Local:** Sumarização local de notas, geração de títulos sugeridos, tags e tarefas pendentes.

---

### 🚀 Instalação & Execução

#### Windows
Para testar e executar de forma automatizada:
1. Execute um clique duplo em `Testar-Instalacao.bat`.
2. Se o ambiente estiver correto, execute `Abrir-Bloco-de-Notas.bat`.

Pelo terminal (PowerShell):
```powershell
.\scripts\run.ps1
```
*Dica: Você também pode baixar o executável `.exe` pronto na [página de releases](https://github.com/SavioCodes/bloco-notas-inteligente/releases).*

#### Linux
Atribua permissão de execução aos scripts e inicie o app:
```bash
chmod +x scripts/run.sh scripts/test.sh
./scripts/run.sh
```
*Caso falte o Tkinter em distribuições baseadas em Debian/Ubuntu, instale-o com:*
```bash
sudo apt install python3-tk
```

---

### ⌨️ Atalhos de Teclado

| Atalho | Ação |
| :--- | :--- |
| `Ctrl+N` | Nova nota |
| `Ctrl+S` | Salvar nota atual |
| `Ctrl+F` | Focar na busca |
| `Ctrl+P` | Alternar preview Markdown |
| `Ctrl+E` | Exportar para Markdown |
| `Ctrl+I` | Importar arquivo de texto |
| `Ctrl+B` | Forçar criação de backup |
| `Ctrl+1` | Exibir painel de notas |
| `Ctrl+2` | Exibir lixeira |
| `Ctrl+Shift+Delete` | Mover nota ativa para a lixeira |
| `Ctrl+Shift+R` | Restaurar nota da lixeira |
| `F5` | Atualizar dados da interface |
| `Esc` | Limpar campo de busca |

---

### 🧪 Suíte de Testes & Build

#### Execução de Testes
**Windows:**
```powershell
# Executar suíte de testes unitários
.\scripts\test.ps1

# Executar smoke tests (teste de fluxo completo do usuário)
.\scripts\smoke_test.ps1
```

**Linux:**
```bash
./scripts/test.sh
```

**Manual (Qualquer Plataforma):**
```bash
PYTHONPATH="$PWD/src" python -m unittest discover -s tests
PYTHONPATH="$PWD/src" python -m compileall src tests
```

#### Empacotamento (Windows)
Para compilar um executável `.exe` autônomo usando PyInstaller:
```powershell
.\scripts\build_windows.ps1
```

---

### 💾 Armazenamento de Dados
O banco de dados SQLite (`notes.sqlite3`) é persistido nos seguintes caminhos padrão:

*   **Windows:** `%LOCALAPPDATA%\BlocoNotasInteligente\notes.sqlite3`
*   **Linux:** `$XDG_DATA_HOME/bloco-notas-inteligente/notes.sqlite3` *(Fallback: `~/.local/share/...`)*

Para alterar o diretório de dados para um modo portátil ou personalizado:
```powershell
# Windows PowerShell
$env:SMART_NOTEPAD_HOME = "C:\Caminho\Personalizado"
```
```bash
# Linux Bash
export SMART_NOTEPAD_HOME="/caminho/personalizado"
```

---

### 📂 Estrutura do Repositório

```
.
├── .github/                 # Workflows do CI/CD (GitHub Actions)
├── assets/                  # Identidade visual e logo do projeto
├── docs/                    # Documentação técnica e roadmap
├── scripts/                 # Scripts utilitários para Windows e Linux
├── src/smart_notepad/       # Código-fonte principal do app
├── tests/                   # Suíte de testes automatizados
├── CHANGELOG.md             # Histórico de alterações do projeto
├── CONTRIBUTING.md          # Diretrizes para novos contribuidores
├── LICENSE                  # Licença de distribuição
├── README.md                # Esta documentação
└── pyproject.toml           # Configurações de build e dependências
```

---

### 📖 Documentação Técnica
Aprofunde-se nos detalhes de projeto e engenharia através dos guias na pasta `docs/`:

*   [Plano de Projeto](docs/PLANO_DO_PROJETO.md) — Planejamento, escopo e premissas.
*   [Arquitetura do Sistema](docs/ARQUITETURA.md) — Estrutura de classes e fluxos de dados.
*   [Decisões Técnicas](docs/DECISOES_TECNICAS.md) — Justificativa de stacks e bibliotecas.
*   [Atalhos & Lixeira](docs/ATALHOS_E_LIXEIRA.md) — Especificação de navegação rápida e estados.
*   [Guia de Ambientes](docs/GUIA_WINDOWS_LINUX.md) — Configurações específicas para OS.
*   [Empacotamento](docs/EMPACOTAMENTO_WINDOWS.md) — Instruções detalhadas para geração de build.
*   [Preview, Backup & Segurança](docs/PREVIEW_BACKUP_TEMAS_SEGURANCA.md) — Detalhes sobre backup e criptografia.
*   [Como Testar](docs/COMO_TESTAR.md) — Guia detalhado de testes unitários e de fumaça.
*   [Roadmap de Desenvolvimento](docs/ROADMAP.md) — Planejamento de novas releases.

---

### 🗺️ Roadmap de Lançamentos

- [x] Visualização de Markdown lado a lado.
- [x] Geração automática e retenção de backups locais.
- [x] Script de empacotamento standalone via PyInstaller.
- [x] Suporte a criptografia simétrica local opcional nas notas.
- [ ] Melhorias no editor nativo (editor rico / Markdown autocomplete).
- [ ] Integração de IA local (ou chave de API externa) controlada pelo usuário.

---

### ⚖️ Licença

Distribuído sob a licença MIT. Consulte a declaração em `LICENSE` para mais informações.

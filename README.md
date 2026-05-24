<p align="center">
  <img src="assets/smart_notepad_3d.png" alt="Smart Notepad 3D Showcase" width="650" style="border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
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

---

<p align="center">
  <strong>Um bloco de notas desktop, local-first e multiplataforma.</strong><br />
  <em>Desenvolvido com Python, Tkinter e SQLite. Leve, rápido e seguro contra perda de dados.</em>
</p>

---

<blockquote>
  <strong>📐 Filosofia de Engenharia:</strong>
  <ul>
    <li><strong>Offline-First:</strong> Banco de dados SQLite local com transações ACID completas.</li>
    <li><strong>Leveza Absoluta:</strong> Interface gráfica nativa via Tkinter, sem o consumo excessivo de Electron ou runtimes de 100MB+.</li>
    <li><strong>Privacidade Nativa:</strong> Criptografia local opcional diretamente no banco para arquivos confidenciais.</li>
  </ul>
</blockquote>

---

<h2 align="center">⚡ Destaques do Sistema</h2>

<table width="100%">
  <tr>
    <td width="33.3%" valign="top" style="border: 1px solid #30363d; padding: 10px; border-radius: 6px;">
      <h3 align="center">📝 Editor & Visuals</h3>
      <ul>
        <li><strong>Markdown Side-by-Side:</strong> Preview formatado em tempo real ao lado do editor.</li>
        <li><strong>Temas Customizados:</strong> Alternância entre <code>Papel/Caderno</code>, <code>Claro</code> e <code>Escuro</code>.</li>
        <li><strong>Import/Export:</strong> Manipulação nativa de arquivos <code>.txt</code> e <code>.md</code>.</li>
      </ul>
    </td>
    <td width="33.3%" valign="top" style="border: 1px solid #30363d; padding: 10px; border-radius: 6px;">
      <h3 align="center">🛡️ Resiliência</h3>
      <ul>
        <li><strong>Criptografia Simétrica:</strong> Proteção local com senha no banco de dados.</li>
        <li><strong>Backups Automatizados:</strong> Rotina automática com regras de retenção.</li>
        <li><strong>Lixeira de Notas:</strong> Recuperação de dois estágios antes da exclusão definitiva.</li>
      </ul>
    </td>
    <td width="33.3%" valign="top" style="border: 1px solid #30363d; padding: 10px; border-radius: 6px;">
      <h3 align="center">🔍 Organização</h3>
      <ul>
        <li><strong>Busca Avançada:</strong> Indexador por título, tags e conteúdo.</li>
        <li><strong>Painel Inteligente Local:</strong> Resumos automáticos, títulos sugeridos, tags e tarefas geradas localmente.</li>
      </ul>
    </td>
  </tr>
</table>

---

<h2 align="center">🚀 Começando Rápido</h2>

<table width="100%">
  <tr>
    <th width="50%" align="left">🏁 Windows Quickstart</th>
    <th width="50%" align="left">🐧 Linux Quickstart</th>
  </tr>
  <tr>
    <td valign="top">
      <ol>
        <li>Execute com duplo clique o script <code>Testar-Instalacao.bat</code>.</li>
        <li>Se tudo estiver ok, execute <code>Abrir-Bloco-de-Notas.bat</code>.</li>
      </ol>
      <p>Via PowerShell:</p>
      <pre><code>.\scripts\run.ps1</code></pre>
      <p><sub><em>Ou baixe o <code>.exe</code> compilado em <a href="https://github.com/SavioCodes/bloco-notas-inteligente/releases">releases</a>.</em></sub></p>
    </td>
    <td valign="top">
      <ol>
        <li>Dê permissão de execução aos utilitários:</li>
      </ol>
      <pre><code>chmod +x scripts/*.sh</code></pre>
      <ol start="2">
        <li>Execute o inicializador:</li>
      </ol>
      <pre><code>./scripts/run.sh</code></pre>
      <p><sub><em>Instalar Tkinter (Debian/Ubuntu) se necessário: <code>sudo apt install python3-tk</code></em></sub></p>
    </td>
  </tr>
</table>

---

<h2 align="center">⌨️ Atalhos Globais</h2>

<table align="center" width="100%">
  <thead>
    <tr>
      <th width="40%">Tecla de Atalho</th>
      <th width="60%">Ação Executada</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>N</kbd></td>
      <td>Cria uma nova nota</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>S</kbd></td>
      <td>Salva a nota ativa imediatamente</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>F</kbd></td>
      <td>Foca o campo de busca de notas</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>P</kbd></td>
      <td>Exibe ou oculta o painel de preview Markdown</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>E</kbd></td>
      <td>Exporta a nota atual para o formato Markdown</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>I</kbd></td>
      <td>Importa um arquivo de texto para a nota ativa</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>B</kbd></td>
      <td>Força a geração imediata de um backup do banco</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>1</kbd></td>
      <td>Ativa a visualização do painel de notas</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>2</kbd></td>
      <td>Ativa a visualização da lixeira</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Delete</kbd></td>
      <td>Mover a nota atual para a lixeira</td>
    </tr>
    <tr>
      <td><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>R</kbd></td>
      <td>Restaura a nota selecionada da lixeira</td>
    </tr>
    <tr>
      <td><kbd>F5</kbd></td>
      <td>Atualiza os dados da interface gráfica</td>
    </tr>
    <tr>
      <td><kbd>Esc</kbd></td>
      <td>Limpa a busca atual e restaura a lista completa</td>
    </tr>
  </tbody>
</table>

---

<h2 align="center">🧪 Suíte de Testes & Builds</h2>

**Execução de Testes (Windows PowerShell):**
```powershell
.\scripts\test.ps1        # Testes unitários completos
.\scripts\smoke_test.ps1   # Smoke tests do fluxo de usuário
```

**Execução de Testes (Linux):**
```bash
./scripts/test.sh
```

**Empacotamento manual do executável Windows:**
```powershell
.\scripts\build_windows.ps1
```

---

### 💾 Localização do Banco de Dados

*   **Windows:** `%LOCALAPPDATA%\BlocoNotasInteligente\notes.sqlite3`
*   **Linux:** `$XDG_DATA_HOME/bloco-notas-inteligente/notes.sqlite3` *(Fallback: `~/.local/share/...`)*

Para definir um diretório customizado (portátil):
```powershell
$env:SMART_NOTEPAD_HOME = "C:\Caminho\Personalizado"
```
```bash
export SMART_NOTEPAD_HOME="/caminho/personalizado"
```

---

### 📂 Organização do Repositório

```text
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
└── pyproject.toml           # Configurações de build e dependências
```

---

### 📖 Documentação Adicional

Explore as especificações do sistema diretamente nos arquivos da pasta `docs/`:
*   [Plano de Projeto](docs/PLANO_DO_PROJETO.md) · [Arquitetura](docs/ARQUITETURA.md) · [Decisões Técnicas](docs/DECISOES_TECNICAS.md)
*   [Atalhos & Lixeira](docs/ATALHOS_E_LIXEIRA.md) · [Guia Windows & Linux](docs/GUIA_WINDOWS_LINUX.md) · [Empacotamento](docs/EMPACOTAMENTO_WINDOWS.md)
*   [Backups & Segurança](docs/PREVIEW_BACKUP_TEMAS_SEGURANCA.md) · [Como Testar](docs/COMO_TESTAR.md) · [Roadmap Geral](docs/ROADMAP.md)

---

### 🗺️ Roteiro de Lançamentos (Roadmap)

- [x] Visualização de Markdown lado a lado.
- [x] Geração automática e retenção de backups locais.
- [x] Script de empacotamento standalone via PyInstaller.
- [x] Suporte a criptografia simétrica local opcional nas notas.
- [ ] Melhorias no editor nativo (editor rico / Markdown autocomplete).
- [ ] Integração de IA local (ou chave de API externa) controlada pelo usuário.

---

### ⚖️ Licença

Distribuído sob a licença MIT. Consulte a declaração em `LICENSE` para mais informações.

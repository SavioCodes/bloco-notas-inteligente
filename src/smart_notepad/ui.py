from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from .backup import BackupManager
from .db import NotesRepository
from .intelligence import SmartAnalysis, analyze_note
from .markdown_preview import MarkdownBlock, parse_markdown
from .models import Note
from .security import create_password_record, verify_password
from .settings import AppSettings, SettingsStore


THEMES = {
    "paper": {
        "name": "Papel/caderno",
        "app_bg": "#f4efe6",
        "panel_bg": "#fffaf0",
        "panel_alt": "#f9f1df",
        "ink": "#17231f",
        "muted": "#65716b",
        "line": "#dbcdb6",
        "accent": "#2f6f5e",
        "accent_dark": "#204b42",
        "accent_soft": "#dcebe4",
        "warning": "#b45309",
        "danger": "#a33a2b",
        "danger_soft": "#f7ded9",
        "gold": "#d79a2b",
        "editor_bg": "#fffdf7",
        "preview_bg": "#fffaf0",
        "selection": "#dfeee7",
    },
    "light": {
        "name": "Claro",
        "app_bg": "#eef4f8",
        "panel_bg": "#ffffff",
        "panel_alt": "#edf4f7",
        "ink": "#10202b",
        "muted": "#5c6b75",
        "line": "#c9d7de",
        "accent": "#1f6f8b",
        "accent_dark": "#14475a",
        "accent_soft": "#d9edf4",
        "warning": "#b7791f",
        "danger": "#b8322a",
        "danger_soft": "#f8dddd",
        "gold": "#c58a18",
        "editor_bg": "#fbfdff",
        "preview_bg": "#ffffff",
        "selection": "#d9edf4",
    },
    "dark": {
        "name": "Escuro",
        "app_bg": "#151a1e",
        "panel_bg": "#1f262b",
        "panel_alt": "#283138",
        "ink": "#edf4f3",
        "muted": "#a6b4b0",
        "line": "#3a474f",
        "accent": "#7cc7a4",
        "accent_dark": "#4da07d",
        "accent_soft": "#2d433c",
        "warning": "#e0aa4f",
        "danger": "#db6b60",
        "danger_soft": "#4b2b2b",
        "gold": "#e0b45b",
        "editor_bg": "#11171b",
        "preview_bg": "#181f23",
        "selection": "#30463e",
    },
}

THEME = THEMES["paper"].copy()

ICONS = {
    "new": "+",
    "save": "OK",
    "search": "?",
    "note": ">",
    "trash": "TR",
    "delete": "X",
    "restore": "R",
    "export": "EX",
    "import": "IN",
    "spark": "*",
    "tag": "#",
    "lock": "LOCK",
    "backup": "BK",
    "preview": "MD",
}


class SmartNotepadApp:
    def __init__(
        self,
        repository: NotesRepository,
        settings_store: SettingsStore | None = None,
        backup_manager: BackupManager | None = None,
    ) -> None:
        self.repository = repository
        self.settings_store = settings_store
        self.settings = settings_store.load() if settings_store else AppSettings()
        self.backup_manager = backup_manager
        self.theme_name = self.settings.theme_name if self.settings.theme_name in THEMES else "paper"
        self._set_theme(self.theme_name, persist=False)
        self.root = tk.Tk()
        self.root.title("Bloco de Notas Inteligente")
        self.root.geometry("1220x780")
        self.root.minsize(980, 620)
        self.root.configure(bg=THEME["app_bg"])

        self.note_ids: list[int] = []
        self.current_note_id: int | None = None
        self.current_note_deleted = False
        self.loading = False
        self.save_after_id: str | None = None
        self.analysis_after_id: str | None = None
        self.search_after_id: str | None = None
        self.preview_after_id: str | None = None
        self.backup_after_id: str | None = None
        self.unlocked = True

        self.view_mode = tk.StringVar(value="notes")
        self.preview_visible_var = tk.BooleanVar(value=self.settings.preview_visible)
        self.search_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto")
        self.counter_var = tk.StringVar()
        self.mode_hint_var = tk.StringVar()
        self.note_meta_var = tk.StringVar()
        self.summary_var = tk.StringVar()
        self.keywords_var = tk.StringVar()
        self.suggested_tags_var = tk.StringVar()
        self.todos_var = tk.StringVar()
        self.stats_var = tk.StringVar()
        self.suggested_title_var = tk.StringVar()
        self.security_var = tk.StringVar()
        self.backup_var = tk.StringVar()

        self._configure_style()
        self._set_window_icon()
        self._build_menu()
        self._build_layout()
        self._bind_events()
        self.unlocked = self._unlock_if_needed()
        if self.unlocked:
            self._run_startup_backup()
            self._load_notes()
            self._schedule_auto_backup()

        if self.unlocked and not self.note_ids:
            self._create_note()

    def run(self) -> None:
        if not self.unlocked:
            self.root.destroy()
            return
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _set_theme(self, theme_name: str, persist: bool = True) -> None:
        global THEME
        self.theme_name = theme_name if theme_name in THEMES else "paper"
        THEME = THEMES[self.theme_name].copy()
        self.settings.theme_name = self.theme_name
        if persist:
            self._save_settings()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        default_font = ("Segoe UI", 10)
        title_font = ("Segoe UI Semibold", 13)
        small_title_font = ("Segoe UI Semibold", 10)

        style.configure(".", font=default_font)
        style.configure("App.TFrame", background=THEME["app_bg"])
        style.configure("Panel.TFrame", background=THEME["panel_bg"])
        style.configure("Alt.TFrame", background=THEME["panel_alt"])
        style.configure("Title.TLabel", background=THEME["panel_bg"], foreground=THEME["ink"], font=title_font)
        style.configure("SmallTitle.TLabel", background=THEME["panel_bg"], foreground=THEME["ink"], font=small_title_font)
        style.configure("Muted.TLabel", background=THEME["panel_bg"], foreground=THEME["muted"])
        style.configure("AppMuted.TLabel", background=THEME["app_bg"], foreground=THEME["muted"])
        style.configure("Status.TLabel", background=THEME["app_bg"], foreground=THEME["muted"])
        style.configure("Toolbar.TButton", padding=(12, 7), font=("Segoe UI Semibold", 9))
        style.configure("Accent.TButton", padding=(12, 7), foreground="#ffffff", background=THEME["accent"])
        style.map("Accent.TButton", background=[("active", THEME["accent_dark"])])
        style.configure("Danger.TButton", padding=(12, 7), foreground="#ffffff", background=THEME["danger"])
        style.map("Danger.TButton", background=[("active", "#7f2f24")])
        style.configure("Soft.TButton", padding=(10, 6))
        style.configure("Card.TLabelframe", background=THEME["panel_bg"], bordercolor=THEME["line"])
        style.configure("Card.TLabelframe.Label", background=THEME["panel_bg"], foreground=THEME["ink"], font=small_title_font)

    def _set_window_icon(self) -> None:
        icon = tk.PhotoImage(width=32, height=32)
        icon.put(THEME["accent_dark"], to=(0, 0, 32, 32))
        icon.put(THEME["panel_bg"], to=(5, 4, 27, 29))
        icon.put(THEME["accent"], to=(8, 8, 24, 11))
        icon.put(THEME["gold"], to=(8, 15, 21, 18))
        icon.put(THEME["line"], to=(8, 22, 24, 24))
        self.app_icon = icon
        self.root.iconphoto(True, self.app_icon)

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Nova nota", accelerator="Ctrl+N", command=self._create_note)
        file_menu.add_command(label="Salvar agora", accelerator="Ctrl+S", command=self._save_current_note)
        file_menu.add_separator()
        file_menu.add_command(label="Importar texto...", accelerator="Ctrl+I", command=self._import_text)
        file_menu.add_command(label="Exportar Markdown...", accelerator="Ctrl+E", command=self._export_markdown)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self._on_close)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=False)
        view_menu.add_command(label="Notas", accelerator="Ctrl+1", command=lambda: self._set_view_mode("notes"))
        view_menu.add_command(label="Lixeira", accelerator="Ctrl+2", command=lambda: self._set_view_mode("trash"))
        view_menu.add_command(label="Buscar", accelerator="Ctrl+F", command=self._focus_search)
        view_menu.add_checkbutton(
            label="Mostrar preview Markdown",
            accelerator="Ctrl+P",
            variable=self.preview_visible_var,
            command=self._apply_preview_visibility,
        )
        theme_menu = tk.Menu(view_menu, tearoff=False)
        for theme_key, theme in THEMES.items():
            theme_menu.add_command(label=str(theme["name"]), command=lambda key=theme_key: self._change_theme(key))
        view_menu.add_cascade(label="Tema", menu=theme_menu)
        view_menu.add_command(label="Atualizar", accelerator="F5", command=self._refresh_notes)
        menu_bar.add_cascade(label="Visualizar", menu=view_menu)

        smart_menu = tk.Menu(menu_bar, tearoff=False)
        smart_menu.add_command(label="Usar titulo sugerido", accelerator="Ctrl+L", command=self._apply_suggested_title)
        smart_menu.add_command(label="Adicionar tags sugeridas", accelerator="Ctrl+Shift+T", command=self._apply_suggested_tags)
        menu_bar.add_cascade(label="Inteligencia", menu=smart_menu)

        trash_menu = tk.Menu(menu_bar, tearoff=False)
        trash_menu.add_command(label="Mover nota para lixeira", accelerator="Ctrl+Shift+Delete", command=self._move_current_note_to_trash)
        trash_menu.add_command(label="Restaurar nota", accelerator="Ctrl+Shift+R", command=self._restore_current_note)
        trash_menu.add_separator()
        trash_menu.add_command(label="Apagar nota definitivamente", command=self._delete_current_note_forever)
        trash_menu.add_command(label="Esvaziar lixeira", command=self._empty_trash)
        menu_bar.add_cascade(label="Lixeira", menu=trash_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=False)
        tools_menu.add_command(label="Criar backup agora", command=self._create_backup_now)
        tools_menu.add_command(label="Abrir pasta de backups", command=self._open_backup_folder)
        tools_menu.add_separator()
        tools_menu.add_command(label="Ativar protecao por senha", command=self._enable_encryption)
        tools_menu.add_command(label="Desativar protecao por senha", command=self._disable_encryption)
        menu_bar.add_cascade(label="Ferramentas", menu=tools_menu)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label="Ver atalhos", command=self._show_shortcuts)
        menu_bar.add_cascade(label="Ajuda", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _build_layout(self) -> None:
        shell = ttk.Frame(self.root, style="App.TFrame", padding=14)
        shell.pack(fill=tk.BOTH, expand=True)

        self._build_topbar(shell)

        body = ttk.PanedWindow(shell, orient=tk.HORIZONTAL)
        body.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        sidebar = self._panel(body, width=330)
        editor_area = ttk.Frame(body, style="App.TFrame")
        body.add(sidebar, weight=1)
        body.add(editor_area, weight=4)

        self._build_sidebar(sidebar)
        self._build_editor(editor_area)

        status = ttk.Label(shell, textvariable=self.status_var, style="Status.TLabel", anchor=tk.W)
        status.pack(fill=tk.X, pady=(10, 0))

    def _build_topbar(self, parent: ttk.Frame) -> None:
        topbar = tk.Frame(parent, bg=THEME["app_bg"])
        topbar.pack(fill=tk.X)

        brand = tk.Frame(topbar, bg=THEME["app_bg"])
        brand.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(
            brand,
            text=f"{ICONS['spark']} Bloco de Notas Inteligente",
            bg=THEME["app_bg"],
            fg=THEME["ink"],
            font=("Segoe UI Semibold", 18),
        ).pack(anchor=tk.W)
        tk.Label(
            brand,
            text="Notas locais, busca rapida, analise inteligente e lixeira segura.",
            bg=THEME["app_bg"],
            fg=THEME["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor=tk.W, pady=(2, 0))

        actions = tk.Frame(topbar, bg=THEME["app_bg"])
        actions.pack(side=tk.RIGHT)
        ttk.Button(actions, text=f"{ICONS['new']} Nova", style="Accent.TButton", command=self._create_note).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text=f"{ICONS['save']} Salvar", style="Toolbar.TButton", command=self._save_current_note).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text=f"{ICONS['preview']} Preview", style="Toolbar.TButton", command=self._toggle_preview).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text=f"{ICONS['backup']} Backup", style="Toolbar.TButton", command=self._create_backup_now).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text=f"{ICONS['export']} Exportar", style="Toolbar.TButton", command=self._export_markdown).pack(side=tk.LEFT)

    def _panel(self, parent: tk.Misc, width: int | None = None) -> tk.Frame:
        panel = tk.Frame(
            parent,
            bg=THEME["panel_bg"],
            highlightbackground=THEME["line"],
            highlightthickness=1,
            bd=0,
        )
        if width is not None:
            panel.configure(width=width)
            panel.pack_propagate(False)
        return panel

    def _build_sidebar(self, parent: tk.Frame) -> None:
        header = tk.Frame(parent, bg=THEME["panel_bg"], padx=14, pady=14)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Biblioteca",
            bg=THEME["panel_bg"],
            fg=THEME["ink"],
            font=("Segoe UI Semibold", 13),
        ).pack(side=tk.LEFT)
        tk.Label(header, textvariable=self.counter_var, bg=THEME["panel_bg"], fg=THEME["muted"]).pack(side=tk.RIGHT)

        search_box = tk.Frame(parent, bg=THEME["panel_bg"], padx=14)
        search_box.pack(fill=tk.X)
        tk.Label(search_box, text=f"{ICONS['search']} Buscar notas", bg=THEME["panel_bg"], fg=THEME["muted"]).pack(anchor=tk.W)
        self.search_entry = tk.Entry(
            search_box,
            textvariable=self.search_var,
            relief=tk.FLAT,
            bg=THEME["editor_bg"],
            fg=THEME["ink"],
            insertbackground=THEME["ink"],
            highlightbackground=THEME["line"],
            highlightcolor=THEME["accent"],
            highlightthickness=1,
            font=("Segoe UI", 10),
        )
        self.search_entry.pack(fill=tk.X, ipady=7, pady=(5, 12))

        modes = tk.Frame(parent, bg=THEME["panel_bg"], padx=14)
        modes.pack(fill=tk.X, pady=(0, 10))
        self.notes_mode_button = self._mode_button(modes, f"{ICONS['note']} Notas", "notes")
        self.trash_mode_button = self._mode_button(modes, f"{ICONS['trash']} Lixeira", "trash")
        self.notes_mode_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.trash_mode_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        hint = tk.Label(
            parent,
            textvariable=self.mode_hint_var,
            bg=THEME["panel_bg"],
            fg=THEME["muted"],
            justify=tk.LEFT,
            wraplength=285,
            padx=14,
        )
        hint.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            parent,
            textvariable=self.security_var,
            bg=THEME["panel_bg"],
            fg=THEME["muted"],
            justify=tk.LEFT,
            wraplength=285,
            padx=14,
        ).pack(fill=tk.X, pady=(0, 4))
        tk.Label(
            parent,
            textvariable=self.backup_var,
            bg=THEME["panel_bg"],
            fg=THEME["muted"],
            justify=tk.LEFT,
            wraplength=285,
            padx=14,
        ).pack(fill=tk.X, pady=(0, 8))

        list_frame = tk.Frame(parent, bg=THEME["panel_bg"], padx=14)
        list_frame.pack(fill=tk.BOTH, expand=True)
        self.notes_list = tk.Listbox(
            list_frame,
            activestyle="none",
            exportselection=False,
            bd=0,
            relief=tk.FLAT,
            bg=THEME["editor_bg"],
            fg=THEME["ink"],
            selectbackground=THEME["accent"],
            selectforeground="#ffffff",
            highlightthickness=1,
            highlightbackground=THEME["line"],
            font=("Segoe UI", 10),
        )
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.notes_list.yview)
        self.notes_list.configure(yscrollcommand=scrollbar.set)
        self.notes_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        actions = tk.Frame(parent, bg=THEME["panel_bg"], padx=14, pady=14)
        actions.pack(fill=tk.X)
        self.primary_sidebar_button = ttk.Button(actions, style="Soft.TButton", command=self._primary_sidebar_action)
        self.secondary_sidebar_button = ttk.Button(actions, style="Soft.TButton", command=self._secondary_sidebar_action)
        self.primary_sidebar_button.pack(fill=tk.X)
        self.secondary_sidebar_button.pack(fill=tk.X, pady=(7, 0))

    def _mode_button(self, parent: tk.Misc, text: str, mode: str) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 9),
            command=lambda: self._set_view_mode(mode),
        )

    def _build_editor(self, parent: ttk.Frame) -> None:
        editor_panel = self._panel(parent)
        editor_panel.pack(fill=tk.BOTH, expand=True)

        meta = tk.Frame(editor_panel, bg=THEME["panel_bg"], padx=16, pady=14)
        meta.pack(fill=tk.X)

        title_group = tk.Frame(meta, bg=THEME["panel_bg"])
        title_group.grid(row=0, column=0, sticky=tk.EW, padx=(0, 12))
        tk.Label(title_group, text="Titulo", bg=THEME["panel_bg"], fg=THEME["muted"]).pack(anchor=tk.W)
        self.title_entry = tk.Entry(
            title_group,
            textvariable=self.title_var,
            relief=tk.FLAT,
            bg=THEME["editor_bg"],
            fg=THEME["ink"],
            insertbackground=THEME["ink"],
            highlightbackground=THEME["line"],
            highlightcolor=THEME["accent"],
            highlightthickness=1,
            font=("Segoe UI Semibold", 13),
        )
        self.title_entry.pack(fill=tk.X, ipady=8, pady=(5, 0))

        tags_group = tk.Frame(meta, bg=THEME["panel_bg"])
        tags_group.grid(row=0, column=1, sticky=tk.EW)
        tk.Label(tags_group, text=f"{ICONS['tag']} Tags separadas por virgula", bg=THEME["panel_bg"], fg=THEME["muted"]).pack(anchor=tk.W)
        self.tags_entry = tk.Entry(
            tags_group,
            textvariable=self.tags_var,
            relief=tk.FLAT,
            bg=THEME["editor_bg"],
            fg=THEME["ink"],
            insertbackground=THEME["ink"],
            highlightbackground=THEME["line"],
            highlightcolor=THEME["accent"],
            highlightthickness=1,
            font=("Segoe UI", 10),
        )
        self.tags_entry.pack(fill=tk.X, ipady=8, pady=(5, 0))
        meta.columnconfigure(0, weight=2)
        meta.columnconfigure(1, weight=1)

        tk.Label(
            editor_panel,
            textvariable=self.note_meta_var,
            bg=THEME["panel_bg"],
            fg=THEME["muted"],
            anchor=tk.W,
            padx=16,
        ).pack(fill=tk.X, pady=(0, 8))

        middle = ttk.PanedWindow(editor_panel, orient=tk.VERTICAL)
        middle.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        editor_frame = tk.Frame(middle, bg=THEME["panel_bg"])
        smart_frame = tk.Frame(middle, bg=THEME["panel_bg"])
        middle.add(editor_frame, weight=4)
        middle.add(smart_frame, weight=1)

        self.editor_split = ttk.PanedWindow(editor_frame, orient=tk.HORIZONTAL)
        self.editor_split.pack(fill=tk.BOTH, expand=True)

        self.editor_column = tk.Frame(self.editor_split, bg=THEME["panel_bg"])
        self.preview_column = tk.Frame(self.editor_split, bg=THEME["panel_bg"])
        self.editor_split.add(self.editor_column, weight=3)
        self.editor_split.add(self.preview_column, weight=2)

        self.editor = tk.Text(
            self.editor_column,
            wrap=tk.WORD,
            undo=True,
            bd=0,
            relief=tk.FLAT,
            bg=THEME["editor_bg"],
            fg=THEME["ink"],
            insertbackground=THEME["ink"],
            selectbackground=THEME["selection"],
            selectforeground=THEME["ink"],
            font=("Cascadia Mono", 12),
            padx=16,
            pady=16,
            highlightbackground=THEME["line"],
            highlightcolor=THEME["accent"],
            highlightthickness=1,
        )
        editor_scroll = ttk.Scrollbar(self.editor_column, orient=tk.VERTICAL, command=self.editor.yview)
        self.editor.configure(yscrollcommand=editor_scroll.set)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        preview_header = tk.Frame(self.preview_column, bg=THEME["panel_bg"])
        preview_header.pack(fill=tk.X, pady=(0, 6))
        tk.Label(
            preview_header,
            text="Preview Markdown",
            bg=THEME["panel_bg"],
            fg=THEME["ink"],
            font=("Segoe UI Semibold", 10),
        ).pack(side=tk.LEFT)
        ttk.Button(preview_header, text="Ocultar", style="Soft.TButton", command=self._toggle_preview).pack(side=tk.RIGHT)

        self.preview = tk.Text(
            self.preview_column,
            wrap=tk.WORD,
            bd=0,
            relief=tk.FLAT,
            bg=THEME["preview_bg"],
            fg=THEME["ink"],
            padx=16,
            pady=16,
            highlightbackground=THEME["line"],
            highlightcolor=THEME["accent"],
            highlightthickness=1,
            font=("Segoe UI", 11),
            state=tk.DISABLED,
        )
        preview_scroll = ttk.Scrollbar(self.preview_column, orient=tk.VERTICAL, command=self.preview.yview)
        self.preview.configure(yscrollcommand=preview_scroll.set)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._configure_preview_tags()
        if not self.preview_visible_var.get():
            self.editor_split.forget(self.preview_column)

        self._build_smart_panel(smart_frame)

    def _build_smart_panel(self, parent: tk.Frame) -> None:
        parent.columnconfigure(0, weight=2)
        parent.columnconfigure(1, weight=1)

        insight_card = ttk.LabelFrame(parent, text=f"{ICONS['spark']} Painel inteligente", style="Card.TLabelframe", padding=10)
        action_card = ttk.LabelFrame(parent, text="Acoes rapidas", style="Card.TLabelframe", padding=10)
        insight_card.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 8), pady=(12, 0))
        action_card.grid(row=0, column=1, sticky=tk.NSEW, padx=(8, 0), pady=(12, 0))

        for variable in (self.summary_var, self.keywords_var, self.suggested_tags_var, self.todos_var, self.stats_var):
            ttk.Label(insight_card, textvariable=variable, style="Muted.TLabel", wraplength=680, justify=tk.LEFT).pack(anchor=tk.W, fill=tk.X, pady=(0, 5))

        ttk.Label(action_card, textvariable=self.suggested_title_var, style="Muted.TLabel", wraplength=300).pack(anchor=tk.W, fill=tk.X, pady=(0, 8))
        ttk.Button(action_card, text="Usar titulo sugerido", style="Soft.TButton", command=self._apply_suggested_title).pack(fill=tk.X)
        ttk.Button(action_card, text="Adicionar tags sugeridas", style="Soft.TButton", command=self._apply_suggested_tags).pack(fill=tk.X, pady=(7, 0))

    def _bind_events(self) -> None:
        self.notes_list.bind("<<ListboxSelect>>", self._on_note_selected)
        self.editor.bind("<<Modified>>", self._on_editor_modified)
        self.title_var.trace_add("write", self._on_metadata_changed)
        self.tags_var.trace_add("write", self._on_metadata_changed)
        self.search_var.trace_add("write", self._on_search_changed)

        self.root.bind_all("<Control-n>", lambda event: self._event(event, self._create_note))
        self.root.bind_all("<Control-s>", lambda event: self._event(event, self._save_current_note))
        self.root.bind_all("<Control-f>", lambda event: self._event(event, self._focus_search))
        self.root.bind_all("<Control-e>", lambda event: self._event(event, self._export_markdown))
        self.root.bind_all("<Control-i>", lambda event: self._event(event, self._import_text))
        self.root.bind_all("<Control-p>", lambda event: self._event(event, self._toggle_preview))
        self.root.bind_all("<Control-b>", lambda event: self._event(event, self._create_backup_now))
        self.root.bind_all("<Control-l>", lambda event: self._event(event, self._apply_suggested_title))
        self.root.bind_all("<Control-Shift-T>", lambda event: self._event(event, self._apply_suggested_tags))
        self.root.bind_all("<Control-Key-1>", lambda event: self._event(event, lambda: self._set_view_mode("notes")))
        self.root.bind_all("<Control-Key-2>", lambda event: self._event(event, lambda: self._set_view_mode("trash")))
        self.root.bind_all("<Control-Shift-Delete>", lambda event: self._event(event, self._move_current_note_to_trash))
        self.root.bind_all("<Control-Shift-R>", lambda event: self._event(event, self._restore_current_note))
        self.root.bind_all("<F5>", lambda event: self._event(event, self._refresh_notes))
        self.root.bind_all("<Escape>", lambda event: self._event(event, self._clear_search))

    @staticmethod
    def _event(_event: tk.Event, callback: object) -> str:
        callback()
        return "break"

    def _load_notes(self, select_id: int | None = None) -> None:
        query = self.search_var.get()
        only_deleted = self._is_trash_view()
        notes = self.repository.list_notes(query, only_deleted=only_deleted)
        self.note_ids = [note.id for note in notes]
        self.notes_list.delete(0, tk.END)

        for note in notes:
            self.notes_list.insert(tk.END, self._note_label(note))

        self._update_mode_buttons()
        self._update_sidebar_actions()
        self._update_mode_text(len(notes))

        if not notes:
            self.current_note_id = None
            self.current_note_deleted = only_deleted
            self._clear_editor()
            return

        target_id = select_id if select_id in self.note_ids else self.note_ids[0]
        index = self.note_ids.index(target_id)
        self.notes_list.selection_clear(0, tk.END)
        self.notes_list.selection_set(index)
        self.notes_list.activate(index)
        self.notes_list.see(index)
        self._load_note(target_id)

    def _note_label(self, note: Note) -> str:
        icon = ICONS["trash"] if note.deleted_at else ICONS["note"]
        tags = f"  #{' #'.join(note.tags[:3])}" if note.tags else ""
        return f"{icon} {note.title}{tags}"

    def _refresh_notes(self) -> None:
        self._load_notes(self.current_note_id)
        self.status_var.set("Lista atualizada")

    def _create_note(self) -> None:
        if self._is_trash_view():
            self._set_view_mode("notes")
        note = self.repository.create_note()
        self.search_var.set("")
        self._load_notes(note.id)
        self.editor.focus_set()
        self.status_var.set("Nova nota criada")

    def _load_note(self, note_id: int) -> None:
        note = self.repository.get_note(note_id)
        self.loading = True
        self.current_note_id = note.id
        self.current_note_deleted = note.deleted_at is not None
        self.title_var.set(note.title)
        self.tags_var.set(", ".join(note.tags))
        self.editor.configure(state=tk.NORMAL)
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", note.content)
        self.editor.edit_modified(False)
        self.loading = False
        self._set_editor_editable(not self.current_note_deleted)
        self._refresh_analysis()
        self._refresh_preview()
        self._update_note_meta(note)
        self._update_sidebar_actions()
        self.status_var.set(f"Editando: {note.title}" if not self.current_note_deleted else f"Na lixeira: {note.title}")

    def _clear_editor(self) -> None:
        self.loading = True
        self.title_var.set("")
        self.tags_var.set("")
        self.editor.configure(state=tk.NORMAL)
        self.editor.delete("1.0", tk.END)
        self.loading = False
        self._set_editor_editable(False)
        self.note_meta_var.set("Nenhuma nota selecionada.")
        self._refresh_analysis()
        self._refresh_preview()

    def _set_editor_editable(self, editable: bool) -> None:
        state = tk.NORMAL if editable else tk.DISABLED
        self.editor.configure(state=state)
        self.title_entry.configure(state=state)
        self.tags_entry.configure(state=state)
        if self.current_note_deleted:
            self.note_meta_var.set("Esta nota esta na lixeira. Restaure para editar novamente.")

    def _on_note_selected(self, _event: tk.Event) -> None:
        if self.loading:
            return
        selection = self.notes_list.curselection()
        if not selection:
            return
        note_id = self.note_ids[selection[0]]
        if note_id != self.current_note_id:
            self._save_current_note()
            self._load_note(note_id)

    def _on_editor_modified(self, _event: tk.Event) -> None:
        if self.loading or self.current_note_deleted or not self.editor.edit_modified():
            return
        self.editor.edit_modified(False)
        self._schedule_save()
        self._schedule_analysis()
        self._schedule_preview()

    def _on_metadata_changed(self, *_args: object) -> None:
        if self.loading or self.current_note_deleted:
            return
        self._schedule_save()

    def _on_search_changed(self, *_args: object) -> None:
        if self.loading:
            return
        if self.search_after_id:
            self.root.after_cancel(self.search_after_id)
        self.search_after_id = self.root.after(180, lambda: self._load_notes(self.current_note_id))

    def _schedule_save(self) -> None:
        if self.save_after_id:
            self.root.after_cancel(self.save_after_id)
        self.status_var.set("Alteracoes pendentes...")
        self.save_after_id = self.root.after(700, self._save_current_note)

    def _schedule_analysis(self) -> None:
        if self.analysis_after_id:
            self.root.after_cancel(self.analysis_after_id)
        self.analysis_after_id = self.root.after(220, self._refresh_analysis)

    def _schedule_preview(self) -> None:
        if self.preview_after_id:
            self.root.after_cancel(self.preview_after_id)
        self.preview_after_id = self.root.after(220, self._refresh_preview)

    def _save_current_note(self) -> None:
        if self.current_note_id is None or self.loading or self.current_note_deleted:
            return
        self.save_after_id = None
        content = self._editor_content()
        title = self.title_var.get().strip() or analyze_note(content).suggested_title
        tags = self._parse_tags(self.tags_var.get())
        try:
            note = self.repository.update_note(self.current_note_id, title, content, tags)
        except KeyError:
            return
        self.current_note_id = note.id
        self.status_var.set("Salvo")
        self._update_note_meta(note)
        self._sync_list_label(note)

    def _primary_sidebar_action(self) -> None:
        if self._is_trash_view():
            self._restore_current_note()
        else:
            self._move_current_note_to_trash()

    def _secondary_sidebar_action(self) -> None:
        if self._is_trash_view():
            self._delete_current_note_forever()
        else:
            self._refresh_notes()

    def _move_current_note_to_trash(self) -> None:
        if self.current_note_id is None or self.current_note_deleted:
            return
        title = self.title_var.get().strip() or "esta nota"
        confirmed = messagebox.askyesno("Mover para lixeira", f"Mover '{title}' para a lixeira?\n\nVoce pode restaurar depois.")
        if not confirmed:
            return
        self.repository.move_to_trash(self.current_note_id)
        self.current_note_id = None
        self._load_notes()
        if not self.note_ids and not self._is_trash_view():
            self._create_note()
        self.status_var.set("Nota movida para a lixeira")

    def _restore_current_note(self) -> None:
        if self.current_note_id is None or not self.current_note_deleted:
            return
        note = self.repository.restore_note(self.current_note_id)
        self.status_var.set("Nota restaurada")
        self._set_view_mode("notes", select_id=note.id)

    def _delete_current_note_forever(self) -> None:
        if self.current_note_id is None:
            return
        title = self.title_var.get().strip() or "esta nota"
        confirmed = messagebox.askyesno(
            "Apagar definitivamente",
            f"Apagar '{title}' definitivamente?\n\nEsta acao nao pode ser desfeita.",
        )
        if not confirmed:
            return
        self.repository.delete_note_forever(self.current_note_id)
        self.current_note_id = None
        self._load_notes()
        self.status_var.set("Nota apagada definitivamente")

    def _empty_trash(self) -> None:
        deleted_notes = self.repository.list_notes(only_deleted=True)
        if not deleted_notes:
            self.status_var.set("A lixeira ja esta vazia")
            return
        confirmed = messagebox.askyesno(
            "Esvaziar lixeira",
            f"Apagar definitivamente {len(deleted_notes)} nota(s) da lixeira?\n\nEsta acao nao pode ser desfeita.",
        )
        if not confirmed:
            return
        removed = self.repository.empty_trash()
        self.current_note_id = None
        self._load_notes()
        self.status_var.set(f"Lixeira esvaziada: {removed} nota(s) removida(s)")

    def _import_text(self) -> None:
        if self._is_trash_view():
            self._set_view_mode("notes")
        path = filedialog.askopenfilename(
            title="Importar texto",
            filetypes=[("Textos", "*.txt *.md"), ("Todos os arquivos", "*.*")],
        )
        if not path:
            return
        file_path = Path(path)
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = file_path.read_text(encoding="latin-1")
        analysis = analyze_note(content)
        note = self.repository.create_note(title=analysis.suggested_title, content=content, tags=analysis.suggested_tags)
        self.search_var.set("")
        self._load_notes(note.id)
        self.status_var.set(f"Importado: {file_path.name}")

    def _export_markdown(self) -> None:
        if self.current_note_id is None:
            return
        if self.current_note_deleted:
            messagebox.showinfo("Nota na lixeira", "Restaure a nota antes de exportar.")
            return
        self._save_current_note()
        title = self.title_var.get().strip() or "nota"
        safe_title = "".join(char for char in title if char.isalnum() or char in (" ", "-", "_")).strip() or "nota"
        path = filedialog.asksaveasfilename(
            title="Exportar Markdown",
            defaultextension=".md",
            initialfile=f"{safe_title}.md",
            filetypes=[("Markdown", "*.md"), ("Texto", "*.txt")],
        )
        if not path:
            return
        tags = self._parse_tags(self.tags_var.get())
        front_matter = ""
        if tags:
            front_matter = "---\n" + "tags: [" + ", ".join(tags) + "]\n---\n\n"
        Path(path).write_text(f"# {title}\n\n{front_matter}{self._editor_content()}", encoding="utf-8")
        self.status_var.set(f"Exportado: {Path(path).name}")

    def _apply_suggested_title(self) -> None:
        if self.current_note_deleted:
            return
        analysis = analyze_note(self._editor_content())
        self.title_var.set(analysis.suggested_title)
        self._save_current_note()

    def _apply_suggested_tags(self) -> None:
        if self.current_note_deleted:
            return
        analysis = analyze_note(self._editor_content())
        existing = self._parse_tags(self.tags_var.get())
        merged = existing[:]
        for tag in analysis.suggested_tags:
            if tag not in merged:
                merged.append(tag)
        self.tags_var.set(", ".join(merged))
        self._save_current_note()

    def _configure_preview_tags(self) -> None:
        self.preview.tag_configure("h1", font=("Segoe UI Semibold", 20), foreground=THEME["accent"], spacing3=10)
        self.preview.tag_configure("h2", font=("Segoe UI Semibold", 16), foreground=THEME["accent"], spacing3=8)
        self.preview.tag_configure("h3", font=("Segoe UI Semibold", 13), foreground=THEME["ink"], spacing3=6)
        self.preview.tag_configure("paragraph", font=("Segoe UI", 11), foreground=THEME["ink"], spacing3=5)
        self.preview.tag_configure("muted", foreground=THEME["muted"])
        self.preview.tag_configure("bullet", lmargin1=18, lmargin2=34, foreground=THEME["ink"], spacing3=4)
        self.preview.tag_configure("quote", lmargin1=18, lmargin2=18, foreground=THEME["muted"], background=THEME["panel_alt"], spacing1=4, spacing3=4)
        self.preview.tag_configure("code", font=("Cascadia Mono", 10), background=THEME["panel_alt"], foreground=THEME["ink"], lmargin1=12, lmargin2=12, spacing1=4, spacing3=4)
        self.preview.tag_configure("rule", foreground=THEME["line"], spacing1=4, spacing3=4)
        self.preview.tag_configure("done", foreground=THEME["muted"], overstrike=True)

    def _refresh_preview(self) -> None:
        if not hasattr(self, "preview"):
            return
        blocks = parse_markdown(self._editor_content())
        self.preview.configure(state=tk.NORMAL)
        self.preview.delete("1.0", tk.END)
        if not blocks:
            self.preview.insert(tk.END, "A preview Markdown aparece aqui enquanto voce escreve.", "muted")
        for block in blocks:
            self._insert_preview_block(block)
        self.preview.configure(state=tk.DISABLED)

    def _insert_preview_block(self, block: MarkdownBlock) -> None:
        if block.kind == "blank":
            self.preview.insert(tk.END, "\n")
        elif block.kind == "heading":
            tag = "h1" if block.level == 1 else "h2" if block.level == 2 else "h3"
            self.preview.insert(tk.END, f"{block.text}\n", tag)
        elif block.kind == "checkbox":
            marker = "[x]" if block.checked else "[ ]"
            tag = "done" if block.checked else "bullet"
            self.preview.insert(tk.END, f"{marker} {block.text}\n", tag)
        elif block.kind == "bullet":
            self.preview.insert(tk.END, f"- {block.text}\n", "bullet")
        elif block.kind == "ordered":
            self.preview.insert(tk.END, f"1. {block.text}\n", "bullet")
        elif block.kind == "quote":
            self.preview.insert(tk.END, f"{block.text}\n", "quote")
        elif block.kind == "code":
            self.preview.insert(tk.END, f"{block.text}\n", "code")
        elif block.kind == "rule":
            self.preview.insert(tk.END, "-" * 48 + "\n", "rule")
        else:
            self.preview.insert(tk.END, f"{block.text}\n", "paragraph")

    def _refresh_analysis(self) -> None:
        analysis = analyze_note(self._editor_content())
        self._render_analysis(analysis)

    def _render_analysis(self, analysis: SmartAnalysis) -> None:
        self.summary_var.set(f"Resumo: {analysis.summary}")
        keywords = ", ".join(analysis.keywords) if analysis.keywords else "nenhuma ainda"
        tags = ", ".join(analysis.suggested_tags) if analysis.suggested_tags else "nenhuma ainda"
        todos = "; ".join(analysis.todos[:3]) if analysis.todos else "nenhuma tarefa detectada"
        self.keywords_var.set(f"Palavras-chave: {keywords}")
        self.suggested_tags_var.set(f"Tags sugeridas: {tags}")
        self.todos_var.set(f"Tarefas: {todos}")
        stats = analysis.stats
        self.stats_var.set(
            f"{stats.words} palavras | {stats.characters} caracteres | {stats.lines} linhas | leitura: {stats.reading_minutes} min"
        )
        self.suggested_title_var.set(f"Titulo sugerido: {analysis.suggested_title}")

    def _sync_list_label(self, note: Note) -> None:
        if note.id not in self.note_ids:
            return
        index = self.note_ids.index(note.id)
        self.notes_list.delete(index)
        self.notes_list.insert(index, self._note_label(note))
        self.notes_list.selection_set(index)
        self.notes_list.activate(index)

    def _set_view_mode(self, mode: str, select_id: int | None = None) -> None:
        if mode not in {"notes", "trash"}:
            return
        self._save_current_note()
        self.view_mode.set(mode)
        self._load_notes(select_id)
        self.status_var.set("Modo Notas" if mode == "notes" else "Modo Lixeira")

    def _update_mode_buttons(self) -> None:
        active = self.view_mode.get()
        buttons = {
            "notes": self.notes_mode_button,
            "trash": self.trash_mode_button,
        }
        for mode, button in buttons.items():
            selected = mode == active
            button.configure(
                bg=THEME["accent"] if selected else THEME["panel_alt"],
                fg="#ffffff" if selected else THEME["ink"],
                activebackground=THEME["accent_dark"] if selected else THEME["accent_soft"],
                activeforeground="#ffffff" if selected else THEME["ink"],
            )

    def _update_sidebar_actions(self) -> None:
        has_note = self.current_note_id is not None
        if self._is_trash_view():
            self.primary_sidebar_button.configure(text=f"{ICONS['restore']} Restaurar nota", state=tk.NORMAL if has_note else tk.DISABLED)
            self.secondary_sidebar_button.configure(text=f"{ICONS['delete']} Apagar definitivo", state=tk.NORMAL if has_note else tk.DISABLED)
        else:
            self.primary_sidebar_button.configure(text=f"{ICONS['trash']} Mover para lixeira", state=tk.NORMAL if has_note else tk.DISABLED)
            self.secondary_sidebar_button.configure(text="Atualizar lista", state=tk.NORMAL)

    def _update_mode_text(self, count: int) -> None:
        if self._is_trash_view():
            self.counter_var.set(f"{count} na lixeira")
            self.mode_hint_var.set("Lixeira: restaure notas importantes ou apague definitivamente quando tiver certeza.")
        else:
            self.counter_var.set(f"{count} nota(s)")
            self.mode_hint_var.set("Notas ativas. Use Ctrl+F para buscar e Ctrl+Shift+Delete para mover para a lixeira.")
        self._update_status_panels()

    def _update_note_meta(self, note: Note) -> None:
        if note.deleted_at:
            self.note_meta_var.set(f"Na lixeira desde {note.deleted_at} | criada em {note.created_at}")
        else:
            self.note_meta_var.set(f"Atualizada em {note.updated_at} | criada em {note.created_at}")

    def _toggle_preview(self) -> None:
        self.preview_visible_var.set(not self.preview_visible_var.get())
        self._apply_preview_visibility()

    def _apply_preview_visibility(self) -> None:
        visible = self.preview_visible_var.get()
        self.settings.preview_visible = visible
        self._save_settings()
        panes = set(self.editor_split.panes()) if hasattr(self, "editor_split") else set()
        preview_name = str(self.preview_column) if hasattr(self, "preview_column") else ""
        if visible and preview_name not in panes:
            self.editor_split.add(self.preview_column, weight=2)
            self._refresh_preview()
        elif not visible and preview_name in panes:
            self.editor_split.forget(self.preview_column)
        self.status_var.set("Preview Markdown ativado" if visible else "Preview Markdown ocultado")

    def _change_theme(self, theme_name: str) -> None:
        self._set_theme(theme_name)
        self.root.configure(bg=THEME["app_bg"])
        self._configure_style()
        self._repaint_widget_tree(self.root)
        self._configure_preview_tags()
        self._update_mode_buttons()
        self._refresh_preview()
        self.status_var.set(f"Tema aplicado: {THEMES[self.theme_name]['name']}")

    def _repaint_widget_tree(self, widget: tk.Misc) -> None:
        widget_class = widget.winfo_class()
        try:
            if widget is self.root:
                widget.configure(bg=THEME["app_bg"])
            elif isinstance(widget, tk.Text):
                if widget is getattr(self, "editor", None):
                    widget.configure(
                        bg=THEME["editor_bg"],
                        fg=THEME["ink"],
                        insertbackground=THEME["ink"],
                        selectbackground=THEME["selection"],
                        highlightbackground=THEME["line"],
                        highlightcolor=THEME["accent"],
                    )
                elif widget is getattr(self, "preview", None):
                    widget.configure(
                        bg=THEME["preview_bg"],
                        fg=THEME["ink"],
                        highlightbackground=THEME["line"],
                        highlightcolor=THEME["accent"],
                    )
            elif isinstance(widget, tk.Listbox):
                widget.configure(
                    bg=THEME["editor_bg"],
                    fg=THEME["ink"],
                    selectbackground=THEME["accent"],
                    selectforeground="#ffffff",
                    highlightbackground=THEME["line"],
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=THEME["editor_bg"],
                    fg=THEME["ink"],
                    insertbackground=THEME["ink"],
                    highlightbackground=THEME["line"],
                    highlightcolor=THEME["accent"],
                )
            elif isinstance(widget, tk.Label):
                widget.configure(bg=THEME["panel_bg"], fg=THEME["ink"])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=THEME["panel_bg"], highlightbackground=THEME["line"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=THEME["panel_alt"], fg=THEME["ink"], activebackground=THEME["accent_soft"])
        except tk.TclError:
            pass

        for child in widget.winfo_children():
            self._repaint_widget_tree(child)

    def _save_settings(self) -> None:
        if self.settings_store:
            self.settings_store.save(self.settings)

    def _unlock_if_needed(self) -> bool:
        if not self.settings.encryption_enabled:
            self.repository.set_password(None)
            self._update_status_panels()
            return True

        for _attempt in range(3):
            password = simpledialog.askstring("Notas protegidas", "Digite a senha das notas:", show="*", parent=self.root)
            if password is None:
                return False
            if verify_password(password, self.settings.password_record):
                self.repository.set_password(password)
                self._update_status_panels()
                return True
            messagebox.showerror("Senha incorreta", "A senha informada nao desbloqueou as notas.")
        return False

    def _prompt_new_password(self) -> str | None:
        password = simpledialog.askstring("Criar senha", "Digite uma senha para proteger as notas:", show="*", parent=self.root)
        if not password:
            return None
        confirmation = simpledialog.askstring("Confirmar senha", "Digite a senha novamente:", show="*", parent=self.root)
        if password != confirmation:
            messagebox.showerror("Senhas diferentes", "As senhas nao conferem.")
            return None
        if len(password) < 8:
            messagebox.showerror("Senha curta", "Use pelo menos 8 caracteres.")
            return None
        return password

    def _enable_encryption(self, password: str | None = None) -> None:
        if self.settings.encryption_enabled:
            self.status_var.set("A protecao por senha ja esta ativa")
            return
        password = password or self._prompt_new_password()
        if not password:
            return
        self._save_current_note()
        self._create_backup_now("antes-criptografia")
        self.repository.encrypt_all_notes(password)
        self.repository.set_password(password)
        self.settings.encryption_enabled = True
        self.settings.password_record = create_password_record(password)
        self._save_settings()
        self._load_notes(self.current_note_id)
        self._update_status_panels()
        self.status_var.set("Protecao por senha ativada")

    def _disable_encryption(self, password: str | None = None) -> None:
        if not self.settings.encryption_enabled:
            self.status_var.set("A protecao por senha ja esta desativada")
            return
        password = password or simpledialog.askstring("Desativar protecao", "Digite a senha atual:", show="*", parent=self.root)
        if not password:
            return
        if not verify_password(password, self.settings.password_record):
            messagebox.showerror("Senha incorreta", "A senha informada esta incorreta.")
            return
        self._save_current_note()
        self._create_backup_now("antes-descriptografia")
        self.repository.decrypt_all_notes(password)
        self.repository.set_password(None)
        self.settings.encryption_enabled = False
        self.settings.password_record = None
        self._save_settings()
        self._load_notes(self.current_note_id)
        self._update_status_panels()
        self.status_var.set("Protecao por senha desativada")

    def _create_backup_now(self, reason: str = "manual") -> None:
        self._save_current_note()
        if not self.backup_manager:
            self.status_var.set("Backup indisponivel neste ambiente")
            return
        backup = self.backup_manager.create_backup(reason)
        if backup:
            self.status_var.set(f"Backup criado: {backup.name}")
        else:
            self.status_var.set("Nenhum banco encontrado para backup")
        self._update_status_panels()

    def _run_startup_backup(self) -> None:
        if not self.backup_manager or not self.settings.backup_enabled:
            self._update_status_panels()
            return
        backup = self.backup_manager.create_backup_if_due(self.settings.backup_interval_minutes, "auto")
        if backup:
            self.status_var.set(f"Backup automatico criado: {backup.name}")
        self._update_status_panels()

    def _schedule_auto_backup(self) -> None:
        if not self.settings.backup_enabled:
            return
        interval_ms = max(1, self.settings.backup_interval_minutes) * 60 * 1000
        self.backup_after_id = self.root.after(interval_ms, self._auto_backup_tick)

    def _auto_backup_tick(self) -> None:
        self._run_startup_backup()
        self._schedule_auto_backup()

    def _open_backup_folder(self) -> None:
        if not self.backup_manager:
            return
        folder = self.backup_manager.backup_dir
        folder.mkdir(parents=True, exist_ok=True)
        if sys.platform.startswith("win"):
            os.startfile(folder)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(folder)])
        else:
            subprocess.Popen(["xdg-open", str(folder)])

    def _update_status_panels(self) -> None:
        self.security_var.set("Seguranca: senha ativa" if self.settings.encryption_enabled else "Seguranca: sem senha")
        if self.backup_manager:
            latest = self.backup_manager.latest_backup()
            label = latest.name if latest else "nenhum backup ainda"
            self.backup_var.set(f"Backup: {label}")
        else:
            self.backup_var.set("Backup: indisponivel")

    def _focus_search(self) -> None:
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def _clear_search(self) -> None:
        if self.search_var.get():
            self.search_var.set("")

    def _show_shortcuts(self) -> None:
        messagebox.showinfo(
            "Atalhos",
            "\n".join(
                [
                    "Ctrl+N - nova nota",
                    "Ctrl+S - salvar agora",
                    "Ctrl+F - buscar",
                    "Ctrl+E - exportar Markdown",
                    "Ctrl+I - importar texto",
                    "Ctrl+P - mostrar/ocultar preview Markdown",
                    "Ctrl+B - criar backup agora",
                    "Ctrl+1 - ver notas",
                    "Ctrl+2 - ver lixeira",
                    "Ctrl+L - usar titulo sugerido",
                    "Ctrl+Shift+T - adicionar tags sugeridas",
                    "Ctrl+Shift+Delete - mover para lixeira",
                    "Ctrl+Shift+R - restaurar nota",
                    "F5 - atualizar",
                    "Esc - limpar busca",
                ]
            ),
        )

    def _editor_content(self) -> str:
        was_disabled = str(self.editor.cget("state")) == tk.DISABLED
        if was_disabled:
            self.editor.configure(state=tk.NORMAL)
        content = self.editor.get("1.0", tk.END).rstrip("\n")
        if was_disabled:
            self.editor.configure(state=tk.DISABLED)
        return content

    def _is_trash_view(self) -> bool:
        return self.view_mode.get() == "trash"

    @staticmethod
    def _parse_tags(raw_tags: str) -> list[str]:
        return [tag.strip().lower().replace(" ", "-") for tag in raw_tags.split(",") if tag.strip()]

    def _on_close(self) -> None:
        self._save_current_note()
        if self.backup_manager and self.settings.backup_enabled:
            self.backup_manager.create_backup_if_due(self.settings.backup_interval_minutes, "fechamento")
        self.root.destroy()

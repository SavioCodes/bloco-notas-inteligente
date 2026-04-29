from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass


STOPWORDS = {
    "a",
    "agora",
    "ao",
    "aos",
    "as",
    "com",
    "como",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "entre",
    "era",
    "essa",
    "esse",
    "esta",
    "este",
    "eu",
    "foi",
    "ha",
    "isso",
    "mais",
    "mas",
    "me",
    "minha",
    "na",
    "nao",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "ou",
    "para",
    "pela",
    "pelo",
    "por",
    "que",
    "se",
    "sem",
    "sua",
    "sao",
    "tem",
    "ter",
    "um",
    "uma",
}

TAG_SIGNALS = {
    "ideia": {"ideia", "brainstorm", "conceito", "inspiracao"},
    "reuniao": {"reuniao", "meeting", "ata", "participantes"},
    "tarefa": {"todo", "tarefa", "pendente", "fazer", "acao"},
    "estudo": {"estudo", "pesquisa", "resumo", "referencia"},
    "projeto": {"projeto", "roadmap", "entrega", "prazo"},
}

TODO_PATTERNS = (
    re.compile(r"^\s*[-*]?\s*\[\s\]\s+(.+)", re.IGNORECASE),
    re.compile(r"\b(todo|tarefa|pendente|fazer|acao)\b", re.IGNORECASE),
)

WORD_RE = re.compile(r"[^\W_]{3,}", re.IGNORECASE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class TextStats:
    characters: int
    words: int
    lines: int
    reading_minutes: int


@dataclass(frozen=True)
class SmartAnalysis:
    summary: str
    keywords: list[str]
    suggested_tags: list[str]
    todos: list[str]
    suggested_title: str
    stats: TextStats


def analyze_note(content: str) -> SmartAnalysis:
    text = content.strip()
    words = _extract_words(text)
    keywords = _keywords(words)
    todos = _todos(text)
    suggested_tags = _suggest_tags(words, keywords, todos)
    stats = TextStats(
        characters=len(content),
        words=len(words),
        lines=content.count("\n") + 1 if content else 0,
        reading_minutes=max(1, round(len(words) / 220)) if words else 0,
    )
    return SmartAnalysis(
        summary=_summary(text),
        keywords=keywords,
        suggested_tags=suggested_tags,
        todos=todos,
        suggested_title=_suggest_title(text, keywords),
        stats=stats,
    )


def _extract_words(text: str) -> list[str]:
    return [_normalize_word(word) for word in WORD_RE.findall(text)]


def _normalize_word(word: str) -> str:
    decomposed = unicodedata.normalize("NFKD", word)
    without_marks = "".join(char for char in decomposed if not unicodedata.combining(char))
    return without_marks.lower()


def _keywords(words: list[str], limit: int = 8) -> list[str]:
    relevant = [word for word in words if word not in STOPWORDS and not word.isdigit()]
    return [word for word, _ in Counter(relevant).most_common(limit)]


def _todos(text: str) -> list[str]:
    todos: list[str] = []
    for line in text.splitlines():
        clean = line.strip()
        if not clean:
            continue
        normalized = _normalize_word(clean)
        if any(pattern.search(clean) or pattern.search(normalized) for pattern in TODO_PATTERNS):
            todos.append(clean)
    return todos[:10]


def _suggest_tags(words: list[str], keywords: list[str], todos: list[str], limit: int = 6) -> list[str]:
    word_set = set(words)
    tags: list[str] = []
    for tag, signals in TAG_SIGNALS.items():
        if word_set.intersection(signals):
            tags.append(tag)
    if todos and "tarefa" not in tags:
        tags.append("tarefa")
    for keyword in keywords:
        if keyword not in tags:
            tags.append(keyword)
        if len(tags) >= limit:
            break
    return tags[:limit]


def _summary(text: str, limit: int = 240) -> str:
    if not text:
        return "Escreva uma nota para ver o resumo inteligente."
    sentences = [sentence.strip() for sentence in SENTENCE_RE.split(text) if sentence.strip()]
    summary = " ".join(sentences[:2]) if sentences else text
    return summary if len(summary) <= limit else summary[: limit - 3].rstrip() + "..."


def _suggest_title(text: str, keywords: list[str]) -> str:
    if not text:
        return "Nota sem titulo"
    for line in text.splitlines():
        clean = line.strip().strip("#").strip()
        if clean:
            return clean[:70]
    if keywords:
        return " ".join(word.capitalize() for word in keywords[:4])
    return "Nota sem titulo"

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownBlock:
    kind: str
    text: str = ""
    level: int = 0
    checked: bool = False


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
ORDERED_RE = re.compile(r"^\s*\d+[.)]\s+(.+)$")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.+)$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+)$")


def parse_markdown(markdown: str) -> list[MarkdownBlock]:
    blocks: list[MarkdownBlock] = []
    in_code = False
    code_lines: list[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("```"):
            if in_code:
                blocks.append(MarkdownBlock("code", "\n".join(code_lines)))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not line.strip():
            blocks.append(MarkdownBlock("blank"))
            continue

        heading = HEADING_RE.match(line)
        if heading:
            blocks.append(MarkdownBlock("heading", heading.group(2).strip(), level=len(heading.group(1))))
            continue

        checkbox = CHECKBOX_RE.match(line)
        if checkbox:
            blocks.append(MarkdownBlock("checkbox", checkbox.group(2).strip(), checked=checkbox.group(1).lower() == "x"))
            continue

        bullet = BULLET_RE.match(line)
        if bullet:
            blocks.append(MarkdownBlock("bullet", bullet.group(1).strip()))
            continue

        ordered = ORDERED_RE.match(line)
        if ordered:
            blocks.append(MarkdownBlock("ordered", ordered.group(1).strip()))
            continue

        if line.startswith(">"):
            blocks.append(MarkdownBlock("quote", line.lstrip("> ").strip()))
            continue

        if set(line.strip()) <= {"-", "*", "_"} and len(line.strip()) >= 3:
            blocks.append(MarkdownBlock("rule"))
            continue

        blocks.append(MarkdownBlock("paragraph", line.strip()))

    if in_code and code_lines:
        blocks.append(MarkdownBlock("code", "\n".join(code_lines)))

    return _compact_blanks(blocks)


def _compact_blanks(blocks: list[MarkdownBlock]) -> list[MarkdownBlock]:
    compact: list[MarkdownBlock] = []
    previous_blank = False
    for block in blocks:
        if block.kind == "blank":
            if not previous_blank:
                compact.append(block)
            previous_blank = True
        else:
            compact.append(block)
            previous_blank = False
    return compact


#!/usr/bin/env python3
"""Vérifie que les liens Markdown internes pointent vers des fichiers existants."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "#"))


def check_file(md_file: Path) -> list[str]:
    errors = []
    text = md_file.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if is_external(target):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        resolved = (md_file.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{md_file.relative_to(ROOT)}: lien mort -> {target}")
    return errors


def main() -> int:
    all_errors = []
    for md_file in sorted(ROOT.rglob("*.md")):
        if ".git" in md_file.parts:
            continue
        all_errors.extend(check_file(md_file))

    if all_errors:
        print("Liens internes cassés :")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print("Tous les liens internes sont valides.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

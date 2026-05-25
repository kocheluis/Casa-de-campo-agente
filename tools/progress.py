"""Recalcula el avance del proyecto leyendo las casillas de PROJECT_PLAN.md.

Cuenta las tareas marcadas con "- [x]" contra el total, dentro del bloque delimitado por
<!-- TASKS:START --> y <!-- TASKS:END -->, ponderando por las horas anotadas como "(6h)".
Luego reescribe el bloque entre <!-- PROGRESS:START --> y <!-- PROGRESS:END --> con una
tabla por fase, una barra de avance global y la fecha de actualización.

Pensado también como primer ejercicio de Python (solo librería estándar). Notas para
quien viene de C/Java:
  - No hay tipos obligatorios ni ';'. La indentación define los bloques (no hay llaves).
  - Una lista es como un ArrayList; un diccionario {} es como un HashMap.
  - 're' es la librería de expresiones regulares; 'pathlib.Path' maneja rutas de archivo.

Uso:
    python tools/progress.py
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

# El plan está en la raíz del repo (un nivel arriba de tools/).
PLAN_PATH = Path(__file__).resolve().parent.parent / "PROJECT_PLAN.md"

# Marcadores que delimitan las zonas que leemos/escribimos.
TASKS_START, TASKS_END = "<!-- TASKS:START -->", "<!-- TASKS:END -->"
PROGRESS_START, PROGRESS_END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"

# Patrones: una tarea "- [ ] texto (6h)", las horas, y un encabezado de fase "### Fase".
TASK_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s+(.*)$")
HOURS_RE = re.compile(r"\((\d+)\s*h\)")
PHASE_RE = re.compile(r"^###\s+(.*)$")


def _between(text: str, start: str, end: str) -> str:
    """Devuelve el texto entre dos marcadores. Falla claro si faltan."""
    if start not in text or end not in text:
        raise SystemExit(f"Faltan los marcadores {start} / {end} en {PLAN_PATH.name}.")
    return text[text.index(start) + len(start): text.index(end)]


def parse_phases(tasks_block: str) -> list[dict]:
    """Recorre el bloque de tareas y agrupa el avance por fase."""
    phases: list[dict] = []
    current: dict | None = None
    for line in tasks_block.splitlines():
        phase_match = PHASE_RE.match(line)
        if phase_match:
            current = {
                "name": phase_match.group(1).strip(),
                "done_h": 0, "total_h": 0, "done_n": 0, "total_n": 0,
            }
            phases.append(current)
            continue
        task_match = TASK_RE.match(line)
        if task_match and current is not None:
            done = task_match.group(1).lower() == "x"
            hours_match = HOURS_RE.search(task_match.group(2))
            hours = int(hours_match.group(1)) if hours_match else 1
            current["total_h"] += hours
            current["total_n"] += 1
            if done:
                current["done_h"] += hours
                current["done_n"] += 1
    return phases


def bar(pct: float, width: int = 20) -> str:
    """Dibuja una barra de progreso con bloques llenos/vacíos."""
    filled = round(pct / 100 * width)
    return "#" * filled + "-" * (width - filled)


def build_progress(phases: list[dict]) -> str:
    """Construye el texto Markdown del bloque de avance."""
    total_h = sum(p["total_h"] for p in phases)
    done_h = sum(p["done_h"] for p in phases)
    overall = (done_h / total_h * 100) if total_h else 0

    lines = [
        f"**Última actualización:** {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"**Avance global: {overall:.0f}%**  `{bar(overall)}`  ({done_h}/{total_h} h)",
        "",
        "| Fase | Avance | Tareas | Horas |",
        "|---|---|---|---|",
    ]
    for p in phases:
        pct = (p["done_h"] / p["total_h"] * 100) if p["total_h"] else 0
        lines.append(
            f"| {p['name']} | {pct:.0f}% `{bar(pct, 12)}` | "
            f"{p['done_n']}/{p['total_n']} | {p['done_h']}/{p['total_h']} |"
        )
    return "\n".join(lines)


def main() -> None:
    if not PLAN_PATH.exists():
        raise SystemExit(f"No se encontró {PLAN_PATH}.")
    text = PLAN_PATH.read_text(encoding="utf-8")

    phases = parse_phases(_between(text, TASKS_START, TASKS_END))
    if not phases:
        raise SystemExit("No se encontraron fases/tareas en el bloque TASKS.")

    progress_md = "\n" + build_progress(phases) + "\n"
    before = text[: text.index(PROGRESS_START) + len(PROGRESS_START)]
    after = text[text.index(PROGRESS_END):]
    PLAN_PATH.write_text(before + progress_md + after, encoding="utf-8")

    # Resumen en consola.
    total_h = sum(p["total_h"] for p in phases)
    done_h = sum(p["done_h"] for p in phases)
    overall = (done_h / total_h * 100) if total_h else 0
    print(f"Avance actualizado en {PLAN_PATH.name}: {overall:.0f}% ({done_h}/{total_h} h)")
    for p in phases:
        pct = (p["done_h"] / p["total_h"] * 100) if p["total_h"] else 0
        print(f"  - {p['name']}: {pct:.0f}% ({p['done_n']}/{p['total_n']} tareas)")


if __name__ == "__main__":
    sys.exit(main())

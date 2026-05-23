"""Genera la respuesta del chatbot como si fuera el dueño de la casa de campo.

Lee la base de conocimiento (`knowledge/casa_de_campo.md`), la inyecta como contexto
(con caché de prompt para abaratar), y pide a Claude una respuesta en el tono del dueño.
Devuelve el texto a enviar y si la conversación debe escalarse a un humano (handoff).

Uso como módulo:
    from claude_reply import generate_reply
    out = generate_reply("¿Está libre este finde?", history=[...])
    print(out["reply"], out["handoff"])

Uso de prueba por consola:
    python tools/claude_reply.py "Hola, ¿cuánto cuesta por noche?"
"""
from __future__ import annotations

import sys
from pathlib import Path

from config import env, ROOT_DIR

try:
    from anthropic import Anthropic
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "anthropic no está instalado. Ejecuta: pip install -r requirements.txt"
    ) from exc

KNOWLEDGE_PATH = ROOT_DIR / "knowledge" / "casa_de_campo.md"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 800

# El modelo termina SIEMPRE con esta línea de control, que quitamos antes de enviar.
HANDOFF_TAG = "HANDOFF:"


def load_knowledge() -> str:
    """Lee la base de conocimiento del dueño."""
    if not KNOWLEDGE_PATH.exists():
        raise SystemExit(
            f"Falta la base de conocimiento en {KNOWLEDGE_PATH}. "
            "Créala a partir de la plantilla y complétala con la info real."
        )
    return KNOWLEDGE_PATH.read_text(encoding="utf-8")


def build_system_prompt(knowledge: str) -> str:
    """Arma las instrucciones del agente más la base de conocimiento."""
    return (
        "Eres el asistente que responde los mensajes iniciales de los clientes de una "
        "casa de campo en alquiler, haciéndolo COMO SI FUERAS EL DUEÑO. Usa el tono "
        "definido en la base de conocimiento. Reglas:\n"
        "- Responde solo con lo que está en la base de conocimiento. Si no sabes algo, "
        "NO inventes: dilo amablemente y avisa que el dueño responderá pronto.\n"
        "- Sé breve, claro y ofrece el siguiente paso.\n"
        "- No compartas la dirección exacta ni datos de pago hasta confirmar la reserva.\n"
        "- Escala al dueño (handoff) cuando: el cliente quiere reservar/separar fechas en "
        "firme, pregunta por pagos, hay una queja, o piden algo fuera de la base de "
        "conocimiento.\n\n"
        "FORMATO OBLIGATORIO de tu salida: primero el mensaje para el cliente, y en la "
        f"ÚLTIMA línea, sola, escribe '{HANDOFF_TAG} yes' si debe intervenir el dueño o "
        f"'{HANDOFF_TAG} no' si tu respuesta basta. Nunca muestres esa línea como parte "
        "del mensaje al cliente.\n\n"
        "=== BASE DE CONOCIMIENTO ===\n"
        f"{knowledge}"
    )


def _parse_output(text: str) -> dict:
    """Separa el mensaje al cliente de la línea de control HANDOFF."""
    handoff = False
    lines = text.strip().splitlines()
    if lines and lines[-1].strip().upper().startswith(HANDOFF_TAG):
        handoff = "yes" in lines[-1].lower()
        lines = lines[:-1]
    reply = "\n".join(lines).strip()
    return {"reply": reply, "handoff": handoff}


def generate_reply(user_message: str, history: list[dict] | None = None) -> dict:
    """Genera la respuesta del chatbot.

    Args:
        user_message: el último mensaje del cliente.
        history: lista opcional de mensajes previos [{"role": "user"|"assistant",
            "content": "..."}].

    Returns:
        dict con: reply (str), handoff (bool).
    """
    api_key = env("ANTHROPIC_API_KEY", required=True)
    model = env("ANTHROPIC_MODEL") or DEFAULT_MODEL
    client = Anthropic(api_key=api_key)

    system_prompt = build_system_prompt(load_knowledge())
    messages = list(history or [])
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        # Caché de prompt: la base de conocimiento es estática y grande -> se cachea
        # para abaratar las siguientes respuestas.
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=messages,
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    return _parse_output(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python tools/claude_reply.py "mensaje del cliente"')
        raise SystemExit(1)
    out = generate_reply(sys.argv[1])
    print("Respuesta:\n" + out["reply"])
    print("\n¿Escalar al dueño? ->", "Sí" if out["handoff"] else "No")

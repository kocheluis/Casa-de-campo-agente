"""Genera la respuesta del chatbot vía CUALQUIER LLM compatible (LiteLLM).

Soporta Anthropic Claude, OpenAI, Google Gemini, DeepSeek y otros 100+ proveedores.
Elige el modelo con dos variables de entorno:

    LLM_PROVIDER=anthropic | openai | gemini | deepseek | ...
    LLM_MODEL=claude-haiku-4-5-20251001 | gpt-4o-mini | gemini-2.5-flash | deepseek-chat

Y la API key del proveedor elegido (cada una en `.env`):

    ANTHROPIC_API_KEY=...
    OPENAI_API_KEY=...
    GEMINI_API_KEY=...
    DEEPSEEK_API_KEY=...

LiteLLM se encarga de hablar con cada API en su formato propio.

Uso CLI:
    python tools/ai_reply.py "Hola, está libre el finde para 4 personas?"
"""
from __future__ import annotations

import sys

from config import ROOT_DIR, env

try:
    from litellm import completion
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "litellm no está instalado. Ejecuta: pip install -r requirements.txt"
    ) from exc

KNOWLEDGE_PATH = ROOT_DIR / "knowledge" / "casa_de_campo.md"
DEFAULT_PROVIDER = "anthropic"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 800

# El modelo termina SIEMPRE con esta línea de control que quitamos antes de enviar.
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
        "- Escala al dueño (handoff) cuando: el cliente quiere reservar/separar fechas "
        "en firme, pregunta por pagos, hay una queja, o piden algo fuera de la base.\n\n"
        "FORMATO OBLIGATORIO de tu salida: primero el mensaje para el cliente, y en la "
        f"ÚLTIMA línea, sola, escribe '{HANDOFF_TAG} yes' si debe intervenir el dueño o "
        f"'{HANDOFF_TAG} no' si tu respuesta basta. Nunca muestres esa línea como parte "
        "del mensaje al cliente.\n\n"
        "=== BASE DE CONOCIMIENTO ===\n"
        f"{knowledge}"
    )


def parse_output(text: str) -> dict:
    """Separa el mensaje al cliente de la línea de control HANDOFF."""
    handoff = False
    lines = text.strip().splitlines()
    if lines and lines[-1].strip().upper().startswith(HANDOFF_TAG):
        handoff = "yes" in lines[-1].lower()
        lines = lines[:-1]
    return {"reply": "\n".join(lines).strip(), "handoff": handoff}


def get_provider() -> str:
    return (env("LLM_PROVIDER") or DEFAULT_PROVIDER).strip().lower()


def get_model_id() -> str:
    """Devuelve el id de modelo en formato LiteLLM ('provider/model'). Idempotente."""
    model = (env("LLM_MODEL") or DEFAULT_MODEL).strip()
    return model if "/" in model else f"{get_provider()}/{model}"


def _build_messages(system_prompt: str, history: list[dict] | None, user_message: str) -> list[dict]:
    """Arma la lista de mensajes. Si el proveedor es Anthropic, marca el system para caché."""
    if get_provider() == "anthropic":
        # Caché de prompt: la base de conocimiento es estática y grande → se cachea
        # para abaratar las siguientes respuestas (solo soportado oficialmente en Claude).
        system_msg = {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        }
    else:
        system_msg = {"role": "system", "content": system_prompt}
    return [system_msg, *(history or []), {"role": "user", "content": user_message}]


def generate_reply(user_message: str, history: list[dict] | None = None) -> dict:
    """Genera la respuesta del chatbot.

    Args:
        user_message: el último mensaje del cliente.
        history: lista opcional de turnos previos [{"role": "user"|"assistant", "content": "..."}].

    Returns:
        dict con: reply (str), handoff (bool).
    """
    system_prompt = build_system_prompt(load_knowledge())
    messages = _build_messages(system_prompt, history, user_message)

    response = completion(
        model=get_model_id(),
        messages=messages,
        max_tokens=MAX_TOKENS,
    )
    text = response.choices[0].message.content or ""
    return parse_output(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python tools/ai_reply.py "mensaje del cliente"')
        raise SystemExit(1)
    print(f"Modelo: {get_model_id()}\n")
    out = generate_reply(sys.argv[1])
    print("Respuesta:\n" + out["reply"])
    print("\n¿Escalar al dueño? ->", "Sí" if out["handoff"] else "No")

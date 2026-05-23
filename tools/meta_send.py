"""Envío de mensajes por los canales de Meta (WhatsApp, Instagram DM, Messenger).

Usa la WhatsApp Cloud API y la Graph API de Messenger/Instagram. Reutiliza la
configuración del framework (`config.env`). Requiere haber verificado el negocio en
Meta Business con el RUC y obtenido el token y el phone number id.

Configura en `.env`: META_ACCESS_TOKEN, META_PHONE_NUMBER_ID, META_GRAPH_VERSION,
y opcionalmente OWNER_WHATSAPP (número del dueño para avisos de handoff).

Uso:
    from meta_send import send_whatsapp, send_messenger, notify_owner
    send_whatsapp(to="51999888777", text="¡Hola! Claro que sí 😊")
"""
from __future__ import annotations

import sys

import requests

from config import env

TIMEOUT = 20
GRAPH = "https://graph.facebook.com"


def _version() -> str:
    return env("META_GRAPH_VERSION") or "v21.0"


def send_whatsapp(to: str, text: str) -> dict:
    """Envía un mensaje de texto por WhatsApp Cloud API.

    `to` es el número en formato internacional sin '+', ej. 51999888777.
    Nota: fuera de la ventana de 24h de WhatsApp solo se pueden enviar plantillas
    aprobadas; este helper es para responder dentro de esa ventana.
    """
    token = env("META_ACCESS_TOKEN", required=True)
    phone_id = env("META_PHONE_NUMBER_ID", required=True)
    url = f"{GRAPH}/{_version()}/{phone_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def send_messenger(recipient_id: str, text: str) -> dict:
    """Envía un mensaje por Messenger o Instagram DM (Graph API de la página).

    `recipient_id` es el PSID/IGSID que llega en el webhook entrante.
    """
    token = env("META_ACCESS_TOKEN", required=True)
    url = f"{GRAPH}/{_version()}/me/messages"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    r = requests.post(
        url,
        params={"access_token": token},
        json=payload,
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def notify_owner(text: str) -> dict | None:
    """Avisa al dueño por WhatsApp (handoff). No falla si OWNER_WHATSAPP no está configurado."""
    owner = env("OWNER_WHATSAPP")
    if not owner:
        print("OWNER_WHATSAPP no configurado; se omite el aviso al dueño.", file=sys.stderr)
        return None
    return send_whatsapp(to=owner, text=text)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Uso: python tools/meta_send.py <numero_whatsapp> "mensaje de prueba"')
        raise SystemExit(1)
    print(send_whatsapp(to=sys.argv[1], text=sys.argv[2]))

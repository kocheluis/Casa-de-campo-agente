"""Cliente para la base de datos autoalojada (NocoDB — elección del proyecto).

Es la única fuente de verdad del negocio: Clientes, Reservas, Inventario,
Conversaciones. Expone operaciones CRUD genéricas y helpers de alto nivel que usa el
chatbot. Reutiliza la configuración del framework (`config.env`).

Se eligió NocoDB sobre Baserow (ver research/02-base-de-datos.md): NocoDB ofrece la
vista Calendario gratis en self-hosted (en Baserow es de pago) y API REST con tokens.
Aun así el cliente soporta ambos vía DB_TYPE por si se decide migrar.

Configura en `.env`:
    DB_API_URL   -> URL base de la API de la tabla (ver .env.example)
    DB_API_TOKEN -> token de la API
    DB_TYPE      -> "nocodb" (por defecto) o "baserow"  [opcional]

NocoDB y Baserow usan cabeceras de auth distintas; este cliente lo resuelve solo.

Uso:
    from db_client import DBClient
    db = DBClient()
    cliente = db.find_or_create_client(telefono="51999...", nombre="Ana", canal="whatsapp")
"""
from __future__ import annotations

import sys

import requests

from config import env

TIMEOUT = 20


class DBClient:
    def __init__(self) -> None:
        self.base_url = env("DB_API_URL", required=True).rstrip("/")
        self.token = env("DB_API_TOKEN", required=True)
        self.db_type = (env("DB_TYPE") or "nocodb").lower()

    def _headers(self) -> dict:
        if self.db_type == "baserow":
            return {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}
        # NocoDB v2 usa la cabecera xc-token.
        return {"xc-token": self.token, "Content-Type": "application/json"}

    # --- CRUD genérico --------------------------------------------------------
    def list_records(self, params: dict | None = None) -> list[dict]:
        r = requests.get(self.base_url, headers=self._headers(), params=params, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        # NocoDB v2 -> {"list": [...]}; Baserow -> {"results": [...]}.
        return data.get("list") or data.get("results") or (data if isinstance(data, list) else [])

    def create_record(self, fields: dict) -> dict:
        r = requests.post(self.base_url, headers=self._headers(), json=fields, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def update_record(self, record_id, fields: dict) -> dict:
        url = f"{self.base_url}/{record_id}"
        r = requests.patch(url, headers=self._headers(), json=fields, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    # --- Helpers de negocio ---------------------------------------------------
    def find_or_create_client(self, telefono: str, nombre: str = "", canal: str = "") -> dict:
        """Busca un cliente por teléfono; si no existe, lo crea (captura de lead)."""
        encontrados = self.list_records(params={"where": f"(Telefono,eq,{telefono})"})
        if encontrados:
            return encontrados[0]
        return self.create_record(
            {"Telefono": telefono, "Nombre": nombre, "Canal": canal}
        )

    def log_conversation(self, telefono: str, mensaje: str, respuesta: str, handoff: bool) -> dict:
        """Guarda un turno de conversación y si requirió intervención humana."""
        return self.create_record(
            {
                "Telefono": telefono,
                "Mensaje": mensaje,
                "Respuesta": respuesta,
                "RequiereHumano": handoff,
            }
        )

    def create_tentative_reservation(self, telefono: str, fecha_inicio: str, fecha_fin: str) -> dict:
        """Crea una reserva tentativa para que el dueño la confirme."""
        return self.create_record(
            {
                "Telefono": telefono,
                "FechaInicio": fecha_inicio,
                "FechaFin": fecha_fin,
                "Estado": "tentativa",
            }
        )


if __name__ == "__main__":
    # Prueba de conexión: lista los primeros registros de la tabla configurada.
    try:
        db = DBClient()
        registros = db.list_records(params={"limit": 3})
        print(f"Conexión OK. {len(registros)} registro(s) de muestra:")
        for r in registros:
            print(" -", r)
    except Exception as exc:  # noqa: BLE001
        print("Error de conexión:", exc, file=sys.stderr)
        raise SystemExit(1)

"""Cliente para la base de datos del proyecto en NocoDB.

NocoDB es la única fuente de verdad: Clientes, Reservas, Inventario y Conversaciones.
Este módulo expone CRUD por tabla y helpers de alto nivel que usa el chatbot.

Se eligió NocoDB sobre Baserow (ver `research/02-base-de-datos.md`): Calendario gratis
en self-hosted y API REST estable con tokens.

Variables de entorno (en `.env`):
    DB_API_URL                  -> URL base de NocoDB (ej. http://localhost:8080)
    DB_API_TOKEN                -> personal API token (xc-token)
    TABLE_ID_CLIENTES           -> id de la tabla Clientes
    TABLE_ID_RESERVAS           -> id de la tabla Reservas
    TABLE_ID_INVENTARIO         -> id de la tabla Inventario
    TABLE_ID_CONVERSACIONES     -> id de la tabla Conversaciones

Las IDs las puebla automáticamente `tools/setup_nocodb.py`.

Uso:
    from db_client import DBClient
    db = DBClient()
    cliente = db.find_or_create_cliente(telefono="51999000111", nombre="Ana", canal="whatsapp")
"""
from __future__ import annotations

import sys

import requests

from config import env

TIMEOUT = 20


class DBClient:
    """Cliente REST de NocoDB orientado a las tablas del proyecto."""

    def __init__(self) -> None:
        self.base_url = env("DB_API_URL", required=True).rstrip("/")
        self.token = env("DB_API_TOKEN", required=True)
        self.tables: dict[str, str] = {
            "clientes": env("TABLE_ID_CLIENTES", required=True),
            "reservas": env("TABLE_ID_RESERVAS", required=True),
            "inventario": env("TABLE_ID_INVENTARIO", required=True),
            "conversaciones": env("TABLE_ID_CONVERSACIONES", required=True),
        }

    # --- internos -------------------------------------------------------------
    def _records_url(self, table: str) -> str:
        return f"{self.base_url}/api/v2/tables/{self.tables[table]}/records"

    def _link_url(self, table: str, link_field_id: str, record_id) -> str:
        return f"{self.base_url}/api/v2/tables/{self.tables[table]}/links/{link_field_id}/records/{record_id}"

    def _headers(self) -> dict[str, str]:
        return {"xc-token": self.token, "Content-Type": "application/json"}

    # --- CRUD genérico --------------------------------------------------------
    def list_records(self, table: str, params: dict | None = None) -> list[dict]:
        r = requests.get(self._records_url(table), headers=self._headers(), params=params, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return data.get("list") or (data if isinstance(data, list) else [])

    def create_record(self, table: str, fields: dict) -> dict:
        r = requests.post(self._records_url(table), headers=self._headers(), json=fields, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def update_record(self, table: str, record_id, fields: dict) -> dict:
        r = requests.patch(
            self._records_url(table),
            headers=self._headers(),
            json={"Id": record_id, **fields},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    def delete_record(self, table: str, record_id) -> dict:
        r = requests.delete(
            self._records_url(table),
            headers=self._headers(),
            json={"Id": record_id},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    # --- helpers de negocio ---------------------------------------------------
    def find_cliente_by_telefono(self, telefono: str) -> dict | None:
        res = self.list_records("clientes", params={"where": f"(Telefono,eq,{telefono})"})
        return res[0] if res else None

    def find_or_create_cliente(self, telefono: str, nombre: str = "", canal: str = "") -> dict:
        """Devuelve el cliente (creándolo si no existe). Captura el lead automáticamente."""
        existing = self.find_cliente_by_telefono(telefono)
        if existing:
            return existing
        return self.create_record(
            "clientes",
            {"Telefono": telefono, "Nombre": nombre or telefono, "Canal": canal},
        )

    def log_conversation(
        self,
        cliente_id: int | str,
        canal: str,
        mensaje: str,
        respuesta: str,
        handoff: bool,
        resumen: str = "",
    ) -> dict:
        """Guarda un turno de conversación enlazado al cliente."""
        return self.create_record(
            "conversaciones",
            {
                "Resumen": resumen or (mensaje[:60] + "..." if len(mensaje) > 60 else mensaje),
                "Canal": canal,
                "Mensaje": mensaje,
                "Respuesta": respuesta,
                "RequiereHumano": handoff,
                "nc_Cliente_id": cliente_id,  # NocoDB: el link se setea con nc_<field>_id
            },
        )

    def create_tentative_reservation(
        self,
        cliente_id: int | str,
        fecha_inicio: str,
        fecha_fin: str,
        num_personas: int | None = None,
    ) -> dict:
        """Crea una reserva en estado 'tentativa' para que el dueño la confirme."""
        return self.create_record(
            "reservas",
            {
                "Codigo": f"R-{cliente_id}-{fecha_inicio}",
                "FechaInicio": fecha_inicio,
                "FechaFin": fecha_fin,
                "Estado": "tentativa",
                "NumPersonas": num_personas,
                "nc_Cliente_id": cliente_id,
            },
        )


if __name__ == "__main__":
    # Prueba rápida de conexión: lista 3 registros de cada tabla.
    try:
        db = DBClient()
        for t in db.tables:
            n = len(db.list_records(t, params={"limit": 3}))
            print(f"{t}: {n} registro(s) (limit 3)")
    except Exception as exc:  # noqa: BLE001
        print("Error de conexión:", exc, file=sys.stderr)
        raise SystemExit(1)

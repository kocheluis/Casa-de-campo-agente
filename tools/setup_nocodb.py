"""Crea automáticamente en NocoDB la base + las 4 tablas del proyecto + relaciones + API token.

Es idempotente para la base (si existe, la reusa). Diseñado para correr una vez en local
y otra vez en el VPS (cambiando `NOCODB_BASE_URL`). El esquema viene de docs/modelo-datos.md.

Uso:
    python tools/setup_nocodb.py
    # Variables opcionales: NOCODB_BASE_URL, NOCODB_EMAIL, NOCODB_PASSWORD
"""
from __future__ import annotations

import os
import sys

import requests

BASE_URL = os.getenv("NOCODB_BASE_URL", "http://localhost:8080")
EMAIL = os.getenv("NOCODB_EMAIL", "admin@casadecampo.local")
PASSWORD = os.getenv("NOCODB_PASSWORD", "CasaDeCampo2026!")
BASE_NAME = "Casa de Campo"
TIMEOUT = 20


def _req(method: str, path: str, headers: dict | None = None, json: dict | None = None) -> requests.Response:
    return requests.request(method, BASE_URL + path, headers=headers, json=json, timeout=TIMEOUT)


def authenticate() -> str:
    """Crea super-admin si no existe, o inicia sesión. Devuelve el JWT."""
    h = {"Content-Type": "application/json"}
    r = _req("POST", "/api/v1/auth/user/signup", h, {"email": EMAIL, "password": PASSWORD})
    if r.status_code in (200, 201):
        print(f"[OK] Super admin creado: {EMAIL}")
        return r.json()["token"]
    r2 = _req("POST", "/api/v1/auth/user/signin", h, {"email": EMAIL, "password": PASSWORD})
    if r2.status_code == 200:
        print(f"[OK] Sign-in con usuario existente: {EMAIL}")
        return r2.json()["token"]
    print(f"[ERR] No se pudo autenticar.\n  signup -> {r.status_code} {r.text[:300]}\n  signin -> {r2.status_code} {r2.text[:300]}")
    sys.exit(1)


def get_or_create_base(hdr: dict) -> str:
    r = _req("GET", "/api/v2/meta/bases/", hdr)
    if r.status_code == 200:
        for b in r.json().get("list", []):
            if b.get("title") == BASE_NAME:
                print(f"[=] Base ya existe: {b['id']}")
                return b["id"]
    r = _req("POST", "/api/v2/meta/bases", hdr, {"title": BASE_NAME})
    if r.status_code not in (200, 201):
        print(f"[ERR] Crear base: {r.status_code} {r.text[:300]}")
        sys.exit(1)
    print(f"[OK] Base creada: {r.json().get('id')}")
    return r.json()["id"]


# Esquema (debe coincidir con docs/modelo-datos.md). El primer campo de texto será el
# "primary value" de cada tabla (lo que se ve en las relaciones).
TABLES: list[tuple[str, list[dict]]] = [
    ("Clientes", [
        {"title": "Nombre", "uidt": "SingleLineText", "pv": True},
        {"title": "Telefono", "uidt": "PhoneNumber"},
        {"title": "Canal", "uidt": "SingleSelect", "dtxp": "'whatsapp','instagram','facebook','otro'"},
        {"title": "Email", "uidt": "Email"},
        {"title": "Etiquetas", "uidt": "MultiSelect", "dtxp": "'interesado','cliente','VIP'"},
        {"title": "Notas", "uidt": "LongText"},
        {"title": "FechaRegistro", "uidt": "CreatedTime"},
    ]),
    ("Reservas", [
        {"title": "Codigo", "uidt": "SingleLineText", "pv": True},
        {"title": "FechaInicio", "uidt": "Date"},
        {"title": "FechaFin", "uidt": "Date"},
        {"title": "Estado", "uidt": "SingleSelect", "dtxp": "'tentativa','confirmada','cancelada','completada'"},
        {"title": "NumPersonas", "uidt": "Number"},
        {"title": "MontoTotal", "uidt": "Currency"},
        {"title": "Adelanto", "uidt": "Currency"},
        {"title": "Notas", "uidt": "LongText"},
        {"title": "FechaCreacion", "uidt": "CreatedTime"},
    ]),
    ("Inventario", [
        {"title": "Item", "uidt": "SingleLineText", "pv": True},
        {"title": "Categoria", "uidt": "SingleSelect", "dtxp": "'cocina','dormitorio','baño','exterior','limpieza','otro'"},
        {"title": "Cantidad", "uidt": "Number"},
        {"title": "Estado", "uidt": "SingleSelect", "dtxp": "'ok','faltante','averiado'"},
        {"title": "Ubicacion", "uidt": "SingleLineText"},
        {"title": "Foto", "uidt": "Attachment"},
        {"title": "UltimaRevision", "uidt": "LastModifiedTime"},
        {"title": "Notas", "uidt": "LongText"},
    ]),
    ("Conversaciones", [
        {"title": "Resumen", "uidt": "SingleLineText", "pv": True},
        {"title": "Canal", "uidt": "SingleSelect", "dtxp": "'whatsapp','instagram','facebook'"},
        {"title": "Mensaje", "uidt": "LongText"},
        {"title": "Respuesta", "uidt": "LongText"},
        {"title": "RequiereHumano", "uidt": "Checkbox"},
        {"title": "FechaHora", "uidt": "CreatedTime"},
    ]),
]


def create_tables(hdr: dict, base_id: str) -> dict[str, str]:
    """Crea las tablas. Devuelve {nombre: tableId}."""
    ids: dict[str, str] = {}
    for name, cols in TABLES:
        body = {"title": name, "table_name": name.lower(), "columns": cols}
        r = _req("POST", f"/api/v2/meta/bases/{base_id}/tables", hdr, body)
        if r.status_code in (200, 201):
            tid = r.json().get("id")
            ids[name] = tid
            print(f"[OK] Tabla: {name} -> {tid}")
        else:
            print(f"[ERR] Tabla {name}: {r.status_code} {r.text[:300]}")
    return ids


def create_relations(hdr: dict, ids: dict[str, str]) -> None:
    """Crea las relaciones N:1 (belongs-to) en las tablas hijas.

    En Reservas y Conversaciones aparece un campo 'Cliente' que apunta a un registro
    de Clientes. NocoDB crea automáticamente el campo inverso en Clientes.
    """
    relations = [
        # (tabla hija, tabla padre, nombre del campo en la hija)
        ("Reservas", "Clientes", "Cliente"),
        ("Conversaciones", "Clientes", "Cliente"),
    ]
    for child, parent, field_name in relations:
        if child not in ids or parent not in ids:
            print(f"[skip] Relación {child}->{parent}: falta alguna tabla.")
            continue
        body = {
            "uidt": "LinkToAnotherRecord",
            "title": field_name,
            "type": "bt",  # belongs-to
            "parentId": ids[parent],
            "childId": ids[child],
        }
        r = _req("POST", f"/api/v2/meta/tables/{ids[child]}/columns", hdr, body)
        if r.status_code in (200, 201):
            print(f"[OK] Relación {child}.{field_name} -> {parent} (N:1)")
        else:
            print(f"[!] Relación {child}->{parent}: {r.status_code} {r.text[:200]}")


def create_api_token(hdr: dict) -> str | None:
    """Intenta crear un API token (los endpoints han cambiado entre versiones)."""
    for path, body in [
        ("/api/v1/tokens", {"description": "WAT proyecto local"}),
        ("/api/v1/db/meta/api-tokens", {"description": "WAT proyecto local"}),
    ]:
        r = _req("POST", path, hdr, body)
        if r.status_code in (200, 201):
            data = r.json()
            token = data.get("token") or data.get("apiToken")
            if token:
                print(f"[OK] API token creado vía {path}")
                return token
    print("[!] No pude crear el API token vía API. Créalo en la UI: avatar -> Account Settings -> Tokens -> +.")
    return None


def main() -> None:
    print(f"NocoDB en {BASE_URL}\n")
    jwt = authenticate()
    hdr = {"xc-auth": jwt, "Content-Type": "application/json"}
    base_id = get_or_create_base(hdr)
    table_ids = create_tables(hdr, base_id)
    create_relations(hdr, table_ids)
    api_token = create_api_token(hdr)

    print("\n=======================================")
    print("RESUMEN — guarda estos datos:")
    print("=======================================")
    print(f"URL:        {BASE_URL}")
    print(f"Email:      {EMAIL}")
    print(f"Password:   {PASSWORD}")
    print(f"Base ID:    {base_id}")
    print("Table IDs:")
    for n, i in table_ids.items():
        print(f"  {n:16s} {i}")
    if api_token:
        print(f"\nAPI Token (para DB_API_TOKEN en .env):\n{api_token}")
    print("=======================================")


if __name__ == "__main__":
    sys.exit(main())

# Errores resueltos — checklist a revisar antes de cambios de código

> **Cómo se usa:**
> 1. **Antes** de modificar código relacionado con alguno de estos componentes, escanea
>    los errores correspondientes para no volver a pisar la misma piedra.
> 2. **Cada vez** que se resuelva un nuevo error, **agregar entrada** al final con la
>    misma plantilla. No se borran entradas: aprenden con el tiempo.
> 3. Formato compacto: síntoma → causa → fix → check preventivo → archivos afectados.

## Componentes afectados (índice rápido)

| Componente | IDs de errores |
|---|---|
| NocoDB / setup_nocodb.py | E-001, E-002, E-007 |
| Docker / WSL en Windows | E-005 |
| Bash tool / commits | E-004 |
| Consola Windows (encoding) | E-003 |
| LLM (LiteLLM, providers) | E-006, E-008 |

---

## E-001 — NocoDB: signup no promueve a super admin
- **Fecha:** 2026-05-28
- **Síntoma:** `403 ERR_FORBIDDEN — You do not have permission to perform the action
  "baseCreate" with the roles: No Access` al crear una base por API después de hacer
  signup del primer usuario.
- **Causa raíz:** En versiones recientes de NocoDB, el signup del primer usuario crea un
  rol `org-level-viewer` (solo lectura). No auto-promueve a super admin.
- **Fix:** Agregar variables `NC_ADMIN_EMAIL` y `NC_ADMIN_PASSWORD` al servicio `nocodb`
  del `docker-compose.yml`. Al arrancar, NocoDB promueve a ese email a `super: true,
  org-level-creator: true`. Recrear el contenedor para que tome las vars.
- **Check preventivo:** Antes de tocar el setup de NocoDB, verificar que `NC_ADMIN_EMAIL`
  y `NC_ADMIN_PASSWORD` estén en `deploy/docker-compose.yml` (servicio `nocodb`) y en
  `deploy/.env`.
- **Archivos:** `deploy/docker-compose.yml`, `deploy/.env`, `tools/setup_nocodb.py`.

## E-002 — NocoDB: relación N:1 duplicada al crear la segunda
- **Fecha:** 2026-05-28
- **Síntoma:** `422 ERR_DUPLICATE_IN_ALIAS — Duplicate column alias 'Cliente'` al crear
  la segunda relación con el mismo nombre.
- **Causa raíz:** El script creaba la relación con `type: "hm"` POSTeando a la tabla
  **padre** (Clientes). NocoDB hacía la columna "Cliente" en la propia tabla padre, así
  que al intentar la segunda con el mismo nombre, colisionaba.
- **Fix:** Cambiar a `type: "bt"` (belongs-to) POSTeando a la tabla **hija**
  (Reservas/Conversaciones). El campo "Cliente" queda donde debe (en la hija) y NocoDB
  crea el inverso automáticamente en la padre.
- **Check preventivo:** Para relaciones N:1, **siempre** POST a la tabla hija con
  `type: "bt"`. Para N:M, POST a cualquiera con `type: "mm"`.
- **Archivos:** `tools/setup_nocodb.py` función `create_relations`.

## E-003 — Consola Windows muestra mojibake en caracteres especiales
- **Fecha:** 2026-05-25
- **Síntoma:** En la consola se ven `Fase 0 �` o `reserv�` en lugar de `Fase 0 —` o
  `reservó`.
- **Causa raíz:** La consola de Windows usa cp1252 por defecto, no UTF-8. Python escribe
  bytes UTF-8 y la consola los interpreta mal.
- **Fix (no bloqueante):** Los archivos están bien grabados en UTF-8 — solo afecta la
  visualización. Para evitarlo al imprimir, se puede configurar `PYTHONIOENCODING=utf-8`
  o llamar a `chcp 65001` en la consola antes de correr scripts. En producción (Linux)
  no aparece.
- **Check preventivo:** No considerar este error como bug funcional. Si una salida en
  consola se ve mal, verificar con `cat` o leyendo el archivo.
- **Archivos:** todos los scripts en `tools/`.

## E-004 — Commit con `@` espurio al inicio del subject
- **Fecha:** 2026-05-25
- **Síntoma:** El commit subject quedó `@ Estructura inicial WAT...` con un `@` inicial.
- **Causa raíz:** Usé sintaxis de here-string PowerShell (`@'...'@`) dentro de la
  herramienta Bash, que corre `bash` no `pwsh`. Bash interpretó `@` como literal y `'...`
  como single-quoted string, dejando el `@` como parte del mensaje.
- **Fix:** `git commit --amend -m "subject" -m "body" -m "Co-Authored-By: ..."` con
  múltiples `-m` (más portable y robusto).
- **Check preventivo:** En la herramienta **Bash**: usar `-m` múltiples o here-doc bash
  (`<<'EOF' ... EOF`). En la herramienta **PowerShell**: aquí sí va `@'...'@`. No mezclar.
- **Archivos:** N/A (instrucción de uso de herramientas).

## E-005 — Docker Desktop "Virtualization not detected" pese a BIOS OK
- **Fecha:** 2026-05-26
- **Síntoma:** Docker Desktop no arranca y muestra el error de virtualización aunque
  Task Manager / `Get-CimInstance Win32_Processor` indica `VirtualizationFirmwareEnabled
  = True`.
- **Causa raíz:** Las features de Windows **Virtual Machine Platform** y **WSL** no
  estaban habilitadas. Docker Desktop con backend WSL2 las necesita.
- **Fix:** En PowerShell **como administrador**:
  `wsl --install --no-distribution` → reiniciar Windows → abrir Docker Desktop.
- **Check preventivo:** Antes de pedir al usuario instalar Docker Desktop, recordarle
  que se haga `wsl --install --no-distribution` primero (si no tiene WSL2). Hacer
  primero la diagnostica con `wsl --status` y `Get-CimInstance Win32_Processor`.
- **Archivos:** `docs/fase-0-cimientos.md` (sumar nota).

## E-006 — Gemini 503 (Service Unavailable) transitorio
- **Fecha:** 2026-05-29
- **Síntoma:** `litellm.ServiceUnavailableError: GeminiException — 503 UNAVAILABLE — This
  model is currently experiencing high demand`.
- **Causa raíz:** Picos de demanda en `gemini-2.5-flash` del lado de Google. No es
  problema del código.
- **Fix temporal:** Reintentar el mismo prompt.
- **Fix definitivo (pendiente para producción):** Implementar retry con backoff
  exponencial en `tools/ai_reply.py` y en el workflow n8n. LiteLLM ya tiene
  `litellm.completion(..., num_retries=3)` — usarlo.
- **Check preventivo:** Antes de prometer "estabilidad" de un proveedor LLM, recordar
  que cualquier proveedor puede tirar 5xx puntualmente. Diseñar siempre con retry.
- **Archivos:** `tools/ai_reply.py`, `deploy/n8n-workflows/responder_mensajes.json`.

## E-007 — NocoDB: campo link en records via API requiere `nc_<Field>_id`
- **Fecha:** 2026-05-28
- **Síntoma:** Al crear un registro vía API enviando `{"Cliente": 1, ...}` para enlazar
  al cliente con Id=1, el enlace **no se aplica**.
- **Causa raíz:** En NocoDB v2, los campos `LinkToAnotherRecord` se setean con la
  convención `nc_<NombreCampo>_id` en el body del POST, no con el nombre visible.
- **Fix:** Usar `{"nc_Cliente_id": 1, ...}` en `db_client.py`.
- **Check preventivo:** Antes de escribir un campo link en NocoDB vía API, recordar la
  convención `nc_<Field>_id`. Si no, fallará en silencio (el registro se crea, pero
  sin el link).
- **Archivos:** `tools/db_client.py` (helpers `log_conversation`, `create_tentative_reservation`).

## E-008 — LiteLLM warnings de botocore al importar
- **Fecha:** 2026-05-29
- **Síntoma:** `litellm: could not pre-load bedrock-runtime response stream shape ...
  Error: No module named 'botocore'`.
- **Causa raíz:** LiteLLM intenta pre-cargar AWS Bedrock/SageMaker pero `botocore` no
  está instalado (no es dependencia del core de LiteLLM).
- **Fix (no aplicable):** Advertencia inofensiva, no usamos AWS. Se puede silenciar con
  `2>&1 | grep -v "LiteLLM:WARNING\|common_utils"` si molesta.
- **Check preventivo:** N/A.
- **Archivos:** N/A.

---

## Plantilla para nuevas entradas

```
## E-XXX — Título corto descriptivo
- **Fecha:** YYYY-MM-DD
- **Síntoma:** (lo que se ve cuando falla, copy/paste del error si aplica)
- **Causa raíz:** (la explicación de por qué pasa)
- **Fix:** (qué cambio resolvió el problema)
- **Check preventivo:** (qué revisar antes de un cambio futuro para no repetirlo)
- **Archivos:** (rutas afectadas)
```

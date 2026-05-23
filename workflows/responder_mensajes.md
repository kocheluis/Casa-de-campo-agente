# Workflow: responder_mensajes

## Objetivo
Responder automáticamente los mensajes iniciales de clientes (WhatsApp, Instagram DM,
Messenger) como si fuera el dueño de la casa de campo, capturar el lead en la base de
datos y escalar al dueño cuando haga falta (reserva en firme, pago, queja o algo fuera
de la base de conocimiento). Es la Fase 1 del proyecto.

## Inputs
- `telefono` / `recipient_id` — identificador del cliente que llega en el webhook de Meta.
- `canal` — whatsapp | instagram | messenger.
- `mensaje` — texto del cliente.
- `history` — turnos previos de la conversación (opcional).
- Credenciales en `.env`: `ANTHROPIC_API_KEY`, `META_ACCESS_TOKEN`,
  `META_PHONE_NUMBER_ID`, `DB_API_URL`, `DB_API_TOKEN`, `OWNER_WHATSAPP`.
- Base de conocimiento completa en `knowledge/casa_de_campo.md`.

## Tools
1. `tools/db_client.py` — `find_or_create_client(...)` captura/recupera el lead.
2. `tools/claude_reply.py` — `generate_reply(mensaje, history)` produce la respuesta y
   la bandera `handoff`.
3. `tools/meta_send.py` — `send_whatsapp(...)` / `send_messenger(...)` responde por el
   mismo canal; `notify_owner(...)` avisa al dueño en caso de handoff.
4. `tools/db_client.py` — `log_conversation(...)` y, si aplica,
   `create_tentative_reservation(...)`.

## Steps
1. Recibir el evento del webhook de Meta (vía n8n en producción) con canal, identificador
   y mensaje del cliente.
2. `find_or_create_client` → registrar/recuperar el cliente en la tabla `Clientes`.
3. `generate_reply(mensaje, history)` → obtener `reply` y `handoff`.
4. Enviar `reply` por el canal correspondiente (`send_whatsapp` o `send_messenger`).
5. Si `handoff` es verdadero → `notify_owner` con un resumen y marcar la conversación.
6. Si el cliente pidió fechas concretas → `create_tentative_reservation` (estado tentativa).
7. `log_conversation` → guardar mensaje, respuesta y si requirió intervención humana.

## Arquitectura en producción
- En producción, **n8n** (en el VPS) escucha el webhook de Meta 24/7 y ejecuta estos
  pasos llamando a los tools. Este workflow documenta la lógica; n8n la orquesta.
- La base de datos (NocoDB/Baserow) y n8n viven en el mismo VPS.

## Output
- Mensaje enviado al cliente por su canal.
- Lead registrado/actualizado en `Clientes`.
- Turno guardado en `Conversaciones` (con bandera de handoff).
- Si aplica, reserva tentativa en `Reservas` y aviso al dueño.

## Edge cases & lecciones aprendidas
- **Ventana de 24h de WhatsApp**: fuera de ese plazo solo se pueden enviar plantillas
  aprobadas, no texto libre. Relevante para campañas y respuestas tardías.
- **No inventar**: si la base de conocimiento no cubre la pregunta, el agente debe
  escalar en vez de adivinar (ya está instruido en el system prompt).
- **TikTok**: no tiene API oficial de DMs; esos mensajes se atienden manualmente o se
  redirige al cliente a WhatsApp.
- **Costos**: usar el modelo Haiku + caché de prompt mantiene barata cada respuesta.
- **Pruebas**: `python tools/claude_reply.py "mensaje"` permite probar el cerebro sin
  depender de Meta ni de la base de datos.

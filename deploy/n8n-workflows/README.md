# Workflows de n8n

Plantillas listas para importar en n8n. Cuando lo importes, hay que reemplazar 3
placeholders con valores reales (búscalos como "REEMPLAZAR_..." en el JSON).

## `responder_mensajes.json` — chatbot Chatwoot → Claude → Chatwoot + log NocoDB

### Qué hace
1. **Webhook** recibe el evento de Chatwoot cuando llega un mensaje del cliente.
2. **Filtra** solo `message_created` entrantes (ignora notas privadas y respuestas del dueño).
3. **Extrae** mensaje, teléfono, nombre, `conversation_id` y `account_id`.
4. **Llama a Claude** (Messages API, modelo Haiku) con el system prompt de la casa.
5. **Devuelve la respuesta a Chatwoot** (el cliente la recibe por WhatsApp/IG/FB).
6. **Guarda** el turno (mensaje + respuesta) en la tabla `Conversaciones` de NocoDB.

### Importar en n8n
1. En n8n abre `Workflows` → ⋯ → **Import from File** → elige `responder_mensajes.json`.
2. Pasa por cada nodo con borde rojo y rellena los **placeholders**:
   - **Llamar a Claude** → header `x-api-key`: tu `ANTHROPIC_API_KEY`.
   - **Responder en Chatwoot** → header `api_access_token`: el access token de tu
     usuario admin en Chatwoot (perfil → *Profile Settings* → *Access Token*).
   - **Guardar en NocoDB** → URL (reemplaza `REEMPLAZAR_TABLE_ID_CONVERSACIONES` por
     el id de la tabla Conversaciones, que aparece en `.env` como `TABLE_ID_CONVERSACIONES`)
     y header `xc-token` con el `DB_API_TOKEN`.
3. Pulsa **Activate** arriba a la derecha.
4. Copia la **Production URL** del webhook (en el nodo *Webhook Chatwoot*).

### Conectar Chatwoot al webhook
En Chatwoot: *Settings → Integrations → Webhooks → Add new webhook* → pega la URL del
paso 4. Marca el evento `message_created`. Guarda.

### Probar sin Meta (local)
Como aún no hay WhatsApp real, puedes simular un mensaje entrante con `curl`:
```bash
curl -X POST http://localhost:5678/webhook/chatwoot-responder \
  -H "Content-Type: application/json" \
  -d '{
    "event": "message_created",
    "message_type": "incoming",
    "content": "Hola, esta libre el finde para 4 personas?",
    "sender": {"name": "Ana", "phone_number": "51999000111", "identifier": "ana"},
    "conversation": {"id": 1, "channel": "Channel::Api"},
    "account": {"id": 1}
  }'
```
Verás en NocoDB que aparece una fila en `Conversaciones` con el mensaje y la respuesta.

### Limitaciones de esta versión (MVP)
Falta por agregar (iterable en n8n con clics; el plan ya lo contempla):
- **Captura de lead** automática en la tabla `Clientes` (find_or_create por teléfono).
- **Detección de handoff** parseando la línea `HANDOFF: yes/no` del modelo y
  notificando al dueño.
- **Pre-reserva** cuando el cliente proponga fechas concretas.

La versión Python (`tools/claude_reply.py`, `tools/db_client.py`) ya tiene toda esa
lógica; lo replicaremos en n8n una vez validado el flujo básico.

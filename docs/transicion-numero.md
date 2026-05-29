# Transición del número de Gerardo a la API de Meta

> **Decisión tomada:** el **número actual** de Gerardo se queda para el **negocio** (Cloud
> API). Conserva la continuidad con clientes históricos. Gerardo saca un **chip nuevo
> para su vida personal**. Durante los primeros meses, el número del negocio recibirá
> mensajes personales (familia, amigos) — el bot tiene que manejarlos con elegancia.

## Riesgos del periodo de transición y cómo mitigarlos

| Riesgo | Mitigación |
|---|---|
| Familia escribe pensando que es Gerardo y el bot intenta venderles la casa | El bot detecta mensajes no relacionados y **escala a Gerardo (handoff)** sin dar precios ni el nuevo número personal |
| El bot revela el nuevo número personal de Gerardo | **Nunca** está en la base de conocimiento → no lo puede compartir |
| Pérdida de mensajes importantes durante el corte | Chatwoot guarda **todo** el historial; Gerardo puede revisar y responder cuando pueda |
| Confusión en el quality rating de Meta si la familia bloquea/reporta | Avisar a la familia con anticipación reduce esto a casi cero |

---

## Plan de transición — calendario sugerido

| Cuándo | Qué hacer | Quién |
|---|---|---|
| **T-14 días** (2 semanas antes de activar la API) | Gerardo **compra el chip nuevo** y lo activa en su WhatsApp personal | Gerardo |
| **T-7 días** | Gerardo manda **mensaje 1** (broadcast) a familia y amigos avisando el cambio | Gerardo |
| **T-3 días** | Gerardo manda **mensaje individual** a los 5-10 contactos más cercanos (Mensaje 2) | Gerardo |
| **T-1 día** | Gerardo manda **recordatorio** (Mensaje 3) | Gerardo |
| **Día 0** | Migración: borra WhatsApp del número del negocio, lo registramos en Meta Cloud API, activamos el bot | Tú |
| **T+1 a T+90 días** | Cualquier mensaje personal que llegue al número del negocio → el bot lo deriva amablemente; Gerardo responde desde su nuevo número personal | Bot + Gerardo |
| **T+90 días** | Revisar logs: ¿siguen llegando muchos personales? Si sí, segunda ronda de aviso | Tú |

---

## Mensajes listos para copiar y pegar

### 📨 Mensaje 1 — Broadcast a todos los contactos (T-7 días)

> ¡Hola! 👋 Quería avisarte de un cambio importante:
>
> Desde el **[FECHA]**, este número (📱 [número actual]) **será exclusivo del negocio**
> *Casa de Campo El Mirador* — voy a tener un equipo y un sistema atendiendo, así que
> los mensajes que lleguen aquí serán de clientes.
>
> Mi **nuevo número personal** es 👉 **[número nuevo]** — guárdalo, y para cualquier cosa
> personal escríbeme a ese 😊
>
> ¡Mil gracias!
> — Gerardo

### 📨 Mensaje 2 — Individual a familia/amigos cercanos (T-3 días)

> Mami / [Nombre], te recuerdo que mi número personal cambia 💛
>
> Apunta este nuevo: **[número nuevo]** — guárdalo como "Gerardo" y bórrame del viejo
> (📱 [número actual]) que se queda para el negocio.
>
> ¡Cualquier cosa por el nuevo!

### 📨 Mensaje 3 — Recordatorio final (T-1 día)

> ¡Hola! 👋 Mañana hago el cambio.
>
> Recuerda guardar mi nuevo número personal: **[número nuevo]** 📱
>
> Este número se queda para el negocio desde mañana. ¡Gracias!

### 📨 Estado de WhatsApp durante la transición

Configurar como **estado** en WhatsApp Business del número del negocio durante el primer mes:

> 🏡 Casa de Campo El Mirador · Reservas y consultas
> *Si buscas a Gerardo en lo personal, su nuevo número es **[número nuevo]***

(Esto es seguro porque el estado solo lo ven los contactos guardados de él.)

---

## Cómo el bot va a manejar los mensajes personales

He ajustado las **reglas del agente** en la base de conocimiento para que:

1. Si el mensaje **no es sobre la casa de campo** (saludos personales, "¿cómo está
   mami?", chistes, fotos familiares, etc.) → el bot responde algo como:

   > ¡Hola! 😊 Mira, este número ahora es de la **Casa de Campo El Mirador**. Si estás
   > buscando a Gerardo en lo personal, escríbele a su nuevo número (él te lo pasó hace
   > poco). Cualquier consulta sobre la casa, ¡con todo gusto te ayudo! 🏡

2. **Marca handoff** automáticamente para que Gerardo lo vea en Chatwoot y pueda
   responder desde su nuevo número personal cuando pueda.

3. **No revela el nuevo número personal de Gerardo** — solo le dice "su nuevo número"
   sin darlo, porque puede ser un cliente confundido o, peor, alguien con malas
   intenciones.

---

## Checklist para Gerardo el día del cambio

- [ ] Chip nuevo activado en su teléfono (línea aparte) o segundo equipo
- [ ] Mensajes 1, 2 y 3 enviados a contactos personales
- [ ] WhatsApp del número del negocio: **eliminado de la app** (perderá los chats antiguos)
- [ ] Confirma a Tu/Tú que el número ya **no aparece** en su app
- [ ] Tú lo registras en Meta Cloud API y conectas al bot

> ⚠️ **Importante:** sin borrar el WhatsApp del número del negocio, la Cloud API
> **no lo deja registrar**. Es paso obligatorio.

---

## Indicadores de éxito (mes 1, 2, 3)

| Mes | Métrica | Bandera roja si... |
|---|---|---|
| Mes 1 | % de mensajes que requieren handoff por ser personales | > 30% |
| Mes 2 | Mismo | > 15% |
| Mes 3 | Mismo | > 5% |

Si la transición no se aplaca, lanzamos una **segunda ronda de aviso** con un mensaje
masivo desde Chatwoot o desde el WhatsApp personal nuevo de Gerardo.

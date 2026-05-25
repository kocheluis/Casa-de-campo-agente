# Conclusiones: investigación de la comunidad vs. plan actual

> Síntesis de las 3 investigaciones (orquestador/chatbot, base de datos, video/social)
> contrastadas con el plan aprobado. Investigación web de mayo 2026 con fuentes citadas
> en cada archivo de esta carpeta. Veredicto general: **el plan está validado en lo
> esencial; hay 4 ajustes concretos recomendados por la comunidad.**

## Veredicto por componente

| Componente | Plan actual | ¿Validado por la comunidad? | Ajuste recomendado |
|---|---|---|---|
| Orquestador | n8n autoalojado | ✅ Sí, es el pick por defecto self-hosted con IA | Mantener n8n |
| Mensajería | Meta Cloud/Graph API oficial | ✅ Sí, la decisión correcta (evita baneos) | Mantener; **NO** usar APIs no oficiales (WAHA) |
| IA | Claude (Haiku) | ✅ Sí, ideal para "responder como el dueño" a bajo costo | Mantener |
| **Bandeja/handoff** | n8n "puro" | ⚠️ Insuficiente | **AÑADIR Chatwoot** (bandeja omnicanal + handoff) |
| **Base de datos** | "NocoDB o Baserow" | ✅ Sí, autoalojar es válido | **Elegir NocoDB** (no Baserow) |
| Video | FFmpeg **o** API de plantillas | ✅ Sí | **Priorizar API de plantillas** (JSON2Video/Creatomate); FFmpeg solo puntual |
| Programador social | Metricool o Publer | ✅ Sí | **Publer (gratis)** principal + Metricool (gratis) para analítica |
| TikTok | Solo publicar, no DMs | ✅ Confirmado | Sigue siendo el cuello de botella (API tarda 2-6 semanas en aprobarse) |

## Los 4 ajustes recomendados

### 1. Añadir Chatwoot como bandeja omnicanal con handoff humano
La crítica más repetida: **n8n "puro" auto-responde pero NO es una bandeja**. El dueño no
tendría dónde ver WhatsApp + IG + FB juntos ni **retomar el control** cuando la IA no deba
responder (reservas en firme, quejas, pagos). El patrón open-source estándar es:
**Meta APIs → Chatwoot (bandeja) → n8n (lógica + Claude) → de vuelta a Chatwoot.**
Chatwoot es gratis (self-hosted) y su "AgentBot" puede delegar en Claude.
→ *Detalle y fuentes: [01-orquestador-y-chatbot.md](01-orquestador-y-chatbot.md)*

### 2. Elegir NocoDB (no Baserow) para la base de datos
Razón decisiva: en **Baserow autoalojado gratuito la vista Calendario es de PAGO**
(Premium); en **NocoDB el Calendario es gratis**. Como el calendario de reservas es el
requisito central, NocoDB gana. Además NocoDB tiene API REST con tokens en self-hosted y
mejor nodo en n8n (Baserow ha tenido carencias de tokens API en self-hosted).
→ *Detalle y fuentes: [02-base-de-datos.md](02-base-de-datos.md)*

### 3. Priorizar una API de plantillas de video sobre FFmpeg
Para uso diario de un dueño NO técnico, la comunidad desaconseja FFmpeg como herramienta
principal (es CLI: scripts y depuración). Mejor una **API de plantillas** orquestada por
n8n: **JSON2Video** (plan gratis más generoso, ~10 min, TTS incluido) o **Creatomate**
(editor visual más amigable, integración n8n nativa). FFmpeg queda como tool puntual y
barato dentro del workflow. *(Cortar reels de videos largos es OTRO problema → Vizard
free/OpusClip.)*
→ *Detalle y fuentes: [03-video-y-programador-social.md](03-video-y-programador-social.md)*

### 4. Publer (gratis) como programador principal
Ambas (Publer/Metricool) están validadas. Para **publicar** en TikTok+IG+FB, **Publer
free** es más práctico (3 cuentas, 10 en cola por cuenta). **Metricool free** topa en 20
posts/mes pero gana en analítica → usar las dos gratis en paralelo.

## Advertencias honestas de la comunidad (a tener en cuenta)

- **Chatwoot + n8n exigen más VPS.** Con Chatwoot (Rails + PostgreSQL + Redis + Sidekiq)
  sumado a n8n y NocoDB, apunta a un VPS de **≥4 GB RAM, idealmente 8 GB**. Sube el costo
  del VPS (ver presupuesto abajo).
- **NocoDB tiene críticas de fiabilidad** (Hacker News, feb 2025: bugs de borrado, sin
  undo). → Mitigación obligatoria: **backups automáticos de PostgreSQL** y operar vía
  vistas/formularios, no edición masiva de esquema.
- **Ni NocoDB ni Baserow tienen app móvil nativa.** En Android será **web/PWA**. Para
  "actualizar inventario desde el móvil" lo robusto es un **Formulario** de NocoDB (URL
  compartible), no editar la tabla en pantalla pequeña.
- **Ventana de 24h de WhatsApp:** fuera de ese plazo solo se puede iniciar con plantillas
  pre-aprobadas. Planificar 1-2 plantillas de utilidad y su aprobación.
- **Instagram/Messenger en n8n da fricción real** (mensajes que no se devuelven, tokens).
  Plan B: usar **ManyChat solo como pasarela de IG** apuntando al webhook de n8n.
- **TikTok es el cuello de botella:** la Content Posting API oficial tarda **2-6 semanas**
  en aprobarse y deja el contenido en modo privado hasta pasar auditoría. Refuerza la
  decisión de tratar TikTok como "publicar", no DMs.
- **Plan B documentado para la base de datos:** si el mantenimiento del VPS supera tu
  capacidad, **pagar Airtable (1-2 asientos) cabe en $70/mes** y elimina la carga
  operativa. Arrancar con NocoDB + buenos backups; Airtable como respaldo.

## Presupuesto revisado (~$70/mes) tras los ajustes

| Pieza | Costo/mes | Nota |
|---|---|---|
| VPS 8 GB (n8n + Chatwoot + NocoDB + Postgres/Redis + FFmpeg) | ~$15–25 | Sube por Chatwoot; antes se estimaba menos |
| Chatwoot + NocoDB (self-hosted) | $0 | Sobre el VPS |
| Claude API (Haiku + caché) | ~$8–12 | |
| WhatsApp (Meta) | ~$0–8 | Conversaciones de servicio entrantes gratis |
| Programador social (Publer/Metricool free) | $0 | |
| Video por plantillas | $0 al inicio / ~$49 al escalar | JSON2Video o Creatomate |
| **Total arrancando (video en free)** | **≈ $25–45/mes** | Holgado dentro de $70 |
| **Total con video de pago** | **≈ $70–90/mes** | ⚠️ Roza/supera el techo |

**Tensión real de presupuesto:** con Chatwoot, el VPS sube; y una API de video de pago
(~$49) puede empujar el total por encima de $70. **Recomendación: faseado.** Fase 1
(chatbot + Chatwoot + NocoDB) entra cómoda en $70. La API de video se arranca en plan
GRATIS y solo se paga cuando el volumen lo exija — y entonces se decide entre subir un
poco el techo o ajustar el VPS. **No pagar video + clips + programador a la vez.**

## Qué NO cambiar
- No migrar a una plataforma dedicada (ManyChat/Botpress/Voiceflow) como núcleo: para
  "responder como el dueño" con tono propio y datos propios, n8n + Claude es superior y
  más barato a largo plazo.
- No usar APIs no oficiales de WhatsApp (WAHA): riesgo real de baneo del número.
- No usar FFmpeg como editor de plantillas para el dueño (sí como tool interno).

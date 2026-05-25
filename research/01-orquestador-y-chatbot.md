# Investigación: Orquestador y chatbot multicanal

> Investigación web realizada en mayo 2026, contrastando recomendaciones de la comunidad (Reddit, Hacker News, foros de n8n/Chatwoot, blogs comparativos 2025-2026) para construir un **agente de respuesta automática multicanal** (WhatsApp + Instagram DM + Facebook Messenger) respondido por IA, para un negocio pequeño de alquiler de casa de campo. Presupuesto ~$70/mes.

## Resumen ejecutivo

La comunidad valida en gran medida el plan: **n8n autoalojado + Meta Cloud/Graph API oficial + Claude** es la combinación más recomendada en 2025-2026 para quien tiene algo de perfil técnico y quiere control, sin costos por operación. La crítica más fuerte y repetida es que **n8n "puro" no es una bandeja de entrada**: para unificar los tres canales con historial de conversación y, sobre todo, **handoff humano** (que el dueño retome la charla cuando la IA no debe responder), la comunidad recomienda casi unánimemente **añadir Chatwoot (open source) como capa de bandeja omnicanal**, con n8n haciendo solo la lógica/IA. Sobre mensajería, la recomendación dominante es usar la **API oficial de Meta** (Cloud API) y evitar APIs no oficiales (riesgo de baneo); muchos negocios pequeños usan un BSP como **360dialog** por la facilidad de alta y el "zero markup", pero el acceso directo a Meta Cloud API que ya tienes planeado es perfectamente válido y más barato. Finalmente, frente a plataformas dedicadas (ManyChat, Botpress, Voiceflow), la comunidad coincide en que para un caso pequeño y muy personalizado (responder "como el dueño") **n8n + Claude da más control y mejor relación costo a largo plazo**, mientras que ManyChat gana en rapidez de arranque pero encarece y limita al crecer.

## Comparativa

### Orquestadores

| Herramienta | Qué dice la comunidad | Pros | Contras | Costo |
|---|---|---|---|---|
| **n8n (self-hosted)** | La opción "por defecto" para self-hosted con IA; el que los power users "realmente mantienen". 181k+ estrellas GitHub, foro enorme, miles de plantillas | Control total, nodos de IA y "AI Agent", ejecuciones ilimitadas, sin costo por operación, integra Claude/WhatsApp/Meta nativamente | Curva de aprendizaje, requiere mantener el VPS (updates, backups), ~1900 integraciones (menos que Zapier); licencia "Sustainable Use" restringe revender como SaaS | Gratis (Community Edition). VPS ~$5-10/mes |
| **Activepieces (self-hosted)** | El alternativo open source que más creció en 2025-2026; "AI-first" y más fácil. Licencia MIT (más permisiva que n8n) | UX más limpia, pasos de IA nativos, soporte MCP (280+ servidores), arranque más rápido (9.1 vs 7.7 en facilidad) | Comunidad y ecosistema más pequeños (~14-15k estrellas), menos maduro y menos estable a escala que n8n, menos plantillas | Gratis (self-host). VPS similar |
| **Make.com** | Bueno y visual, pero **solo nube**: descartado si self-hosting es requisito | Editor visual potente, muchas apps | No se puede autoalojar (incompatible con tu enfoque/VPS); costo por operación que escala | De pago por operaciones |
| **Zapier** | Considerado caro y no self-hostable para este caso | Máximas integraciones (5000+), muy fácil | Caro a escala ($600+/mes en casos altos), sin self-host, menos control de IA | Caro |

### Bandeja / capa de unificación

| Herramienta | Qué dice la comunidad | Pros | Contras | Costo |
|---|---|---|---|---|
| **Chatwoot (open source)** | Recomendado como la "interfaz humana" del stack open source (WhatsApp + IG + FB + email en una sola bandeja). Patrón típico: Chatwoot (bandeja) + n8n (lógica/IA) | Bandeja omnicanal real, historial, asignación de agentes, handoff humano, notas internas, AgentBot que puede llamar a IA (OpenAI/Claude/Gemini), nodo comunitario para n8n | Autoalojarlo pide DevOps (Docker, PostgreSQL, Redis); no es "plug and play"; consume RAM (suma carga al VPS) | Gratis (self-host, MIT). Cloud de pago |
| **Typebot** | Útil para flujos guiados tipo formulario/quiz, no como bandeja omnicanal ni handoff | Builder visual de conversaciones, self-host | No resuelve bandeja unificada ni handoff multicanal; rol distinto | Gratis (self-host) |
| **n8n "puro" (sin bandeja)** | Funciona para auto-responder, pero la comunidad advierte que no hay UI para que el humano vea/retome conversaciones | Más simple, menos servicios que mantener | Sin bandeja ni handoff nativo; el dueño no tiene dónde "ver" todo y tomar el control | — |

### Mensajería

| Vía | Qué dice la comunidad | Pros | Contras | Costo |
|---|---|---|---|---|
| **Meta Cloud API (oficial, directa)** | Lo correcto/seguro; la comunidad insiste en usar la API oficial y no las no oficiales | Sin intermediario, más barato, conversaciones de servicio (entrantes) gratis desde nov-2024 | Tú montas toda la infra (lo cual ya tienes resuelto con n8n); verificación de negocio con Meta; ventana 24h y plantillas para iniciar fuera de ella | Solo costos de Meta por plantillas (servicio gratis) |
| **360dialog (BSP)** | Favorito de SMEs por costo: suscripción + mensajes de Meta a "zero markup" | Alta más fácil, sin recargo por mensaje | Cuota fija mensual extra; intermediario | Suscripción + tarifas Meta |
| **Twilio** | Potente pero caro para negocio pequeño | Escalable, multicanal | Costos altos, complejidad | Pago por uso, alto |
| **Wati / ManyChat (BSP no-code)** | Fáciles para no técnicos | Sin código, rápido | Recargos, menos control, te atan a su plataforma | Suscripción + recargos |
| **WAHA / APIs no oficiales (WhatsApp Web)** | Usado en stacks open source baratos, pero **viola los TOS de WhatsApp** | Sin verificación de Meta, gratis | **Riesgo real de baneo del número**, sobre todo en envíos salientes/masivos | Gratis (riesgoso) |

### Chatbot dedicado vs n8n+Claude

| Plataforma | Qué dice la comunidad | Pros | Contras | Costo |
|---|---|---|---|---|
| **n8n + Claude** | Preferido para casos personalizados y control de costos | Respuestas a medida ("como el dueño"), elige modelo (Haiku barato), sin atadura, datos propios | Más trabajo de armado y mantenimiento | API de Claude por uso + VPS |
| **ManyChat** | El más usado para IG/FB/WhatsApp no-code, pero criticado por precios | Multicanal amplio, rápido de lanzar, visual | **Recorte del free a 25 contactos (marzo 2026)**, precio sube con contactos, add-on de IA $29/mes, soporte lento (3-5 días), recargos de WhatsApp | Pro desde $15/mes + IA $29 + recargos |
| **Botpress** | Bueno para bots de IA personalizables multicanal | Muchos canales, features de IA, live chat integrado | Más orientado a soporte/escala; otra plataforma que aprender | Free 500 msg/mes, luego de pago |
| **Voiceflow** | Bueno para web/telefonía; permite elegir LLM (incluido Claude) | Multi-LLM, fácil de diseñar flujos | Menos enfocado a la bandeja WhatsApp/IG/FB de un negocio chico | De pago |

## Hallazgos por tema

### 1. Orquestador: n8n vs Make vs Activepieces vs Zapier

- **n8n es el pick por defecto para self-hosted con IA.** Reviews 2026 lo describen como "el de automatización que los power users realmente mantienen" y destacan que el self-host es gratis con ejecuciones ilimitadas, con ahorro fuerte frente a Zapier (caso de ~150k ejecuciones/mes a ~$50 de VPS vs $600+ en Zapier). Fuente: [upskillist.com n8n review 2026](https://www.upskillist.com/blog/n8n-review/), [syncgtm.com n8n review 2026](https://syncgtm.com/blog/n8n-review), [infralovers.com 2025](https://www.infralovers.com/blog/2025-05-09-n8n-workflow-automation/).
- **Crítica honesta a n8n:** la propia comunidad/documentación advierte que el self-host es "para usuarios expertos" y que errores pueden causar pérdida de datos o caídas; el costo real es el tiempo de ingeniería (updates, backups, monitoreo), no el hosting. No recomendado para equipos sin perfil técnico. Fuente: [docs.n8n.io/hosting](https://docs.n8n.io/hosting/), [scalevise.com](https://scalevise.com/resources/n8n-workflow-automation/).
- **Make.com queda descartado** para tu caso: es **solo nube**, no se autoaloja. Fuente: [activepieces.com n8n vs Make](https://www.activepieces.com/blog/n8n-vs-make-com).
- **Activepieces** es el alternativo open source que más creció (MIT, "AI-first", soporte MCP nativo de 280+ servidores, arranque más fácil 9.1 vs 7.7). Pero comunidad/ecosistema mucho menores (~14-15k vs 181k estrellas) y menos maduro a escala. Veredicto comunitario: "n8n es el pick más seguro a escala; Activepieces el mejor para empezar si quieres flujos muy AI-heavy". Fuente: [dev.to ciphernutz 2026](https://dev.to/ciphernutz/n8n-vs-activepieces-for-developer-workflow-automation-a-practical-2026-comparison-3i4k), [stacksheriff.com](https://stacksheriff.com/automation/n8n-vs-activepieces/), [aiworkshack.com 2026](https://aiworkshack.com/tools/activepieces/activepieces-vs-n8n-an-honest-comparison-for-self-hosters-in-2026.html).

### 2. n8n "puro" vs sumar bandeja omnicanal (Chatwoot / Typebot)

- El patrón open source recomendado por la comunidad para unificar WhatsApp + IG + FB **con handoff humano** es **Chatwoot como bandeja + n8n como motor de lógica/IA**. Chatwoot ofrece bandeja omnicanal real, historial, asignación de agentes, notas internas y un "AgentBot" que puede delegar a IA (OpenAI, **Claude**, Gemini). Fuente: [chatwoot.com](https://www.chatwoot.com/), [chatwoot.com/features/channels](https://www.chatwoot.com/features/channels), [github.com/chatwoot/chatwoot](https://github.com/chatwoot/chatwoot), [chatwoot docs - Agent bots](https://www.chatwoot.com/hc/user-guide/articles/1677497472-how-to-use-agent-bots).
- Hay plantilla oficial de n8n para "asistente de soporte multicanal con Chatwoot": webhook recibe el evento de mensaje, recupera historial vía API, genera respuesta con IA y la devuelve a la conversación correcta de Chatwoot. También existe un nodo comunitario `n8n-nodes-chatwoot`. Fuente: [n8n.io workflow 8260](https://n8n.io/workflows/8260-build-a-multichannel-customer-support-ai-assistant-with-chatwoot-and-openrouter/), [github.com/fazer-ai/n8n-nodes-chatwoot](https://github.com/fazer-ai/n8n-nodes-chatwoot).
- El stack open source más citado (DEV.to) es **n8n (lógica) + Chatwoot (interfaz humana) + WAHA (transporte WhatsApp)** a ~$50/mes vs $300+ de SaaS. **OJO:** ese artículo usa WAHA (API no oficial de WhatsApp Web), que viola los TOS; el propio autor recomienda usar la **API oficial** para mensajería saliente/promocional. En tu caso, reemplaza WAHA por la Meta Cloud API oficial y mantén la idea Chatwoot + n8n. Fuente: [dev.to - n8n + Chatwoot + WAHA](https://dev.to/achiya-automation/building-an-open-source-whatsapp-customer-support-stack-n8n-chatwoot-waha-3o86).
- **Costo del handoff:** Chatwoot autoalojado suma carga al VPS (Rails + Sidekiq + PostgreSQL/pgvector + Redis) y pide DevOps; no es plug-and-play. Hay que dimensionar el VPS para que aguante n8n + Chatwoot juntos. Fuente: [github.com/chatwoot/chatwoot](https://github.com/chatwoot/chatwoot).
- **Typebot** sirve para flujos conversacionales guiados (tipo formulario/quiz), no como bandeja omnicanal ni para handoff: rol distinto al de Chatwoot.

### 3. Mensajería: Meta Cloud API oficial vs intermediarios (Twilio/360dialog/Wati/ManyChat)

- Consenso: para el 95% de negocios que NO quieren montar infra, vale un BSP; pero si montas la infra tú mismo (como con n8n), **acceso directo a Meta Cloud API** es válido y más barato. Para SMEs sin perfil técnico, recomiendan **360dialog (costo, zero markup)** o **Wati (facilidad no-code)**. Twilio es potente pero caro para negocio pequeño. Fuente: [kommunicate.io Twilio vs 360dialog](https://www.kommunicate.io/blog/twilio-vs-360dialog-a-comparison/), [prelude.so top BSPs 2026](https://prelude.so/blog/best-whatsapp-business-solution-providers), [ezcontact.ai BSP comparison 2026](https://ezcontact.ai/en/blog/whatsapp-bsp-comparison/).
- **Precios de Meta (clave para tu caso de soporte/atención):**
  - Desde **1 nov 2024**, las **conversaciones de servicio (iniciadas por el usuario) son gratis e ilimitadas**. Como tus clientes te escriben primero (alquiler), gran parte de tu tráfico no tiene costo de mensajería.
  - Desde **1 jul 2025**, Meta cobra **por mensaje de plantilla entregado** (modelo per-message), no por conversación, con tarifas por categoría (marketing/utility/authentication) y por país, y tiers de volumen.
  - Mensajes no-plantilla y todo lo enviado dentro de la ventana de servicio abierta son gratis. Fuente: [developers.facebook.com WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing), [ycloud.com pricing update jul 2025](https://www.ycloud.com/blog/whatsapp-api-pricing-update).
- **Riesgos/quejas comunes (sé consciente):**
  - **Ventana de 24h:** fuera de las 24h desde el último mensaje del cliente, solo puedes iniciar con **plantillas pre-aprobadas** (la aprobación tarda hasta 24h). Esto afecta a tu bot: no podrá "retomar" libremente a un cliente que escribió hace 2 días sin plantilla.
  - **Baneos/restricciones:** enviar demasiado rápido, mensajear fuera de la ventana sin plantilla, o que muchos usuarios te reporten/bloqueen baja tu "quality rating" y limita el envío. Apelaciones a Meta tardan 24-48h.
  - **APIs no oficiales (WAHA y similares):** violan TOS; riesgo real de baneo del número, sobre todo en saliente/masivo. Para inbound puro es "relativamente seguro" pero no recomendado para un negocio que depende de su número. Fuente: [chakrahq.com - WhatsApp API bans](https://chakrahq.com/article/whatsapp-api-account-restricted-or-blocked-find-out-why-and-how-to-resolve/), [trengo.com - banned](https://trengo.com/blog/whatsapp-business-banned), [developers.facebook.com policy enforcement](https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement).
- **Instagram DM / Messenger por Graph API en n8n:** hay plantillas y guías (auto-DM, responder DMs/comentarios/menciones), pero la comunidad documenta fricción real: hay quien recibe el webhook y genera la respuesta IA pero **falla al devolver el mensaje** a Instagram por el nodo de Graph API. Requiere configuración cuidadosa de tokens/permisos de Meta. Fuente: [community.n8n.io - Instagram DM not delivering](https://community.n8n.io/t/instagram-dm-automation-messages-not-delivering-via-facebook-graph-api/242053), [n8n.io workflow 6632 auto-respond IG/FB/WhatsApp](https://n8n.io/workflows/6632-auto-respond-to-instagram-facebook-and-whatsapp-with-llama-32/), [medium JAA Consulting - Instagram API n8n](https://medium.com/@j.a.alves/instagram-api-for-n8n-automations-to-handle-dm-comments-and-mentions-8d4aab89ecd5).

### 4. ¿n8n + Claude o plataforma dedicada (ManyChat / Botpress / Voiceflow)?

- **ManyChat** es el más popular para IG/FB/WhatsApp no-code y el más rápido de lanzar, pero criticado en 2026: el plan free se recortó a **solo 25 contactos** (marzo 2026, "la mayor queja de la comunidad"), el precio sube con los contactos, el **add-on de IA cuesta $29/mes adicionales** (solo en Pro/Business), pasa recargos de WhatsApp y el soporte es lento (3-5 días hábiles). Fuente: [flowgent.ai ManyChat pricing](https://flowgent.ai/blog/manychat-pricing), [roborhythms.com review tras el cambio de precios](https://www.roborhythms.com/manychat-review/).
- **Botpress** y **Voiceflow** apuntan más a volúmenes medios/altos y soporte; Voiceflow permite elegir LLM (incluido Claude). Para un negocio pequeño y muy personalizado son sobredimensionados. Fuente: [chatimize.com Botpress vs Voiceflow](https://chatimize.com/botpress-vs-voiceflow/), [nation.ai Botpress guide](https://nation.ai/the-complete-botpress-guide-botpress-reviews-features-prices-and-comparison-of-the-best-ai-standalone-chatbot-alternatives/).
- Para tu caso (responder "como el dueño", tono propio, presupuesto ajustado, control de datos), la comunidad apoya **n8n + Claude**: hay numerosas guías y plantillas 2025-2026 de "AI receptionist" para alquiler/hospitalidad con n8n que responden FAQs (wifi, check-out, parking), escalan a humano y guardan historial, usando pocos nodos. Costo: solo API de Claude (Haiku es barato) + VPS, sin per-operation. Fuente: [vonage - n8n WhatsApp receptionist](https://developer.vonage.com/en/blog/build-a-5-node-ai-whatsapp-receptionist-with-n8n-and-vonage-mcp-tools), [n8n.io workflow 3043 asistente hospitality](https://n8n.io/workflows/3043-ai-powered-whatsapp-assistant-for-restaurants-and-delivery-automation/), [ritz7.com - WhatsApp AI agent n8n 2026](https://ritz7.com/blog/whatsapp-automation-build-chatbots-with-n8n).
- Patrón híbrido frecuente: usar **ManyChat solo como pasarela de IG** apuntando a un webhook de n8n para la IA, cuando el nodo nativo de IG da problemas. Es una alternativa si la Graph API directa en n8n se complica. Fuente: [n8n.io workflow 2718 - AI agent IG DM con ManyChat + IA](https://n8n.io/workflows/2718-ai-agent-for-instagram-dminbox-manychat-open-ai-integration/), [community.n8n.io - ¿n8n hace todo lo de ManyChat?](https://community.n8n.io/t/can-n8n-do-all-that-can-be-done-with-manychat/21130).

## Contraste con el plan actual

**¿Es n8n + Meta API + Claude lo más recomendado? — Sí, en lo esencial está validado.** Es exactamente el stack que la comunidad recomienda para self-hosted con IA, control de costos y datos propios, y encaja con tu presupuesto (~$70/mes: VPS + API de Claude Haiku, con conversaciones de servicio de WhatsApp gratis). La elección de la **Meta Cloud/Graph API oficial** (no APIs no oficiales) es la decisión correcta y la que evita baneos. Usar **Claude Haiku** para generar respuestas es coherente con costo y calidad para FAQs de alquiler.

**Qué ajustaría / añadiría:**

1. **Añadir Chatwoot (open source) como bandeja omnicanal con handoff humano.** Es el cambio más recomendado por la comunidad. n8n "puro" auto-responde, pero no te da una bandeja donde el dueño vea WhatsApp + IG + FB juntos y **retome el control** cuando la IA no deba responder (reservas en firme, quejas, casos delicados). Arquitectura sugerida: Meta APIs → Chatwoot (bandeja) → n8n (lógica + Claude) → de vuelta a Chatwoot. Costo: solo más RAM en el VPS.
2. **Dimensionar el VPS para n8n + Chatwoot juntos.** Chatwoot pide PostgreSQL + Redis + Sidekiq; con $70/mes total, asegúrate de un VPS con suficiente RAM (apunta a >=4 GB, idealmente 8 GB) o el sistema se quedará corto.
3. **Diseñar para la ventana de 24h desde el inicio.** El bot responderá gratis y sin fricción mientras el cliente esté dentro de las 24h. Para reactivar conversaciones más viejas (p.ej. confirmar disponibilidad días después) necesitarás **plantillas de utilidad pre-aprobadas**. Planifica 1-2 plantillas y su aprobación.
4. **Prever fricción real con Instagram/Messenger en n8n.** Es lo que más se queja la comunidad (mensajes que no se entregan de vuelta, permisos/tokens de Meta). Reserva tiempo para esto y ten como plan B usar ManyChat solo como pasarela de IG apuntando al webhook de n8n si la Graph API directa se complica.
5. **Activepieces solo si quieres un arranque más simple y muy AI-first;** pero para este proyecto **n8n es la apuesta más segura** por madurez, comunidad y plantillas listas de WhatsApp/hospitality. No cambies de n8n salvo que el equipo lo prefiera por UX.
6. **Reglas anti-baneo:** no enviar masivo/saliente agresivo, respetar la ventana, usar el número con verificación de negocio (tu RUC en Perú ayuda), y monitorear el quality rating en el panel de Meta.

**No recomendaría** cambiar a una plataforma dedicada (ManyChat/Botpress/Voiceflow) como núcleo: para "responder como el dueño" con tono propio, control de datos y costo bajo, n8n + Claude es superior; ManyChat encarece con IA y contactos y ata a su plataforma.

## Fuentes

- https://www.activepieces.com/blog/n8n-vs-make-com
- https://www.upskillist.com/blog/n8n-review/
- https://syncgtm.com/blog/n8n-review
- https://www.infralovers.com/blog/2025-05-09-n8n-workflow-automation/
- https://scalevise.com/resources/n8n-workflow-automation/
- https://docs.n8n.io/hosting/
- https://dev.to/ciphernutz/n8n-vs-activepieces-for-developer-workflow-automation-a-practical-2026-comparison-3i4k
- https://stacksheriff.com/automation/n8n-vs-activepieces/
- https://aiworkshack.com/tools/activepieces/activepieces-vs-n8n-an-honest-comparison-for-self-hosters-in-2026.html
- https://www.chatwoot.com/
- https://www.chatwoot.com/features/channels
- https://github.com/chatwoot/chatwoot
- https://www.chatwoot.com/hc/user-guide/articles/1677497472-how-to-use-agent-bots
- https://n8n.io/workflows/8260-build-a-multichannel-customer-support-ai-assistant-with-chatwoot-and-openrouter/
- https://github.com/fazer-ai/n8n-nodes-chatwoot
- https://dev.to/achiya-automation/building-an-open-source-whatsapp-customer-support-stack-n8n-chatwoot-waha-3o86
- https://www.kommunicate.io/blog/twilio-vs-360dialog-a-comparison/
- https://prelude.so/blog/best-whatsapp-business-solution-providers
- https://ezcontact.ai/en/blog/whatsapp-bsp-comparison/
- https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- https://www.ycloud.com/blog/whatsapp-api-pricing-update
- https://chakrahq.com/article/whatsapp-api-account-restricted-or-blocked-find-out-why-and-how-to-resolve/
- https://trengo.com/blog/whatsapp-business-banned
- https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement
- https://community.n8n.io/t/instagram-dm-automation-messages-not-delivering-via-facebook-graph-api/242053
- https://n8n.io/workflows/6632-auto-respond-to-instagram-facebook-and-whatsapp-with-llama-32/
- https://medium.com/@j.a.alves/instagram-api-for-n8n-automations-to-handle-dm-comments-and-mentions-8d4aab89ecd5
- https://flowgent.ai/blog/manychat-pricing
- https://www.roborhythms.com/manychat-review/
- https://chatimize.com/botpress-vs-voiceflow/
- https://nation.ai/the-complete-botpress-guide-botpress-reviews-features-prices-and-comparison-of-the-best-ai-standalone-chatbot-alternatives/
- https://developer.vonage.com/en/blog/build-a-5-node-ai-whatsapp-receptionist-with-n8n-and-vonage-mcp-tools
- https://n8n.io/workflows/3043-ai-powered-whatsapp-assistant-for-restaurants-and-delivery-automation/
- https://ritz7.com/blog/whatsapp-automation-build-chatbots-with-n8n
- https://n8n.io/workflows/2718-ai-agent-for-instagram-dminbox-manychat-open-ai-integration/
- https://community.n8n.io/t/can-n8n-do-all-that-can-be-done-with-manychat/21130

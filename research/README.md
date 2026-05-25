# Investigación de la comunidad — herramientas del proyecto

Esta carpeta contiene la investigación web (mayo 2026) que contrasta las herramientas
elegidas en el plan con lo que más recomienda la comunidad (Reddit r/selfhosted, Hacker
News, foros de n8n/Chatwoot, comparativas de blogs 2025-2026). Cada archivo cita sus
fuentes (URLs).

## Índice

| Archivo | Contenido |
|---|---|
| [00-conclusiones-vs-plan.md](00-conclusiones-vs-plan.md) | **Empieza aquí.** Síntesis: veredicto por componente, los 4 ajustes recomendados, advertencias y presupuesto revisado. |
| [01-orquestador-y-chatbot.md](01-orquestador-y-chatbot.md) | n8n vs Make/Activepieces/Zapier · bandeja Chatwoot + handoff · Meta API oficial vs intermediarios · n8n+Claude vs ManyChat/Botpress. |
| [02-base-de-datos.md](02-base-de-datos.md) | NocoDB vs Baserow vs Teable/Grist/Supabase · calendario/formularios/PWA · integración n8n · autoalojar vs pagar Airtable. |
| [03-video-y-programador-social.md](03-video-y-programador-social.md) | Video por plantillas (FFmpeg vs JSON2Video/Creatomate/Shotstack…) · clips (OpusClip/Vizard) · programadores (Publer/Metricool/Buffer/Postiz). |

## Conclusión en una línea

El plan está **validado en lo esencial** (n8n + Meta API oficial + Claude + autoalojar +
APIs de plantillas + programador gratis). **4 ajustes:** (1) añadir **Chatwoot** para la
bandeja y el handoff, (2) elegir **NocoDB** (no Baserow, su calendario es de pago), (3)
priorizar **API de plantillas de video** sobre FFmpeg, (4) **Publer gratis** como
programador. Ojo al VPS más grande (≥4-8 GB por Chatwoot) y a no pagar video+clips+
programador a la vez dentro de $70.

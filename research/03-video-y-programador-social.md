# Investigación: Generación de video y programador social

> Negocio: alquiler de casa de campo · Presupuesto total ~$70/mes · Stack disponible: VPS + n8n
> Fecha de investigación: mayo 2026 · Fuentes: comparativas de blogs 2025-2026, docs oficiales, hilos de comunidad. Donde una fuente es de un vendedor (Creatomate, JSON2Video, Plainly, Postiz) lo señalo porque su comparación es interesada.

## Resumen ejecutivo

- **Video por plantillas:** para un dueño NO técnico, la comunidad NO recomienda FFmpeg como herramienta de uso diario (es gratis y potente, pero es CLI: hay que mantener scripts y depurar errores). Recomienda una **API de render con plantillas** orquestada desde n8n. La opción con mejor relación calidad/precio/facilidad para "plantilla de marca + datos" es **Creatomate** (editor visual + integración nativa n8n) o **JSON2Video** (más generoso en plan gratis y TTS incluido, pero más orientado a código).
- **Importante:** "plantilla de marca" (intro/outro, logo, música, subtítulos fijos) y "cortar clips automáticos de un video largo" son DOS problemas distintos. Para lo primero sirven las APIs de plantillas. Si además quiere generar reels a partir de videos largos, las herramientas recomendadas son **OpusClip / Submagic / Vizard** (estas SÍ ponen subtítulos animados solas).
- **Programador social:** la comunidad valida **Publer** y **Metricool** como mejores planes gratis reales. Para TikTok + Instagram + Facebook a la vez, **Publer (free)** es algo más práctico (3 cuentas, 10 posts en cola por cuenta, soporta los 3). **Metricool (free)** limita a 20 posts publicados/mes y arrastra quejas por subida de video/IG/TikTok.
- **Recomendación de presupuesto:** dejar el programador social en plan GRATIS (Publer o Metricool) y gastar los ~$70 en la API de video o en una herramienta de clips. Hacer las dos cosas de pago a la vez NO entra en $70.

---

## A) Video por plantillas — Comparativa y hallazgos

### Tabla comparativa

| Herramienta | Tipo | Plan gratis | Precio entrada | ¿No técnico? | Integración n8n | Notas |
|---|---|---|---|---|---|---|
| **FFmpeg** | CLI / código | $0 (ilimitado) | $0 | No (CLI, scripts) | Vía nodo Execute Command en el VPS | Gratis y total control; alto mantenimiento |
| **Creatomate** | API + editor visual | 50 créditos (~3 min), con marca de agua | ~$41–$54/mo (2.000 créditos) | Sí (editor drag-and-drop) | Nativa (también Make/Zapier) | Cobra créditos extra por TTS |
| **JSON2Video** | API code-first | 600 créditos (~10 min), sin tarjeta | ~$49,95/mo (200 min Full HD) | Medio (orientado a código/JSON) | Nativa (también Make) | TTS Azure/ElevenLabs incluido |
| **Shotstack** | API developer-first | Sí (sandbox) | ~$49/mo | No (developer-first) | Vía HTTP | Para equipos que construyen pipelines |
| **Remotion** | Framework React | Gratis (open source, licencia) | $0 + infra render | No (requiere React) | Solo programático | Potente para devs; no apto no técnicos |
| **Plainly** | API sobre After Effects | Trial 14 días | $69/mo (50 min render) | Sí (plantillas AE) | Sí (API/no-code) | Calidad pro AE, pero caro y depende de Adobe |
| **Bannerbear** | API + builder visual | No claro | $49/mo (1.000 créditos) | Sí (UI limpia) | Vía API | Accesible para no devs |
| **Placid** | API no-code | No especificado | $19/mo (500 créditos) | Sí | Vía API | Económico, branded visuals |

### Hallazgos con citas

- **FFmpeg = potente pero no para no técnicos en el día a día.** "FFmpeg sigue siendo el rey del procesamiento de video gratis, pero tiene desventajas significativas para usuarios no técnicos... los desarrolladores pasan más tiempo gestionando scripts y depurando errores oscuros que construyendo features." (Rendi, 2025 — https://www.rendi.dev/blog/best-video-generation-apis ; IT Path Solutions, "Moving Beyond FFmpeg", 2025 — https://www.itpathsolutions.com/top-ffmpeg-alternatives). Para tareas simples FFmpeg basta; "para video a escala / generación automatizada, no alcanza" (Creatomate blog — https://creatomate.com/how-to/edit-video-by-api).

- **Creatomate** trae editor en la nube drag-and-drop, timeline, preview en tiempo real y editor JSON; "puede usarse por equipos no técnicos vía Zapier, Make y n8n" (Creatomate — https://creatomate.com/blog/how-to-automate-video-creation-with-n8n). Plan gratis = 50 créditos (~3 min) **con marca de agua**; Essential ~$54/mo con 2.000 créditos. Crítica recurrente: **cobra créditos adicionales por TTS** además del render (json2video.com/how-to/creatomate-alternative/ — fuente del competidor, sesgada; y Thinkpeak AI — https://thinkpeak.ai/json2video-free-alternatives/).

- **JSON2Video** destaca por plan gratis más generoso: **600 créditos (~10 min) sin tarjeta**, y **TTS (Azure 120+ voces, ElevenLabs) incluido** en los créditos de render. Es más "code-first" (flujo por JSON, ideal Make.com/n8n) y por tanto un poco menos amigable que el editor visual de Creatomate para diseñar la plantilla. Entrada ~$49,95/mo (200 min Full HD). (json2video.com/how-to/creatomate-alternative/ — vendedor; y Plainly, "7 Best video editing API" 2026 — https://www.plainlyvideos.com/blog/best-video-editing-api).

- **Shotstack**: API developer-first, ~$49/mo, recomendada para equipos que arman su propio pipeline; no es la elección para un no técnico (Creatomate, "Best Video Generation APIs" — https://creatomate.com/blog/the-best-video-generation-apis).

- **Remotion**: "requiere conocimiento sólido de React y animaciones web; NO apto para usuarios no técnicos". Excelente para devs y datos variables, pero el setup del pipeline de render (sobre todo Lambda) "puede ser complejo para principiantes" (Remotion docs/GitHub y reseñas 2026 — https://www.remotion.dev/ ; https://github.com/remotion-dev/remotion). **Descartable** para este caso.

- **Plainly**: plantillas hechas en Adobe After Effects renderizadas en la nube; "conecta diseño profesional con automatización no-code" pero **el plan más barato es $69/mo (50 min render)**, lo que se come casi todo el presupuesto, y depende del ecosistema Adobe (Plainly — https://www.plainlyvideos.com/blog/best-video-editing-api ; Thinkpeak AI — https://thinkpeak.ai/json2video-free-alternatives/). Mejor calidad de motion graphics, peor encaje con $70.

- **Alternativas económicas mencionadas:** Placid ($19/mo, 500 créditos), Bannerbear ($49/mo), Templated (50 renders gratis sin marca de agua) — todas "no-code friendly" para visuales/branded templates (Plainly — https://www.plainlyvideos.com/blog/best-video-editing-api ; Templated — https://templated.io/alternative-to/creatomate/).

### Caso especial: "cortar clips" ≠ "plantilla de marca"

Si el dueño además quiere convertir video largo (un tour de la casa, un día completo) en varios reels cortos con subtítulos, esto es repurposing automático, NO una plantilla. La comunidad recomienda:

- **OpusClip** — "mejor para velocidad y clips estilo viral"; subtítulos animados con ~97% de precisión, emojis y "Virality Score" (Drone & Cam 2025 — https://droneandcam.com/en/post/opus-clip-alternatives-which-tool-to-choose-in-2025/ ; Reap — https://reap.video/blog/top-5-ai-clipping-tools-2025).
- **Submagic** — "mejor para contenido short-form con subtítulos"; subtítulos animados/estilizados muy llamativos.
- **Vizard** — "más barato y simple"; **plan gratis generoso (60 min/mes)**, buena relación costo-por-minuto (Vizard — https://vizard.ai/alternatives/opus ; Reap 2026 — https://reap.video/blog/top-ai-clipping-tools-in-2026).

Para un solo negocio pequeño con poco volumen, **Vizard (free 60 min/mes)** u **OpusClip** cubren los clips automáticos sin tocar el presupuesto.

---

## B) Programador social — Comparativa y hallazgos

### Tabla comparativa

| Herramienta | Plan gratis (2025-2026) | TikTok | IG | FB | Límite clave del free | Notas / quejas |
|---|---|---|---|---|---|---|
| **Publer** | 3 cuentas, 1 workspace, 10 posts en cola/cuenta, 25 borradores | Sí | Sí | Sí | Cola de 10/cuenta (no mensual); historial 24h | El free más completo; pruebas temporales de funciones pro |
| **Metricool** | 1 marca, 1 perfil por red, 20 posts publicados/mes | Sí | Sí | Sí | 20 publicaciones/mes; analítica 3 meses | Quejas con subida de video IG/TikTok/Shorts |
| **Buffer** | 3 canales, 10 posts en cola/canal (hasta 30) | Sí | Sí | Sí | Cola, no analítica; algunos formatos limitados | Soporta Reels/Stories en free; sin analítica |
| **Postiz** (open source) | Gratis self-hosted (Apache/AGPL) 18+ redes | Sí* | Sí* | Sí* | Tú montas la app dev y OAuth de cada red | Muy activo (30k+ stars); editor tipo Canva + IA |
| **Mixpost** (open source) | Pago único, self-hosted (MIT) | Sí* | Sí* | Sí* | Igual: requiere apps dev propias | Analítica avanzada, roles/aprobaciones; menos activo |

\* En las herramientas self-hosted la publicación depende de que TÚ crees y obtengas aprobación de apps de desarrollador en cada plataforma (ver sección n8n/APIs).

### Hallazgos con citas

- **Publer free** = 1 usuario, 1 workspace, hasta **3 cuentas sociales**, **10 posts en cola por cuenta** (al publicarse uno se libera el slot), 25 borradores. Soporta FB, IG, TikTok, LinkedIn, Pinterest, GBP, YouTube, Telegram, Mastodon, Bluesky, Threads (X NO en free por restricciones de API). Punto flojo: **historial limitado a últimas 24h** (poca analítica). (Publer Help Center — https://publer.com/help/en/article/what-are-publers-plans-and-pricing-15h4yqh/ ; Schedchie 2025 — https://www.schedchie.com/blog/7-free--affordable-social-media-scheduling-tools-2025-edition).

- **Metricool free** = plan gratis permanente, **1 marca y 1 perfil por red**, **20 posts publicados/mes** (cuenta solo los publicados, no los programados), analítica de 3 meses, sin reportes descargables. Quejas reportadas: "muchas limitaciones al publicar en Instagram, TikTok y YouTube Shorts; problemas de tamaño de archivo de video y de formato de caption". Su fuerte real es la **analítica multiplataforma**. (Metricool Help — https://help.metricool.com/en/article/main-differences-between-free-and-premium-plans-1udj06m/ ; Efficient App review 2026 — https://efficient.app/apps/metricool ; Tygart Media — https://tygartmedia.com/metricool-free-plan-review/).

- **Buffer free** = **3 canales, 10 posts en cola por canal (hasta 30)**; soporta TikTok e IG (feed, Reels, Stories) y FB; **sin analítica** y sin team. Es límite de cola, no mensual. (Buffer support — https://support.buffer.com/article/595-features-available-on-each-buffer-plan ; Glow Social 2026 — https://glowsocial.com/blog/buffer-pricing-free-plan-limits-2026 ; Buffer free review — https://schedulala.com/blog/buffer-free-plan-review).

- **Postiz (open source)**: completamente gratis self-hosted, 18+ redes (IG, TikTok, FB, etc.), licencia Apache/AGPL, **30.275 stars en GitHub vs 3.223 de Mixpost** y desarrollo muy activo (commits recientes). Incluye editor tipo Canva y asistente IA. (Postiz blog — https://postiz.com/blog/open-source-social-media-scheduler ; comparativa OpenAlternative — https://openalternative.co/compare/mixpost/vs/postiz ; GitHub — https://github.com/gitroomhq/postiz-app).

- **Mixpost (open source)**: modelo de **pago único** (no suscripción), licencia MIT (más permisiva para uso comercial), analítica avanzada, biblioteca de medios, workspaces y flujos de aprobación. Menos actividad de desarrollo que Postiz. (OpenAlternative — https://openalternative.co/compare/mixpost/vs/postiz ; Mixpost — https://mixpost.app/blog/why-open-source-social-media-management-tools-are-perfect-for-startups).

- **Realidad del self-hosted (clave):** Postiz/Mixpost no almacenan tus API keys; usan OAuth, pero **tú debes crear tu propia app de desarrollador en cada red**. Para TikTok específicamente Postiz documenta que "requiere cuenta de developer de TikTok, un sitio web público con HTTPS y poder subir un archivo para verificar propiedad". Es decir: gratis en software, pero con coste de setup técnico y aprobaciones. (Postiz docs TikTok — https://docs.postiz.com/providers/tiktok).

---

## C) Integración con n8n y fiabilidad de las APIs oficiales

- **La comunidad sí integra esto con n8n**, pero con matices. Hay 560+ workflows de social media en la librería de n8n, incluyendo plantillas que: publican a IG Business + FB Pages vía **Meta Graph API** (tokens de usuario de sistema), o leen un **calendario en Google Sheets**, descargan el video de Drive y lo suben a varias redes. (n8n workflows — https://n8n.io/workflows/categories/social-media/ ; Meta Graph API template — https://n8n.io/workflows/5457-... ; Google Sheets scheduler — https://n8n.io/workflows/9786-...).

- **TikTok es el punto débil de la automatización.** La **Content Posting API** oficial existe (modo Direct Post y Creator Draft), PERO:
  - Aprobación **manual de 2 a 6 semanas**; en 2025 TikTok endureció el proceso (más pasos y detalles requeridos).
  - **Hasta no pasar la auditoría, todo lo publicado por el cliente API queda en modo privado.**
  - Rate limits: ~100 posts/día por app aprobada.
  (TikTok developers — https://developers.tiktok.com/doc/content-posting-api-get-started ; Zernio 2026 — https://zernio.com/blog/tiktok-posting-api ; EchoTik 2025 — https://www.echotik.live/blog/is-tiktoks-api-public-access-approval-process-2025/).

- **Conclusión práctica sobre n8n para TikTok/IG/FB:** montar la publicación nativa con APIs oficiales desde n8n es viable para IG/FB (Meta Graph API es estable con system user tokens) pero **TikTok añade fricción real** (auditoría, modo privado hasta aprobar). Por eso muchos workflows usan **intermediarios** tipo Blotato o Upload-Post que centralizan la publicación a TikTok/IG/YT/FB en una sola llamada API — pero esos servicios son de pago y se sumarían al presupuesto. (Blotato template — https://n8n.io/workflows/7187-... ; Upload-Post — https://www.upload-post.com/how-to/automate-social-media-with-n8n/).

---

## Contraste con el plan actual

### ¿FFmpeg o API de plantillas? → **API de plantillas (validado, con matiz)**

- **No recomiendo FFmpeg como herramienta de uso diario para el dueño no técnico.** La comunidad es clara: FFmpeg es gratis y total, pero su coste real es mantenimiento y depuración de scripts. Encaja con la filosofía WAT (un `tool/` determinista en el VPS), pero quien arma/repara ese tool eres tú (el agente/dev), no el dueño. Como **tool puntual** dentro de n8n (ej. concatenar intro+clip+outro ya definidos) FFmpeg es perfectamente válido y $0; como sistema de plantillas editable por el dueño, no.
- **Recomendación: empezar por una API de plantillas.** Entre las del plan:
  - **JSON2Video** si priorizas plan gratis (600 créditos ~10 min, TTS incluido) y un flujo por JSON desde n8n. Ideal para validar sin pagar.
  - **Creatomate** si priorizas que alguien edite la plantilla en un **editor visual** (más amigable para no técnico) y tienes la integración n8n nativa; ojo al cobro extra de TTS.
- Veredicto: **el plan es correcto.** La ruta sensata es: **diseñar la plantilla de marca una vez (Creatomate o JSON2Video) → render automático vía API desde n8n con el material crudo**. Reservar FFmpeg para pasos simples/baratos dentro del workflow.

### ¿Metricool o Publer u otra? → **Publer (free) como principal; Metricool (free) para analítica**

- Ambas elecciones del plan están **validadas por la comunidad** como mejores planes gratis reales.
- Para **publicar** en TikTok+IG+FB desde calendario, **Publer free** es algo más flexible (3 cuentas, 10 en cola por cuenta, soporta las 3 redes). **Metricool free** topa en **20 publicaciones/mes** y tiene quejas de subida de video en IG/TikTok/Shorts.
- Si el dueño quiere **analítica**, Metricool gana ahí; se pueden usar **las dos gratis a la vez** (Publer para programar, Metricool para medir) sin gastar.
- **Postiz/Mixpost (open source)** encajan con tu filosofía self-hosted y son $0 de licencia, pero el coste oculto es montar apps de developer y pasar auditorías (sobre todo TikTok). Recomendado solo si quieres invertir tiempo técnico; para arrancar ya, un SaaS free (Publer) evita esa fricción.

### Encaje con el presupuesto de ~$70/mes

- **Programador social: $0** (Publer free, opcional Metricool free).
- **Video: el gasto principal.** Opciones que caben:
  - Validar gratis con **JSON2Video free** o **Creatomate free** ($0) mientras se ajusta la plantilla.
  - Al escalar, una sola API de plantillas (~$41–$54/mo Creatomate o ~$49,95/mo JSON2Video) **entra holgadamente** en $70. Plainly ($69) lo agota casi entero.
  - Si además quiere clips automáticos, **Vizard free (60 min/mes)** suma $0.
- **No cabe** pagar API de plantillas + herramienta de clips de pago + programador de pago simultáneamente dentro de $70. Prioriza: video de pago (1 herramienta) + resto en planes gratis.

---

## Fuentes (URLs)

Video por plantillas / FFmpeg:
- https://www.rendi.dev/blog/best-video-generation-apis
- https://www.itpathsolutions.com/top-ffmpeg-alternatives
- https://www.plainlyvideos.com/blog/best-video-editing-api
- https://creatomate.com/blog/the-best-video-generation-apis
- https://creatomate.com/how-to/edit-video-by-api
- https://creatomate.com/blog/how-to-automate-video-creation-with-n8n
- https://json2video.com/how-to/creatomate-alternative/ (fuente del competidor JSON2Video — sesgada)
- https://thinkpeak.ai/json2video-free-alternatives/
- https://templated.io/alternative-to/creatomate/
- https://www.remotion.dev/
- https://github.com/remotion-dev/remotion

Clips automáticos:
- https://droneandcam.com/en/post/opus-clip-alternatives-which-tool-to-choose-in-2025/
- https://reap.video/blog/top-5-ai-clipping-tools-2025
- https://reap.video/blog/top-ai-clipping-tools-in-2026
- https://vizard.ai/alternatives/opus

Programador social:
- https://publer.com/help/en/article/what-are-publers-plans-and-pricing-15h4yqh/
- https://www.schedchie.com/blog/7-free--affordable-social-media-scheduling-tools-2025-edition
- https://help.metricool.com/en/article/main-differences-between-free-and-premium-plans-1udj06m/
- https://efficient.app/apps/metricool
- https://tygartmedia.com/metricool-free-plan-review/
- https://support.buffer.com/article/595-features-available-on-each-buffer-plan
- https://glowsocial.com/blog/buffer-pricing-free-plan-limits-2026
- https://schedulala.com/blog/buffer-free-plan-review
- https://postiz.com/blog/open-source-social-media-scheduler
- https://openalternative.co/compare/mixpost/vs/postiz
- https://github.com/gitroomhq/postiz-app
- https://docs.postiz.com/providers/tiktok
- https://mixpost.app/blog/why-open-source-social-media-management-tools-are-perfect-for-startups

n8n e integración / APIs oficiales:
- https://n8n.io/workflows/categories/social-media/
- https://n8n.io/workflows/5457-automate-instagram-and-facebook-posting-with-meta-graph-api-and-system-user-tokens/
- https://n8n.io/workflows/9786-schedule-and-auto-post-videos-to-instagram-linkedin-and-tiktok-with-google-sheets/
- https://n8n.io/workflows/7187-automate-content-publishing-to-tiktok-youtube-instagram-facebook-via-blotato/
- https://www.upload-post.com/how-to/automate-social-media-with-n8n/
- https://developers.tiktok.com/doc/content-posting-api-get-started
- https://zernio.com/blog/tiktok-posting-api
- https://www.echotik.live/blog/is-tiktoks-api-public-access-approval-process-2025/
</content>
</invoke>

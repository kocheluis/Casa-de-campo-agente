# Investigación: Base de datos autoalojada (alternativa a Airtable)

> Caso: alquiler de casa de campo operado por **una persona no técnica**. Necesita CRM de clientes, calendario de reservas, base para campañas e inventario actualizable (faltante/averiado), visible en Android y Windows. Presupuesto total ~$70/mes. Plan actual: NocoDB o Baserow autoalojado en VPS + n8n + Python.

## Resumen ejecutivo

Para una alternativa **autoalojada** a Airtable en 2025-2026, la comunidad (r/selfhosted, Hacker News, comparativas de blogs) tiende a recomendar **NocoDB** como la opción más madura, completa y "lista para usar" gratis, seguida muy de cerca por **Baserow** (más amigable y colaborativa, pero con un detalle clave) y por **Teable** (la más prometedora y moderna, pero más nueva). **Hallazgo crítico:** en Baserow autoalojado **la vista Calendario NO está en el plan gratuito** (es función Premium de pago); en cambio en NocoDB el Calendario sí es gratuito en la Community Edition. Como tu requisito central es calendario de reservas, esto inclina la balanza hacia **NocoDB**. Sin embargo, la comunidad es honesta: para un usuario **no técnico** sin nadie que mantenga el VPS, varias fuentes recomiendan directamente **pagar Airtable/Notion** por la menor carga de mantenimiento. NocoDB también arrastra críticas serias de fiabilidad (hilo de Hacker News, feb 2025).

## Comparativa

| Herramienta | Qué dice la comunidad | Calendario / Formularios / PWA-móvil | Integración n8n | Contras principales |
|---|---|---|---|---|
| **NocoDB** | La alternativa autoalojada a Airtable más popular y citada; "la mejor para casa o negocio" (XDA). ~62k★ GitHub. Más orientada a desarrollador pero usable. | **Calendario: SÍ gratis** (Community). Formularios: SÍ. Móvil: **sin app nativa**, solo web responsive + cliente Android no oficial en prototipo. | **Nodo nativo en n8n** (create/read/update/delete). API REST completa con tokens en self-hosted. | Hilo HN (2025): "no maduro para producción", bugs de integridad de datos, borrados que cuelgan ~50%, sin undo, sin tiempo real (hay que refrescar). Licencia "Sustainable Use" (no AGPL). |
| **Baserow** | La más **fácil para no técnicos**, UI colaborativa estilo Airtable, edición en tiempo real. Licencia MIT (núcleo). | **Calendario: NO en el plan gratis self-hosted** (es Premium de pago). Formularios: SÍ (gratis). Móvil: **sin app nativa**, web. | Nodo nativo en n8n. API-first, webhooks. *Tokens de API faltaron históricamente en la variante self-hosted.* | Calendario/Kanban/Survey son de pago. Stack pesado (Django + PostgreSQL + Redis), más recursos en VPS. Sin app móvil. |
| **Teable** | La más "de la que se habla" y moderna; built on Postgres, rápida, AI nativo. ~20k★. "Próxima generación". | Calendario: SÍ (incluso en free). Formularios: SÍ. Móvil: web (sin datos claros de app nativa). | **Sin nodo nativo dedicado tan establecido**; se usa vía HTTP/API REST. Menos automatización en free. | **Más nueva y menos madura**, comunidad y plantillas más pequeñas, ecosistema de integraciones aún creciendo. Docker manual (no en CasaOS/YunoHost). |
| **Grist** | Querida por equipos "tipo hoja de cálculo" con fórmulas Python; permisos finos por fila/celda; muchas plantillas. | Vistas y formularios sí; orientada a hoja de cálculo más que a "vistas Airtable". PWA/móvil no es su fuerte. | Sin nodo nativo fuerte en n8n; integración vía API REST/HTTP. | En el hilo HN se mencionó pero se descartó como "poco inspiradora". Menos enfoque en CRM/calendario visual. |
| **Mathesar** | Capa visual sobre PostgreSQL existente; muy "base de datos" pura. | Sin vistas tipo Airtable (calendario/kanban) reales; sin formularios robustos ni móvil. | Sin integración n8n nativa. | Demasiado orientada a DBA; **no apta** para un usuario no técnico que quiere CRM + calendario + formularios. |
| **Supabase** | Excelente backend Postgres + Auth + API, pero **no es un "Airtable"**; no tiene UI de hojas/vistas/calendario/formularios para usuario final. | No (es backend, no app no-code). | Nodo n8n disponible (a nivel base de datos). | Requiere construir tú la interfaz. **No apta** para una persona no técnica como producto final. |

## Hallazgos por tema (con citas/URLs)

### 1. ¿Cuál prefiere la comunidad como alternativa autoalojada a Airtable?
- **NocoDB** es repetidamente señalada como la alternativa autoalojada más popular y la "mejor para casa o negocio". XDA Developers, "NocoDB is the best self-hosted Airtable alternative" (2025): https://www.xda-developers.com/nocodb-is-the-best-self-hosted-airtable-alternative/
- **Baserow es más fácil para equipos no técnicos** (UI estilo Airtable, tiempo real), mientras **NocoDB es más orientado a desarrollador**. Softr, "Baserow vs NocoDB: which one to choose in 2026": https://www.softr.io/blog/baserow-vs-nocodb ; comparativa elest.io: https://blog.elest.io/nocodb-vs-baserow-which-open-source-airtable-alternative-should-you-pick/
- **Teable** es descrita como la "próxima generación" y de las más comentadas en 2026, construida sobre PostgreSQL, rápida, con IA, pero **más nueva y con menos comunidad/plantillas**. NocoBase blog (2025-2026): https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives ; GitHub Teable: https://github.com/teableio/teable
- Resumen del ecosistema (NocoDB/Baserow/Teable/SeaTable) en el blog de Baserow "Best Airtable Alternative Tools (2026)": https://baserow.io/blog/best-airtable-alternatives

### 2. Calendario, Formularios, PWA/móvil y facilidad para no técnicos
- **Baserow self-hosted gratuito NO incluye Calendario** (ni Kanban ni Survey); son funciones del plan **Premium de pago** por usuario/mes. El plan gratis solo trae Grid, Form y Gallery. Comunidad Baserow: https://community.baserow.io/t/baserow-free-tier-limits/211 ; precios: https://baserow.io/user-docs/pricing-plans ; nota también en Grist: https://www.getgrist.com/lookup/grist-vs-baserow/ ("Baserow ... still missing some key features – notably Kanban, survey, and calendar views" en self-hosted gratis).
- **NocoDB sí ofrece Calendario gratis** en la Community Edition; tipos de vista: Grid, Form, Gallery, Kanban, Calendar, Timeline, List, Map. Docs NocoDB: https://nocodb.com/docs/product-docs/views ; vista Calendario: https://nocodb.com/docs/product-docs/views/view-types/calendar . Limitación: el Calendario soporta un único campo de fecha; el **rango de fechas avanzado es solo en NocoDB Cloud**, no en self-hosted.
- **Formularios**: ambos (NocoDB, Baserow, Teable) tienen vista Formulario, ideal para que el operador actualice inventario desde el móvil con un formulario web.
- **Móvil/PWA**: ni NocoDB ni Baserow tienen **app móvil nativa oficial**; usan web responsive. NocoDB tiene un cliente Android **no oficial en estado prototipo** y un issue abierto de larga data sobre responsive/móvil. GitHub issue #158: https://github.com/nocodb/nocodb/issues/158 ; cliente prototipo: https://github.com/enm10k/nocodb-mobile ; foro NocoDB "NocoDB on Android": https://community.nocodb.com/t/nocodb-on-android-mar-25/272 . Baserow tampoco tiene app móvil nativa (penalizado por ello en reseñas).
- **Facilidad para no técnicos**: Baserow gana en simplicidad y colaboración; NocoDB es algo más técnico de instalar y configurar.

### 3. Integración con n8n y API REST
- **Ambos tienen nodo nativo en n8n.** NocoDB: nodo dedicado documentado (create/get/update/delete filas) — https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.nocodb/ y https://n8n.io/integrations/nocodb/ . Baserow: nodo nativo — https://n8n.io/integrations/baserow/
- Matiz de la comunidad: los nodos de Airtable/Google Sheets ofrecen acciones "create/append/update" más pulidas que los de NocoDB/Baserow, aunque ambos cubren CRUD vía API. Fuente: https://n8n.io/integrations/baserow/and/nocodb/
- **API REST**: NocoDB expone API REST completa con tokens en self-hosted. **Baserow históricamente no implementó tokens de API en su variante self-hosted** (punto a favor de NocoDB para automatización con n8n/Python). NocoBase blog: https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives

### 4. Críticas y limitaciones reales (honestidad)
- **NocoDB — Hacker News, "Bad Experience with NoCoDB" (feb 2025):** https://news.ycombinator.com/item?id=43108868 . Conclusión del autor: "no es suficientemente maduro para producción". Problemas reportados:
  - Integridad de datos: cambiar JSON a JSONB hace **desaparecer columnas** sin aviso; import CSV falla en silencio; borrar varias filas sin guardar borra todas.
  - UI/UX: borrado de fila se **cuelga ~50%** de las veces (requiere recargar); **sin función deshacer (undo)**; borrar tabla con solo 3 clics (riesgo de borrado accidental).
  - Funcional: sin UUID; filtros/orden en vistas por defecto afectan a **todos los usuarios** globalmente; "la mitad de las funciones no funcionan como aparentan". En el mismo hilo, Grist se mencionó (descartado como "poco inspirador") y Baserow como "tan cerca de la grandeza" pero con silos de datos.
  - **Sin colaboración en tiempo real**: en NocoDB hay que refrescar la página para ver cambios de otros; en Baserow es instantáneo. Fuente: https://blog.elest.io/nocodb-vs-baserow-which-open-source-airtable-alternative-should-you-pick/
- **Baserow — limitaciones:** Calendario/Kanban/Survey de pago; **sin app móvil**; tokens de API ausentes en self-hosted; stack más pesado (Django+PostgreSQL+Redis) que consume más recursos en el VPS. Fuentes: https://baserow.io/user-docs/pricing-plans , https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives
- **Teable — limitaciones:** más nueva, comunidad/plantillas más pequeñas, integraciones de terceros aún madurando, automatización limitada en free, despliegue solo Docker manual (no en CasaOS/YunoHost). Fuentes: https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives , https://github.com/teableio/teable
- **Instalación/mantenimiento en VPS:** la comunidad advierte que self-hosting exige manejar PostgreSQL, Redis, gateway, backups y actualizaciones; "los fundadores no técnicos pueden encontrar el setup intimidante". Fuente: https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives

### 5. ¿Autoalojar o simplemente pagar Airtable/Notion?
- El consenso para perfiles **no técnicos** es matizado pero claro en varias fuentes: **"Considera Airtable o Notion si no tienes experiencia en self-hosting"**; las opciones cloud de pago son "más seguras por la menor carga de mantenimiento" pese al mayor coste por usuario. Fuentes: https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives , https://selfh.st/alternatives/airtable/ (guía de self-hosting de Airtable)
- **Cuándo conviene cada uno:**
  - **Pagar (Airtable/Notion):** equipo no técnico, sin sysadmin, prioridad en fiabilidad y app móvil pulida, pocos usuarios. Airtable Team ronda ~$20-24/usuario/mes; para 1-2 usuarios entra holgado en el presupuesto de $70/mes.
  - **Autoalojar (NocoDB/Baserow/Teable):** quieres datos 100% propios, registros ilimitados gratis, y **ya tienes el VPS + n8n + alguien (tú vía Claude) que lo mantiene**. El coste marginal de la base de datos es ~$0 sobre el VPS existente.

## Contraste con el plan actual (¿NocoDB o Baserow? ¿autoalojar o pagar?)

**Entre NocoDB y Baserow, gana NocoDB para este caso** por tres razones decisivas:
1. **Calendario gratis.** Tu requisito #1 es calendario de reservas. En **Baserow self-hosted el Calendario es de pago** (Premium); en **NocoDB es gratis**. Esto por sí solo descarta el Baserow gratuito para tu necesidad central (o te obligaría a pagar Premium de Baserow, perdiendo la ventaja "gratis").
2. **API REST con tokens en self-hosted** y **nodo nativo en n8n** sólido: NocoDB se integra mejor con tu orquestador n8n y tus scripts Python. Baserow ha tenido carencia de tokens de API en self-hosted.
3. **Vistas completas gratis** (Grid + Calendar + Form + Kanban) cubren CRM, reservas, formulario de inventario y base para campañas sin pagar nada.

**Peros honestos sobre NocoDB que debes asumir:**
- Críticas serias de fiabilidad en Hacker News (feb 2025): bugs de borrado, sin undo, riesgos de integridad de datos. → **Mitigación:** backups automáticos del PostgreSQL, versión estable reciente, y que el usuario opere sobre vistas/formularios (no edición masiva de esquema).
- **Sin app móvil nativa**: en Android se usará como **web/PWA responsive** desde el navegador. Para "actualizar inventario desde el móvil", lo robusto es un **Formulario** de NocoDB (URL compartible) en lugar de editar el grid en pantalla pequeña.
- Sin tiempo real (refrescar para ver cambios) — irrelevante con un solo operador.

**Alternativa a vigilar:** **Teable** es técnicamente la más atractiva (Postgres, Calendario gratis, UI moderna, Docker ligero), pero su **menor madurez/comunidad** la hace más arriesgada que NocoDB para un negocio operado por alguien no técnico. Buena candidata para reevaluar en 6-12 meses.

**¿Autoalojar o pagar?** **Validado autoalojar con matices.** Como **ya tienes VPS + n8n** y Claude actúa como el "técnico" que instala y mantiene, autoalojar NocoDB es coherente y mantiene el coste cercano a $0 dentro del presupuesto de $70/mes. **Pero** si en la práctica el mantenimiento (backups, updates, caídas) supera tu capacidad, la recomendación de la comunidad es legítima: **pagar Airtable Team (1-2 asientos) cabe en el presupuesto** y elimina la carga operativa y el riesgo de bugs. Recomendación pragmática: **arranca con NocoDB autoalojado con backups bien configurados**, y ten Airtable como plan B documentado.

## Fuentes (URLs)

- XDA Developers — NocoDB la mejor alternativa autoalojada: https://www.xda-developers.com/nocodb-is-the-best-self-hosted-airtable-alternative/
- NocoBase — 5 alternativas autoalojadas comparadas (coste/funciones): https://www.nocobase.com/en/blog/5-self-hosted-airtable-alternatives
- elest.io — NocoDB vs Baserow: https://blog.elest.io/nocodb-vs-baserow-which-open-source-airtable-alternative-should-you-pick/
- Softr — Baserow vs NocoDB (2026): https://www.softr.io/blog/baserow-vs-nocodb
- Baserow — Best Airtable Alternative Tools (2026): https://baserow.io/blog/best-airtable-alternatives
- Baserow — límites del free tier (foro comunidad): https://community.baserow.io/t/baserow-free-tier-limits/211
- Baserow — planes y precios (Calendario = Premium): https://baserow.io/user-docs/pricing-plans
- Grist — Grist vs Baserow (Baserow self-hosted gratis sin calendar/kanban): https://www.getgrist.com/lookup/grist-vs-baserow/
- NocoDB docs — Vistas: https://nocodb.com/docs/product-docs/views
- NocoDB docs — Vista Calendario: https://nocodb.com/docs/product-docs/views/view-types/calendar
- NocoDB — Community vs Enterprise: https://nocodb.com/docs/product-docs/cloud-enterprise-edition/community-vs-paid-editions
- n8n — nodo NocoDB (docs): https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.nocodb/
- n8n — integración NocoDB: https://n8n.io/integrations/nocodb/
- n8n — integración Baserow: https://n8n.io/integrations/baserow/
- n8n — Baserow + NocoDB (matiz CRUD): https://n8n.io/integrations/baserow/and/nocodb/
- Hacker News — "Bad Experience with NoCoDB" (feb 2025): https://news.ycombinator.com/item?id=43108868
- GitHub — NocoDB: https://github.com/nocodb/nocodb
- GitHub — issue responsive/móvil NocoDB #158: https://github.com/nocodb/nocodb/issues/158
- GitHub — cliente móvil NocoDB (prototipo no oficial): https://github.com/enm10k/nocodb-mobile
- Foro NocoDB — NocoDB en Android: https://community.nocodb.com/t/nocodb-on-android-mar-25/272
- GitHub — Teable: https://github.com/teableio/teable
- selfh.st — Guía self-hosting alternativas a Airtable: https://selfh.st/alternatives/airtable/

# Fase 0 — Guía de cimientos (paso a paso)

> Esta es la infraestructura base sobre la que corre todo el sistema. Hazla **una vez**.
> Como la verificación de Meta tarda días, **empieza la Parte A y la Parte B en paralelo**.
> Marca cada casilla `[ ]` a medida que avanzas.

## Visión general — qué vamos a montar

```
        Cliente escribe por WhatsApp / Instagram / Facebook
                                │
                     [ APIs oficiales de Meta ]
                                │
                          [ Chatwoot ]   ← bandeja: el dueño ve todo y retoma (handoff)
                                │ (webhook)
                            [ n8n ]      ← lógica: llama a Claude y a la base de datos
                           ╱        ╲
                   [ Claude API ]   [ NocoDB ]  ← CRM, reservas, inventario, clientes
                                
   Chatwoot + n8n + NocoDB viven en UN VPS (servidor en la nube, encendido 24/7)
```

**Costos aproximados de esta fase:** VPS 8 GB ~$15–25/mes · dominio ~$10–15/año ·
Meta y el software (Chatwoot/n8n/NocoDB): gratis.

---

## Parte A — Meta Business + WhatsApp Cloud API

> Objetivo: tener el número de WhatsApp del negocio conectado a la API oficial, más
> Instagram y Messenger, todo en una sola App de Meta. **Empieza esto primero** (la
> verificación tarda).

- [ ] **A1. Cuenta de Meta Business.** Entra a [business.facebook.com](https://business.facebook.com)
  e inicia o crea el **Business Manager** del negocio.
- [ ] **A2. Verificación del negocio con el RUC.** En *Configuración del negocio →
  Centro de seguridad → Verificación del negocio*, sube los datos y el **RUC** (Perú).
  Esto es lo que puede tardar **días**; inícialo cuanto antes.
- [ ] **A3. Crear la App.** Ve a [developers.facebook.com](https://developers.facebook.com)
  → *Mis Apps → Crear App → tipo "Negocio (Business)"*. Vincúlala al Business Manager.
- [ ] **A4. Añadir WhatsApp.** Dentro de la App → *Agregar producto → WhatsApp → Configurar*.
  Meta te da un **número de prueba** gratis para empezar a testear de inmediato.
- [ ] **A5. Registrar el número real.** Cuando vayas a producción, agrega y verifica el
  número de WhatsApp del negocio (no debe estar activo en la app normal de WhatsApp).
- [ ] **A6. Datos que necesito guardar en `.env`:**
  - `META_PHONE_NUMBER_ID` → en *WhatsApp → Configuración de la API* (debajo del número).
  - `META_ACCESS_TOKEN` → genera un **token permanente** con un **Usuario del sistema**
    (*Configuración del negocio → Usuarios → Usuarios del sistema → Generar token*),
    con permisos `whatsapp_business_messaging` y `whatsapp_business_management`. El token
    temporal de la pantalla inicial caduca en 24 h; el del usuario del sistema no.
  - `META_VERIFY_TOKEN` → una palabra/clave que **tú inventas** (ej. `casa-campo-2026`);
    se usa para validar el webhook (paso A8). Debe coincidir en Meta y en n8n.
- [ ] **A7. Instagram + Messenger.** Conecta la **Página de Facebook** del negocio y la
  **cuenta de Instagram profesional** a la App, y añade los productos *Messenger* e
  *Instagram*. (Estos canales se enchufan luego a Chatwoot.)
- [ ] **A8. Webhook.** El webhook (la URL pública a la que Meta envía los mensajes) se
  configura **después** de tener el VPS con HTTPS y Chatwoot/n8n arriba (Parte B). Apunta
  a la URL de Chatwoot/n8n y usa el `META_VERIFY_TOKEN` del paso A6.

📎 Docs: WhatsApp Cloud API — https://developers.facebook.com/docs/whatsapp/cloud-api

---

## Parte B — VPS (el servidor 24/7)

> Objetivo: un servidor en la nube con Docker, donde corren Chatwoot + n8n + NocoDB.

- [ ] **B1. Contratar el VPS.** Proveedores recomendados por relación precio/recursos:
  - **Contabo** (muy barato, 8 GB ~$8–13/mes), **Hostinger VPS**, o **Hetzner** (excelente, ~€15).
  - Pide **mínimo 4 GB RAM; ideal 8 GB** y 2–4 vCPU. Sistema: **Ubuntu 24.04 LTS**.
- [ ] **B2. Acceso.** Anota la **IP pública** del VPS y conéctate por SSH
  (en Windows: PowerShell → `ssh root@TU_IP`). El proveedor te da la contraseña inicial.
- [ ] **B3. Actualizar e instalar Docker:**
  ```bash
  apt update && apt upgrade -y
  curl -fsSL https://get.docker.com | sh
  apt install -y docker-compose-plugin
  ```
- [ ] **B4. Seguridad básica (recomendado):** crear un usuario no-root, activar el
  firewall (`ufw allow OpenSSH; ufw allow 80; ufw allow 443; ufw enable`).

---

## Parte C — Dominio y HTTPS (obligatorio para los webhooks)

> Meta y Chatwoot necesitan URLs públicas con **HTTPS**. Para eso hace falta un dominio.

- [ ] **C1. Comprar un dominio** barato (Namecheap, Cloudflare, GoDaddy) ~$10–15/año.
  Ej.: `casadecampo.app`.
- [ ] **C2. Crear 3 subdominios** apuntando (registro DNS tipo A) a la **IP del VPS**:
  - `chat.tudominio.com` → Chatwoot
  - `n8n.tudominio.com` → n8n
  - `db.tudominio.com` → NocoDB
- [ ] **C3. HTTPS automático.** Usar un **reverse proxy** que saca certificados gratis de
  Let's Encrypt solo: recomendado **Caddy** (el más simple) o **Nginx Proxy Manager**
  (con interfaz web). Esto da el candado 🔒 a los 3 subdominios.

---

## Parte D — Desplegar los servicios (Docker)

> Se despliegan con `docker compose`. **Yo te puedo generar los archivos
> `docker-compose.yml` y la config del proxy** listos para pegar — solo dímelo.

- [ ] **D1. NocoDB** + su PostgreSQL (la base de datos del negocio).
- [ ] **D2. n8n** (orquestador) conectado al mismo PostgreSQL o al suyo.
- [ ] **D3. Chatwoot** (bandeja) — necesita PostgreSQL + Redis (lo trae su compose oficial).
- [ ] **D4. Caddy / Nginx Proxy Manager** enrutando los 3 subdominios con HTTPS.
- [ ] **D5. Conectar los canales en Chatwoot:** WhatsApp (Cloud API), Instagram y
  Facebook, usando los datos de la Parte A.

📎 Docs: Chatwoot self-hosted — https://www.chatwoot.com/docs/self-hosted ·
n8n Docker — https://docs.n8n.io/hosting/ · NocoDB — https://nocodb.com/docs

---

## Parte E — Backups (no opcional)

> NocoDB tiene críticas de fiabilidad; sin backups un error puede costar datos.

- [ ] **E1.** Backup automático diario del PostgreSQL (un `cron` con `pg_dump` o el
  add-on de respaldo del proveedor del VPS).
- [ ] **E2.** Guardar una copia fuera del VPS (ej. un bucket barato o tu PC).

---

## Checklist final de la Fase 0

- [ ] Negocio verificado en Meta con el RUC.
- [ ] App de Meta con WhatsApp + Instagram + Messenger.
- [ ] `META_ACCESS_TOKEN`, `META_PHONE_NUMBER_ID`, `META_VERIFY_TOKEN` obtenidos.
- [ ] VPS con Docker y firewall.
- [ ] Dominio con 3 subdominios y HTTPS.
- [ ] Chatwoot + n8n + NocoDB corriendo y accesibles por sus URLs.
- [ ] Canales conectados en Chatwoot.
- [ ] Backups del PostgreSQL activos.
- [ ] Datos sensibles cargados en el `.env` del proyecto (nunca en GitHub).

Cuando esto esté listo, pasamos a la **Fase 1**: cargar los workflows en n8n y conectar
los tools de Python (`ai_reply.py`, `db_client.py`, `meta_send.py`).

---

## Qué necesito de ti para ayudarte mejor

1. ¿Quieres que **genere los archivos `docker-compose.yml`** (Chatwoot + n8n + NocoDB +
   proxy con HTTPS) listos para pegar en el VPS?
2. ¿Ya tienes **dominio**? Si no, te recomiendo uno y dónde comprarlo.
3. ¿Prefieres **Caddy** (más simple, todo por archivo) o **Nginx Proxy Manager** (con
   interfaz web para clic)?

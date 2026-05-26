# Despliegue de la infraestructura (Fase 0)

Levanta en un VPS: **Caddy** (HTTPS) + **PostgreSQL** + **Redis** + **NocoDB** + **n8n**
+ **Chatwoot**. Sigue los pasos en orden.

> Plantilla de arranque. Si algo falla en el primer arranque (sobre todo Chatwoot),
> lo ajustamos juntos viendo los logs.

---

## ⚡ Recomendado: probar PRIMERO en tu PC (local)

Antes de tocar el VPS, valida que todo levante en tu PC con **Docker Desktop**. Lo que
funcione en local funcionará casi igual en el VPS.

1. Instala **Docker Desktop** (Windows, con WSL2) y ábrelo.
2. En la carpeta `deploy/`, crea el `.env` (igual que el paso 2 de abajo).
3. Levanta en modo local (sin Caddy/HTTPS, por `localhost`):
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.local.yml up -d
   docker compose -f docker-compose.yml -f docker-compose.local.yml logs -f
   ```
4. Abre en el navegador y crea las cuentas:
   - NocoDB → http://localhost:8080
   - n8n → http://localhost:5678
   - Chatwoot → http://localhost:3000
5. Detener: `docker compose -f docker-compose.yml -f docker-compose.local.yml down`

**Qué se prueba en local:** que los servicios levanten y se comuniquen, crear cuentas,
modelar tablas en NocoDB y construir el workflow de n8n. **Lo único que NO** se puede
probar en local son los **webhooks de Meta** (localhost no es público); para eso, en su
momento, se usa un túnel temporal (ngrok / cloudflared) o ya directamente el VPS.

Requisito de RAM: levantar todo a la vez consume bastante; ten varios GB libres.

---

## Despliegue en el VPS (producción)

## Requisitos previos
- [ ] **VPS** con Ubuntu 24.04, **≥4 GB RAM (ideal 8 GB)**, con Docker instalado
  (ver [../docs/fase-0-cimientos.md](../docs/fase-0-cimientos.md), Parte B).
- [ ] **Dominio** con 3 subdominios apuntando (registro DNS tipo A) a la IP del VPS:
  `chat.TUDOMINIO`, `n8n.TUDOMINIO`, `db.TUDOMINIO`.
- [ ] Puertos **80** y **443** abiertos en el firewall.

## Pasos

1. **Copiar esta carpeta al VPS** (por ejemplo con `scp` o clonando el repo):
   ```bash
   git clone https://github.com/kocheluis/Casa-de-campo-agente.git
   cd Casa-de-campo-agente/deploy
   ```

2. **Crear el archivo de secretos** a partir del ejemplo y rellenarlo:
   ```bash
   cp .env.deploy.example .env
   nano .env
   ```
   Genera las claves que faltan con:
   ```bash
   openssl rand -hex 24    # para N8N_ENCRYPTION_KEY
   openssl rand -hex 64    # para CHATWOOT_SECRET_KEY_BASE
   ```

3. **Permisos del script de base de datos:**
   ```bash
   chmod +x init-db.sh
   ```

4. **Levantar todo** (en el VPS sí incluimos Caddy con el profile `proxy`):
   ```bash
   docker compose --profile proxy up -d
   ```
   La primera vez tarda (descarga imágenes y Chatwoot prepara su base de datos).
   Sigue el avance con:
   ```bash
   docker compose logs -f
   ```

5. **Verificar en el navegador** (Caddy emite el certificado HTTPS solo la primera vez):
   - `https://db.TUDOMINIO`   → NocoDB (crea tu cuenta de admin)
   - `https://n8n.TUDOMINIO`  → n8n (crea el usuario propietario)
   - `https://chat.TUDOMINIO` → Chatwoot (crea la cuenta de admin)

6. **Obtener las credenciales para el proyecto** y ponerlas en el `.env` de la raíz
   (el del framework WAT, no este):
   - **NocoDB:** crea un *API Token* → `DB_API_TOKEN`; arma `DB_API_URL` con el id de tabla.
   - **Chatwoot:** perfil → *Access Token* → `CHATWOOT_API_TOKEN`, y la URL base + account id.

## Comandos útiles
| Acción | Comando |
|---|---|
| Ver estado | `docker compose ps` |
| Ver logs de un servicio | `docker compose logs -f chatwoot-rails` |
| Reiniciar un servicio | `docker compose restart n8n` |
| Detener todo (datos a salvo) | `docker compose down` |
| Actualizar imágenes (VPS) | `docker compose --profile proxy pull && docker compose --profile proxy up -d` |

## Backups (Fase 0 — no opcional)
Respaldo diario del PostgreSQL (ajusta y ponlo en un `cron`):
```bash
docker compose exec -T postgres pg_dumpall -U postgres > backup_$(date +%F).sql
```
Guarda una copia **fuera del VPS**.

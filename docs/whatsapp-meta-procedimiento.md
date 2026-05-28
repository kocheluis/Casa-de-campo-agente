# Registrar el WhatsApp del negocio en Meta (Cloud API)

> Decisión clave a tomar **antes** de empezar: ¿usar el número personal de Gerardo o un
> número nuevo dedicado al negocio? Ver pros/contras al final.

## Visión general — qué es esto

Para que el bot responda WhatsApp **automáticamente**, el número del negocio tiene que
estar registrado en la **WhatsApp Business Platform (Cloud API)** de Meta. No es la app
normal de WhatsApp ni la app "WhatsApp Business" — es una API que vive en la nube de Meta.

Importante: **un número solo puede estar en uno** — o en la app normal, o en WhatsApp
Business, o en la Cloud API. **No en dos lados a la vez.** Pasar un número de la app a la
API significa que **dejas de poder usar ese WhatsApp en el móvil** (los chats antiguos
de ese número en la app se pierden o quedan congelados).

---

## Procedimiento paso a paso

### Paso 0 — Prerrequisitos
- [ ] **Cuenta de Meta Business** creada (lo hace Gerardo con su email).
- [ ] **Verificación del negocio con RUC** iniciada *(la del docs/fase-0-cimientos.md, Parte A)*.
- [ ] **Página de Facebook** del negocio (Meta la necesita para vincular).
- [ ] **Cuenta de Instagram Business o Creator** (no personal). Se puede convertir desde
  la app de Instagram → *Settings → Account → Switch to Professional Account*.

### Paso 1 — Crear la "WhatsApp Business Account" (WABA)
1. Entra a [business.facebook.com](https://business.facebook.com) → tu negocio.
2. *Configuración del negocio → Cuentas → Cuentas de WhatsApp → **Agregar**.*
3. Acepta términos.

### Paso 2 — Crear la App de desarrollador
1. Ve a [developers.facebook.com/apps](https://developers.facebook.com/apps) → **Crear App** → tipo **"Business"**.
2. Vincula al Business Manager.
3. Dentro de la App → *Agregar producto → **WhatsApp** → Configurar*.

### Paso 3 — Agregar y verificar el número
1. En la sección *WhatsApp → API Setup* tienes un **número de prueba** gratis (sirve para
   testear localmente sin compromiso).
2. Cuando vayas a producción: clic en **Agregar número de teléfono**.
3. Importante — **antes** de agregarlo:
   - Si ese número está en la app de WhatsApp o WhatsApp Business → **bórralo de ahí**
     primero (*Configuración → Cuenta → Eliminar mi cuenta*). Se pierden los chats.
   - El número debe poder recibir SMS o llamada (para el código de verificación).
4. Mete el número con código de país (sin +). Ej. para Perú: `51999000111`.
5. Elige **SMS o llamada** para verificar → recibes un código de 6 dígitos → lo metes.
6. ✅ Listo: el número quedó en la API. Anota el **Phone Number ID** (se ve en la API Setup).

### Paso 4 — Token permanente
El token que se ve por defecto en la pantalla **caduca en 24 horas**. Para tener uno
permanente:
1. *Configuración del negocio → Usuarios → Usuarios del sistema → **Agregar***.
2. Crea un usuario tipo *Administrador* (ej. "bot-casa-campo").
3. Asígnale permisos sobre tu App y tu WABA.
4. Clic en **Generar token** → marca los scopes:
   `whatsapp_business_messaging`, `whatsapp_business_management`.
5. Caducidad: **nunca** o **60 días** (elige nunca). **Cópialo y guárdalo en el `.env`** —
   no se vuelve a mostrar.

### Paso 5 — Nombre comercial (display name)
1. En el WABA → *Configuración → Perfil → Nombre para mostrar*.
2. Meta tarda **1-2 días** en aprobarlo (debe coincidir razonablemente con el negocio
   verificado por RUC).

### Paso 6 — Webhook
1. *WhatsApp → Configuración → Webhook → Configurar Webhooks*.
2. Pega la URL pública HTTPS donde corre Chatwoot/n8n (ej. `https://chat.tudominio.com/...`).
3. Pega el **Verify Token** que tú inventaste (el `META_VERIFY_TOKEN` del `.env`).
4. Suscríbete al campo **messages**.
5. Meta hace un ping de validación; si el token coincide, lo da por OK.

### Paso 7 — Plantillas de mensaje *(para campañas y para iniciar fuera de 24h)*
1. En el WABA → *Plantillas de mensaje → Crear*.
2. Elige categoría: **Utility** (recordatorios, confirmaciones) o **Marketing** (promos).
3. Escribe el contenido con variables `{{1}}`, `{{2}}` etc.
4. Meta tarda **~24 h** en aprobar cada plantilla.

---

## Tiempos (realistas)

| Paso | Tiempo |
|---|---|
| Verificación del negocio con RUC | **1-7 días** (a veces más; depende de Meta) |
| Crear WABA + App | minutos |
| Verificar el número (SMS) | minutos |
| Token permanente | minutos |
| Aprobación del display name | 1-2 días |
| Aprobación de cada plantilla | ~24 h |
| **Tiempo total para estar 100% productivo** | **3-10 días** desde que arrancas |

**Recomendación:** **inicia el paso de Verificación del negocio el día 1** del proyecto.
Es lo que más tarda y bloquea todo lo demás.

---

## Costos (precios oficiales de Meta — pueden cambiar, confirmar en
[developers.facebook.com/docs/whatsapp/pricing](https://developers.facebook.com/docs/whatsapp/pricing))

Meta cambió en 2024-2025 al modelo **per-message** (antes era per-conversation).

| Tipo de mensaje | Quién lo inicia | Costo aprox. (Perú) |
|---|---|---|
| **Service** (dentro de los 24 h desde el último mensaje del cliente) | Cliente o negocio | **GRATIS** |
| **Utility** (plantilla aprobada: confirmación de reserva, recordatorio, ticket) | Negocio | ~$0.005-0.02 USD por mensaje |
| **Marketing** (plantilla de promoción) | Negocio | ~$0.04-0.10 USD por mensaje |
| **Authentication** (OTP) | Negocio | ~$0.005 USD |

**Realidad para tu caso (casa de campo):**
- Los clientes escriben primero pidiendo info → entras en **ventana de servicio gratis 24h**.
- Confirmar fechas / enviar datos de pago → **gratis** (dentro de las 24h).
- Si Gerardo quiere reactivar una conversación pasada (ej. "hola, ¿qué tal aquel finde?")
  fuera de 24h → necesita una **plantilla aprobada** y paga ese mensaje.
- Si hace una campaña promocional → paga **Marketing**.

**Estimado mensual realista:** **$0-5 USD** para un negocio pequeño con respuestas
automáticas y alguna campaña ocasional. Es prácticamente gratis.

---

## ⚖️ Pros y contras de usar el número PERSONAL de Gerardo

### ✅ Pros
- **Continuidad** — sus clientes ya tienen ese número guardado.
- Lo encuentran en tarjetas, redes sociales, perfil de Google Maps, etc.
- Cero confusión para los clientes existentes.

### ❌ Contras (importantes)
- **Pierde WhatsApp personal en ese número.** No podrá responder mensajes a su familia,
  amigos o cualquiera por la app normal con ese mismo número. **Todos los chats
  llegarán al sistema del negocio** (Chatwoot), no a su teléfono.
- **Pierde los chats antiguos** de ese número en su app (se borran al eliminar la cuenta
  para migrar).
- **Mezcla vida personal y laboral.** Mamá, esposa, amigos quedarían atrapados en el
  flujo del bot/Chatwoot, lo que es incómodo y poco profesional.
- **Riesgo de baneo del número** — si alguien (incluso por error) lo reporta como spam,
  Meta puede limitar o bloquear el número y queda sin WhatsApp en ambos roles.
- **Difícil revertir.** Sacar un número de Cloud API requiere trámite. Volver a usarlo
  en la app personal es engorroso.
- **Confusión emocional** — Gerardo va a ver respuestas del bot como si las hubiera
  mandado él mismo. Se le hará raro.

### Alternativa recomendada: **número NUEVO dedicado al negocio**

- **Costo:** ~$5-10 USD una vez (chip nuevo) + plan básico mensual (~S/15-30/mes en Perú).
- **Cómo:** Gerardo compra un chip nuevo de Claro/Movistar/Entel, lo activa, y ese
  número es el que se registra en Meta.
- **Transición con clientes existentes:** publica en sus redes "ahora atendemos por este
  nuevo número 📱: …", lo pone en su perfil de Instagram/Facebook, y reenvía a ese
  número desde el viejo durante 1-2 meses.
- **Bonus:** Gerardo conserva su WhatsApp personal **intacto** para su vida fuera del
  trabajo.

> 💡 **Para un negocio formal con RUC, lo estándar de la industria es número dedicado.**
> Mi recomendación clara es: **número nuevo**.

### Excepción: ¿cuándo SÍ usar el personal?
Solo si Gerardo:
- Ya viene atendiendo el negocio desde ese número y lo tiene **muy** difundido entre clientes.
- Tiene poca o nula actividad personal en ese WhatsApp.
- Acepta perder la app personal en ese número para siempre.
- Está dispuesto a comprarse OTRO chip personal y migrarse él a ese.

---

## Checklist para hablar con Gerardo

- [ ] ¿Tiene ya un número exclusivo del negocio, o usa el personal?
- [ ] Si usa el personal: ¿está dispuesto a moverse a un número nuevo? Le explicas el
      por qué.
- [ ] Si insiste en el personal: ¿está consciente de que pierde el WhatsApp personal en
      ese número?
- [ ] ¿Tiene RUC activo y vigente?
- [ ] ¿Tiene página de Facebook del negocio?
- [ ] ¿Tiene Instagram **profesional** (Business o Creator), no personal?
- [ ] ¿Email del negocio para crear las cuentas?

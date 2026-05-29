# Pendientes con Gerardo — segunda ronda

> Lista limpia de info que falta o quedó ambigua tras la entrevista del 2026-05-29.
> Pensada para enviarse en 1-2 mensajes cortos de WhatsApp, no en otra reunión larga.
> El orden es por **prioridad de desbloqueo del proyecto**.

## 🚨 CRÍTICO — bloquea Fase 0 (Meta Business)

1. **RUC.** Gerardo dijo "puedo crearlo". Sin RUC, Meta no nos verifica el negocio y el
   bot no puede activarse en WhatsApp. Tipo recomendado: **persona natural con
   negocio**. Trámite online en SUNAT (~30 minutos). **Hacerlo esta semana.**

## 📎 Listas que se comprometió a enviar (mientras antes, mejor)

2. **Lista de utensilios de cocina** (la que ya maneja con la persona de mantenimiento).
3. **Lista de juegos y áreas** de la casa (todo lo que el huésped puede usar).
4. **Material audiovisual**: fotos y videos de la casa, exteriores, interior, piscina,
   parrilla. Sirve para Fase 3 (video automático) y para que la base de conocimiento
   gane peso.
5. **5-10 capturas/copias de chats reales** que él haya respondido a clientes —
   para afinar el tono y los modismos exactos del bot.

## 🏡 Datos de la propiedad que no quedaron claros

6. **Número de habitaciones** y tipo de camas en cada una.
7. **Cuántos baños** hay.
8. **¿Hay wifi?** Velocidad / clave para los huéspedes.
9. **¿Hay TV con Netflix u otros streaming?**
10. **Tiempo / referencia desde Lima**: ¿cuánto demora desde el centro? ¿Hay
    transporte público o solo en carro?
11. **El aforo de 15 personas: ¿incluye personas pernoctando o solo es para
    reuniones?** (suelen ser distintos: pueden caber 10 durmiendo y hasta 15 en una
    reunión, por ejemplo).

## 💵 Reservas y pagos — faltan detalles

12. **Política de cancelación**: si el cliente paga el 20% y después cancela, ¿se
    devuelve el adelanto, se mantiene, hay un % no reembolsable, depende de cuántos
    días antes? El bot necesita saberlo para no escalar siempre.
13. **Métodos de pago específicos**: ¿qué cuenta bancaria, Yape, Plin? Esto no se
    mete en el bot (Gerardo lo pasa al cerrar), pero conviene tenerlo claro para
    armar la plantilla de WhatsApp que él enviará al confirmar.
14. **Devolución de garantía**: ¿en cuánto tiempo se devuelve la garantía de S/ 300?
    El día del check-out, en 24 horas, en una semana...
15. **¿Pide DNI / edad mínima?** Para reservas y check-in.

## 🚭 Reglas

16. **Política de fumadores**: ¿se puede fumar dentro de la casa, solo afuera, está
    totalmente prohibido?

## 📲 Datos administrativos para Meta y herramientas (necesarios para Fase 0)

17. **Email del negocio** para crear cuentas en NocoDB, Chatwoot, Anthropic, etc.
18. **Página de Facebook** del negocio (URL).
19. **Cuenta de Instagram en modo Business o Creator** (no personal) — URL.
    Si está en modo personal, se convierte gratis en *Settings → Account → Switch
    to Professional Account*.
20. **Confirmación de que el número actual de WhatsApp** sigue activo y va a usarse
    para el negocio (decisión ya tomada — solo confirmar).

## 🤔 Decisiones por confirmar

21. **¿Dominio del negocio?** Para las URLs del VPS (`chat.tudominio.com`,
    `n8n.tudominio.com`, `db.tudominio.com`). Si no tiene, sugerimos `gerardushouse.com`
    o `.pe`. Cuesta ~S/40-60 al año.
22. **¿Cuándo planea sacar el chip nuevo para personal?** Esto define cuándo
    activamos formalmente el bot y comenzamos la transición. Ver
    `docs/transicion-numero.md` para el calendario T-14/T-7/T-3/T-1.
23. **Campañas a futuro**: Gerardo dijo "probablemente a futuro". Queda registrado
    como Fase 4 del plan, sin urgencia.

---

## Mensaje sugerido para mandarle a Gerardo (copy/paste)

> ¡Hola Gerardo! Mientras voy preparando todo, **estos son los puntos sueltos** que
> me quedaron de la entrevista. Si me los puedes pasar cuando tengas un rato:
>
> **Urgente (esta semana):**
> 1. ¿Cuándo sacas el RUC? Sin eso no podemos activar el WhatsApp del bot.
>
> **Las listas que quedamos:**
> 2. Lista de utensilios de cocina.
> 3. Lista de juegos y áreas de la casa.
> 4. Fotos y videos para usar en las publicaciones.
> 5. Si puedes, **mándame capturas de 5-10 chats** que hayas respondido a clientes
>    (sirve para que el bot suene como tú).
>
> **Datos rápidos** (solo respóndeme en una línea cada uno):
> 6. ¿Cuántas habitaciones y baños tiene la casa?
> 7. ¿Wifi? ¿Tele con Netflix?
> 8. ¿Qué pasa con el adelanto si alguien cancela?
> 9. ¿Permites fumar dentro? ¿Solo afuera? ¿Para nada?
> 10. Email del negocio + tu Facebook y tu Instagram (en modo profesional, no
>     personal).
>
> Con eso ya queda redondo. ¡Gracias! 🙌

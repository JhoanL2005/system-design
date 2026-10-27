# Semana 10, Sesión 1: Colas de mensajes, procesamiento asíncrono y stateful vs. stateless

> Objetivo de la sesión: desacoplar dos componentes de un sistema mediante una cola de mensajes, y justificar por qué un servicio stateless facilita el escalamiento horizontal frente a uno stateful.

**Lectura previa de esta sesión:** [What are Message Queues and When to Use Them? (AlgoMaster)](https://blog.algomaster.io/p/message-queues)

**Referencia de esta sesión:** [Amazon SQS Developer Guide (AWS)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-setting-up.html)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-10-sesion-01
```

`cola.py` trae una cola de mensajes en memoria que trabaja como Amazon SQS: un mensaje recibido queda oculto hasta que alguien lo confirma, y `vencer_visibilidad()` devuelve a la cola los que nadie confirmó. `servicios.py` trae el repositorio de reservas y un servicio de correo que puedes tumbar con `correo.caido = True`. `infraestructura.py` trae un almacén compartido (como Redis) y el balanceador round robin de la Semana 8. Los tres archivos ya están completos: no los modifiques.

## Respuesta sobre la lectura

Según el artículo, ¿qué papel cumplen el productor, el consumidor y la cola? ¿Qué gana el productor al no esperar al consumidor?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

Al confirmar una reserva, ReservaU envía un correo. Si el servicio de correo se cae justo en ese momento, ¿qué pasa con la reserva y con el correo, tal como está escrito ReservaU hoy?

_(tu respuesta)_

## Ejercicio 1: Sacar el correo del camino de la reserva

Este ejercicio se resuelve en vivo, sobre `desacoplar_correo_ejercicio1.py`. Antes de que se muestre cada resultado, responde:

**Respuesta 1:** en la versión síncrona, con el correo caído, ¿qué le responde el servicio a ana? ¿Qué pasa cuando ana reintenta?

_(tu respuesta)_

**Respuesta 2:** en la versión con cola, con el correo caído, ¿qué le responde el servicio a ana, y dónde queda el correo mientras el proveedor no vuelve?

_(tu respuesta)_

## Durante los ConcepTests

**ConcepTest 1. Tu voto, antes de discutir en pareja** (A, B, C o D):

_(tu voto)_

**Tu razonamiento:**

_(tu respuesta)_

**Después de discutir en pareja, ¿cambiaste de voto? ¿Por qué?**

_(tu respuesta)_

**ConcepTest 2. Tu voto, antes de discutir en pareja** (A, B o C):

_(tu voto)_

**Tu razonamiento:**

_(tu respuesta)_

## Ejercicio 2: Un trabajador que no pierde mensajes

Ahora te toca a ti. `trabajador_confiable_ejercicio2.py` trae la clase `TrabajadorConfiable`, que recibe la cola de correos, el servicio de correo, una segunda cola para los mensajes que fallaron demasiadas veces y el número máximo de intentos.

1. Completa `procesar_uno()`: recibe, envía, y confirma solo lo que ya se envió o lo que agotó sus intentos (este último, después de publicarlo en la cola de mensajes muertos).
2. Corre las pruebas:
   ```
   pytest test_trabajador_confiable_ejercicio2.py
   ```
3. Responde: ¿qué pasaría con el mensaje si confirmaras antes de enviar y el trabajador cayera entre las dos líneas? ¿Qué muestra `test_al_menos_una_vez_puede_entregar_dos_veces` sobre el orden que elegiste?

_(tu respuesta)_

## Ejercicio 3: Una reserva en tres pasos, en varios servidores

`reserva_en_pasos_ejercicio3.py` trae `ServidorConEstado`, que guarda el borrador de cada estudiante (cancha elegida, hora elegida) en su propia memoria entre un paso y el siguiente. La primera prueba muestra qué le pasa detrás del balanceador.

1. Completa `ServidorSinEstado`: el mismo comportamiento, con el borrador en el `AlmacenCompartido` bajo la clave `"borrador:" + estudiante`.
2. Corre las pruebas:
   ```
   pytest test_reserva_en_pasos_ejercicio3.py
   ```
3. Responde: con `ServidorSinEstado`, ¿qué tienes que hacer para pasar de 2 a 10 servidores en un día de inscripciones? ¿Y con `ServidorConEstado`?

_(tu respuesta)_

4. Responde: el estado del borrador no desapareció, se mudó. ¿Dónde vive ahora, y qué de la Semana 9 tendrías que aplicarle para que no se vuelva el nuevo punto único de falla?

_(tu respuesta)_

5. Responde: otra salida sería configurar el balanceador para que mande siempre al mismo estudiante al mismo servidor (sesión persistente). ¿Qué pierde ana si ese servidor se reinicia a mitad de su reserva?

_(tu respuesta)_

### Checklist final

- [ ] `ServicioConCola.reservar` responde sin llamar al correo.
- [ ] `TrabajadorConfiable` confirma un mensaje solo después de enviarlo, o después de pasarlo a la cola de mensajes muertos.
- [ ] `ServidorSinEstado` no guarda ningún dato del estudiante en `self`.
- [ ] `ServidorSinEstado.elegir_hora` vuelve a guardar el borrador después de cambiarlo.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Designing robust and predictable APIs with idempotency (Stripe Engineering)](https://stripe.com/blog/idempotency)

En el Ejercicio 2, un mismo correo puede llegar dos veces. Si en vez de un correo fuera el cobro de la garantía de la cancha, ¿qué pasaría? ¿Cómo podría el servicio de pagos reconocer que una solicitud ya la procesó?

_(tu respuesta)_

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

Según el artículo, el **productor** es quien envía mensajes a la cola, sin seguir el estado del consumidor. El **consumidor** es quien lee los mensajes de la cola y los procesa. La **cola** es la estructura que guarda los mensajes hasta que alguien los consume; la administra un broker, que se encarga de entregarlos. La cola queda en medio para que productor y consumidor no tengan que hablarse directamente.

Al no esperar al consumidor, el productor gana tres cosas:
- **Asincronía:** publica el mensaje y sigue con su trabajo de inmediato, lo que mejora el throughput del sistema.
- **Desacoplamiento:** no necesita saber si el consumidor existe, si está disponible o si es lento. Cada uno funciona y escala por su lado.
- **Protección ante fallas y picos:** si el consumidor se atrasa o se cae, los mensajes se acumulan en la cola en vez de bloquear o tumbar al productor.

## Respuesta sobre la pregunta de la sesión pasada

Al confirmar una reserva, ReservaU envía un correo. Si el servicio de correo se cae justo en ese momento, ¿qué pasa con la reserva y con el correo, tal como está escrito ReservaU hoy?

Hoy (la `ServicioSincrono` del Ejercicio 1) la reserva y el correo están en el mismo camino: primero se registra la reserva y después, en la misma solicitud, se llama al correo. Si el correo se cae justo ahí, **la reserva queda registrada**, pero el servicio le responde `"error"` a la estudiante, y **el correo se pierde**: nadie lo guarda ni lo vuelve a intentar.

El sistema queda inconsistente: la estudiante cree que no reservó, pero la cancha está ocupada a su nombre, y si reintenta le responden `"ocupada"`. Un servicio secundario (el correo) termina tumbando la operación principal (la reserva).

## Ejercicio 1: Sacar el correo del camino de la reserva

Este ejercicio se resuelve en vivo, sobre `desacoplar_correo_ejercicio1.py`. Antes de que se muestre cada resultado, responde:

**Respuesta 1:** en la versión síncrona, con el correo caído, ¿qué le responde el servicio a ana? ¿Qué pasa cuando ana reintenta?

Le responde `"error"`, aunque la reserva sí quedó registrada: en el repositorio hay 1 reserva y se enviaron 0 correos. Cuando ana reintenta, le responde `"ocupada"`, porque la cancha está ocupada por su propia reserva. Ana no sabe si tiene la cancha o no, y no le llega ningún correo.

**Respuesta 2:** en la versión con cola, con el correo caído, ¿qué le responde el servicio a ana, y dónde queda el correo mientras el proveedor no vuelve?

Le responde `"confirmada"`, porque el servicio ya no llama al correo: registra la reserva, publica un mensaje y responde. Mientras el proveedor está caído, el correo queda **como un mensaje en la cola** (`Mensajes esperando en la cola: 1`). Cuando el correo vuelve, el `TrabajadorDeCorreo` recibe el mensaje, envía el correo y confirma el mensaje: `Correos enviados: 1` y la cola queda en 0. La caída del correo solo atrasa el correo; ya no afecta la reserva.

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

Si confirmara antes de enviar y el trabajador cayera entre las dos líneas, **el mensaje se perdería para siempre**: la cola ya lo borró, así que `vencer_visibilidad()` no lo devuelve, y el correo nunca salió. Lo probé confirmando sin enviar y venciendo la visibilidad: la cola queda con 0 mensajes disponibles, 0 en proceso y 0 correos enviados. Ese orden da entrega *a lo más una vez*.

Por eso elegí enviar primero y confirmar después: si el trabajador cae entre las dos líneas, el mensaje no se confirmó, vuelve a la cola cuando vence la visibilidad y otro intento lo envía.

`test_al_menos_una_vez_puede_entregar_dos_veces` muestra el costo de ese orden. Simula un trabajador que alcanzó a enviar el correo pero cayó antes de confirmar: el mensaje vuelve, se envía de nuevo y ana recibe **2 correos**. Es entrega *al menos una vez*: no se pierde ningún mensaje, a cambio de que alguno pueda llegar duplicado. Para un correo de confirmación, un duplicado es una molestia aceptable; perder la confirmación no.

## Ejercicio 3: Una reserva en tres pasos, en varios servidores

`reserva_en_pasos_ejercicio3.py` trae `ServidorConEstado`, que guarda el borrador de cada estudiante (cancha elegida, hora elegida) en su propia memoria entre un paso y el siguiente. La primera prueba muestra qué le pasa detrás del balanceador.

1. Completa `ServidorSinEstado`: el mismo comportamiento, con el borrador en el `AlmacenCompartido` bajo la clave `"borrador:" + estudiante`.
2. Corre las pruebas:
   ```
   pytest test_reserva_en_pasos_ejercicio3.py
   ```
3. Responde: con `ServidorSinEstado`, ¿qué tienes que hacer para pasar de 2 a 10 servidores en un día de inscripciones? ¿Y con `ServidorConEstado`?

**Con `ServidorSinEstado`:** solo hay que levantar 8 servidores más, idénticos, conectados al mismo repositorio, a la misma cola y al mismo almacén, y agregarlos al balanceador (`balanceador.agregar(...)`). No hay que mover datos ni avisarle a nadie: como el borrador vive en el almacén, cualquier servidor puede atender cualquier paso, incluso el de una reserva que empezó antes de agregarlos. Al terminar el día se pueden apagar igual de fácil. Lo probé con 10 reservas, agregando 8 servidores a mitad: se confirmaron 10 de 10.

**Con `ServidorConEstado`:** no basta con agregar servidores. Detrás de un round robin ya falla con 2, que es lo que muestra la primera prueba: el paso 2 cae en otro servidor y responde `"sin borrador"`. En la misma prueba de 10 reservas, se confirmaron 0 de 10. Para usarlo habría que configurar sesiones persistentes en el balanceador. Aun así, los servidores nuevos solo recibirían a estudiantes nuevos (no se puede repartir la carga de los que ya están en curso), y no se puede apagar ni reiniciar un servidor sin perder los borradores de todos sus estudiantes.

4. Responde: el estado del borrador no desapareció, se mudó. ¿Dónde vive ahora, y qué de la Semana 9 tendrías que aplicarle para que no se vuelva el nuevo punto único de falla?

Ahora vive en el `AlmacenCompartido` (en un sistema real, un Redis al que se conectan todos los servidores), bajo la clave `"borrador:" + estudiante`. Los servidores quedaron sin estado, pero si ese almacén se cae, ningún estudiante puede avanzar su reserva: es el nuevo punto único de falla.

De la Semana 9 le aplicaría:
- **Replicación:** una primaria con al menos una réplica y conmutación por error (failover), para que si la primaria cae, una réplica tome su lugar. Con el mismo cuidado de esa semana: la replicación es asincrónica, y `elegir_hora` lee el borrador justo después de que `iniciar` lo escribió. Esas lecturas tienen que ir a la primaria (leer lo que uno mismo escribió); si no, una réplica atrasada respondería `"sin borrador"`.
- **Sharding**, si el almacén creciera más de lo que cabe en un nodo: por hash del estudiante. Cada paso busca el borrador de un solo estudiante, así que todas las consultas quedan dirigidas a un solo shard.

5. Responde: otra salida sería configurar el balanceador para que mande siempre al mismo estudiante al mismo servidor (sesión persistente). ¿Qué pierde ana si ese servidor se reinicia a mitad de su reserva?

Pierde **su borrador**: la cancha y la hora que ya había elegido vivían solo en la memoria de ese servidor. Cuando el servidor se reinicia, el siguiente paso responde `"sin borrador"` y ana tiene que empezar la reserva desde cero. Mientras tanto, otro estudiante puede quedarse con la hora que ella había elegido, porque el borrador no la apartaba. Lo que ya estaba confirmado no se pierde, porque está en el repositorio.

Además, la sesión persistente ata a cada estudiante a un servidor: la carga no se reparte de forma pareja, y agregar servidores no alivia a los que ya están cargados.

### Checklist final

- [x] `ServicioConCola.reservar` responde sin llamar al correo.
- [x] `TrabajadorConfiable` confirma un mensaje solo después de enviarlo, o después de pasarlo a la cola de mensajes muertos.
- [x] `ServidorSinEstado` no guarda ningún dato del estudiante en `self`.
- [x] `ServidorSinEstado.elegir_hora` vuelve a guardar el borrador después de cambiarlo.
- [x] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Designing robust and predictable APIs with idempotency (Stripe Engineering)](https://stripe.com/blog/idempotency)

En el Ejercicio 2, un mismo correo puede llegar dos veces. Si en vez de un correo fuera el cobro de la garantía de la cancha, ¿qué pasaría? ¿Cómo podría el servicio de pagos reconocer que una solicitud ya la procesó?

Si fuera el cobro de la garantía, una entrega duplicada sería **cobrarle dos veces** a la estudiante. Un correo repetido es una molestia; un cobro repetido es plata que hay que devolver y un reclamo. Con entrega al menos una vez, el duplicado no es raro: pasa cada vez que un trabajador cobra y cae antes de confirmar el mensaje.

El servicio de pagos podría reconocerlo con una **clave de idempotencia**: un identificador único de la operación, por ejemplo `"garantia-" + id de la reserva`, generado una sola vez y enviado en el mensaje y en cada reintento. El servicio guarda cada clave que ya procesó junto con su resultado. Si llega una solicitud con una clave conocida, devuelve el resultado guardado sin cobrar otra vez.

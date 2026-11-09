# Semana 10, Sesión 2: Diseño de APIs REST: contratos, versionado, idempotencia

> Objetivo de la sesión: diseñar un endpoint REST idempotente y una estrategia de versionado que no rompa a los clientes existentes de la API.

**Lectura previa de esta sesión:** [Designing robust and predictable APIs with idempotency (Stripe Engineering)](https://stripe.com/blog/idempotency)

**Referencia de esta sesión:** [API Design Guide (Google Cloud)](https://docs.cloud.google.com/apis/design)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-10-sesion-02
```

`http_simulado.py` trae una versión mínima de HTTP: `Solicitud`, `Respuesta`, un `Cliente` que reenvía la misma solicitud si no le llega respuesta, y una `RedInestable` que entrega cada solicitud a la API pero pierde las primeras respuestas en el camino de vuelta. `dominio.py` trae el repositorio de reservas y la pasarela que cobra la garantía de cada reserva. Los dos archivos ya están completos: no los modifiques.

## Respuesta sobre la lectura

Según el artículo, ¿qué problema resuelve una clave de idempotencia, y quién la genera: el cliente o el servidor? ¿Por qué el artículo dice que reintentar es inevitable en una red?

Una clave de idempotencia resuelve el problema de **reintentar una operación con efectos sin hacerla dos veces**. Si un cliente manda un cobro y no recibe respuesta, no sabe si el cobro se hizo, y sin clave un reintento puede cobrar dos veces. Con la clave, el servidor reconoce que es la misma operación: si nunca la recibió, la procesa; si ya la completó, devuelve el resultado guardado en vez de repetirla.

La genera **el cliente**: crea un identificador único por operación y lo manda en la cabecera `Idempotency-Key`, en el primer intento y en todos los reintentos. El servidor la usa para emparejar los reintentos con la solicitud original.

Reintentar es inevitable porque **las redes no son confiables**. Una llamada puede fallar al conectarse, a mitad del procesamiento, o después de que el servidor terminó pero antes de que la respuesta llegue al cliente. En los dos últimos casos el cliente no puede saber qué pasó, y la única forma de llegar a un resultado es volver a intentarlo. El artículo recomienda además reintentar con espera exponencial y una variación aleatoria (jitter), para no saturar a un servidor que ya está en problemas.

## Respuesta sobre la pregunta de la sesión pasada

Un mismo correo puede llegar dos veces cuando la cola entrega al menos una vez. Si en vez de un correo fuera el cobro de la garantía de la cancha, ¿qué pasaría? ¿Cómo podría el servicio de pagos reconocer que una solicitud ya la procesó?

Se le cobraría la garantía dos veces a la estudiante. Lo muestra `test_un_post_reintentado_por_la_red_cobra_dos_veces` del Ejercicio 1: la red pierde una respuesta, el cliente reenvía el mismo POST y la pasarela registra 2 cobros. En la demo, con dos respuestas perdidas, son 3 cobros. A diferencia de la reserva, no hay ninguna validación que frene el duplicado.

El servicio de pagos lo reconocería con una **clave de idempotencia**: un identificador único de la operación, generado por quien pide el cobro antes del primer intento y enviado igual en cada reintento. El servicio guarda cada clave con la respuesta que dio. Si llega una clave conocida, devuelve esa respuesta sin cobrar otra vez. Es lo que implementa el Ejercicio 2.

## Ejercicio 1: El contrato de las reservas

Este ejercicio se resuelve en vivo, sobre `api_v1_ejercicio1.py`. Antes de que se muestre cada resultado, responde:

**Respuesta 1:** `POST /v1/reservas` con un cuerpo sin `fecha` ni `hora`. ¿Qué código de estado corresponde, y por qué no 404 ni 500?

**400 Bad Request.** El problema está en la solicitud del cliente: le faltan campos obligatorios, y el cuerpo `{"error": "faltan campos obligatorios"}` le dice qué corregir.
- **No es 404** porque la ruta `/v1/reservas` sí existe. 404 significa que el recurso pedido no se encontró, y el cliente buscaría el error en la URL.
- **No es 500** porque el servidor no falló. Un 5xx significa "falla mía, del servidor", y muchos clientes reintentan automáticamente un 5xx, lo que aquí sería inútil: la misma solicitud siempre va a estar incompleta.

En la demo: `POST reserva sin fecha ni hora: 400`.

**Respuesta 2:** beto crea una reserva y la red pierde la respuesta. El cliente reenvía la misma solicitud. ¿Qué código recibe beto, y cuántas reservas hay en el repositorio?

Beto recibe **409** (`{"error": "fecha y hora ocupadas"}`), y en el repositorio hay **2 reservas**: la de ana y una sola de beto. La primera solicitud sí creó su reserva, pero el 201 se perdió en la red. El reintento llegó cuando la hora ya estaba ocupada, por él mismo.

La validación de choque evitó una reserva duplicada, pero beto recibe un error sobre una reserva que sí tiene. El `POST` no es idempotente: la misma solicitud, repetida, da otra respuesta.

## Durante los ConcepTests

**ConcepTest 1. Tu voto, antes de discutir en pareja** (A, B, C o D):

_(tu voto)_

**Tu razonamiento:**

_(tu respuesta)_

**Después de discutir en pareja, ¿cambiaste de voto? ¿Por qué?**

_(tu respuesta)_

**ConcepTest 2. Tu voto, antes de discutir en pareja** (A, B, C o D):

_(tu voto)_

**Tu razonamiento:**

_(tu respuesta)_

## Ejercicio 2: Un pago que no se cobra dos veces

Ahora te toca a ti. `pagos_idempotentes_ejercicio2.py` trae `ApiDePagos` con un solo endpoint, `POST /v1/pagos`.

1. Completa `crear_pago(...)` con la cabecera `Idempotency-Key`: sin clave, 400; clave repetida con el mismo cuerpo, la respuesta guardada; clave repetida con otro cuerpo, 422; clave nueva, el pago.
2. Corre las pruebas:
   ```
   pytest test_pagos_idempotentes_ejercicio2.py
   ```
3. Responde: en `test_con_la_red_perdiendo_tres_respuestas_cobra_una_sola_vez`, la API recibe la misma solicitud cuatro veces. ¿Por qué el cliente tiene que generar la clave una sola vez, antes del primer intento, y no una nueva en cada reintento?

Porque la clave identifica **la operación**, no el intento. El cliente no sabe si el primer intento se procesó: para él, una respuesta perdida es igual a una solicitud que nunca llegó. Por eso todos los reintentos tienen que llevar la misma clave, para que la API los reconozca como la misma operación.

Si generara una clave nueva en cada reintento, la API vería cuatro operaciones distintas y cobraría cuatro veces. Lo probé con un cliente que crea un UUID nuevo en cada intento: la pasarela registró **4 cobros**, igual que sin clave. Con la clave generada una vez, antes del primer intento, la API cobra en el primero y devuelve la respuesta guardada (`cobro-1`) en los otros tres.

4. Responde: tu API guarda las respuestas en un diccionario de la instancia. ¿Qué pasa con la idempotencia si ReservaU corre tres instancias de la API detrás del balanceador, como en la sesión pasada? ¿Dónde tendrían que vivir las respuestas guardadas?

La idempotencia se rompe. Cada instancia tiene su propio diccionario, y el balanceador manda cada reintento a una instancia distinta, que no conoce la clave y cobra de nuevo. Lo probé con 3 instancias en round robin y la red perdiendo 3 respuestas: la pasarela registró **3 cobros** con la misma clave. El cliente recibió `cobro-1`, porque la cuarta solicitud volvió a la primera instancia, así que ni siquiera se entera de los otros dos. Es el mismo problema del `ServidorConEstado` de la sesión pasada: la API guarda estado en su propia memoria.

Las respuestas guardadas tendrían que vivir **fuera de las instancias, en un almacén compartido por todas**: como el `AlmacenCompartido` (Redis) de la sesión pasada, o una tabla en la base de datos, con la clave de idempotencia como clave y una expiración (por ejemplo, 24 horas). Además:
- La API tendría que reservar la clave de forma atómica antes de cobrar (con una restricción única en la tabla, o `SET NX` en Redis), para que dos reintentos simultáneos en instancias distintas no cobren los dos.
- Ese almacén necesita replicación, como en la Semana 9, para no volverse el punto único de falla.

## Ejercicio 3: Una versión 2 que no rompe la versión 1

`versionado_ejercicio3.py` trae `ApiVersionada`, con la versión 1 completa. La versión 2 cambia la forma de la hora (`"inicio": "18:00"` y `"duracion_min"` al crear, `"inicio"` y `"fin"` al leer) y las dos versiones comparten las mismas reservas.

1. Completa `representar_v2`, `crear_reserva_v2`, `obtener_reserva_v2` y `borrar_reserva`.
2. Corre las pruebas:
   ```
   pytest test_versionado_ejercicio3.py
   ```
3. Responde: el equipo de la web propone otra salida, cambiar `"hora"` por `"inicio"` directamente en `/v1/` "porque es más claro". ¿Qué le pasa a la app del celular que nadie actualizó? ¿Qué cambio sí podrías hacerle a la respuesta de `/v1/` sin crear una versión nueva?

**La app del celular se rompe.** Sigue mandando `"hora"`, así que si `/v1/` ahora exige `"inicio"`, cada `POST` responde 400 y nadie con la app vieja puede reservar. Al leer, la app busca `"hora"` en la respuesta y no la encuentra, así que falla o muestra la reserva incompleta. Renombrar un campo es un cambio incompatible: un contrato publicado es una promesa a clientes que no controlas y que no se actualizan al ritmo del servidor. Por eso el cambio va en `/v2/` y `/v1/` queda igual.

Sin crear una versión nueva sí puedo hacer **cambios aditivos**: agregar un campo nuevo a la respuesta sin quitar ni cambiar los existentes, por ejemplo `"duracion_min": 60` junto a `"hora"`, o aceptar un campo opcional nuevo en la solicitud, con un valor por defecto. Los clientes que no lo conocen lo ignoran. Lo que no puedo es quitar ni renombrar un campo, cambiarle el tipo (por ejemplo `"hora": "18:00"`) ni volver obligatorio algo que era opcional.

Un matiz: en este laboratorio `test_el_contrato_de_v1_no_cambia` compara el cuerpo completo de `/v1/`, así que incluso un campo agregado haría fallar esa prueba. Agregar campos solo es seguro si los clientes ignoran los campos que no conocen.

4. Responde: en `test_un_delete_reintentado_por_la_red_no_borra_otra_cosa`, el cliente recibe 404 aunque su primer DELETE sí borró la reserva. ¿Es idempotente tu DELETE? Justifica con lo que queda en el repositorio.

**Sí.** Idempotente significa que repetir la solicitud deja el servidor **en el mismo estado** que hacerla una vez, no que la respuesta sea la misma. En esa prueba la API recibe el mismo DELETE tres veces: la primera responde 204 y borra `r-1`, y las otras dos responden 404 porque `r-1` ya no existe (la secuencia es `[204, 404, 404]`). Al final en el repositorio queda exactamente `["r-2"]`, lo mismo que si el DELETE hubiera llegado una sola vez: no se borró nada más ni se tocó `r-2`.

El 404 solo informa que la reserva ya no está. Un cliente que reintenta un DELETE y recibe 404 puede tomarlo como éxito.

5. Escribe el contrato del recurso reservas de ReservaU en su versión 2: una fila por endpoint, con método, ruta, cuerpo que recibe, respuestas posibles (código y cuerpo) y si es idempotente.

| Método | Ruta | Cuerpo | Respuestas | ¿Idempotente? |
|---|---|---|---|---|
| `POST` | `/v2/reservas` | `{"estudiante", "cancha", "fecha": "AAAA-MM-DD", "inicio": "HH:00" (de "07:00" a "20:00"), "duracion_min": 60}` | **201** `{"id", "estudiante", "cancha", "fecha", "inicio", "fin"}`<br>**400** `{"error": "faltan campos"}`, `{"error": "duracion no permitida"}` o `{"error": "inicio invalido"}`<br>**404** `{"error": "cancha desconocida"}`<br>**409** `{"error": "hora ocupada"}` | **No.** Cada llamada nueva crea una reserva, y el reintento de una que sí se creó recibe 409. Se podría volver idempotente con `Idempotency-Key`, como en el Ejercicio 2. |
| `GET` | `/v2/reservas/{id}` | Sin cuerpo | **200** `{"id", "estudiante", "cancha", "fecha", "inicio", "fin"}`<br>**404** `{"error": "reserva desconocida"}` | **Sí.** Solo lee; no cambia nada. |
| `DELETE` | `/v2/reservas/{id}` | Sin cuerpo | **204** sin cuerpo<br>**404** `{"error": "reserva desconocida"}` | **Sí.** Repetirlo deja el mismo estado: la reserva borrada. |

Las dos versiones comparten las mismas reservas: una reserva creada en `/v1/` se lee en `/v2/`, y al revés. Cualquier versión distinta de `v1` o `v2` responde 404 con `{"error": "version desconocida"}`.

### Checklist final

- [x] `crear_reserva` (v1) responde 400, 404, 409 o 201, en ese orden de verificación.
- [x] `crear_pago` no cobra nunca dos veces con la misma clave.
- [x] La respuesta guardada se devuelve tal cual, con el mismo id de cobro.
- [x] Ningún cambio de la versión 2 modifica `representar_v1` ni `crear_reserva_v1`.
- [x] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture)

En `ApiVersionada`, la misma clase lee rutas, valida cuerpos, traduce formatos, decide si una hora está ocupada y habla con el repositorio. Si mañana cambias el repositorio en memoria por PostgreSQL, ¿cuántos métodos tienes que tocar? ¿Y si agregas una versión 3?

**PostgreSQL:** depende de si el repositorio nuevo respeta la misma interfaz. El repositorio ya llega por el constructor, así que si escribo una clase `RepositorioPostgres` con los mismos métodos (`ocupada`, `crear`, `buscar`, `borrar`), no toco **ningún** método de `ApiVersionada`: solo cambio el objeto que le paso. Si no, por ejemplo si escribo las consultas SQL directo en la API, tengo que tocar **5 de sus 6 métodos** (sin contar `__init__`), todos menos `manejar`: `crear_reserva_v1`, `obtener_reserva_v1`, `crear_reserva_v2`, `obtener_reserva_v2` y `borrar_reserva`.

**Versión 3:** tengo que tocar `manejar`, que hoy solo conoce `v1` y `v2`, y agregar `representar_v3`, `crear_reserva_v3` y `obtener_reserva_v3`. Además, `crear_reserva_v3` copiaría por tercera vez la regla del negocio (cancha conocida; hora ocupada, 409), que hoy ya está duplicada entre v1 y v2. Si esa regla cambia, hay que cambiarla en cada versión.

El problema de fondo es que una sola clase mezcla HTTP, formatos, reglas y almacenamiento. Lo ideal sería que las reglas de las reservas vivieran en un núcleo; que cada versión de la API fuera solo un traductor de formatos hacia ese núcleo, y que el repositorio quedara detrás de una interfaz. Así, PostgreSQL y la v3 serían piezas nuevas, sin tocar las reglas.

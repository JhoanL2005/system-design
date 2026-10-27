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

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

Un mismo correo puede llegar dos veces cuando la cola entrega al menos una vez. Si en vez de un correo fuera el cobro de la garantía de la cancha, ¿qué pasaría? ¿Cómo podría el servicio de pagos reconocer que una solicitud ya la procesó?

_(tu respuesta)_

## Ejercicio 1: El contrato de las reservas

Este ejercicio se resuelve en vivo, sobre `api_v1_ejercicio1.py`. Antes de que se muestre cada resultado, responde:

**Respuesta 1:** `POST /v1/reservas` con un cuerpo sin `fecha` ni `hora`. ¿Qué código de estado corresponde, y por qué no 404 ni 500?

_(tu respuesta)_

**Respuesta 2:** beto crea una reserva y la red pierde la respuesta. El cliente reenvía la misma solicitud. ¿Qué código recibe beto, y cuántas reservas hay en el repositorio?

_(tu respuesta)_

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

_(tu respuesta)_

4. Responde: tu API guarda las respuestas en un diccionario de la instancia. ¿Qué pasa con la idempotencia si ReservaU corre tres instancias de la API detrás del balanceador, como en la sesión pasada? ¿Dónde tendrían que vivir las respuestas guardadas?

_(tu respuesta)_

## Ejercicio 3: Una versión 2 que no rompe la versión 1

`versionado_ejercicio3.py` trae `ApiVersionada`, con la versión 1 completa. La versión 2 cambia la forma de la hora (`"inicio": "18:00"` y `"duracion_min"` al crear, `"inicio"` y `"fin"` al leer) y las dos versiones comparten las mismas reservas.

1. Completa `representar_v2`, `crear_reserva_v2`, `obtener_reserva_v2` y `borrar_reserva`.
2. Corre las pruebas:
   ```
   pytest test_versionado_ejercicio3.py
   ```
3. Responde: el equipo de la web propone otra salida, cambiar `"hora"` por `"inicio"` directamente en `/v1/` "porque es más claro". ¿Qué le pasa a la app del celular que nadie actualizó? ¿Qué cambio sí podrías hacerle a la respuesta de `/v1/` sin crear una versión nueva?

_(tu respuesta)_

4. Responde: en `test_un_delete_reintentado_por_la_red_no_borra_otra_cosa`, el cliente recibe 404 aunque su primer DELETE sí borró la reserva. ¿Es idempotente tu DELETE? Justifica con lo que queda en el repositorio.

_(tu respuesta)_

5. Escribe el contrato del recurso reservas de ReservaU en su versión 2: una fila por endpoint, con método, ruta, cuerpo que recibe, respuestas posibles (código y cuerpo) y si es idempotente.

| Método | Ruta | Cuerpo | Respuestas | ¿Idempotente? |
|---|---|---|---|---|
| _(…)_ | _(…)_ | _(…)_ | _(…)_ | _(…)_ |

### Checklist final

- [ ] `crear_reserva` (v1) responde 400, 404, 409 o 201, en ese orden de verificación.
- [ ] `crear_pago` no cobra nunca dos veces con la misma clave.
- [ ] La respuesta guardada se devuelve tal cual, con el mismo id de cobro.
- [ ] Ningún cambio de la versión 2 modifica `representar_v1` ni `crear_reserva_v1`.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture)

En `ApiVersionada`, la misma clase lee rutas, valida cuerpos, traduce formatos, decide si una hora está ocupada y habla con el repositorio. Si mañana cambias el repositorio en memoria por PostgreSQL, ¿cuántos métodos tienes que tocar? ¿Y si agregas una versión 3?

_(tu respuesta)_

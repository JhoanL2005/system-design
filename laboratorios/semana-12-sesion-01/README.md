# Semana 12, Sesión 1: ReservaU con patrón Observer: lista de espera de un espacio

> Objetivo de la sesión: diseñar la notificación a una lista de espera cuando un espacio reservado se cancela, usando el patrón Observer, y argumentar sus límites frente a alternativas.

**Lectura previa de esta sesión:** [A Case Against the Observer Pattern (Medium)](https://medium.com/@JamieScanlon/a-case-against-the-observer-pattern-dc1cbd80a6a1)

**Referencia de esta sesión:** [Observer (Refactoring.Guru)](https://refactoring.guru/design-patterns/observer)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-12-sesion-01
```

`reservas.py` trae el dominio de Reservas de la sesión pasada, ya resuelto (`FranjaHoraria`, `Reserva`, `CalendarioDeCancha`), con dos consultas nuevas: `esta_libre` y `franja_de`. `notificaciones.py` y `reloj.py` traen un notificador en memoria y un reloj simulado. Ninguno de los tres se modifica.

Los tres ejercicios se encadenan: el Ejercicio 2 importa `ListaDeEspera` de `espera_ejercicio1.py`, y el Ejercicio 3 importa `ObservadorDeReservas` de `eventos_ejercicio2.py`. Cada uno necesita completo el anterior.

## Respuesta sobre la lectura

Según el artículo, ¿qué problemas trae el patrón Observer cuando un sistema crece? Elige uno y di si ReservaU lo tendría con una lista de espera.

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

Cuando ana cancela su reserva de las 18:00, beto, que la estaba esperando, no se entera hasta que vuelve a abrir la app y consulta. Si la app consultara sola cada 30 segundos, ¿cuántas consultas haría un día de inscripciones con 2000 estudiantes esperando? ¿Quién debería avisarle a beto?

_(tu respuesta)_

## Ejercicio 1: la lista de espera

Este ejercicio se resuelve en vivo, sobre `espera_ejercicio1.py`. Córrelo una vez antes de que empiece: la Parte A funciona, y la Parte B termina con un error porque todavía no existe `suscribir`.

```
python3 espera_ejercicio1.py
```

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** en la Parte A, ana cancela en el segundo 5500. ¿En qué segundo se entera beto si su app consulta cada 30 segundos, y cuántas consultas hizo? ¿Y cada 300 segundos?

_(tu respuesta)_

**Respuesta 2:** en la Parte B se cancelan dos reservas: la de carla (9 a 10) y la de ana (18 a 19). beto y dani esperan la de 18 a 19. ¿Cuántas veces llama el calendario a `al_liberarse`, y cuántos mensajes se envían?

_(tu respuesta)_

**Respuesta 3:** si antes de la lista de espera se suscribe otro observador cuyo `al_liberarse` lanza `ValueError`, ¿qué pasa al cancelar la reserva de ana? ¿Queda cancelada? ¿Se entera beto?

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

## Ejercicio 2: dos eventos y tres observadores

`eventos_ejercicio2.py` trae `CalendarioConEventos`, que avisa dos eventos ("ocupada" y "liberada"), y tres observadores: la lista de espera del Ejercicio 1, una caché de disponibilidad (la de la Semana 9, invalidada por el calendario) y un registro de auditoría. Su comentario describe qué hace cada uno.

1. Completa los cinco `TODO`.
2. Corre el archivo y las pruebas:
   ```
   python3 eventos_ejercicio2.py
   pytest test_eventos_ejercicio2.py
   ```
3. Completa la tabla: qué observadores tiene que tener cada evento en ReservaU, y por qué. Agrega los que creas que faltan.

| Evento | Observadores | Por qué cada uno |
|---|---|---|
| "ocupada" | _(…)_ | _(…)_ |
| "liberada" | _(…)_ | _(…)_ |

4. Responde: en el `main`, ¿cuántas veces recorrió la caché el calendario? Si la caché se suscribiera solo a "liberada", ¿qué mostraría `cache.libres(calendario)` después de que beto reserva?

_(tu respuesta)_

5. Responde: `CalendarioConEventos` no importa `CacheDeDisponibilidad` ni `RegistroDeAuditoria`. Si mañana hay que mandar un mensaje al chat del equipo de mantenimiento cada vez que se libera una cancha, ¿qué archivos cambias?

_(tu respuesta)_

## Ejercicio 3: la lista de espera con plazo

`ofertas_ejercicio3.py` describe en su comentario `ListaDeEsperaConPlazo`: la franja liberada se ofrece al primero de la fila, que tiene un plazo para aceptarla; si no acepta, pasa al siguiente. Esta vez no hay código de partida: escribes la clase.

1. Escribe `ListaDeEsperaConPlazo`.
2. Corre las pruebas:
   ```
   pytest test_ofertas_ejercicio3.py
   ```
3. Responde: `aceptar` reserva la franja con `calendario.reservar`, y eso avisa "ocupada" a todos los suscritos, incluida la propia lista. ¿Qué tuviste que cuidar para que quien acepta no reciba "ya no está disponible"?

_(tu respuesta)_

4. Responde: el plazo vence aunque nadie haga nada, pero el calendario no avisa cuando pasa el tiempo: alguien tiene que llamar `revisar_vencidas`. ¿Quién lo hace en la app en producción, y qué tiene de parecido con la Parte A del Ejercicio 1?

_(tu respuesta)_

5. Compara las tres formas de avisarle a beto. La cola de mensajes es la de la Semana 10: el calendario publica "reserva cancelada" y la lista de espera la consume en otro proceso.

| Criterio | Consultar cada 30 s | Observer (este laboratorio) | Cola de mensajes |
|---|---|---|---|
| Cuánto tarda beto en enterarse | _(…)_ | _(…)_ | _(…)_ |
| Trabajo que hace el sistema mientras nada cambia | _(…)_ | _(…)_ | _(…)_ |
| Qué sabe el calendario de quien espera | _(…)_ | _(…)_ | _(…)_ |
| Qué pasa si quien recibe el aviso falla | _(…)_ | _(…)_ | _(…)_ |
| ¿Funciona si la lista de espera corre en otro servidor? | _(…)_ | _(…)_ | _(…)_ |

### Checklist final

- [ ] El calendario avisa después de cambiar su estado, nunca antes, y una operación rechazada no avisa a nadie.
- [ ] El calendario no importa ninguna clase de observador: solo conoce su interfaz.
- [ ] Cada observador está suscrito solo a los eventos que usa.
- [ ] Una oferta vencida, aceptada o perdida por una reserva directa queda cerrada, y la fila sigue con el siguiente.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Composite Pattern: A Better Way to Build Tree Structures (Medium)](https://medium.com/@prabhavithreddy/composite-pattern-a-better-way-to-build-tree-structures-86c3d31e3f42)

La universidad pide agregar a ReservaU las salas de estudio de la biblioteca y el préstamo de proyectores. Las canchas están en el complejo deportivo; las salas, en los pisos de la biblioteca; los proyectores, en las salas. Si quieres saber qué hay libre el martes de 18 a 19 en todo el campus de Cumbayá, ¿cómo recorrerías esa estructura? ¿Qué pasa con tu recorrido si mañana agregan un nivel más, por ejemplo "piso" dentro de "edificio"?

_(tu respuesta)_

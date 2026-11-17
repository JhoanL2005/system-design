# Semana 14, Sesión 1: Test-Driven Development: el ciclo red-green-refactor

> Objetivo de la sesión: aplicar el ciclo red-green-refactor para desarrollar una funcionalidad nueva del sistema propio, escribiendo la prueba antes que el código de producción.

**Lectura previa de esta sesión:** [Is the Red-Green-Refactor Cycle of Test-Driven Development Good? (News UK Technology, Medium)](https://medium.com/news-uk-technology/is-the-red-green-refactor-cycle-of-test-driven-development-good-9e2b1b52d721)

**Referencia de esta sesión:** [Test Driven Development (Martin Fowler, bliki)](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-14-sesion-01
```

`reservas.py` es el dominio de Reservas de la Semana 13 (no se modifica); lo usa el Ejercicio 3. Hoy los archivos empiezan casi vacíos a propósito: el código se escribe solo para hacer pasar una prueba que falló. Corre cada archivo de prueba por separado.

## Respuesta sobre la lectura

Según el artículo, ¿qué pasa en cada una de las tres fases del ciclo? ¿Qué critican quienes dicen que TDD es una pérdida de tiempo, y qué responde el artículo?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

En los laboratorios recientes, las pruebas ya estaban escritas cuando abrías el archivo. ¿Cambió eso la forma en que escribiste el código? ¿Escribirías las pruebas antes en tu sistema propio?

_(tu respuesta)_

## El debate

Antes de ver código: **¿escribir la prueba antes es disciplina o pérdida de tiempo?** Anota tu posición y tu mejor argumento. Al final de la sesión vuelves a esta pregunta.

_(tu posición y tu argumento)_

## Ejercicio 1: las penalizaciones por cancelar tarde

Este ejercicio se resuelve en vivo, sobre `penalizaciones_ejercicio1.py` y `test_penalizaciones_ejercicio1.py`, que empiezan vacíos. La regla y la lista de pruebas están en el comentario de `penalizaciones_ejercicio1.py`.

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** la primera prueba es `assert puntos_por_cancelar(2000) == 0`, y todavía no existe ninguna función. ¿Con qué mensaje falla? ¿Cuál es el código más simple que la hace pasar?

_(tu respuesta)_

**Respuesta 2:** después de la segunda prueba (`600` minutos da `1`), el código es un `if`. La prueba del borde (`1440` da `0`, `120` da `1`), ¿va a pasar sin cambiar nada? ¿Por qué importa saberlo antes de correrla?

_(tu respuesta)_

**Respuesta 3:** con las ocho pruebas en verde, el código tiene tres `if` con números sueltos. ¿Qué cambiarías en la fase de refactor, y cómo sabes que no rompiste nada?

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

## Ejercicio 2: el cupo semanal

`cupos_ejercicio2.py` describe en su comentario `CupoSemanal`: tres reservas por estudiante por semana, seis para los equipos oficiales. `test_cupos_ejercicio2.py` trae la primera prueba escrita y la lista de las siete, en orden. `semana_de` ya está resuelta.

1. Corre la primera prueba y mírala fallar. Escribe el código mínimo para que pase.
2. Por cada prueba siguiente de la lista: escríbela, córrela y mírala fallar, escribe el código mínimo, córrela en verde y refactoriza con todas en verde. Llena la bitácora:

| Prueba | ¿Con qué mensaje falló? | Qué cambiaste para que pase | Qué refactorizaste |
|---|---|---|---|
| 1 | _(…)_ | _(…)_ | _(…)_ |
| 2 | _(…)_ | _(…)_ | _(…)_ |
| 3 | _(…)_ | _(…)_ | _(…)_ |
| 4 | _(…)_ | _(…)_ | _(…)_ |
| 5 | _(…)_ | _(…)_ | _(…)_ |
| 6 | _(…)_ | _(…)_ | _(…)_ |
| 7 | _(…)_ | _(…)_ | _(…)_ |

3. Cuando termines la lista, y no antes, corre las pruebas de aceptación:
   ```
   pytest test_aceptacion_cupos.py
   ```
4. Responde: ¿pasaron todas? Si alguna falló, ¿qué caso no estaba en tu lista? ¿Lo habrías escrito si hubieras empezado por el código?

_(tu respuesta)_

5. Responde: alguna prueba de tu lista, ¿pasó apenas la escribiste, sin cambiar el código? ¿Qué hiciste con ella?

_(tu respuesta)_

## Ejercicio 3: reservas recurrentes, en pareja

`recurrentes_ejercicio3.py` describe en su comentario `AgendaDeCancha` y `reservar_cada_semana`: reservar la misma franja durante varias semanas, saltando las ocupadas. No hay código ni pruebas de partida.

1. Antes de escribir código, escriban su lista de pruebas, en orden:

_(su lista)_

2. Desarrollen la funcionalidad en ping-pong: una persona escribe una prueba que falla, la otra escribe el código mínimo que la hace pasar y la siguiente prueba, cambiando de rol en cada prueba. Refactoricen con todas en verde.
3. Responde: ¿cuántas pruebas agregaron a la lista mientras trabajaban? ¿Cuál fue la primera que no se les había ocurrido?

_(tu respuesta)_

4. Responde: la regla de no usar `try`/`except` los obligó a preguntar antes de reservar (`esta_libre`, `horas_de`). ¿Qué prueba los llevó a eso?

_(tu respuesta)_

### Checklist final

- [ ] Ninguna línea de código de producción se escribió sin una prueba que fallara antes.
- [ ] Cada prueba falló por la razón esperada, no por un error de escritura.
- [ ] El refactor se hizo con todas las pruebas en verde, y siguieron en verde.
- [ ] Las pruebas de aceptación del Ejercicio 2 pasan.
- [ ] Los nombres de las pruebas se leen como la especificación.

## Vuelta al debate

**Después de hoy, ¿disciplina o pérdida de tiempo? ¿En qué parte de tu sistema propio lo usarías, y en cuál no?**

_(tu respuesta)_

## Antes de la próxima sesión

**Lectura:** [Just Say No to More End-to-End Tests (Google Testing Blog)](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)

Las pruebas de hoy prueban una clase sola, en milisegundos. Imagina que ReservaU solo tuviera pruebas que abren el navegador, inician sesión, buscan una cancha y reservan: 300 pruebas de 40 segundos cada una, y unas cuantas que fallan una vez de cada diez sin que nada haya cambiado. ¿Qué le pasa al equipo que las mantiene?

_(tu respuesta)_

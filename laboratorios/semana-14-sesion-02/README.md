# Semana 14, Sesión 2: Testing de software: unitario, integración y end-to-end

> Objetivo de la sesión: clasificar una prueba como unitaria, de integración o end-to-end, y justificar la proporción de cada tipo según la pirámide de testing para el sistema propio.

**Lectura previa de esta sesión:** [Just Say No to More End-to-End Tests (Google Testing Blog)](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)

**Referencia de esta sesión:** [Testing in .NET (Microsoft Learn)](https://learn.microsoft.com/en-us/dotnet/core/testing/)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-14-sesion-02
```

Hoy ReservaU tiene sus capas completas, en pequeño:

- `dominio.py`: las reglas de la sesión pasada (el cupo semanal y los puntos por cancelar). No se modifica.
- `repositorio.py`: `RepositorioSQLite`, que guarda en una base SQLite de verdad (`sqlite3`, de la biblioteca estándar), y `RepositorioEnMemoria`, un doble de prueba con los mismos métodos.
- `servicio.py`: `ServicioDeReservas`, que aplica las reglas sobre el repositorio que se le pase.
- `api.py`: la API simulada, como en la Semana 10.
- `entorno_e2e.py`: `NavegadorSimulado`, que usa ReservaU completo como una persona desde el navegador. Como una prueba de punta a punta de verdad, cada acción tarda, y de vez en cuando falla por algo ajeno a ReservaU. No se modifica.
- `test_suite_heredada.py`: la suite que dejó el equipo anterior. No se modifica.

Corre cada archivo de prueba por separado, con `--durations=0` para ver cuánto tarda cada prueba.

## Respuesta sobre la lectura

Según el artículo, ¿qué le pasó al equipo del ejemplo en los días antes de su entrega? ¿Qué tres propiedades tiene que tener un buen ciclo de retroalimentación, y qué tipo de prueba las cumple mejor?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

Si ReservaU solo tuviera pruebas que abren el navegador, inician sesión y reservan, 300 pruebas de 40 segundos y algunas que fallan una vez de cada diez sin que nada cambie, ¿qué le pasa al equipo que las mantiene?

_(tu respuesta)_

## Ejercicio 1: la suite heredada

Este ejercicio se resuelve en vivo: primero sobre `test_suite_heredada.py`, después sobre `test_rapidas_ejercicio1.py`, que empieza vacío.

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** clasifica las 12 pruebas de la suite heredada: ¿cuántas son unitarias, cuántas de integración y cuántas de punta a punta? ¿Qué forma tiene esa suite?

_(tu respuesta)_

**Respuesta 2:** ¿cuánto crees que tarda la suite completa? Si la corres cinco veces sin cambiar nada, ¿cuántas veces pasa entera?

_(tu respuesta)_

**Respuesta 3:** con la suite repartida en la pirámide, introduzco un error en `contar_en_semana` (deja de filtrar por semana). ¿Qué prueba falla en la suite heredada, y qué dice su mensaje? ¿Y en la nueva?

_(tu respuesta)_

**Lo que midió la suite:**

| Suite | Pruebas | Unitarias | Integración | Punta a punta | Tiempo |
|---|---|---|---|---|---|
| Heredada | 12 | _(…)_ | _(…)_ | _(…)_ | _(…)_ |
| Nueva | _(…)_ | _(…)_ | _(…)_ | _(…)_ | _(…)_ |

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

## Ejercicio 2: el contrato del doble

`test_contrato_repositorio_ejercicio2.py` corre cada prueba dos veces: una con `RepositorioEnMemoria` y otra con `RepositorioSQLite` (la fixture `repositorio` tiene dos parámetros, y `tmp_path` le da a cada prueba una carpeta nueva para su base). La primera prueba ya está escrita.

1. Escribe las cuatro pruebas de los `TODO`.
2. Corre el archivo con `-v`: cada prueba aparece dos veces, `[memoria]` y `[sqlite]`.
   ```
   pytest test_contrato_repositorio_ejercicio2.py -v
   ```
3. Responde: ¿de qué tipo son estas pruebas cuando corren con `[sqlite]`? ¿Y con `[memoria]`?

_(tu respuesta)_

4. Responde: las pruebas unitarias del servicio usan `RepositorioEnMemoria`. ¿Qué podría pasar si el doble se comportara distinto de SQLite en algo que estas pruebas no cubren?

_(tu respuesta)_

## Ejercicio 3: las pruebas de cancelar

`ServicioDeReservas.cancelar` borra la reserva y suma los puntos que corresponden. La suite heredada lo prueba de punta a punta, y pasa. Esta vez no hay pruebas de partida.

1. Escribe en `test_cancelar_ejercicio3.py` un conjunto balanceado de pruebas de `cancelar`: decide cuáles son unitarias (el servicio con el doble), cuáles de integración (con `RepositorioSQLite(":memory:")`) y si hace falta alguna de punta a punta.
2. Corre tus pruebas. Si alguna falla, encuentra el error en el código de ReservaU (no en tu prueba) y corrígelo.
3. Clasifica tus pruebas:

| Prueba | Tipo | Qué parte de ReservaU ejecuta de verdad | Cuánto tarda |
|---|---|---|---|
| _(…)_ | _(…)_ | _(…)_ | _(…)_ |

4. Responde: ¿encontraste un error? ¿Qué tipo de prueba lo encontró? ¿Por qué no lo encontraron las pruebas unitarias ni la suite heredada?

_(tu respuesta)_

5. Responde: para tu sistema propio, ¿en qué proporción repartirías las pruebas? Justifícalo con lo que mediste hoy, no con el 70/20/10.

_(tu respuesta)_

### Checklist final

- [ ] Cada prueba tiene un nombre que dice qué comportamiento comprueba.
- [ ] Ninguna prueba unitaria abre una base de datos ni el navegador.
- [ ] Las pruebas de contrato pasan con los dos repositorios.
- [ ] El error de `cancelar` está corregido, y una prueba lo atraparía si volviera.
- [ ] La suite nueva tarda una fracción de la heredada y cubre lo mismo.

## Antes de la próxima sesión

**Lectura:** [Continuous Integration (Martin Fowler)](https://martinfowler.com/articles/continuousIntegration.html)

Hoy la suite rápida tarda alrededor de un segundo. Imagina un equipo de seis personas que trabajan cada una en su rama durante un mes, y que juntan todo el último día: tres días de conflictos de fusión, y pruebas que pasaban en cada rama y fallan juntas. ¿Qué cambiarías en la forma de trabajar, y qué tendría que pasar automáticamente cada vez que alguien sube un cambio?

_(tu respuesta)_

# Semana 13, Sesión 2: El feed de actividad de ReservaU: fan-out y ranking

> Objetivo de la sesión: elegir entre fan-out on write y fan-out on read para construir el feed de actividad de ReservaU (próximos partidos de equipos oficiales, espacios más reservados), justificando la decisión según el ratio de lectura/escritura y el tamaño de la audiencia.

**Lectura previa de esta sesión:** [Mastering News Feed System Design: A Comprehensive Deep Dive (Medium)](https://medium.com/@rafinutshaw/mastering-news-feed-system-design-a-comprehensive-deep-dive-bae6f57289be)

**Referencia de esta sesión:** [Design Twitter timeline/feed (system-design-primer, GitHub)](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-13-sesion-02
```

`actividad.py` trae las piezas comunes: `Publicacion`, un `Almacen` que cuenta escrituras y lecturas (para comparar estrategias), y `mas_recientes`. No se modifica.

El Ejercicio 2 importa las dos clases de `feed_ejercicio1.py`, así que necesita completo el Ejercicio 1. Corre cada archivo de prueba por separado.

## Respuesta sobre la lectura

Según el artículo, ¿qué es fan-out on write y qué es fan-out on read? ¿Qué problema tiene cada uno, y qué proponen para las cuentas con muchísimos seguidores?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

El equipo de fútbol de un curso lo siguen 10 personas; la final del campeonato, 8000. Si cada publicación se copia a la lista de cada seguidor, ¿cuántas escrituras cuesta cada caso? ¿Se te ocurre otra forma?

_(tu respuesta)_

## Ejercicio 1: el feed, de dos formas

Este ejercicio se resuelve en vivo, sobre `feed_ejercicio1.py`. Córrelo una vez antes de que empiece: termina con `NotImplementedError`.

```
python3 feed_ejercicio1.py
```

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** con fan-out on write, ¿cuántas escrituras cuesta la publicación del equipo de arquitectura (10 seguidores)? ¿Y la de la final (8000)? ¿Cuántas lecturas cuesta que ana, que sigue a 300 equipos, abra su feed?

_(tu respuesta)_

**Respuesta 2:** las mismas tres preguntas con fan-out on read.

_(tu respuesta)_

**Respuesta 3:** con fan-out on write, beto empieza a seguir a un equipo hoy. ¿Ve en su feed lo que ese equipo publicó ayer? ¿Y con fan-out on read?

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

## Ejercicio 2: el feed híbrido

`hibrido_ejercicio2.py` trae `FeedHibrido`: los autores con más de `umbral` seguidores se leen al abrir el feed, y los demás se copian al publicar. Su comentario describe la regla.

1. Completa los tres `TODO`.
2. Corre el archivo y las pruebas (el archivo tarda unos segundos: simula un día completo):
   ```
   python3 hibrido_ejercicio2.py
   pytest test_hibrido_ejercicio2.py
   ```
3. Completa la tabla con lo que imprime el `main` para un día de inscripciones:

| Estrategia | Escrituras en el día | Lecturas en el día |
|---|---|---|
| Fan-out on write | _(…)_ | _(…)_ |
| Fan-out on read | _(…)_ | _(…)_ |
| Híbrido | _(…)_ | _(…)_ |

4. Responde: en ese día, ¿cuántas veces se lee cada feed por cada publicación? Con ese ratio de lectura a escritura, ¿qué estrategia elegirías para ReservaU, y por qué no es la que hace menos escrituras?

_(tu respuesta)_

5. Responde: el `umbral` es 1000. Un equipo con 999 seguidores consigue uno más. ¿Qué pasa con sus publicaciones viejas y con las nuevas? ¿Qué umbral elegirías, y con qué dato?

_(tu respuesta)_

## Ejercicio 3: el orden del feed

`ranking_ejercicio3.py` describe en su comentario `OrdenadorDeFeed`: un puntaje que combina interacciones, si el equipo es tuyo y cuánto tiempo pasó, una regla para no mostrar tres seguidas del mismo autor, y los espacios más reservados de la semana. Esta vez no hay código de partida: escribes la clase.

1. Escribe `OrdenadorDeFeed`.
2. Corre las pruebas:
   ```
   pytest test_ranking_ejercicio3.py
   ```
3. Responde: el puntaje se calcula al leer el feed, no al publicar. ¿Por qué no se puede guardar una sola vez con la publicación? ¿Qué parte de él sí se podría guardar?

_(tu respuesta)_

4. Responde: un equipo descubre que si sus jugadores confirman y desconfirman asistencia muchas veces, su publicación sube en el feed de todo el campus. ¿Qué cambiarías en el puntaje?

_(tu respuesta)_

5. Diseña el feed de ReservaU: qué estrategia de fan-out usa cada tipo de autor (equipos de un curso, equipos oficiales, la final del campeonato, los espacios), dónde se calcula el ranking, y qué número de la tabla del Ejercicio 2 justifica cada decisión.

_(tu respuesta)_

### Checklist final

- [ ] Cada estrategia cuenta sus escrituras y lecturas como dice su comentario.
- [ ] El feed híbrido copia solo a los autores que no son masivos, y junta los masivos al leer.
- [ ] El orden del feed se puede explicar en una oración.
- [ ] Ninguna operación cambia la lista que recibe.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Is the Red-Green-Refactor Cycle of Test-Driven Development Good? (News UK Technology, Medium)](https://medium.com/news-uk-technology/is-the-red-green-refactor-cycle-of-test-driven-development-good-9e2b1b52d721)

En los laboratorios de las últimas semanas, las pruebas ya estaban escritas cuando abrías el archivo, y tu trabajo era hacerlas pasar. ¿Cambió eso la forma en que escribiste el código? ¿Escribirías las pruebas antes en tu sistema propio, o te parece una pérdida de tiempo?

_(tu respuesta)_

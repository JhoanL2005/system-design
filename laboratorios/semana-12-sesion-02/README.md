# Semana 12, Sesión 2: ReservaU con patrón Composite: jerarquía de espacios tras la expansión

> Objetivo de la sesión: representar la jerarquía de campus, edificios y espacios de ReservaU (espacio simple y espacio compuesto) con el patrón Composite, tratándolos de forma uniforme al buscar disponibilidad.

**Lectura previa de esta sesión:** [Composite Pattern: A Better Way to Build Tree Structures (Medium)](https://medium.com/@prabhavithreddy/composite-pattern-a-better-way-to-build-tree-structures-86c3d31e3f42)

**Referencia de esta sesión:** [Composite (Refactoring.Guru)](https://refactoring.guru/design-patterns/composite)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-12-sesion-02
```

`reservas.py` es el mismo de la sesión pasada: cada espacio y cada equipo que se reserva tiene su propio `CalendarioDeCancha`. No se modifica.

El Ejercicio 3 importa `Recurso` y `Reservable` de `inventario_ejercicio2.py`, así que necesita completo el Ejercicio 2.

## Respuesta sobre la lectura

Según el artículo, ¿qué problema resuelve el patrón Composite? ¿Qué tienen en común, en su ejemplo, el objeto simple y el compuesto?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

Con las salas de estudio en los pisos de la biblioteca y los proyectores en las salas, ¿cómo recorrerías el campus para saber qué hay libre el martes de 18 a 19? ¿Qué pasa con ese recorrido si mañana agregan un nivel más?

_(tu respuesta)_

## Ejercicio 1: la jerarquía de espacios del campus

Este ejercicio se resuelve en vivo, sobre `espacios_ejercicio1.py`. Córrelo una vez antes de que empiece: la Parte A funciona, y la Parte B termina con `NotImplementedError`.

```
python3 espacios_ejercicio1.py
```

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** en el campus de la Parte A, la cancha-1 y la sala-102 están reservadas de 18 a 19. Hay 3 canchas y 3 salas. ¿Qué devuelve `buscar_libres_preguntando` para esa franja, y por qué?

_(tu respuesta)_

**Respuesta 2:** con la Parte B resuelta, `biblioteca.libres(18, 19)` y `campus.libres(18, 19)` se llaman igual. ¿Qué devuelve cada una? ¿Qué habría que cambiar en `GrupoDeRecursos` para que la búsqueda vea un "Ala norte" dentro de un "Piso 3"?

_(tu respuesta)_

**Respuesta 3:** ¿cuál es la capacidad total de la biblioteca, y en qué momento deja de llamarse `capacidad_total` hacia abajo?

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

## Ejercicio 2: espacios y equipos en el mismo árbol

`inventario_ejercicio2.py` pone en un solo árbol las canchas, las salas, los balones y los proyectores. Su comentario describe las cuatro operaciones que tiene que responder cualquier nodo: `buscar`, `contar`, `encontrar` y `rutas`.

1. Completa los `TODO` 1 a 4, la hoja y el compuesto de cada uno.
2. Corre el archivo y las pruebas:
   ```
   python3 inventario_ejercicio2.py
   pytest test_inventario_ejercicio2.py
   ```
3. Responde: `reservar_en` encuentra el recurso por su nombre y lo reserva, sin saber si es una cancha o un proyector, ni en qué nivel está. ¿Qué tuviste que cambiar en `Grupo` o en `Reservable` para que `test_un_tipo_nuevo_no_cambia_ningun_metodo` pasara con los casilleros?

_(tu respuesta)_

4. Responde: `agregar` está en `Grupo` y no en `Recurso`. ¿Qué ganas y qué pierdes con eso? Piensa en qué pasa si alguien llama `agregar` sobre un proyector.

_(tu respuesta)_

## Ejercicio 3: la cancha que se divide en dos

`cancha_divisible_ejercicio3.py` describe en su comentario `CanchaDivisible`: una cancha que se reserva completa o por mitades. Esta vez no hay código de partida: escribes la clase.

1. Escribe `CanchaDivisible`.
2. Corre las pruebas:
   ```
   pytest test_cancha_divisible_ejercicio3.py
   ```
3. Responde: ¿`CanchaDivisible` es una hoja o un compuesto? ¿Qué tiene de cada uno?

_(tu respuesta)_

4. Responde: ¿por qué `reservar` verifica las dos mitades antes de reservar la primera? ¿Qué regla de la Semana 11 es esa?

_(tu respuesta)_

5. Responde: si alguien hace `biblioteca.agregar(campus)`, el campus queda adentro de uno de sus propios hijos. ¿Qué pasa la próxima vez que alguien llama `campus.buscar("sala", 18, 19)`? ¿Dónde pondrías la verificación para impedirlo, y qué tendría que saber hacer cada nodo?

_(tu respuesta)_

### Checklist final

- [ ] Ninguna búsqueda pregunta de qué clase es un nodo.
- [ ] Agregar un nivel, o un tipo de recurso nuevo, no cambia ningún método.
- [ ] Cualquier nodo del árbol responde las mismas operaciones, y la recursión termina en las hojas.
- [ ] Reservar la cancha completa no deja nunca media reserva.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Real-time communication at scale with Elixir at Discord (Discord Engineering, elixir-lang.org)](https://elixir-lang.org/blog/2020/10/08/real-time-communication-at-scale-with-elixir-at-discord/)

La semana pasada, el calendario avisaba a una lista de espera que vivía en la misma memoria. Ahora imagina 300 estudiantes con la app abierta en el calendario de la cancha-1 el día de inscripciones: cuando alguien reserva, los 300 tienen que ver la franja ocupada sin refrescar. ¿Quién tendría que avisar a esos 300 teléfonos, y por qué Observer, como lo escribimos, no alcanza?

_(tu respuesta)_

# Semana 11, Sesión 2: Domain-Driven Design: bounded contexts, agregados y value objects

> Objetivo de la sesión: delimitar el bounded context del sistema propio y diseñar al menos un agregado con su raíz, sus entidades internas y sus value objects.

**Lectura previa de esta sesión:** [Aggregates in Domain Driven Design (Medium)](https://medium.com/ingeniouslysimple/aggregates-in-domain-driven-design-5aab3ef9901d)

**Referencia de esta sesión:** [Use tactical DDD to design microservices (Microsoft Learn, Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-11-sesion-02
```

El Ejercicio 2 importa `FranjaHoraria` y `Reserva` de `franja_ejercicio1.py`, así que necesita ese archivo completo.

## Respuesta sobre la lectura

Según el artículo, ¿qué es un agregado? ¿Qué reglas protege el agregado `Car` del ejemplo, y por qué la regla de las 4 ruedas no se puede verificar desde una `Wheel`?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

La regla "un estudiante no puede tener más de 2 reservas el mismo día" vive hoy en una función que recibe un número que le pasa el caso de uso. Si dos solicitudes de ana llegan al mismo tiempo, las dos pueden leer "1 reserva" y confirmarse. ¿Qué objeto del dominio tendría que ser el dueño de esa regla para que nadie pueda saltársela?

_(tu respuesta)_

## Ejercicio 1: Una franja y una reserva

Este ejercicio se resuelve en vivo, sobre `franja_ejercicio1.py`. Córrelo una vez antes de que empiece:

```
python3 franja_ejercicio1.py
```

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** sin resolver, `franja_a == franja_b` imprime `False` aunque las dos franjas tienen la misma fecha y las mismas horas, y una franja de 20 a 18 tiene duración -2. ¿Qué esperas que cambie en esas dos líneas con `@dataclass(frozen=True)` y `__post_init__`?

_(tu respuesta)_

**Respuesta 2:** `reserva` y `la_misma_leida_otra_vez` tienen el mismo id y franjas distintas. Con el `__eq__` por id, ¿son iguales? ¿Por qué una reserva no se compara como una franja?

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

## Ejercicio 2: El calendario de una cancha

`calendario_ejercicio2.py` trae `CalendarioDeCancha`, la raíz de un agregado que guarda todas las reservas de una cancha en un día. Su comentario describe las dos reglas que tiene que cumplir siempre.

1. Completa los cinco `TODO`.
2. Corre las pruebas:
   ```
   pytest test_calendario_ejercicio2.py
   ```
3. Responde: `reservas()` devuelve tuplas `(id, estudiante, franja)` y no los objetos `Reserva` de `self._reservas`. ¿Qué podría hacer alguien de afuera si recibiera los objetos `Reserva`? ¿Por qué con la franja no hay ese riesgo?

_(tu respuesta)_

4. Responde: este agregado puede garantizar "máximo 2 horas por estudiante en esta cancha este día". ¿Puede garantizar "máximo 2 horas por estudiante entre todas las canchas"? ¿Qué agregado haría falta, y qué regla dejaría de poder garantizar ese otro agregado?

_(tu respuesta)_

## Ejercicio 3: La garantía, en el contexto de Pagos

`garantias_ejercicio3.py` describe en su comentario dos piezas del contexto de Pagos de ReservaU: el value object `Dinero` y el agregado `GarantiaDeReserva`. Esta vez no hay código de partida: escribes las dos clases.

1. Escribe `Dinero` y `GarantiaDeReserva`.
2. Corre las pruebas:
   ```
   pytest test_garantias_ejercicio3.py
   ```
3. Completa el mapa de contextos de ReservaU: una fila por bounded context, con qué significa "Estudiante" (o cómo se le llama) adentro, y qué agregado o agregados viven ahí. Agrega los contextos que creas que faltan.

| Bounded context | Qué significa "Estudiante" adentro | Agregados |
|---|---|---|
| Reservas | _(…)_ | `CalendarioDeCancha` |
| Pagos | _(…)_ | `GarantiaDeReserva` |
| Identidad | _(…)_ | _(…)_ |
| _(…)_ | _(…)_ | _(…)_ |

4. Responde: `GarantiaDeReserva` guarda `id_reserva` como un texto, no la `Reserva`. ¿Qué pasaría si guardara el objeto: quién podría cambiar la reserva, y qué tendría que cargarse de la base de datos cada vez que se cobra una garantía?

_(tu respuesta)_

5. Responde: cuando ana no se presenta, Reservas y Pagos tienen que enterarse. ¿Cambiarías la reserva y la garantía en la misma operación, o una después de la otra? ¿Qué pasa si la segunda falla?

_(tu respuesta)_

### Checklist final

- [ ] Ningún value object se puede modificar después de creado, y uno inválido no llega a existir.
- [ ] Dos entidades son iguales solo si tienen el mismo id.
- [ ] Ninguna operación rechazada del calendario ni de la garantía deja el objeto cambiado.
- [ ] Nada de lo que devuelve `CalendarioDeCancha` permite cambiarlo sin pasar por sus métodos.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [A Case Against the Observer Pattern (Medium)](https://medium.com/@JamieScanlon/a-case-against-the-observer-pattern-dc1cbd80a6a1)

Cuando ana cancela su reserva de las 18:00, beto, que la estaba esperando, no se entera hasta que vuelve a abrir la app y consulta. Si la app consultara sola cada 30 segundos, ¿cuántas consultas haría un día de inscripciones con 2000 estudiantes esperando? ¿Quién debería avisarle a beto?

_(tu respuesta)_

# Semana 11, Sesión 1: Arquitectura limpia (Clean Architecture) y arquitectura hexagonal

> Objetivo de la sesión: identificar las capas y la regla de dependencia de Clean Architecture y de la arquitectura hexagonal, y refactorizar un módulo con lógica de negocio acoplada al framework o a la base de datos.

**Lectura previa de esta sesión:** [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture)

**Referencia de esta sesión:** [Common web application architectures (Microsoft Learn)](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-11-sesion-01
```

Cada ejercicio tiene su propia carpeta, con un archivo por capa (`dominio.py`, `puertos.py`, `casos_de_uso.py`, `adaptadores.py`). Las pruebas de cada ejercicio se corren dentro de su carpeta. La base de datos de hoy es SQLite, que viene con Python (módulo `sqlite3`): el SQL ya está escrito, no hace falta instalar nada ni saber SQL para resolver los ejercicios.

## Respuesta sobre la lectura

Según Cockburn, ¿qué problema quiere resolver la arquitectura hexagonal? ¿Qué es un puerto y qué es un adaptador?

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

En `ApiVersionada`, la misma clase lee rutas, valida cuerpos, traduce formatos, decide si una hora está ocupada y habla con el repositorio. Si mañana cambias el repositorio en memoria por PostgreSQL, ¿cuántos métodos tienes que tocar? ¿Y si agregas una versión 3?

_(tu respuesta)_

## Ejercicio 1: ReservaU por capas

Este ejercicio se resuelve en vivo, en la carpeta `ejercicio1/`. `reservas_acopladas.py` es la API de reservas tal como está hoy: una clase que recibe HTTP, aplica las reglas y escribe en SQLite. Córrelo una vez:

```
cd ejercicio1
python3 reservas_acopladas.py
```

Los otros cuatro archivos son la misma aplicación separada en capas, con 3 `TODO`. Antes de que se muestre cada resultado, responde:

**Respuesta 1:** en `reservas_acopladas.py`, ¿qué líneas tendrías que cambiar si la universidad pasa de SQLite a PostgreSQL? ¿Y si las reservas empiezan a llegar por un chat en vez de HTTP? ¿Qué líneas no cambian en ninguno de los dos casos?

_(tu respuesta)_

**Respuesta 2:** cuando `ReservarCancha` funcione, ¿qué necesita la prueba `test_el_caso_de_uso_rechaza_sin_guardar` para correr: SQLite, HTTP, los dos, o ninguno?

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

## Ejercicio 2: Una segunda puerta de entrada y un puerto de salida

Carpeta `ejercicio2/`. Parte de ReservaU por capas, tal como quedó en el Ejercicio 1, con dos cambios pedidos por la universidad: los estudiantes quieren reservar por chat, y cada reserva confirmada tiene que avisarle al estudiante.

1. Completa los `TODO` 1 a 3: `ReservarCancha` recibe un `Notificador` y lo usa al confirmar; `NotificadorEnMemoria` guarda lo que se envía; `AdaptadorDeMensajeria` traduce un mensaje de texto en una llamada al caso de uso.
2. Corre las pruebas:
   ```
   cd ejercicio2
   pytest test_ejercicio2.py
   ```
3. Completa el `TODO 4` de `main_ejercicio2.py` y córrelo: `python3 main_ejercicio2.py`.
4. Responde: para agregar el chat, ¿qué archivos tocaste y cuáles no? ¿Cambió `ApiHttp`? ¿Por qué el caso de uso no sabe si la reserva llegó por HTTP o por chat?

_(tu respuesta)_

5. Responde: `casos_de_uso.py` llama a `self.notificador.notificar(...)` pero no importa `NotificadorEnMemoria` ni ningún otro adaptador. ¿Quién decide qué notificador recibe? ¿Qué cambiarías para enviar los avisos por correo de verdad?

_(tu respuesta)_

## Ejercicio 3: La cancelación, de acoplada a hexagonal

Carpeta `ejercicio3/`. `cancelaciones_acopladas.py` cancela reservas leyendo y escribiendo en SQLite, mirando la hora del computador y enviando un correo, todo en un método. Su comentario describe las cuatro reglas. Córrelo: el resultado depende de la hora a la que lo corras.

Los puertos ya están definidos en `puertos.py` (`RepositorioDeReservas`, `Reloj`, `Notificador`), y `adaptadores.py` ya trae los dos adaptadores que hablan con el sistema real (`RelojDelSistema`, `NotificadorPorCorreo`). Te toca el resto.

1. Completa los `TODO` 1 a 6: la regla de clasificación en el dominio, el caso de uso `CancelarReserva`, el repositorio en SQLite (con el SQL que hoy está dentro de `cancelaciones_acopladas.py`), el repositorio en memoria, un reloj fijo y un notificador en memoria.
2. Corre las pruebas:
   ```
   cd ejercicio3
   pytest test_ejercicio3.py
   ```
3. Responde: con `cancelaciones_acopladas.py`, ¿cómo probarías que cancelar a las 17:00 una reserva de las 18:00 penaliza, sin esperar a que el reloj marque las 17:00? ¿Qué te permite hacerlo en tu versión?

_(tu respuesta)_

4. Responde: las pruebas de `test_el_repositorio_cumple_el_puerto` corren dos veces, una con cada repositorio. ¿Qué te garantiza que las dos pasen? ¿Qué no te garantiza sobre la base de datos de producción?

_(tu respuesta)_

5. Dibuja, en texto, el hexágono de la cancelación: qué hay en el centro, qué puertos tiene, qué adaptadores se conectan a cada uno (los de prueba y los reales), y hacia dónde apuntan los `import`.

_(tu diagrama)_

### Checklist final

- [ ] `dominio.py` no importa nada.
- [ ] `casos_de_uso.py` solo importa `dominio`.
- [ ] Todo el SQL vive en `adaptadores.py`.
- [ ] Los tests de los tres ejercicios pasan.
- [ ] `main_ejercicio2.py` imprime la reserva de ana por chat, el 409 de beto por HTTP y las dos notificaciones.

## Antes de la próxima sesión

**Lectura:** [Aggregates in Domain Driven Design (Medium)](https://medium.com/ingeniouslysimple/aggregates-in-domain-driven-design-5aab3ef9901d)

La regla "un estudiante no puede tener más de 2 reservas el mismo día" vive hoy en una función del dominio que recibe un número que le pasa el caso de uso. Si dos solicitudes de ana llegan al mismo tiempo, las dos pueden leer "1 reserva" y las dos confirmarse. ¿Qué objeto del dominio tendría que ser el dueño de esa regla para que nadie pueda saltársela?

_(tu respuesta)_

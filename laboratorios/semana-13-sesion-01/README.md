# Semana 13, Sesión 1: ReservaU en tiempo real: calendario de disponibilidad con WebSockets y pub/sub

> Objetivo de la sesión: diseñar la actualización en tiempo real del calendario de disponibilidad de ReservaU con WebSockets, y aplicar el patrón publicador-suscriptor para distribuir cambios de estado entre todos los usuarios que ven el mismo espacio.

**Lectura previa de esta sesión:** [Real-time communication at scale with Elixir at Discord (Discord Engineering, elixir-lang.org)](https://elixir-lang.org/blog/2020/10/08/real-time-communication-at-scale-with-elixir-at-discord/)

**Referencia de esta sesión:** [WebSocket API (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

## Antes de empezar

Entra a esta carpeta:

```
cd laboratorios/semana-13-sesion-01
```

`calendario_eventos.py` trae el calendario que avisa eventos de la Semana 12, ya resuelto, y `reservas.py`, su dominio. `conexiones.py` trae una conexión simulada: representa el WebSocket abierto entre el servidor y la app de un estudiante, como el HTTP simulado de la Semana 10. Ninguno de los tres se modifica.

Los tres ejercicios se encadenan: el Ejercicio 2 y el Ejercicio 3 importan `Canales` de `canales_ejercicio1.py`, así que necesitan completo el Ejercicio 1. Corre cada archivo de prueba por separado.

## Respuesta sobre la lectura

Según el artículo, ¿qué decisiones de diseño le permiten a Discord mantener millones de conexiones abiertas al mismo tiempo? Elige una y di si ReservaU la necesitaría.

_(tu respuesta)_

## Respuesta sobre la pregunta de la sesión pasada

300 estudiantes miran el calendario de la cancha-1 en la app el día de inscripciones; cuando alguien reserva, los 300 tienen que ver la franja ocupada sin refrescar. ¿Quién tendría que avisar a esos 300 teléfonos, y por qué Observer, como lo escribimos, no alcanza?

_(tu respuesta)_

## Ejercicio 1: el calendario en vivo de una cancha

Este ejercicio se resuelve en vivo, sobre `canales_ejercicio1.py`. Córrelo una vez antes de que empiece: termina con `NotImplementedError`.

```
python3 canales_ejercicio1.py
```

Antes de que se muestre cada resultado, responde:

**Respuesta 1:** 300 apps miran la cancha-1 y 50 la cancha-2. Cuando ana reserva la cancha-1, ¿cuántos mensajes salen del servidor? Si en vez de eso cada app refrescara cada 5 segundos durante los 10 minutos de inscripciones, ¿cuántas consultas haría la cancha-1?

_(tu respuesta)_

**Respuesta 2:** estudiante-0 deja de mirar la cancha-1 y pasa a la cancha-2. Después beto reserva la cancha-2. ¿Cuántos mensajes salen? ¿Qué pasaría si la app de estudiante-0 hubiera olvidado desuscribirse de la cancha-1?

_(tu respuesta)_

**Respuesta 3:** el teléfono de estudiante-1 pierde la señal y su conexión se cierra. Después ana cancela. ¿Cuántos mensajes se entregan? ¿Cuántas conexiones siguen suscritas a la cancha-1, y qué problema trae eso con el tiempo?

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

## Ejercicio 2: el calendario en vivo con varios servidores

`servidores_ejercicio2.py` reparte las conexiones entre varios servidores y los une con un bus (en producción, por ejemplo, Redis Pub/Sub). Su comentario describe qué hace cada pieza.

1. Completa los cuatro `TODO`.
2. Corre el archivo y las pruebas:
   ```
   python3 servidores_ejercicio2.py
   pytest test_servidores_ejercicio2.py
   ```
3. Responde: en el `main`, 1000 conexiones miran la cancha-1, repartidas en 4 servidores. ¿Cuántos envíos hace el bus para un aviso de la cancha-1? ¿Y para la cancha-3, que mira una sola persona? ¿Qué pasaría con esa cuenta si el bus enviara cada aviso a todos los servidores?

_(tu respuesta)_

4. Responde: `BusEntreServidores.publicar` recorre una copia de la lista de servidores. Sin la copia, ¿qué falla en `test_un_servidor_que_pierde_todas_sus_conexiones_no_salta_al_siguiente`, y por qué?

_(tu respuesta)_

5. Responde: el servidor-2 se cae y sus 250 conexiones se cortan. Las apps se reconectan solas en segundos, a otros servidores. ¿Qué se pierden mientras tanto?

_(tu respuesta)_

## Ejercicio 3: reconectarse sin perder avisos

`reconexion_ejercicio3.py` describe en su comentario `CanalConHistorial`: un intermediario que numera los avisos de cada tema y guarda los últimos, para que una app que se reconecta reciba lo que se perdió. Esta vez no hay código de partida: escribes la clase.

1. Escribe `CanalConHistorial`.
2. Corre las pruebas:
   ```
   pytest test_reconexion_ejercicio3.py
   ```
3. Responde: ¿por qué la app manda el último número que vio, y no la hora a la que perdió la conexión?

_(tu respuesta)_

4. Responde: el historial guarda los últimos 50 avisos de cada tema. ¿Qué pasa si el historial fuera infinito? ¿Y si guardara uno solo? ¿Qué número elegirías para la cancha-1 el día de inscripciones, y con qué dato lo calcularías?

_(tu respuesta)_

5. Diseña, en un diagrama o en una lista de pasos, el camino completo de un aviso en ReservaU: desde que ana reserva en la API (Semana 10) hasta que el teléfono de beto muestra la franja ocupada. Nombra cada pieza (calendario, observador, bus, servidor de conexiones, WebSocket) y qué pasa si cada una falla.

_(tu respuesta)_

### Checklist final

- [ ] Quien publica no conoce a ninguna conexión: solo el tema.
- [ ] Un aviso llega solo a quien mira ese espacio, y una sola vez.
- [ ] Las conexiones cerradas no se quedan para siempre en el servidor.
- [ ] El bus solo envía a los servidores que tienen alguien mirando el tema.
- [ ] Una app que se reconecta recibe lo que se perdió, o sabe que tiene que recargar.
- [ ] Los tests de los tres ejercicios pasan.

## Antes de la próxima sesión

**Lectura:** [Mastering News Feed System Design: A Comprehensive Deep Dive (Medium)](https://medium.com/@rafinutshaw/mastering-news-feed-system-design-a-comprehensive-deep-dive-bae6f57289be)

ReservaU va a tener un feed de actividad: los próximos partidos de los equipos que sigues y los espacios más reservados. El equipo de fútbol de un curso lo siguen 10 personas; el partido de la final del campeonato lo sigue todo el campus, 8000 personas. Si cada vez que alguien publica algo se copia a la lista de cada seguidor, ¿cuántas escrituras cuesta cada uno de esos dos casos? ¿Se te ocurre otra forma?

_(tu respuesta)_

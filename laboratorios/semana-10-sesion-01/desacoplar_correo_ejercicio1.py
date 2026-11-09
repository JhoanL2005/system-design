"""Ejercicio 1: sacar el envio del correo del camino de la reserva, con
una cola de mensajes entre los dos.

Corre esto para ver el resultado:

    python3 desacoplar_correo_ejercicio1.py

Y las pruebas con:

    pytest test_desacoplar_correo_ejercicio1.py
"""

from cola import ColaDeMensajes
from servicios import RepositorioDeReservas, ServicioDeCorreo, asunto_de_confirmacion


class ServicioSincrono:
    def __init__(self, repositorio, correo):
        self.repositorio = repositorio
        self.correo = correo

    def reservar(self, estudiante, cancha, hora):
        if not self.repositorio.esta_libre(cancha, hora):
            return "ocupada"
        self.repositorio.registrar(estudiante, cancha, hora)
        cuerpo = {"estudiante": estudiante, "cancha": cancha, "hora": hora}
        enviado = self.correo.enviar(estudiante, asunto_de_confirmacion(cuerpo))
        if not enviado:
            return "error"
        return "confirmada"


class ServicioConCola:
    def __init__(self, repositorio, cola):
        self.repositorio = repositorio
        self.cola = cola

    def reservar(self, estudiante, cancha, hora):
        # Igual que ServicioSincrono, pero sin tocar el correo: la reserva
        # se confirma apenas queda registrada, y el correo queda como un
        # mensaje en la cola para que lo envie el trabajador.
        if not self.repositorio.esta_libre(cancha, hora):
            return "ocupada"
        self.repositorio.registrar(estudiante, cancha, hora)
        cuerpo = {"estudiante": estudiante, "cancha": cancha, "hora": hora}
        self.cola.publicar(cuerpo)
        return "confirmada"


class TrabajadorDeCorreo:
    def __init__(self, cola, correo):
        self.cola = cola
        self.correo = correo

    def procesar_pendientes(self):
        # Mientras haya mensajes, envia cada correo y confirma el mensaje
        # solo si el envio salio bien. Si falla, se detiene sin confirmar:
        # el mensaje queda en la cola y vuelve cuando venza su visibilidad.
        mensaje = self.cola.recibir()
        while mensaje is not None:
            cuerpo = mensaje["cuerpo"]
            enviado = self.correo.enviar(cuerpo["estudiante"], asunto_de_confirmacion(cuerpo))
            if not enviado:
                return
            self.cola.confirmar(mensaje["id"])
            mensaje = self.cola.recibir()


if __name__ == "__main__":
    print("Version sincrona")
    repositorio = RepositorioDeReservas()
    correo = ServicioDeCorreo()
    correo.caido = True
    servicio = ServicioSincrono(repositorio, correo)
    print("Respuesta a ana:", servicio.reservar("ana", "Cancha 1", 18))
    print("Reservas en el repositorio:", len(repositorio.reservas))
    print("Correos enviados:", len(correo.enviados))
    print("Ana reintenta:", servicio.reservar("ana", "Cancha 1", 18))

    print()
    print("Version con cola")
    repositorio = RepositorioDeReservas()
    correo = ServicioDeCorreo()
    correo.caido = True
    cola = ColaDeMensajes("correos")
    servicio = ServicioConCola(repositorio, cola)
    print("Respuesta a ana:", servicio.reservar("ana", "Cancha 1", 18))
    print("Reservas en el repositorio:", len(repositorio.reservas))
    print("Mensajes esperando en la cola:", cola.cantidad_disponibles())

    correo.caido = False
    print("El correo vuelve")
    trabajador = TrabajadorDeCorreo(cola, correo)
    trabajador.procesar_pendientes()
    print("Correos enviados:", len(correo.enviados))
    print("Mensajes esperando en la cola:", cola.cantidad_disponibles())

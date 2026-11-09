"""Ejercicio 3: la reserva en tres pasos (elegir cancha, elegir hora,
confirmar), detras de un balanceador con varios servidores.

ServidorConEstado ya esta completo: guarda el borrador de cada
estudiante en su propia memoria. Tu trabajo es ServidorSinEstado, con
el mismo comportamiento, pero sin guardar nada propio entre una llamada
y la siguiente.

Corre las pruebas con:

    pytest test_reserva_en_pasos_ejercicio3.py

No cambies los nombres de las clases ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class ServidorConEstado:
    def __init__(self, nombre, repositorio, cola):
        self.nombre = nombre
        self.repositorio = repositorio
        self.cola = cola
        self.borradores = {}

    def iniciar(self, estudiante, cancha):
        self.borradores[estudiante] = {"cancha": cancha, "hora": None}
        return "ok"

    def elegir_hora(self, estudiante, hora):
        borrador = self.borradores.get(estudiante)
        if borrador is None:
            return "sin borrador"
        if not self.repositorio.esta_libre(borrador["cancha"], hora):
            return "ocupada"
        borrador["hora"] = hora
        return "ok"

    def confirmar(self, estudiante):
        borrador = self.borradores.get(estudiante)
        if borrador is None or borrador["hora"] is None:
            return "sin borrador"
        if not self.repositorio.esta_libre(borrador["cancha"], borrador["hora"]):
            return "ocupada"
        self.repositorio.registrar(estudiante, borrador["cancha"], borrador["hora"])
        self.cola.publicar({"estudiante": estudiante, "cancha": borrador["cancha"], "hora": borrador["hora"]})
        self.borradores.pop(estudiante)
        return "confirmada"


class ServidorSinEstado:
    def __init__(self, nombre, repositorio, cola, almacen):
        self.nombre = nombre
        self.repositorio = repositorio
        self.cola = cola
        self.almacen = almacen

    # Ningun metodo guarda datos del estudiante en self: el borrador vive en
    # el almacen compartido, asi que cualquier servidor puede atender
    # cualquier paso de la reserva.

    def clave_de(self, estudiante):
        return "borrador:" + estudiante

    def iniciar(self, estudiante, cancha):
        self.almacen.guardar(self.clave_de(estudiante), {"cancha": cancha, "hora": None})
        return "ok"

    def elegir_hora(self, estudiante, hora):
        borrador = self.almacen.leer(self.clave_de(estudiante))
        if borrador is None:
            return "sin borrador"
        if not self.repositorio.esta_libre(borrador["cancha"], hora):
            return "ocupada"
        borrador["hora"] = hora
        # El almacen entrego una copia: hay que volver a guardarla.
        self.almacen.guardar(self.clave_de(estudiante), borrador)
        return "ok"

    def confirmar(self, estudiante):
        borrador = self.almacen.leer(self.clave_de(estudiante))
        if borrador is None or borrador["hora"] is None:
            return "sin borrador"
        if not self.repositorio.esta_libre(borrador["cancha"], borrador["hora"]):
            return "ocupada"
        self.repositorio.registrar(estudiante, borrador["cancha"], borrador["hora"])
        self.cola.publicar({"estudiante": estudiante, "cancha": borrador["cancha"], "hora": borrador["hora"]})
        self.almacen.borrar(self.clave_de(estudiante))
        return "confirmada"

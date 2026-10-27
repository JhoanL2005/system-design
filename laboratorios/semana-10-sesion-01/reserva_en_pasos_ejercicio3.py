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

    def iniciar(self, estudiante, cancha):
        # TODO: guarda el borrador {"cancha": ..., "hora": None} en
        # self.almacen, con la clave "borrador:" + estudiante. Devuelve "ok".
        raise NotImplementedError

    def elegir_hora(self, estudiante, hora):
        # TODO: mismo comportamiento que ServidorConEstado.elegir_hora, con
        # el borrador leido del almacen. Recuerda que el almacen entrega una
        # copia: si cambias la hora, vuelve a guardar el borrador.
        raise NotImplementedError

    def confirmar(self, estudiante):
        # TODO: mismo comportamiento que ServidorConEstado.confirmar, con el
        # borrador leido del almacen. Al confirmar, borra el borrador del
        # almacen.
        raise NotImplementedError

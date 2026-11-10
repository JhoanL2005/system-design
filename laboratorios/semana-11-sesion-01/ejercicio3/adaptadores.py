"""Los adaptadores de la cancelacion. RelojDelSistema y NotificadorPorCorreo
ya estan completos; los demas son tuyos."""

import sqlite3
import time

import correo_simulado
from dominio import Reserva
from puertos import Notificador, Reloj, RepositorioDeReservas


class RepositorioSqlite(RepositorioDeReservas):
    # TODO 3: el SQL de cancelaciones_acopladas.py, movido aqui: las dos
    # tablas en el constructor, y un metodo por cada metodo del puerto.
    # El id que devuelve y recibe es "r-" seguido del numero de SQLite.
    def __init__(self, ruta_base_de_datos):
        self.conexion = sqlite3.connect(ruta_base_de_datos)


class RepositorioEnMemoria(RepositorioDeReservas):
    # TODO 4: el mismo puerto sobre diccionarios, con ids "r-1", "r-2", ...
    pass


class RelojFijo(Reloj):
    # TODO 5: un reloj que siempre devuelve la fecha y la hora que recibio
    # al construirse: RelojFijo("2026-11-10", 16).
    pass


class RelojDelSistema(Reloj):
    def ahora(self):
        return (time.strftime("%Y-%m-%d"), time.localtime().tm_hour)


class NotificadorEnMemoria(Notificador):
    # TODO 6: guarda cada notificacion en self.enviados como una tupla
    # (estudiante, mensaje).
    pass


class NotificadorPorCorreo(Notificador):
    def notificar(self, estudiante, mensaje):
        correo_simulado.enviar_correo(estudiante, mensaje)

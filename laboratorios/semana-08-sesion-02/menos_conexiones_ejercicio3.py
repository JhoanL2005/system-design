"""Ejercicio 3: balanceador de menos conexiones (least connections).

Corre las pruebas con:

    pytest test_menos_conexiones_ejercicio3.py

Las pruebas tambien usan tu BalanceadorRoundRobin del Ejercicio 2, para
comparar los dos algoritmos con el mismo trafico.
"""


class BalanceadorMenosConexiones:
    def __init__(self, servidores):
        self.servidores = servidores

    def enviar(self, duracion):
        # TODO: elige, entre los servidores sanos que todavia pueden
        # atender, el que tiene menos conexiones activas en este momento.
        # Si hay empate, gana el que aparece primero en la lista.
        # Enviale la solicitud y devuelve su nombre. Si ningun servidor
        # puede atenderla, devuelve None.
        for servidores in self.servidores:
            if servidores.health_check() and servidores.puede_atender():
                servidor_menos_conexiones = min(
                    (s for s in self.servidores if s.health_check() and s.puede_atender()),
                    key=lambda s: s.conexiones_activas(),
                    default=None
                )
                if servidor_menos_conexiones:
                    servidor_menos_conexiones.atender(duracion)
                    return servidor_menos_conexiones.nombre
                
        
    
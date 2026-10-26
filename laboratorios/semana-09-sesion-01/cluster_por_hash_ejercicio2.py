"""Ejercicio 2: sharding por hash del estudiante, consulta dirigida y
scatter-gather.

Corre las pruebas con:

    pytest test_cluster_por_hash_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from datos_reservas import hash_estable


class ClusterPorHash:
    def __init__(self, cantidad_de_shards):
        self.cantidad_de_shards = cantidad_de_shards
        self.shards = []
        for _ in range(cantidad_de_shards):
            self.shards.append([])

    def shard_de(self, id_estudiante):
        return hash_estable(id_estudiante) % self.cantidad_de_shards

    def insertar(self, reserva):
        shard_reserva = self.shard_de(reserva.id_estudiante)
        self.shards[shard_reserva].append(reserva)

    def tamanos(self):
        contar = []
        for shard in self.shards:
            contar.append(len(shard))
        return contar
    

    def reservas_de_estudiante(self, id_estudiante):
        reservas = []
        shard_id = self.shard_de(id_estudiante)

        for reserva in self.shards[shard_id]:
            if reserva.id_estudiante == id_estudiante:
                reservas.append(reserva)
        return reservas, 1

    def reservas_de_cancha(self, campus, cancha, fecha):
        reservas_encontradas = []
        for shar in self.shards:
            for reservas in shar:
                if reservas.campus == campus and reservas.cancha == cancha and reservas.fecha == fecha:
                    reservas_encontradas.append(reservas)
        return reservas_encontradas, self.cantidad_de_shards


def fraccion_que_cambia_de_shard(claves, shards_antes, shards_despues):
    cambian = 0
    for clave in claves:
        if hash_estable(clave) % shards_antes != hash_estable(clave) % shards_despues:
            cambian += 1
    return cambian / len(claves)
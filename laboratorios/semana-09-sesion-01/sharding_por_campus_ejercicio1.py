"""Ejercicio 1: repartir las reservas de ReservaU en 4 shards, uno por
campus (reparto por lista).

Corre esto para ver el resultado:

    python3 sharding_por_campus_ejercicio1.py

Y las pruebas con:

    pytest test_sharding_por_campus_ejercicio1.py
"""

from datos_reservas import generar_reservas

SHARD_DE_CAMPUS = {
    "Campus Norte": 0,
    "Campus Sur": 1,
    "Campus Centro": 2,
    "Campus Este": 3,
}


def shard_por_campus(reserva):
    return SHARD_DE_CAMPUS[reserva.campus]


def contar_por_shard(reservas, cantidad_de_shards):
    contar = [0 for i in range(cantidad_de_shards)]
    for reserva in reservas:
        shard = shard_por_campus(reserva)
        contar[shard] += 1
    return contar


if __name__ == "__main__":
    conteo = contar_por_shard(generar_reservas(), 4)
    print("Reservas por shard (campus):", conteo)
    print("El shard mas cargado tiene", max(conteo), "de", sum(conteo), "reservas")

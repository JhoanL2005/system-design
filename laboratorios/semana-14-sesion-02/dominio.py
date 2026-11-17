"""Las reglas de ReservaU de la sesion pasada, ya resueltas: el cupo
semanal y los puntos por cancelar tarde. No lo modifiques.
"""

from datetime import date

CUPO_SEMANAL = 3
PUNTOS_PARA_BLOQUEAR = 3
TRAMOS = [(1440, 0), (120, 1), (0, 2)]


def semana_de(fecha):
    """La semana de una fecha "AAAA-MM-DD", como texto "AAAA-SS"."""
    anio, semana, _ = date.fromisoformat(fecha).isocalendar()
    return str(anio) + "-" + str(semana).zfill(2)


def puntos_por_cancelar(minutos_de_anticipacion):
    for desde, puntos in TRAMOS:
        if minutos_de_anticipacion >= desde:
            return puntos
    return TRAMOS[-1][1]

import dataclasses

import pytest

from garantias_ejercicio3 import Dinero, GarantiaDeReserva


def test_dinero_es_un_value_object():
    assert Dinero(500, "USD") == Dinero(500, "USD")
    assert Dinero(500, "USD") != Dinero(500, "EUR")
    with pytest.raises(dataclasses.FrozenInstanceError):
        Dinero(500, "USD").centavos = 1


def test_dinero_invalido_no_llega_a_existir():
    with pytest.raises(ValueError, match="monto negativo"):
        Dinero(-1, "USD")
    with pytest.raises(ValueError, match="moneda invalida"):
        Dinero(100, "US")


def test_sumar_restar_y_comparar():
    assert Dinero(500, "USD").sumar(Dinero(250, "USD")) == Dinero(750, "USD")
    assert Dinero(500, "USD").restar(Dinero(500, "USD")) == Dinero(0, "USD")
    assert Dinero(501, "USD").es_mayor_que(Dinero(500, "USD"))
    assert not Dinero(500, "USD").es_mayor_que(Dinero(500, "USD"))
    with pytest.raises(ValueError, match="monto negativo"):
        Dinero(100, "USD").restar(Dinero(101, "USD"))


def test_no_se_mezclan_monedas():
    with pytest.raises(ValueError, match="monedas distintas"):
        Dinero(500, "USD").sumar(Dinero(500, "EUR"))
    with pytest.raises(ValueError, match="monedas distintas"):
        Dinero(500, "USD").restar(Dinero(1, "EUR"))
    with pytest.raises(ValueError, match="monedas distintas"):
        Dinero(500, "USD").es_mayor_que(Dinero(1, "EUR"))


def test_texto():
    assert Dinero(500, "USD").texto() == "USD 5.00"
    assert Dinero(1205, "USD").texto() == "USD 12.05"
    assert Dinero(7, "USD").texto() == "USD 0.07"


def garantia():
    return GarantiaDeReserva("g-1", "r-1", "ana", Dinero(500, "USD"))


def test_una_garantia_nueva_esta_retenida():
    g = garantia()
    assert g.estado == "retenida"
    assert g.cobrado == Dinero(0, "USD")
    assert g.id_reserva == "r-1"


def test_devolver():
    g = garantia()
    assert g.devolver() == Dinero(500, "USD")
    assert g.estado == "devuelta"


def test_cobrar_una_parte():
    g = garantia()
    assert g.cobrar(Dinero(200, "USD")) == Dinero(300, "USD")
    assert g.estado == "cobrada"
    assert g.cobrado == Dinero(200, "USD")


def test_cobrar_el_total():
    g = garantia()
    assert g.cobrar(Dinero(500, "USD")) == Dinero(0, "USD")


def test_no_se_cobra_mas_que_la_garantia():
    g = garantia()
    with pytest.raises(ValueError, match="el cobro supera la garantia"):
        g.cobrar(Dinero(501, "USD"))
    assert g.estado == "retenida"
    assert g.cobrado == Dinero(0, "USD")


def test_no_se_cobra_en_otra_moneda():
    g = garantia()
    with pytest.raises(ValueError, match="monedas distintas"):
        g.cobrar(Dinero(100, "EUR"))
    assert g.estado == "retenida"


def test_una_garantia_se_resuelve_una_sola_vez():
    g = garantia()
    g.cobrar(Dinero(200, "USD"))
    with pytest.raises(ValueError, match="la garantia ya fue resuelta"):
        g.devolver()
    with pytest.raises(ValueError, match="la garantia ya fue resuelta"):
        g.cobrar(Dinero(100, "USD"))
    assert g.cobrado == Dinero(200, "USD")
    otra = garantia()
    otra.devolver()
    with pytest.raises(ValueError, match="la garantia ya fue resuelta"):
        otra.cobrar(Dinero(100, "USD"))
    assert otra.estado == "devuelta"


def test_identidad_de_la_garantia():
    a = GarantiaDeReserva("g-1", "r-1", "ana", Dinero(500, "USD"))
    b = GarantiaDeReserva("g-1", "r-1", "ana", Dinero(500, "USD"))
    b.devolver()
    assert a == b
    assert a != GarantiaDeReserva("g-2", "r-1", "ana", Dinero(500, "USD"))

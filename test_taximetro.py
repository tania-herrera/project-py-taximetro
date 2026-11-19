"""Tests de la lógica de tarifas (fase 2). Ejecutar con: python -m pytest"""
import pytest

from taximetro import importe_tramo

TARIFAS = {"tarifa_parado": 0.02, "tarifa_movimiento": 0.05}

def test_parado_10_segundos():
    assert importe_tramo(10, "parado", TARIFAS) == pytest.approx(0.20)

def test_movimiento_10_segundos():
    assert importe_tramo(10, "movimiento", TARIFAS) == pytest.approx(0.50)

def test_segundos_negativos_dan_error():
    with pytest.raises(ValueError):
        importe_tramo(-1, "parado", TARIFAS)

def test_carrera_mixta_suma_tramos():
    importe_parado = importe_tramo(10, "parado", TARIFAS)
    importe_movimiento = importe_tramo(10, "movimiento", TARIFAS)

    total = importe_parado + importe_movimiento

    assert total == pytest.approx(0.70)   

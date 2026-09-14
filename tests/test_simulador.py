"""
Pruebas unitarias para el Simulador Ferroviario RailBoard.
Verifica las funciones lógicas del proyecto:
- Carga de línea de ejemplo y validaciones.
- Búsqueda de trayectos en ambos sentidos (ida y vuelta).
- Cálculo de tiempos estimados en minutos y segundos.
- Cálculo de tarifas y precios de boletos.
- Estadísticas globales de la línea (tramos más largos/cortos, promedios).
- Algoritmo de ordenamiento por burbuja para el historial de simulaciones.
"""

import unittest
from logica import (
    crear_linea_ejemplo,
    validar_datos_linea,
    calcular_recorrido,
    calcular_costo,
    calcular_estadisticas,
    ordenar_simulaciones_por_distancia,
    buscar_posicion_estacion,
)


class TestSimuladorFerroviario(unittest.TestCase):

    def setUp(self):
        self.estaciones, self.distancias, self.velocidad_media, self.distancia_total = crear_linea_ejemplo()

    def test_linea_ejemplo_valida(self):
        """Verifica que los datos de la Línea San Martín precargada sean consistentes."""
        self.assertEqual(len(self.estaciones), 15)
        self.assertEqual(len(self.distancias), 14)
        self.assertEqual(self.velocidad_media, 60.0)
        self.assertEqual(self.distancia_total, 63.0)
        
        es_valido, msj = validar_datos_linea(self.estaciones, self.distancias, self.velocidad_media)
        self.assertTrue(es_valido)
        self.assertEqual(msj, "")

    def test_validacion_linea_rechaza_errores(self):
        """Verifica que el validador detecte estaciones repetidas, distancias negativas y velocidades inválidas."""
        # Menos de 2 estaciones
        valido, _ = validar_datos_linea(["Estación A"], [], 60)
        self.assertFalse(valido)

        # Estación repetida
        valido, _ = validar_datos_linea(["A", "B", "a"], [5.0, 5.0], 60)
        self.assertFalse(valido)

        # Distancia no positiva
        valido, _ = validar_datos_linea(["A", "B", "C"], [5.0, -2.0], 60)
        self.assertFalse(valido)

        # Velocidad negativa o cero
        valido, _ = validar_datos_linea(["A", "B"], [5.0], 0)
        self.assertFalse(valido)

        # Valores no finitos
        valido, _ = validar_datos_linea(["A", "B"], [float("nan")], 60)
        self.assertFalse(valido)
        valido, _ = validar_datos_linea(["A", "B"], [5.0], float("inf"))
        self.assertFalse(valido)

    def test_recorrido_sentido_directo(self):
        """Verifica una simulación de ida (San Miguel -> Retiro)."""
        res = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, "san miguel", "retiro")
        self.assertTrue(res["es_valido"])
        self.assertEqual(res["sentido"], "ida")
        self.assertEqual(res["distancia_total_viaje"], 63.0)
        self.assertEqual(len(res["carteles"]), 14)
        self.assertEqual(res["carteles"][0]["estacion_actual"], "san miguel")
        self.assertEqual(res["carteles"][0]["siguiente_estacion"], "muñiz")
        self.assertEqual(res["cartel_final"]["estacion_actual"], "retiro")
        self.assertEqual(res["cartel_final"]["tiempo_total_minutos"], 63)

    def test_recorrido_sentido_inverso(self):
        """Verifica una simulación de vuelta (Retiro -> San Miguel)."""
        res = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, "retiro", "san miguel")
        self.assertTrue(res["es_valido"])
        self.assertEqual(res["sentido"], "vuelta")
        self.assertEqual(res["distancia_total_viaje"], 63.0)
        self.assertEqual(len(res["carteles"]), 14)
        self.assertEqual(res["carteles"][0]["estacion_actual"], "retiro")
        self.assertEqual(res["carteles"][0]["siguiente_estacion"], "palermo")
        self.assertEqual(res["cartel_final"]["estacion_actual"], "san miguel")
        self.assertEqual(res["cartel_final"]["tiempo_total_minutos"], 63)

    def test_recorrido_tramo_intermedio(self):
        """Verifica una simulación de tramo intermedio (Bella Vista -> Hurlingham)."""
        res = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, "bella vista", "hurlingham")
        self.assertTrue(res["es_valido"])
        # Bella Vista -> Morris (5km) + Morris -> Hurlingham (5km) = 10km
        self.assertEqual(res["distancia_total_viaje"], 10.0)
        self.assertEqual(len(res["carteles"]), 2)

    def test_recorrido_estaciones_invalidas(self):
        """Verifica que se rechacen estaciones inexistentes o iguales."""
        # Misma estación
        res = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, "morris", "morris")
        self.assertFalse(res["es_valido"])

        # Estación inexistente
        res = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, "estacion fantasmal", "retiro")
        self.assertFalse(res["es_valido"])

    def test_calculo_costos(self):
        """Verifica la fórmula de cálculo de tarifas: tarifa_base + distancia * tarifa_km."""
        # 10 km, tarifa_base = 50, tarifa_km = 15 -> 50 + 150 = 200
        costo = calcular_costo(10.0, 50.0, 15.0)
        self.assertTrue(costo["es_valido"])
        self.assertEqual(costo["costo_km"], 150.0)
        self.assertEqual(costo["precio_total"], 200.0)

        # Tarifas inválidas
        costo_invalido = calcular_costo(10.0, -10.0, 15.0)
        self.assertFalse(costo_invalido["es_valido"])

        costo_invalido_km = calcular_costo(10.0, 50.0, 0.0)
        self.assertFalse(costo_invalido_km["es_valido"])

        costo_no_finito = calcular_costo(10.0, 50.0, float("nan"))
        self.assertFalse(costo_no_finito["es_valido"])

    def test_estadisticas_linea(self):
        """Verifica el cálculo de estadísticas generales de la línea."""
        stats = calcular_estadisticas(self.estaciones, self.distancias, self.velocidad_media, self.distancia_total)
        self.assertTrue(stats["es_valido"])
        self.assertEqual(stats["total_estaciones"], 15)
        self.assertEqual(stats["distancia_total"], 63.0)
        self.assertAlmostEqual(stats["distancia_promedio"], 63.0 / 14, places=2)
        
        # Tramo más largo en la línea San Martín es Palermo -> Retiro (10 km)
        self.assertEqual(stats["tramo_mas_largo"]["distancia"], 10.0)
        self.assertEqual(stats["tramo_mas_largo"]["origen"], "palermo")
        self.assertEqual(stats["tramo_mas_largo"]["destino"], "retiro")

        # Tramo más corto es de 3 km (por ejemplo San Miguel -> Muñiz)
        self.assertEqual(stats["tramo_mas_corto"]["distancia"], 3.0)

    def test_ordenamiento_burbuja_historial(self):
        """Verifica que el algoritmo de ordenamiento por burbuja ordene correctamente los trayectos por distancia."""
        simulaciones = [
            "Retiro -> San Miguel",
            "Bella Vista -> Morris",
            "Palermo -> Retiro",
            "Caseros -> Devoto"
        ]
        distancias = [63.0, 5.0, 10.0, 7.0]

        sim_ord, dist_ord = ordenar_simulaciones_por_distancia(simulaciones, distancias)

        self.assertEqual(dist_ord, [5.0, 7.0, 10.0, 63.0])
        self.assertEqual(sim_ord, [
            "Bella Vista -> Morris",
            "Caseros -> Devoto",
            "Palermo -> Retiro",
            "Retiro -> San Miguel"
        ])


if __name__ == "__main__":
    unittest.main()

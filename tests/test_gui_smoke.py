"""
Smoke test para la interfaz gráfica SimuladorFerroviarioApp.
Verifica que todas las vistas y transiciones de pantalla se construyan
y ejecuten sin lanzar excepciones en Tkinter.
"""

import unittest
import tkinter as tk
from app_gui import SimuladorFerroviarioApp


class TestGUISmoke(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana durante pruebas
        self.app = SimuladorFerroviarioApp(self.root)

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_flujo_completo_vistas(self):
        """Recorre todas las pantallas de la interfaz asegurando que no fallen."""
        # 1. Presentación
        self.app.mostrar_presentacion()
        self.app.root.update_idletasks()

        # 2. Elección de inicio
        self.app.mostrar_eleccion_inicio()
        self.app.root.update_idletasks()

        # 3. Cargar ejemplo
        self.app.cargar_ejemplo_y_confirmar()
        self.app.root.update_idletasks()
        self.assertEqual(len(self.app.estaciones), 15)

        # 4. Menú principal
        self.app.mostrar_menu_principal()
        self.app.root.update_idletasks()

        # 5. Simulación de viaje
        self.app.mostrar_simulacion_viaje()
        self.app.root.update_idletasks()

        # 6. Simulación de costos
        self.app.mostrar_simulacion_costos()
        self.app.root.update_idletasks()

        # 7. Estadísticas
        self.app.mostrar_estadisticas()
        self.app.root.update_idletasks()

        # 8. Datos de la línea
        self.app.mostrar_datos_linea()
        self.app.root.update_idletasks()

        # 9. Historial
        self.app.mostrar_historial()
        self.app.root.update_idletasks()

        # 10. Carga manual
        self.app.mostrar_carga_datos_tren()
        self.app.root.update_idletasks()

        # 11. Cierre
        self.app.mostrar_cierre_programa()
        self.app.root.update_idletasks()


if __name__ == "__main__":
    unittest.main()


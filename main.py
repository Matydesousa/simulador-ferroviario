"""
Punto de entrada principal para RAIL BOARD — Simulador Ferroviario.
Desarrollado por Matías Joaquín De Sousa.

Ejecución:
    py -3 main.py
"""

from app_gui import SimuladorFerroviarioApp


def main():
    app = SimuladorFerroviarioApp()
    app.ejecutar()


if __name__ == "__main__":
    main()


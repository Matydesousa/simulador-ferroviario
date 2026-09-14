# RailBoard — Simulador Ferroviario

Aplicación de escritorio interactiva desarrollada en Python para simular el panel informativo, los recorridos, los tiempos estimados, las tarifas y las estadísticas de una línea ferroviaria.

El proyecto nació como trabajo final de **Introducción a la Programación**. Esta versión reemplaza la interacción por terminal con una interfaz gráfica en Tkinter, conservando el flujo, los cálculos y el algoritmo de ordenamiento por burbuja del trabajo original.

## Funcionalidades

- Presentación y configuración inicial guiada.
- Carga manual de estaciones, distancias y velocidad media.
- Línea de ejemplo precargada, inspirada en la Línea San Martín.
- Confirmación y consulta completa de los datos ingresados.
- Simulación de viajes en ambos sentidos.
- Carteles ferroviarios secuenciales con avance manual o automático.
- Tiempo estimado por tramo y tiempo total del recorrido.
- Cálculo de tarifas mediante precio base y valor por kilómetro.
- Estadísticas de la línea: distancia total y promedio, tramos extremos y duración.
- Historial cronológico y ordenado por distancia mediante el algoritmo de burbuja original.

## Tecnologías

- Python 3.10 o superior.
- Tkinter y ttk.
- `unittest` para las pruebas automatizadas.

No requiere instalar paquetes externos.

## Ejecución

Desde la carpeta del proyecto:

```powershell
py -3 main.py
```

También puede ejecutarse con:

```bash
python main.py
```

## Pruebas

```powershell
py -3 -m unittest discover -s tests -v
```

## Estructura

```text
simulador-ferroviario/
├── main.py                  # Punto de entrada
├── app_gui.py               # Interfaz gráfica y flujo de la aplicación
├── logica.py                # Recorridos, tarifas, estadísticas y ordenamiento
├── tests/
│   ├── test_simulador.py   # Pruebas de la lógica
│   └── test_gui_smoke.py   # Comprobación de las vistas gráficas
├── README.md
└── .gitignore
```

## Datos demostrativos

La línea precargada utiliza datos ilustrativos. Sus distancias y tiempos no representan información ferroviaria oficial ni en tiempo real.

## Autor

Desarrollado por **Matías Joaquín De Sousa** como proyecto final de introducción a la programación.

GitHub: [Matydesousa](https://github.com/Matydesousa)

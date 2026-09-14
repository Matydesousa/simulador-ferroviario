# RailBoard — Simulador ferroviario
# RailBoard — Simulador Ferroviario

Aplicación de escritorio para configurar una línea ferroviaria y simular recorridos, tiempos estimados y tarifas entre sus estaciones.
Aplicación de escritorio interactiva en **Python** para simular el panel informativo, recorridos, tiempos estimados, tarifas y estadísticas de una línea ferroviaria.

RailBoard nació como trabajo final de introducción a la programación y fue reorganizado como proyecto de portfolio: la lógica de negocio está separada de la interfaz, las validaciones son reutilizables y los cálculos principales están cubiertos por pruebas unitarias.
Este proyecto nació como trabajo final de la materia **Introducción a la Programación** y fue optimizado con una **interfaz gráfica moderna (GUI)** en Tkinter que preserva intacta la lógica, el flujo y los algoritmos procedurales originales.

## Funcionalidades
---

- Panel general con estaciones, distancia total, velocidad y duración completa.
- Simulación de recorridos en ambos sentidos.
- Carteles paso a paso con controles manuales y reproducción automática.
- Detalle de cada tramo y tiempo estimado hasta la siguiente estación.
- Cálculo y desglose de tarifas mediante precio base y valor por kilómetro.
- Estadísticas del tramo más corto, más largo y distancia promedio.
- Historial filtrable y ordenable por momento o distancia.
- Editor visual para crear una línea estación por estación.
- Línea de ejemplo precargada para explorar la aplicación inmediatamente.
- Sección informativa sobre el proyecto original y su autor.
## 🚆 Características Principales

## Tecnologías
1. **Cartel Informativo Ferroviario Digital**:
   - Visualización estilo panel LED de estaciones de tren.
   - Recorrido paso a paso: estación actual, próxima parada y tiempo estimado (en minutos o segundos).
   - Avance manual o reproducción automática con barra de progreso.
   - Simulación de viajes en **ambos sentidos** (ida y vuelta) y tramos intermedios.
   - Cartel final de arribo con tiempo total de viaje.

- Python 3.10+
- Tkinter y ttk
- `dataclasses`, `decimal` y `unittest` de la biblioteca estándar
2. **Simulación de Costos y Tarifas**:
   - Ingreso de tarifa base y tarifa por kilómetro.
   - Desglose completo del boleto: distancia recorrida, cargo por distancia, tarifa base y precio final.

No requiere paquetes externos.
3. **Estadísticas de la Línea**:
   - Cantidad total de estaciones y tramos.
   - Distancia total y promedio de kilómetros entre estaciones.
   - Identificación automática del **tramo más largo** y el **tramo más corto** con nombres de estaciones.
   - Tiempo total de recorrido de la línea completa a la velocidad media configurada.

## Ejecutar
4. **Historial con Ordenamiento por Burbuja**:
   - Registro en memoria de todas las simulaciones de viaje y costos realizadas.
   - Doble visualización: **orden cronológico** y **ordenado por distancia** (aplicando el algoritmo de ordenamiento por burbuja original).

Desde la raíz del proyecto:
5. **Carga Guiada y Línea Predefinida**:
   - Asistente de carga para ingresar una nueva línea con validación de entradas (nombres únicos, distancias positivas y velocidad).
   - Línea de ejemplo precargada inspirada en la **Línea San Martín** (15 estaciones desde San Miguel hasta Retiro, 14 tramos, 60 km/h).

---

## 🛠️ Tecnologías y Requisitos

- **Python 3.10 o superior**
- **Tkinter** y **ttk** (incluidos en la biblioteca estándar de Python)
- **unittest** (para pruebas automatizadas)

> [!NOTE]
> No requiere la instalación de librerías ni paquetes externos (`pip`). Funciona directamente con la instalación estándar de Python.

---

## 🚀 Cómo Ejecutar

Desde la carpeta del proyecto:

```powershell
py -3 main.py
```

## Pruebas
O también:

```bash
python main.py
```

---

## 🧪 Pruebas Automatizadas

Para ejecutar la suite de pruebas unitarias y pruebas de renderizado de la interfaz:

```powershell
py -3 -m unittest discover -s tests -v
```

## Estructura
---

## 📁 Estructura del Proyecto

```text
simulador-ferroviario/
├── main.py                 # Punto de entrada
├── railboard/
│   ├── models.py           # Línea, recorridos, tarifas y estadísticas
│   └── ui.py               # Interfaz gráfica
└── tests/
    └── test_models.py      # Pruebas del dominio
├── main.py                  # Punto de entrada de la aplicación
├── logica.py                # Lógica procedural, cálculos de ruta, tarifas, estadísticas y ordenamiento burbuja
├── app_gui.py               # Interfaz gráfica moderna con panel LED y navegación interactiva (Tkinter)
├── tests/
│   ├── test_simulador.py   # Pruebas unitarias de la lógica del dominio
│   └── test_gui_smoke.py   # Pruebas de integración de la interfaz gráfica
├── README.md                # Documentación del proyecto
└── .gitignore               # Exclusiones de Git para Python
```

## Datos demostrativos
---

La línea precargada está inspirada en un recorrido ferroviario del área metropolitana de Buenos Aires. Sus distancias y tiempos son ilustrativos y no deben interpretarse como información oficial ni en tiempo real.
## 👤 Autor

## Autor
Desarrollado por **Matías Joaquín De Sousa** como proyecto final de introducción a la programación.

Desarrollado por **Matias Joaquin De Sousa** como trabajo final de introducción a la programación.

Perfil de GitHub del autor: [manuelventuradesousa1035-prog](https://github.com/manuelventuradesousa1035-prog).
- GitHub: [manuelventuradesousa1035-prog](https://github.com/manuelventuradesousa1035-prog) *(cuenta personal del autor)*

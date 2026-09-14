"""
Módulo de lógica del Simulador Ferroviario RailBoard.
Basado en el proyecto original de introducción a la programación por Matías Joaquín De Sousa.

Contiene las funciones principales para:
- Creación y validación de datos de líneas ferroviarias.
- Cálculo de distancias y tiempos de viaje (ida y vuelta).
- Generación de carteles informativos secuenciales.
- Simulación y desglose de tarifas.
- Cálculo de estadísticas de la línea.
- Algoritmo de ordenamiento por burbuja para el historial de simulaciones.
"""

from math import isfinite
from typing import List, Tuple, Dict, Any


def crear_linea_ejemplo() -> Tuple[List[str], List[float], float, float]:
    """
    Retorna los datos predefinidos de la Línea San Martín (ejemplo original del proyecto):
    - estaciones: Lista de nombres de estaciones.
    - distancias: Lista de distancias entre estaciones consecutivas (en km).
    - velocidad_media: Velocidad media del tren en km/h (60 km/h).
    - distancia_total: Suma de todas las distancias en km.
    """
    estaciones = [
        "san miguel",
        "muñiz",
        "bella vista",
        "morris",
        "hurlingham",
        "el palomar",
        "caseros",
        "santos lugares",
        "saenz peña",
        "devoto",
        "villa del parque",
        "la paternal",
        "villa crespo",
        "palermo",
        "retiro"
    ]
    distancias = [3.0, 4.0, 5.0, 5.0, 5.0, 5.0, 4.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 10.0]
    velocidad_media = 60.0
    distancia_total = sum(distancias)
    return estaciones, distancias, velocidad_media, distancia_total


def validar_datos_linea(
    estaciones: List[str],
    distancias: List[float],
    velocidad_media: float
) -> Tuple[bool, str]:
    """
    Valida la coherencia de los datos ingresados para una línea ferroviaria.
    Retorna (True, "") si es válido, o (False, mensaje_error) si no lo es.
    """
    if len(estaciones) < 2:
        return False, "El número de estaciones debe ser mayor a 1."

    # Validar nombres de estaciones no vacíos
    for i, est in enumerate(estaciones):
        if not est or not est.strip():
            return False, f"El nombre de la estación {i + 1} no puede estar vacío."

    # Validar que no haya estaciones repetidas (sin distinguir mayúsculas/minúsculas)
    nombres_limpios = [e.strip().lower() for e in estaciones]
    for i in range(len(nombres_limpios)):
        for j in range(i + 1, len(nombres_limpios)):
            if nombres_limpios[i] == nombres_limpios[j]:
                return False, f"La estación '{estaciones[i]}' está repetida. Ingrese nombres únicos."

    if len(distancias) != len(estaciones) - 1:
        return False, "La cantidad de distancias debe ser igual a la cantidad de estaciones menos una."

    # Validar distancias positivas
    for i, dist in enumerate(distancias):
        try:
            val = float(dist)
            if not isfinite(val) or val <= 0:
                return False, f"La distancia del tramo {i + 1} ({estaciones[i]} -> {estaciones[i + 1]}) debe ser positiva."
        except (ValueError, TypeError):
            return False, f"La distancia del tramo {i + 1} debe ser un número válido."

    # Validar velocidad media positiva
    try:
        vel = float(velocidad_media)
        if not isfinite(vel) or vel <= 0:
            return False, "La velocidad media del tren debe ser positiva."
    except (ValueError, TypeError):
        return False, "La velocidad media debe ser un número válido."

    return True, ""


def buscar_posicion_estacion(estaciones: List[str], nombre: str) -> int:
    """
    Busca la posición de una estación en la lista (coincidencia insensible a mayúsculas y espacios).
    Retorna el índice si existe, o -1 si no se encuentra.
    """
    nombre_buscado = nombre.strip().lower()
    for i, est in enumerate(estaciones):
        if est.strip().lower() == nombre_buscado:
            return i
    return -1


def calcular_recorrido(
    estaciones: List[str],
    distancias: List[float],
    velocidad_media: float,
    inicio: str,
    destino: str
) -> Dict[str, Any]:
    """
    Calcula los datos del recorrido entre inicio y destino (funciona en ambos sentidos).
    Genera la lista de carteles informativos paso a paso con los tiempos estimados.

    Retorna un diccionario con:
    - es_valido: bool
    - mensaje_error: str
    - pos_inicio: int
    - pos_destino: int
    - sentido: 'ida' | 'vuelta'
    - distancia_total_viaje: float
    - tiempo_total_minutos: float
    - carteles: List[Dict] (cada cartel con num, estacion_actual, siguiente_estacion, tiempo_valor, tiempo_unidad, distancia_tramo)
    - cartel_final: Dict (estacion_actual, tiempo_total_minutos)
    """
    datos_validos, mensaje_error = validar_datos_linea(
        estaciones, distancias, velocidad_media
    )
    if not datos_validos:
        return {"es_valido": False, "mensaje_error": mensaje_error}

    pos_inicio = buscar_posicion_estacion(estaciones, inicio)
    pos_destino = buscar_posicion_estacion(estaciones, destino)

    if pos_inicio == -1:
        return {"es_valido": False, "mensaje_error": f"La estación de inicio '{inicio}' no existe en la línea."}
    if pos_destino == -1:
        return {"es_valido": False, "mensaje_error": f"La estación de destino '{destino}' no existe en la línea."}
    if pos_inicio == pos_destino:
        return {"es_valido": False, "mensaje_error": "La estación de inicio y destino no pueden ser la misma."}

    carteles = []
    distancia_total_viaje = 0.0
    tiempo_acumulado_minutos = 0.0
    num_cartel = 0

    if pos_inicio < pos_destino:
        # Sentido directo (ida)
        sentido = "ida"
        for i in range(pos_inicio, pos_destino):
            dist_tramo = distancias[i]
            distancia_total_viaje += dist_tramo
            tiempo_min = (dist_tramo / velocidad_media) * 60.0
            tiempo_acumulado_minutos += tiempo_min
            num_cartel += 1

            if tiempo_min >= 1.0:
                tiempo_valor = int(tiempo_min)
                tiempo_unidad = "min"
            else:
                tiempo_valor = int(tiempo_min * 60.0)
                tiempo_unidad = "seg"

            carteles.append({
                "numero": num_cartel,
                "estacion_actual": estaciones[i],
                "siguiente_estacion": estaciones[i + 1],
                "distancia_tramo": dist_tramo,
                "tiempo_minutos_exacto": tiempo_min,
                "tiempo_valor": tiempo_valor,
                "tiempo_unidad": tiempo_unidad,
                "es_llegada": False
            })
    else:
        # Sentido inverso (vuelta)
        sentido = "vuelta"
        for i in range(pos_inicio, pos_destino, -1):
            dist_tramo = distancias[i - 1]
            distancia_total_viaje += dist_tramo
            tiempo_min = (dist_tramo / velocidad_media) * 60.0
            tiempo_acumulado_minutos += tiempo_min
            num_cartel += 1

            if tiempo_min >= 1.0:
                tiempo_valor = int(tiempo_min)
                tiempo_unidad = "min"
            else:
                tiempo_valor = int(tiempo_min * 60.0)
                tiempo_unidad = "seg"

            carteles.append({
                "numero": num_cartel,
                "estacion_actual": estaciones[i],
                "siguiente_estacion": estaciones[i - 1],
                "distancia_tramo": dist_tramo,
                "tiempo_minutos_exacto": tiempo_min,
                "tiempo_valor": tiempo_valor,
                "tiempo_unidad": tiempo_unidad,
                "es_llegada": False
            })

    num_cartel += 1
    cartel_final = {
        "numero": num_cartel,
        "estacion_actual": estaciones[pos_destino],
        "siguiente_estacion": None,
        "mensaje": "¡Llegó a su destino!",
        "tiempo_total_minutos": int(tiempo_acumulado_minutos),
        "tiempo_total_exacto": tiempo_acumulado_minutos,
        "es_llegada": True
    }

    return {
        "es_valido": True,
        "mensaje_error": "",
        "pos_inicio": pos_inicio,
        "pos_destino": pos_destino,
        "inicio": estaciones[pos_inicio],
        "destino": estaciones[pos_destino],
        "sentido": sentido,
        "distancia_total_viaje": distancia_total_viaje,
        "tiempo_total_minutos": tiempo_acumulado_minutos,
        "carteles": carteles,
        "cartel_final": cartel_final
    }


def calcular_costo(
    distancia_km: float,
    tarifa_base: float,
    tarifa_km: float
) -> Dict[str, Any]:
    """
    Calcula el costo del viaje a partir de la distancia recorrida, tarifa base y tarifa por km.
    Fórmula original: precio = tarifa_base + km_total * tarifa_km
    """
    if not all(isfinite(valor) for valor in (distancia_km, tarifa_base, tarifa_km)):
        return {"es_valido": False, "mensaje_error": "Las tarifas y la distancia deben ser números finitos."}
    if distancia_km < 0:
        return {"es_valido": False, "mensaje_error": "La distancia no puede ser negativa."}
    if tarifa_km <= 0:
        return {"es_valido": False, "mensaje_error": "La tarifa por kilómetro debe ser un número positivo."}
    if tarifa_base < 0:
        return {"es_valido": False, "mensaje_error": "La tarifa base debe ser mayor o igual a 0."}

    costo_km = distancia_km * tarifa_km
    precio_total = tarifa_base + costo_km

    return {
        "es_valido": True,
        "distancia_km": distancia_km,
        "tarifa_base": tarifa_base,
        "tarifa_km": tarifa_km,
        "costo_km": costo_km,
        "precio_total": precio_total
    }


def calcular_estadisticas(
    estaciones: List[str],
    distancias: List[float],
    velocidad_media: float,
    distancia_total: float
) -> Dict[str, Any]:
    """
    Calcula las estadísticas globales de la línea ferroviaria:
    - total_estaciones
    - distancia_total
    - promedio_distancia (distancia_total / (total_estaciones - 1))
    - tramo_mas_largo (origen, destino, distancia)
    - tramo_mas_corto (origen, destino, distancia)
    - tiempo_total_linea ((distancia_total / velocidad_media) * 60)
    """
    total_estaciones = len(estaciones)
    if total_estaciones < 2 or len(distancias) == 0:
        return {"es_valido": False, "mensaje_error": "Datos insuficientes para calcular estadísticas."}

    distancia_mayor = distancias[0]
    distancia_menor = distancias[0]
    idx_mayor = 0
    idx_menor = 0

    for i in range(len(distancias)):
        if distancias[i] > distancia_mayor:
            distancia_mayor = distancias[i]
            idx_mayor = i
        if distancias[i] < distancia_menor:
            distancia_menor = distancias[i]
            idx_menor = i

    tiempo_viaje_minutos = (distancia_total / velocidad_media) * 60.0
    promedio_km = distancia_total / (total_estaciones - 1)

    return {
        "es_valido": True,
        "total_estaciones": total_estaciones,
        "distancia_total": distancia_total,
        "distancia_promedio": promedio_km,
        "tramo_mas_largo": {
            "origen": estaciones[idx_mayor],
            "destino": estaciones[idx_mayor + 1],
            "distancia": distancia_mayor
        },
        "tramo_mas_corto": {
            "origen": estaciones[idx_menor],
            "destino": estaciones[idx_menor + 1],
            "distancia": distancia_menor
        },
        "tiempo_total_linea_minutos": tiempo_viaje_minutos
    }


def ordenar_simulaciones_por_distancia(
    simulaciones_realizadas: List[str],
    distancias_simulaciones: List[float]
) -> Tuple[List[str], List[float]]:
    """
    Ordena el historial de simulaciones de menor a mayor distancia
    utilizando el algoritmo de burbuja original del proyecto.
    """
    simulaciones_ordenadas = list(simulaciones_realizadas)
    distancias_ordenadas = list(distancias_simulaciones)

    num_pasada = len(distancias_ordenadas) - 1
    intercambios = 1

    while num_pasada > 0 and intercambios != 0:
        intercambios = 0
        for i in range(num_pasada):
            if distancias_ordenadas[i] > distancias_ordenadas[i + 1]:
                # Intercambio de distancias
                aux = distancias_ordenadas[i]
                distancias_ordenadas[i] = distancias_ordenadas[i + 1]
                distancias_ordenadas[i + 1] = aux

                # Intercambio sincronizado de simulaciones
                aux2 = simulaciones_ordenadas[i]
                simulaciones_ordenadas[i] = simulaciones_ordenadas[i + 1]
                simulaciones_ordenadas[i + 1] = aux2

                intercambios = 1
        num_pasada -= 1

    return simulaciones_ordenadas, distancias_ordenadas

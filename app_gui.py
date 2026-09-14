"""
Interfaz Gráfica de Usuario (GUI) para RAIL BOARD - Simulador Ferroviario.
Desarrollado con Tkinter para brindar una experiencia visual moderna, limpia
y fiel al trabajo final de programación original de Matías Joaquín De Sousa.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Dict, Any

from logica import (
    crear_linea_ejemplo,
    validar_datos_linea,
    calcular_recorrido,
    calcular_costo,
    calcular_estadisticas,
    ordenar_simulaciones_por_distancia,
)

# Paleta de colores estilo tablero ferroviario moderno
COLOR_BG = "#0f172a"          # Fondo principal azul marino oscuro
COLOR_CARD = "#1e293b"        # Fondo de tarjetas y paneles
COLOR_CARD_BORDER = "#334155" # Borde sutil
COLOR_PRIMARY = "#0284c7"     # Azul ferroviario de acción
COLOR_PRIMARY_HOVER = "#0369a1"
COLOR_ACCENT = "#38bdf8"      # Celeste cian brillante
COLOR_TEXT = "#f8fafc"        # Texto principal blanco brillante
COLOR_TEXT_MUTED = "#94a3b8"  # Texto secundario grisáceo
COLOR_SUCCESS = "#10b981"     # Verde éxito
COLOR_WARNING = "#f59e0b"     # Ámbar alerta
COLOR_DANGER = "#ef4444"      # Rojo
COLOR_LED_BG = "#020617"      # Fondo de cartel LED digital
COLOR_LED_CYAN = "#00f0ff"    # Letras del cartel LED


class SimuladorFerroviarioApp:
    def __init__(self, root: Optional[tk.Tk] = None):
        if root is None:
            self.root = tk.Tk()
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False

        self.root.title("RAIL BOARD — Simulador Ferroviario")
        self.root.geometry("960x720")
        self.root.minsize(900, 680)
        self.root.configure(bg=COLOR_BG)

        # Estado del programa (idéntico al original)
        self.estaciones: List[str] = []
        self.distancias: List[float] = []
        self.velocidad_media: float = 60.0
        self.distancia_total: float = 0.0
        self.simulaciones_realizadas: List[str] = []
        self.distancias_simulaciones: List[float] = []

        # Estado para reproducción de carteles
        self._viaje_actual: Optional[Dict[str, Any]] = None
        self._indice_cartel_actual: int = 0
        self._auto_reproduciendo: bool = False
        self._timer_id: Optional[str] = None

        # Contenedor principal donde se montan las vistas
        self.container = tk.Frame(self.root, bg=COLOR_BG)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Iniciar en la pantalla de presentación
        self.mostrar_presentacion()

    def limpiar_contenedor(self):
        """Cancela timers pendientes y limpia los widgets del contenedor principal."""
        if self._timer_id:
            try:
                self.root.after_cancel(self._timer_id)
            except Exception:
                pass
            self._timer_id = None
        self._auto_reproduciendo = False

        for widget in self.container.winfo_children():
            widget.destroy()

    # =========================================================================
    # 1. PANTALLA DE PRESENTACIÓN (presentacion)
    # =========================================================================
    def mostrar_presentacion(self, desde_menu: bool = False):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=780, height=580)

        # Encabezado
        lbl_badge = tk.Label(
            card,
            text="PROYECTO FINAL DE PROGRAMACIÓN",
            bg="#0369a1",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3
        )
        lbl_badge.pack(pady=(25, 10))

        lbl_titulo = tk.Label(
            card,
            text="BIENVENIDO AL SIMULADOR FERROVIARIO\nRAIL BOARD",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 18, "bold"),
            justify=tk.CENTER
        )
        lbl_titulo.pack(pady=(0, 15))

        # Descripción del programa
        frame_desc = tk.Frame(card, bg="#0f172a", padx=20, pady=15)
        frame_desc.pack(fill=tk.X, padx=35, pady=5)

        items_desc = [
            "• Simula el cartel informativo de una línea ferroviaria con estaciones y distancias.",
            "• Proporciona próximas estaciones y tiempos estimados de llegada (minutos y segundos).",
            "• Realiza simulaciones de costos y viajes en ambos sentidos de circulación.",
            "• Brinda estadísticas completas de la línea y administra un historial de simulaciones.",
            "• Algoritmo de ordenamiento por burbuja para comparar trayectos por distancia."
        ]

        for item in items_desc:
            lbl_item = tk.Label(
                frame_desc,
                text=item,
                bg="#0f172a",
                fg=COLOR_ACCENT,
                font=("Segoe UI", 10),
                anchor="w",
                justify=tk.LEFT
            )
            lbl_item.pack(fill=tk.X, pady=2)

        # Autor
        lbl_autor = tk.Label(
            card,
            text="Desarrollado por: De Sousa Matias Joaquin\nTrabajo final de introducción a la programación",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10, "italic"),
            justify=tk.CENTER
        )
        lbl_autor.pack(pady=(15, 15))

        # Botón para continuar
        if desde_menu:
            btn_volver = tk.Button(
                card,
                text="← Volver al Menú Principal",
                bg=COLOR_PRIMARY,
                fg="#ffffff",
                activebackground=COLOR_PRIMARY_HOVER,
                activeforeground="#ffffff",
                font=("Segoe UI", 11, "bold"),
                relief=tk.FLAT,
                padx=20,
                pady=8,
                cursor="hand2",
                command=self.mostrar_menu_principal
            )
            btn_volver.pack(pady=(5, 20))
        else:
            btn_continuar = tk.Button(
                card,
                text="Comenzar Simulación →",
                bg=COLOR_SUCCESS,
                fg="#ffffff",
                activebackground="#059669",
                activeforeground="#ffffff",
                font=("Segoe UI", 12, "bold"),
                relief=tk.FLAT,
                padx=25,
                pady=9,
                cursor="hand2",
                command=self.mostrar_eleccion_inicio
            )
            btn_continuar.pack(pady=(5, 20))

    # =========================================================================
    # 2. PANTALLA DE ELECCIÓN INICIAL (inicio)
    # =========================================================================
    def mostrar_eleccion_inicio(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=780, height=540)

        lbl_titulo = tk.Label(
            card,
            text="CONFIGURACIÓN INICIAL DE LA LÍNEA",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(30, 10))

        lbl_sub = tk.Label(
            card,
            text="¿Desea cargar los datos de una nueva línea o utilizar un ejemplo predefinido?",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 11)
        )
        lbl_sub.pack(pady=(0, 25))

        # Contenedor de las dos opciones
        frame_opciones = tk.Frame(card, bg=COLOR_CARD)
        frame_opciones.pack(padx=40, pady=10, fill=tk.BOTH, expand=True)

        # Opción 1: Cargar nueva línea
        opc1 = tk.Frame(frame_opciones, bg="#0f172a", bd=1, relief=tk.SOLID, padx=20, pady=20)
        opc1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        lbl_opc1_tit = tk.Label(opc1, text="1. Cargar Nueva Línea", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 13, "bold"))
        lbl_opc1_tit.pack(anchor="w")

        lbl_opc1_desc = tk.Label(
            opc1,
            text="Ingrese manualmente la cantidad de estaciones, nombres de cada estación, distancias entre ellas y velocidad media del tren.",
            bg="#0f172a",
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10),
            wraplength=280,
            justify=tk.LEFT
        )
        lbl_opc1_desc.pack(anchor="w", pady=(10, 20))

        btn_opc1 = tk.Button(
            opc1,
            text="Cargar Datos Manualmente",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=8,
            cursor="hand2",
            command=self.mostrar_carga_datos_tren
        )
        btn_opc1.pack(fill=tk.X, side=tk.BOTTOM)

        # Opción 2: Cargar ejemplo
        opc2 = tk.Frame(frame_opciones, bg="#0f172a", bd=1, relief=tk.SOLID, padx=20, pady=20)
        opc2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        lbl_opc2_tit = tk.Label(opc2, text="2. Cargar Ejemplo Predefinido", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 13, "bold"))
        lbl_opc2_tit.pack(anchor="w")

        lbl_opc2_desc = tk.Label(
            opc2,
            text="Línea San Martín (15 estaciones: San Miguel hasta Retiro, 14 tramos, velocidad media de 60 km/h).",
            bg="#0f172a",
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10),
            wraplength=280,
            justify=tk.LEFT
        )
        lbl_opc2_desc.pack(anchor="w", pady=(10, 20))

        btn_opc2 = tk.Button(
            opc2,
            text="Cargar Línea de Ejemplo",
            bg=COLOR_SUCCESS,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=8,
            cursor="hand2",
            command=self.cargar_ejemplo_y_confirmar
        )
        btn_opc2.pack(fill=tk.X, side=tk.BOTTOM)

    def cargar_ejemplo_y_confirmar(self):
        """Carga los datos de ejemplo y muestra la pantalla de confirmación/datos."""
        self.estaciones, self.distancias, self.velocidad_media, self.distancia_total = crear_linea_ejemplo()
        self.mostrar_confirmacion_linea(es_ejemplo=True)

    # =========================================================================
    # 3. FORMULARIO DE CARGA DE DATOS (carga_datos_tren)
    # =========================================================================
    def mostrar_carga_datos_tren(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=820, height=620)

        lbl_titulo = tk.Label(
            card,
            text="INGRESO DE DATOS DE LA LÍNEA FERROVIARIA",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 15, "bold")
        )
        lbl_titulo.pack(pady=(20, 5))

        lbl_sub = tk.Label(
            card,
            text="Defina la cantidad de estaciones, sus nombres, distancias y velocidad media.",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        )
        lbl_sub.pack(pady=(0, 10))

        # Panel superior: Cantidad de estaciones y velocidad
        frame_top = tk.Frame(card, bg="#0f172a", padx=15, pady=10)
        frame_top.pack(fill=tk.X, padx=25, pady=(0, 10))

        tk.Label(frame_top, text="Cantidad de estaciones:", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_num_est = tk.Entry(frame_top, font=("Segoe UI", 10), width=8, justify="center")
        entry_num_est.grid(row=0, column=1, padx=5, pady=5)
        entry_num_est.insert(0, "4")

        tk.Label(frame_top, text="Velocidad media (km/h):", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(20, 5), pady=5)
        entry_vel = tk.Entry(frame_top, font=("Segoe UI", 10), width=8, justify="center")
        entry_vel.grid(row=0, column=3, padx=5, pady=5)
        entry_vel.insert(0, "60")

        # Contenedor scrollable para las estaciones y distancias
        frame_scroll_container = tk.Frame(card, bg=COLOR_CARD)
        frame_scroll_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        canvas = tk.Canvas(frame_scroll_container, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll_container, orient=tk.VERTICAL, command=canvas.yview)
        frame_filas = tk.Frame(canvas, bg="#0f172a")

        frame_filas.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame_filas, anchor="nw", width=750)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        entradas_estaciones: List[tk.Entry] = []
        entradas_distancias: List[tk.Entry] = []

        def generar_filas():
            nonlocal entradas_estaciones, entradas_distancias
            for w in frame_filas.winfo_children():
                w.destroy()
            entradas_estaciones = []
            entradas_distancias = []

            try:
                num = int(entry_num_est.get())
                if num < 2:
                    messagebox.showerror("Error", "La cantidad de estaciones debe ser mayor a 1.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número entero válido para la cantidad de estaciones.")
                return

            # Cabecera de la tabla
            header = tk.Frame(frame_filas, bg="#1e293b", pady=6)
            header.pack(fill=tk.X, padx=10, pady=(5, 5))
            tk.Label(header, text="Estación", bg="#1e293b", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold"), width=30, anchor="w").pack(side=tk.LEFT, padx=10)
            tk.Label(header, text="Distancia al siguiente tramo (km)", bg="#1e293b", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT, padx=10)

            for i in range(1, num + 1):
                fila = tk.Frame(frame_filas, bg="#0f172a", pady=4)
                fila.pack(fill=tk.X, padx=10)

                lbl_num = tk.Label(fila, text=f"Estación {i}:", bg="#0f172a", fg=COLOR_ACCENT, font=("Segoe UI", 10, "bold"), width=12, anchor="w")
                lbl_num.pack(side=tk.LEFT, padx=(5, 5))

                ent_est = tk.Entry(fila, font=("Segoe UI", 10), width=24)
                ent_est.pack(side=tk.LEFT, padx=5)
                ent_est.insert(0, f"Estación {chr(64 + i) if i <= 26 else i}")
                entradas_estaciones.append(ent_est)

                if i < num:
                    lbl_a = tk.Label(fila, text="→  Distancia a siguiente:", bg="#0f172a", fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9))
                    lbl_a.pack(side=tk.LEFT, padx=(10, 5))

                    ent_dist = tk.Entry(fila, font=("Segoe UI", 10), width=8, justify="center")
                    ent_dist.pack(side=tk.LEFT, padx=5)
                    ent_dist.insert(0, "5.0")
                    entradas_distancias.append(ent_dist)

                    lbl_km = tk.Label(fila, text="km", bg="#0f172a", fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9))
                    lbl_km.pack(side=tk.LEFT)

        btn_generar = tk.Button(
            frame_top,
            text="Generar Campos",
            bg="#334155",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            cursor="hand2",
            command=generar_filas
        )
        btn_generar.grid(row=0, column=4, padx=(15, 5), pady=5)

        # Generar filas por defecto
        generar_filas()

        # Botones inferiores
        frame_bottom = tk.Frame(card, bg=COLOR_CARD, pady=10)
        frame_bottom.pack(fill=tk.X, padx=25)

        def guardar_datos():
            try:
                cantidad_indicada = int(entry_num_est.get())
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad de estaciones válida.")
                return

            if cantidad_indicada != len(entradas_estaciones):
                messagebox.showwarning(
                    "Campos sin actualizar",
                    "Después de cambiar la cantidad de estaciones, presione "
                    "'Generar Campos' antes de guardar.",
                )
                return

            est_list = [e.get().strip() for e in entradas_estaciones]
            dist_list = []
            for d in entradas_distancias:
                try:
                    val = float(d.get().replace(",", "."))
                    dist_list.append(val)
                except ValueError:
                    messagebox.showerror("Error", "Todas las distancias deben ser números válidos.")
                    return

            try:
                vel = float(entry_vel.get().replace(",", "."))
            except ValueError:
                messagebox.showerror("Error", "La velocidad media debe ser un número válido.")
                return

            es_valido, msj = validar_datos_linea(est_list, dist_list, vel)
            if not es_valido:
                messagebox.showerror("Validación de Línea", msj)
                return

            self.estaciones = est_list
            self.distancias = dist_list
            self.velocidad_media = vel
            self.distancia_total = sum(dist_list)

            self.mostrar_confirmacion_linea(es_ejemplo=False)

        btn_volver = tk.Button(
            frame_bottom,
            text="← Volver",
            bg="#334155",
            fg="#ffffff",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.mostrar_eleccion_inicio
        )
        btn_volver.pack(side=tk.LEFT)

        btn_guardar = tk.Button(
            frame_bottom,
            text="Guardar y Continuar →",
            bg=COLOR_SUCCESS,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2",
            command=guardar_datos
        )
        btn_guardar.pack(side=tk.RIGHT)

    # =========================================================================
    # 4. PANTALLA DE CONFIRMACIÓN / IMPRESIÓN DE DATOS (impresion_datos_tren)
    # =========================================================================
    def mostrar_confirmacion_linea(self, es_ejemplo: bool = False):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=820, height=620)

        titulo_texto = "LÍNEA DE EJEMPLO CARGADA" if es_ejemplo else "INFORMACIÓN DE LA LÍNEA INGRESADA"
        lbl_titulo = tk.Label(
            card,
            text=titulo_texto,
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(20, 5))

        # Tarjetas de resumen
        frame_resumen = tk.Frame(card, bg=COLOR_CARD)
        frame_resumen.pack(fill=tk.X, padx=30, pady=10)

        def crear_tarjeta_resumen(parent, titulo, valor):
            f = tk.Frame(parent, bg="#0f172a", bd=1, relief=tk.SOLID, padx=15, pady=8)
            f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            tk.Label(f, text=titulo, bg="#0f172a", fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9)).pack()
            tk.Label(f, text=valor, bg="#0f172a", fg=COLOR_ACCENT, font=("Segoe UI", 13, "bold")).pack()

        crear_tarjeta_resumen(frame_resumen, "Total Estaciones", f"{len(self.estaciones)}")
        crear_tarjeta_resumen(frame_resumen, "Distancia Total", f"{self.distancia_total:.1f} km")
        crear_tarjeta_resumen(frame_resumen, "Velocidad Media", f"{self.velocidad_media:.0f} km/h")

        # Lista de tramos con scroll
        lbl_tramos = tk.Label(card, text="Detalle de estaciones y distancias entre cada una:", bg=COLOR_CARD, fg=COLOR_TEXT, font=("Segoe UI", 10, "bold"), anchor="w")
        lbl_tramos.pack(fill=tk.X, padx=35, pady=(10, 5))

        frame_scroll = tk.Frame(card, bg="#0f172a")
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=35, pady=(0, 15))

        canvas = tk.Canvas(frame_scroll, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient=tk.VERTICAL, command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="#0f172a")

        frame_lista.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame_lista, anchor="nw", width=730)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for i in range(len(self.distancias)):
            fila = tk.Frame(frame_lista, bg="#0f172a", pady=3)
            fila.pack(fill=tk.X, padx=10)

            lbl_tramo = tk.Label(
                fila,
                text=f"•  {self.estaciones[i].title()}  →  ({self.distancias[i]:.1f} km)  →  {self.estaciones[i + 1].title()}",
                bg="#0f172a",
                fg=COLOR_TEXT,
                font=("Segoe UI", 10)
            )
            lbl_tramo.pack(anchor="w")

        # Botones de confirmación
        frame_btn = tk.Frame(card, bg=COLOR_CARD)
        frame_btn.pack(fill=tk.X, padx=35, pady=(0, 20))

        btn_reingresar = tk.Button(
            frame_btn,
            text="✏️ Volver a Cargar Datos",
            bg="#334155",
            fg="#ffffff",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.mostrar_carga_datos_tren
        )
        btn_reingresar.pack(side=tk.LEFT)

        btn_confirmar = tk.Button(
            frame_btn,
            text="Confirmar e ir al Menú Principal →",
            bg=COLOR_SUCCESS,
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=7,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_confirmar.pack(side=tk.RIGHT)

    # =========================================================================
    # 5. MENÚ PRINCIPAL (menu_principal - 9 Opciones)
    # =========================================================================
    def mostrar_menu_principal(self):
        self.limpiar_contenedor()

        # Barra superior con resumen de línea
        top_bar = tk.Frame(self.container, bg="#1e293b", padx=20, pady=10)
        top_bar.pack(fill=tk.X)

        tk.Label(
            top_bar,
            text="🚆 RAIL BOARD",
            bg="#1e293b",
            fg=COLOR_ACCENT,
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT)

        info_linea = f"Línea activa: {len(self.estaciones)} estaciones | {self.distancia_total:.1f} km totales | Vel: {self.velocidad_media:.0f} km/h"
        tk.Label(
            top_bar,
            text=info_linea,
            bg="#1e293b",
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        ).pack(side=tk.RIGHT)

        # Panel central del menú
        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.53, anchor=tk.CENTER, width=820, height=540)

        lbl_tit_menu = tk.Label(
            card,
            text="MENÚ PRINCIPAL",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_tit_menu.pack(pady=(20, 5))

        lbl_sub_menu = tk.Label(
            card,
            text="Seleccione una opción para operar el simulador ferroviario:",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        )
        lbl_sub_menu.pack(pady=(0, 15))

        # Grid de botones para las 9 opciones
        frame_grid = tk.Frame(card, bg=COLOR_CARD)
        frame_grid.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Configurar 3 columnas
        for col in range(3):
            frame_grid.columnconfigure(col, weight=1, uniform="col")

        opciones = [
            ("1. Simulación de Viaje", "🚊", "Recorrer la línea cartel por cartel con tiempos estimados", self.mostrar_simulacion_viaje, COLOR_PRIMARY),
            ("2. Simulación de Costos", "🎫", "Calcular tarifas con precio base y valor por kilómetro", self.mostrar_simulacion_costos, COLOR_PRIMARY),
            ("3. Estadísticas de Línea", "📊", "Ver tramos extremos, promedios y tiempo total", self.mostrar_estadisticas, COLOR_PRIMARY),
            ("4. Cargar Nueva Línea", "✏️", "Volver a ingresar manualmente todos los datos", self.mostrar_carga_datos_tren, "#334155"),
            ("5. Cargar Ejemplo", "🔄", "Restaurar los datos de la Línea San Martín", self.cargar_ejemplo_desde_menu, "#334155"),
            ("6. Presentación / Info", "ℹ️", "Ver créditos y objetivos del proyecto", lambda: self.mostrar_presentacion(desde_menu=True), "#334155"),
            ("7. Ver Datos de Línea", "🗺️", "Listado completo de estaciones y distancias", self.mostrar_datos_linea, "#334155"),
            ("8. Historial de Viajes", "📜", "Ver historial cronológico y ordenado por distancia", self.mostrar_historial, "#334155"),
            ("9. Finalizar Programa", "🚪", "Cerrar el simulador ferroviario", self.mostrar_cierre_programa, COLOR_DANGER),
        ]

        for i, (titulo, icono, desc, comando, color_btn) in enumerate(opciones):
            row = i // 3
            col = i % 3

            btn_box = tk.Button(
                frame_grid,
                text=f"{icono}  {titulo}\n{desc}",
                bg="#0f172a",
                fg=COLOR_TEXT,
                activebackground=color_btn,
                activeforeground="#ffffff",
                font=("Segoe UI", 9, "bold"),
                relief=tk.SOLID,
                bd=1,
                padx=10,
                pady=10,
                justify=tk.CENTER,
                wraplength=200,
                cursor="hand2",
                command=comando
            )
            btn_box.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    def cargar_ejemplo_desde_menu(self):
        """Carga el ejemplo predefinido desde el menú principal con confirmación."""
        self.estaciones, self.distancias, self.velocidad_media, self.distancia_total = crear_linea_ejemplo()
        messagebox.showinfo("Línea Restaurada", "Se ha cargado correctamente la Línea San Martín de ejemplo (15 estaciones).")
        self.mostrar_menu_principal()

    # =========================================================================
    # 6. SIMULACIÓN DE VIAJE (simulacion_viaje & Carteles LED)
    # =========================================================================
    def mostrar_simulacion_viaje(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=860, height=640)

        lbl_titulo = tk.Label(
            card,
            text="SIMULACIÓN DE VIAJE — CARTEL INFORMATIVO",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(15, 5))

        # Panel de selección de Origen y Destino
        frame_sel = tk.Frame(card, bg="#0f172a", padx=15, pady=10)
        frame_sel.pack(fill=tk.X, padx=25, pady=(0, 10))

        tk.Label(frame_sel, text="Estación Origen:", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        combo_origen = ttk.Combobox(frame_sel, values=[e.title() for e in self.estaciones], state="readonly", width=20, font=("Segoe UI", 10))
        combo_origen.grid(row=0, column=1, padx=5)
        combo_origen.current(0)

        tk.Label(frame_sel, text="Estación Destino:", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(20, 5))
        combo_destino = ttk.Combobox(frame_sel, values=[e.title() for e in self.estaciones], state="readonly", width=20, font=("Segoe UI", 10))
        combo_destino.grid(row=0, column=3, padx=5)
        combo_destino.current(len(self.estaciones) - 1)

        # Panel LED Digital
        frame_led_border = tk.Frame(card, bg="#0284c7", padx=2, pady=2)
        frame_led_border.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        frame_led = tk.Frame(frame_led_border, bg=COLOR_LED_BG, padx=20, pady=15)
        frame_led.pack(fill=tk.BOTH, expand=True)

        lbl_cartel_num = tk.Label(frame_led, text="PANEL FERROVIARIO DIGITAL", bg=COLOR_LED_BG, fg=COLOR_WARNING, font=("Segoe UI", 11, "bold"))
        lbl_cartel_num.pack(anchor="center", pady=(5, 10))

        lbl_est_actual = tk.Label(frame_led, text="ESTACIÓN ACTUAL: ---", bg=COLOR_LED_BG, fg=COLOR_TEXT, font=("Segoe UI", 15, "bold"))
        lbl_est_actual.pack(anchor="center", pady=4)

        lbl_prox_est = tk.Label(frame_led, text="PRÓXIMA ESTACIÓN: ---", bg=COLOR_LED_BG, fg=COLOR_LED_CYAN, font=("Segoe UI", 16, "bold"))
        lbl_prox_est.pack(anchor="center", pady=4)

        lbl_tiempo = tk.Label(frame_led, text="TIEMPO ESTIMADO: ---", bg=COLOR_LED_BG, fg=COLOR_SUCCESS, font=("Segoe UI", 14, "bold"))
        lbl_tiempo.pack(anchor="center", pady=4)

        lbl_tramo_info = tk.Label(frame_led, text="Seleccione origen y destino para iniciar la simulación", bg=COLOR_LED_BG, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 10))
        lbl_tramo_info.pack(anchor="center", pady=(10, 5))

        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(frame_led, variable=progress_var, maximum=100)
        progress_bar.pack(fill=tk.X, padx=40, pady=(5, 5))

        # Panel de Controles
        frame_controles = tk.Frame(card, bg=COLOR_CARD, pady=10)
        frame_controles.pack(fill=tk.X, padx=25)

        btn_anterior = tk.Button(frame_controles, text="⏮️ Anterior", bg="#334155", fg="#ffffff", font=("Segoe UI", 10), relief=tk.FLAT, state=tk.DISABLED, padx=12, pady=6)
        btn_anterior.pack(side=tk.LEFT, padx=3)

        btn_siguiente = tk.Button(frame_controles, text="Siguiente Cartel ⏭️", bg=COLOR_PRIMARY, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, state=tk.DISABLED, padx=12, pady=6)
        btn_siguiente.pack(side=tk.LEFT, padx=3)

        btn_auto = tk.Button(frame_controles, text="▶️ Reproducción Automática", bg="#059669", fg="#ffffff", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, state=tk.DISABLED, padx=12, pady=6)
        btn_auto.pack(side=tk.LEFT, padx=3)

        btn_volver = tk.Button(
            frame_controles,
            text="← Volver al Menú",
            bg="#334155",
            fg="#ffffff",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(side=tk.RIGHT)

        def renderizar_cartel():
            if not self._viaje_actual:
                return

            carteles = self._viaje_actual["carteles"]
            total_pasos = len(carteles) + 1  # Incluyendo cartel final
            idx = self._indice_cartel_actual

            if idx < len(carteles):
                c = carteles[idx]
                lbl_cartel_num.config(text=f"CARTEL ({c['numero']} DE {total_pasos}) — EN TRAYECTO", fg=COLOR_WARNING)
                lbl_est_actual.config(text=f"ESTACIÓN ACTUAL:  {c['estacion_actual'].upper()}", fg=COLOR_TEXT)
                lbl_prox_est.config(text=f"PRÓXIMA ESTACIÓN:  {c['siguiente_estacion'].upper()}", fg=COLOR_LED_CYAN)
                lbl_tiempo.config(text=f"TIEMPO ESTIMADO:  Aproximadamente en {c['tiempo_valor']} {c['tiempo_unidad']}", fg=COLOR_SUCCESS)
                lbl_tramo_info.config(text=f"Distancia del tramo: {c['distancia_tramo']:.1f} km  |  Sentido: {self._viaje_actual['sentido'].upper()}")
                progress_var.set((idx / total_pasos) * 100)
            else:
                # Cartel Final de llegada
                cf = self._viaje_actual["cartel_final"]
                lbl_cartel_num.config(text=f"CARTEL ({cf['numero']} DE {total_pasos}) — DESTINO ALCANZADO", fg=COLOR_SUCCESS)
                lbl_est_actual.config(text=f"ESTACIÓN ACTUAL:  {cf['estacion_actual'].upper()}", fg=COLOR_TEXT)
                lbl_prox_est.config(text="¡LLEGÓ A SU DESTINO!", fg=COLOR_SUCCESS)
                lbl_tiempo.config(text=f"TIEMPO TOTAL DE VIAJE:  {cf['tiempo_total_minutos']} MINUTOS", fg=COLOR_WARNING)
                lbl_tramo_info.config(text=f"Distancia total recorrida: {self._viaje_actual['distancia_total_viaje']:.1f} km")
                progress_var.set(100)

            btn_anterior.config(state=tk.NORMAL if idx > 0 else tk.DISABLED)
            btn_siguiente.config(state=tk.NORMAL if idx < len(carteles) else tk.DISABLED)

        def avanzar_cartel():
            if not self._viaje_actual:
                return
            if self._indice_cartel_actual < len(self._viaje_actual["carteles"]):
                self._indice_cartel_actual += 1
                renderizar_cartel()
                if self._indice_cartel_actual == len(self._viaje_actual["carteles"]) and self._auto_reproduciendo:
                    detener_auto()

        def retroceder_cartel():
            if not self._viaje_actual:
                return
            if self._indice_cartel_actual > 0:
                self._indice_cartel_actual -= 1
                renderizar_cartel()

        def paso_automatico():
            if not self._auto_reproduciendo:
                return
            if self._viaje_actual and self._indice_cartel_actual < len(self._viaje_actual["carteles"]):
                avanzar_cartel()
                if self._auto_reproduciendo and self._indice_cartel_actual <= len(self._viaje_actual["carteles"]):
                    self._timer_id = self.root.after(1600, paso_automatico)
            else:
                detener_auto()

        def detener_auto():
            self._auto_reproduciendo = False
            if self._timer_id:
                try:
                    self.root.after_cancel(self._timer_id)
                except Exception:
                    pass
                self._timer_id = None
            btn_auto.config(text="▶️ Reproducción Automática", bg="#059669")

        def toggle_auto():
            if self._auto_reproduciendo:
                detener_auto()
            else:
                if self._indice_cartel_actual >= len(self._viaje_actual["carteles"]):
                    self._indice_cartel_actual = 0
                    renderizar_cartel()
                self._auto_reproduciendo = True
                btn_auto.config(text="⏸️ Pausar Reproducción", bg="#d97706")
                self._timer_id = self.root.after(800, paso_automatico)

        def iniciar_simulacion():
            detener_auto()
            ini = combo_origen.get()
            dest = combo_destino.get()

            res = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, ini, dest)
            if not res["es_valido"]:
                messagebox.showerror("Error en Simulación", res["mensaje_error"])
                return

            self._viaje_actual = res
            self._indice_cartel_actual = 0

            # Registrar en el historial original
            nombre_viaje = f"{res['inicio'].title()} -> {res['destino'].title()}"
            self.simulaciones_realizadas.append(nombre_viaje)
            self.distancias_simulaciones.append(res["distancia_total_viaje"])

            btn_anterior.config(state=tk.NORMAL)
            btn_siguiente.config(state=tk.NORMAL)
            btn_auto.config(state=tk.NORMAL)
            btn_anterior.config(command=retroceder_cartel, cursor="hand2")
            btn_siguiente.config(command=avanzar_cartel, cursor="hand2")
            btn_auto.config(command=toggle_auto, cursor="hand2")

            renderizar_cartel()

        btn_iniciar = tk.Button(
            frame_sel,
            text="Iniciar Simulación →",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=4,
            cursor="hand2",
            command=iniciar_simulacion
        )
        btn_iniciar.grid(row=0, column=4, padx=(15, 5))

    # =========================================================================
    # 7. SIMULACIÓN DE COSTOS (simulacion_costos)
    # =========================================================================
    def mostrar_simulacion_costos(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=820, height=580)

        lbl_titulo = tk.Label(
            card,
            text="SIMULACIÓN DE COSTOS Y TARIFAS",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(20, 5))

        lbl_sub = tk.Label(
            card,
            text="Calcule el costo del pasaje a partir de la tarifa base, valor por kilómetro y tramo seleccionado.",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        )
        lbl_sub.pack(pady=(0, 15))

        # Formulario de tarifas
        frame_form = tk.Frame(card, bg="#0f172a", padx=20, pady=15)
        frame_form.pack(fill=tk.X, padx=30, pady=(0, 15))

        # Fila 1: Tarifas
        tk.Label(frame_form, text="Tarifa por km ($):", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_tarifa_km = tk.Entry(frame_form, font=("Segoe UI", 10), width=10, justify="center")
        entry_tarifa_km.grid(row=0, column=1, padx=5, pady=5)
        entry_tarifa_km.insert(0, "15.00")

        tk.Label(frame_form, text="Tarifa base ($):", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(20, 5), pady=5)
        entry_tarifa_base = tk.Entry(frame_form, font=("Segoe UI", 10), width=10, justify="center")
        entry_tarifa_base.grid(row=0, column=3, padx=5, pady=5)
        entry_tarifa_base.insert(0, "50.00")

        # Fila 2: Estaciones
        tk.Label(frame_form, text="Estación Origen:", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=10)
        combo_origen = ttk.Combobox(frame_form, values=[e.title() for e in self.estaciones], state="readonly", width=18, font=("Segoe UI", 10))
        combo_origen.grid(row=1, column=1, padx=5, pady=10)
        combo_origen.current(0)

        tk.Label(frame_form, text="Estación Destino:", bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky="w", padx=(20, 5), pady=10)
        combo_destino = ttk.Combobox(frame_form, values=[e.title() for e in self.estaciones], state="readonly", width=18, font=("Segoe UI", 10))
        combo_destino.grid(row=1, column=3, padx=5, pady=10)
        combo_destino.current(len(self.estaciones) - 1)

        # Panel de Resultado del Boleto / Desglose
        frame_boleto = tk.Frame(card, bg="#020617", bd=1, relief=tk.SOLID, padx=25, pady=15)
        frame_boleto.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 15))

        lbl_boleto_tit = tk.Label(frame_boleto, text="DETALLE DEL BOLETO", bg="#020617", fg=COLOR_ACCENT, font=("Segoe UI", 12, "bold"))
        lbl_boleto_tit.pack(anchor="w", pady=(0, 5))

        lbl_res_dist = tk.Label(frame_boleto, text="• Distancia recorrida: ---", bg="#020617", fg=COLOR_TEXT, font=("Segoe UI", 11))
        lbl_res_dist.pack(anchor="w", pady=2)

        lbl_res_tkm = tk.Label(frame_boleto, text="• Tarifa por kilómetro: ---", bg="#020617", fg=COLOR_TEXT, font=("Segoe UI", 11))
        lbl_res_tkm.pack(anchor="w", pady=2)

        lbl_res_tbase = tk.Label(frame_boleto, text="• Tarifa base: ---", bg="#020617", fg=COLOR_TEXT, font=("Segoe UI", 11))
        lbl_res_tbase.pack(anchor="w", pady=2)

        lbl_res_total = tk.Label(frame_boleto, text="PRECIO TOTAL DEL VIAJE: ---", bg="#020617", fg=COLOR_SUCCESS, font=("Segoe UI", 14, "bold"))
        lbl_res_total.pack(anchor="w", pady=(10, 2))

        def calcular():
            ini = combo_origen.get()
            dest = combo_destino.get()

            try:
                t_km = float(entry_tarifa_km.get().replace(",", "."))
                t_base = float(entry_tarifa_base.get().replace(",", "."))
            except ValueError:
                messagebox.showerror("Error", "Las tarifas deben ser números válidos.")
                return

            res_viaje = calcular_recorrido(self.estaciones, self.distancias, self.velocidad_media, ini, dest)
            if not res_viaje["es_valido"]:
                messagebox.showerror("Error", res_viaje["mensaje_error"])
                return

            res_costo = calcular_costo(res_viaje["distancia_total_viaje"], t_base, t_km)
            if not res_costo["es_valido"]:
                messagebox.showerror("Error", res_costo["mensaje_error"])
                return

            # Actualizar visualización
            lbl_res_dist.config(text=f"• Distancia recorrida: {res_costo['distancia_km']:.1f} km ({res_viaje['inicio'].title()} → {res_viaje['destino'].title()})")
            lbl_res_tkm.config(text=f"• Tarifa por kilómetro: ${res_costo['tarifa_km']:.2f} (Costo por tramos: ${res_costo['costo_km']:.2f})")
            lbl_res_tbase.config(text=f"• Tarifa base: ${res_costo['tarifa_base']:.2f}")
            lbl_res_total.config(text=f"PRECIO TOTAL DEL VIAJE: ${res_costo['precio_total']:.2f}")

            # Registrar en historial
            nombre_viaje = f"{res_viaje['inicio'].title()} -> {res_viaje['destino'].title()}"
            self.simulaciones_realizadas.append(nombre_viaje)
            self.distancias_simulaciones.append(res_costo["distancia_km"])

        btn_calc = tk.Button(
            frame_form,
            text="Calcular Tarifa 🧮",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=4,
            cursor="hand2",
            command=calcular
        )
        btn_calc.grid(row=1, column=4, padx=(15, 5), pady=10)

        # Botón volver
        frame_bot = tk.Frame(card, bg=COLOR_CARD)
        frame_bot.pack(fill=tk.X, padx=30, pady=(0, 15))

        btn_volver = tk.Button(
            frame_bot,
            text="← Volver al Menú Principal",
            bg="#334155",
            fg="#ffffff",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(side=tk.LEFT)

    # =========================================================================
    # 8. ESTADÍSTICAS DE LA LÍNEA (estadisticas)
    # =========================================================================
    def mostrar_estadisticas(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=820, height=580)

        lbl_titulo = tk.Label(
            card,
            text="ESTADÍSTICAS DE LA LÍNEA FERROVIARIA",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(25, 5))

        lbl_sub = tk.Label(
            card,
            text="Métricas globales, tramos extremos y tiempos completos de la línea activa.",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        )
        lbl_sub.pack(pady=(0, 20))

        stats = calcular_estadisticas(self.estaciones, self.distancias, self.velocidad_media, self.distancia_total)

        if not stats["es_valido"]:
            messagebox.showerror("Error", stats["mensaje_error"])
            self.mostrar_menu_principal()
            return

        # Cuadrícula de tarjetas de estadísticas
        frame_grid = tk.Frame(card, bg=COLOR_CARD)
        frame_grid.pack(fill=tk.BOTH, expand=True, padx=30, pady=5)

        for col in range(2):
            frame_grid.columnconfigure(col, weight=1, uniform="stat_col")

        def crear_card_stat(parent, row, col, titulo, valor_grande, subtitulo, color_val=COLOR_ACCENT):
            f = tk.Frame(parent, bg="#0f172a", bd=1, relief=tk.SOLID, padx=15, pady=12)
            f.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            tk.Label(f, text=titulo, bg="#0f172a", fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(f, text=valor_grande, bg="#0f172a", fg=color_val, font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(4, 2))
            if subtitulo:
                tk.Label(f, text=subtitulo, bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 9)).pack(anchor="w")

        crear_card_stat(frame_grid, 0, 0, "TOTAL DE ESTACIONES", f"{stats['total_estaciones']} estaciones", f"{len(self.distancias)} tramos consecutivos")
        crear_card_stat(frame_grid, 0, 1, "DISTANCIA TOTAL", f"{stats['distancia_total']:.1f} km", f"Promedio entre estaciones: {stats['distancia_promedio']:.2f} km")

        tl = stats["tramo_mas_largo"]
        crear_card_stat(frame_grid, 1, 0, "TRAMO MÁS LARGO", f"{tl['distancia']:.1f} km", f"De {tl['origen'].title()} a {tl['destino'].title()}", COLOR_WARNING)

        tc = stats["tramo_mas_corto"]
        crear_card_stat(frame_grid, 1, 1, "TRAMO MÁS CORTO", f"{tc['distancia']:.1f} km", f"De {tc['origen'].title()} a {tc['destino'].title()}", COLOR_SUCCESS)

        crear_card_stat(frame_grid, 2, 0, "TIEMPO TOTAL DE LA LÍNEA", f"{stats['tiempo_total_linea_minutos']:.1f} min", f"Recorrido completo a {self.velocidad_media:.0f} km/h")
        crear_card_stat(frame_grid, 2, 1, "VELOCIDAD MEDIA", f"{self.velocidad_media:.0f} km/h", "Velocidad operativa de referencia")

        # Botón volver
        btn_volver = tk.Button(
            card,
            text="← Volver al Menú Principal",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(pady=(15, 20))

    # =========================================================================
    # 9. DATOS DE LA LÍNEA (impresion_datos_tren)
    # =========================================================================
    def mostrar_datos_linea(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=820, height=580)

        lbl_titulo = tk.Label(
            card,
            text="DATOS PROPORCIONADOS DE LA LÍNEA",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(20, 5))

        lbl_sub = tk.Label(
            card,
            text=f"Total: {len(self.estaciones)} estaciones | Distancia total: {self.distancia_total:.1f} km | Velocidad: {self.velocidad_media:.0f} km/h",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        )
        lbl_sub.pack(pady=(0, 15))

        # Lista scrollable de tramos
        frame_scroll = tk.Frame(card, bg="#0f172a")
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 15))

        canvas = tk.Canvas(frame_scroll, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient=tk.VERTICAL, command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="#0f172a")

        frame_lista.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame_lista, anchor="nw", width=730)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for i in range(len(self.distancias)):
            fila = tk.Frame(frame_lista, bg="#0f172a", pady=4)
            fila.pack(fill=tk.X, padx=15)

            tk.Label(
                fila,
                text=f"{i + 1:02d}.",
                bg="#0f172a",
                fg=COLOR_ACCENT,
                font=("Segoe UI", 10, "bold"),
                width=4,
                anchor="w"
            ).pack(side=tk.LEFT)

            lbl_origen = tk.Label(fila, text=self.estaciones[i].title(), bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold"), width=18, anchor="w")
            lbl_origen.pack(side=tk.LEFT)

            lbl_flecha = tk.Label(fila, text=f"─── ({self.distancias[i]:.1f} km) ───▶", bg="#0f172a", fg=COLOR_WARNING, font=("Segoe UI", 9))
            lbl_flecha.pack(side=tk.LEFT, padx=10)

            lbl_dest = tk.Label(fila, text=self.estaciones[i + 1].title(), bg="#0f172a", fg=COLOR_TEXT, font=("Segoe UI", 10, "bold"), width=18, anchor="w")
            lbl_dest.pack(side=tk.LEFT)

        btn_volver = tk.Button(
            card,
            text="← Volver al Menú Principal",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=7,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(pady=(5, 20))

    # =========================================================================
    # 10. HISTORIAL DE SIMULACIONES (historial_simulaciones & Burbuja)
    # =========================================================================
    def mostrar_historial(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=860, height=600)

        lbl_titulo = tk.Label(
            card,
            text="HISTORIAL DE SIMULACIONES REALIZADAS",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=(20, 5))

        if len(self.simulaciones_realizadas) == 0:
            lbl_vacio = tk.Label(
                card,
                text="No se han realizado simulaciones hasta el momento.\nRealice una simulación de viaje o de costos desde el Menú Principal.",
                bg=COLOR_CARD,
                fg=COLOR_TEXT_MUTED,
                font=("Segoe UI", 11),
                justify=tk.CENTER
            )
            lbl_vacio.pack(expand=True, pady=40)
        else:
            # Pestañas / Paneles comparativos: Cronológico vs Ordenado por Distancia (Burbuja)
            frame_dos_listas = tk.Frame(card, bg=COLOR_CARD)
            frame_dos_listas.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

            # Panel 1: Cronológico
            p1 = tk.Frame(frame_dos_listas, bg="#0f172a", bd=1, relief=tk.SOLID, padx=12, pady=10)
            p1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

            tk.Label(p1, text="1. Orden Cronológico", bg="#0f172a", fg=COLOR_ACCENT, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

            lista_crono = tk.Listbox(p1, bg="#020617", fg=COLOR_TEXT, font=("Segoe UI", 10), selectbackground=COLOR_PRIMARY, highlightthickness=0, bd=0)
            lista_crono.pack(fill=tk.BOTH, expand=True)

            for i in range(len(self.simulaciones_realizadas)):
                lista_crono.insert(tk.END, f"{i + 1}. {self.simulaciones_realizadas[i]} — {self.distancias_simulaciones[i]:.2f} km")

            # Panel 2: Ordenado por Distancia (Algoritmo de Burbuja)
            p2 = tk.Frame(frame_dos_listas, bg="#0f172a", bd=1, relief=tk.SOLID, padx=12, pady=10)
            p2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

            tk.Label(p2, text="2. Ordenado por Distancia (Burbuja)", bg="#0f172a", fg=COLOR_SUCCESS, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

            lista_ordenada = tk.Listbox(p2, bg="#020617", fg=COLOR_TEXT, font=("Segoe UI", 10), selectbackground=COLOR_PRIMARY, highlightthickness=0, bd=0)
            lista_ordenada.pack(fill=tk.BOTH, expand=True)

            sim_ord, dist_ord = ordenar_simulaciones_por_distancia(self.simulaciones_realizadas, self.distancias_simulaciones)

            for i in range(len(sim_ord)):
                lista_ordenada.insert(tk.END, f"{i + 1}. {sim_ord[i]} — {dist_ord[i]:.2f} km")

        btn_volver = tk.Button(
            card,
            text="← Volver al Menú Principal",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=7,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(pady=(10, 20))

    # =========================================================================
    # 11. CIERRE DEL PROGRAMA (cierre_programa)
    # =========================================================================
    def mostrar_cierre_programa(self):
        self.limpiar_contenedor()

        card = tk.Frame(self.container, bg=COLOR_CARD, bd=1, relief=tk.SOLID, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=740, height=480)

        lbl_icono = tk.Label(card, text="🚂", bg=COLOR_CARD, font=("Segoe UI", 36))
        lbl_icono.pack(pady=(35, 10))

        lbl_tit = tk.Label(
            card,
            text="¡GRACIAS POR UTILIZAR RAIL BOARD!",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        )
        lbl_tit.pack(pady=(0, 10))

        lbl_msg = tk.Label(
            card,
            text="El programa ha finalizado correctamente.\n\nProyecto final de introducción a la programación - 2025\nAutor: De Sousa Matias Joaquin",
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 11),
            justify=tk.CENTER
        )
        lbl_msg.pack(pady=(0, 30))

        frame_btn = tk.Frame(card, bg=COLOR_CARD)
        frame_btn.pack()

        btn_menu = tk.Button(
            frame_btn,
            text="Volver al Menú",
            bg="#334155",
            fg="#ffffff",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.mostrar_menu_principal
        )
        btn_menu.pack(side=tk.LEFT, padx=10)

        btn_salir = tk.Button(
            frame_btn,
            text="Cerrar Aplicación ✖",
            bg=COLOR_DANGER,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2",
            command=self.root.destroy
        )
        btn_salir.pack(side=tk.LEFT, padx=10)

    def ejecutar(self):
        """Inicia el bucle principal de la aplicación gráfica."""
        if self._owns_root:
            self.root.mainloop()

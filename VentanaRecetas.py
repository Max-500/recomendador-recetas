import tkinter as tk
from tkinter import ttk
from recetas_completo import recetas

class SegundaPantalla(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Segunda Pantalla")
        self.configure(background="white")

        # Crear un Frame para contener las recetas
        self.scrollable_frame = ttk.Frame(self)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Agregar un área de desplazamiento vertical
        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        # Crear un lienzo para colocar los widgets
        self.canvas = tk.Canvas(self.scrollable_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Agregar un segundo Frame dentro del lienzo
        self.interior = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        self.mostrar_recetas()

        # Configurar la opción scrollregion para el lienzo
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Configurar el lienzo para que se desplace con la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Configurar la barra de desplazamiento
        self.scrollbar.config(command=self.canvas.yview)

    def mostrar_recetas(self):
        for receta in recetas:
            frame_receta = ttk.Frame(self.interior)
            frame_receta.pack(pady=10, padx=10)

            ttk.Label(frame_receta, text=receta["nombre"], font=("Helvetica", 16, "bold")).pack(anchor="w")
            ttk.Label(frame_receta, text=f"Tipo: {receta['tipo']}", font=("Helvetica", 12)).pack(anchor="w", pady=5)

            ingredientes_frame = ttk.Frame(frame_receta)
            ingredientes_frame.pack(anchor="w")
            ttk.Label(ingredientes_frame, text="Ingredientes:", font=("Helvetica", 12, "bold")).pack(anchor="w")

            for ingrediente in receta["ingredientes"]:
                ttk.Label(ingredientes_frame, text=f"{ingrediente['cantidad']} {ingrediente['nombre']}", font=("Helvetica", 11)).pack(anchor="w")

            preparacion_frame = ttk.Frame(frame_receta)
            preparacion_frame.pack(anchor="w", pady=5)
            ttk.Label(preparacion_frame, text="Método de Preparación:", font=("Helvetica", 12, "bold")).pack(anchor="w")

            for index, paso in enumerate(receta["metodo_preparacion"], start=1):
                ttk.Label(preparacion_frame, text=f"{index}. {paso}", font=("Helvetica", 11)).pack(anchor="w")

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta/120), "units")

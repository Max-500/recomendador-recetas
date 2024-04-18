import tkinter as tk
from tkinter import ttk
from recetas_completo import recetas
from ingredientes_completo import ingredientes
from variables import actualizar_ingredientes_guardados

class VentanaIngredientes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Mis Ingredientes")
        self.geometry("800x800")

        # Crear un marco principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Crear un lienzo dentro del marco para contenido desplazable
        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Agregar una barra de desplazamiento vertical al lienzo
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un segundo marco dentro del lienzo para el contenido
        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Configurar el marco de contenido para cambiar de tamaño con el lienzo
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        nombre_ingredientes = []
        for receta in recetas:
            for ingrediente in receta["ingredientes"]:
                if ingrediente['nombre'] not in nombre_ingredientes:
                    nombre_ingredientes.append(ingrediente['nombre'])
                
        # Crear un diccionario para almacenar los valores de los ingredientes ingresados
        self.valores_ingredientes = {}

        # Crear etiquetas e inputs dinámicos para cada ingrediente
        for nombre_ingrediente in nombre_ingredientes:
            # Crear etiqueta
            etiqueta = ttk.Label(content_frame, text=nombre_ingrediente)
            etiqueta.pack()

            # Crear entrada
            entrada = ttk.Entry(content_frame)
            entrada.pack()

            # Agregar la entrada al diccionario de valores de ingredientes
            self.valores_ingredientes[nombre_ingrediente] = entrada

        # Botón para guardar los ingredientes ingresados
        boton_guardar = ttk.Button(content_frame, text="Guardar", command=self.guardar_ingredientes)
        boton_guardar.pack()

        # Asegurar que el contenido del lienzo se ajuste correctamente
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def guardar_ingredientes(self):
        # Crear un diccionario para almacenar los valores ingresados
        valores_guardados = {}
        
        # Obtener los valores de las entradas y almacenarlos en el diccionario
        for nombre_ingrediente, entrada in self.valores_ingredientes.items():
            valor = entrada.get()
            if valor:
                valores_guardados[nombre_ingrediente] = ingredientes[nombre_ingrediente] * float(entrada.get())

        actualizar_ingredientes_guardados(valores_guardados)
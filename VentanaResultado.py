import tkinter as tk
from tkinter import ttk
from recetas_completo import obtener_receta_por_id
from ingredientes_completo import ingredientes_nuevos as ingredientes_conversion

class VentanaResultados(tk.Toplevel):
    def __init__(self, parent, dataframe, ingredientes_usuario):
        super().__init__(parent)
        self.title("Resultados")
        self.geometry("800x400")

        # Crear el marco principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Crear un lienzo dentro del marco para contenido desplazable
        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Agregar una barra de desplazamiento vertical al lienzo
        scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar_y.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar_y.set)

        # Crear un segundo marco dentro del lienzo para el contenido
        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Anchura deseada para las columnas
        column_width = 40

        # Crear 6 columnas en la interfaz de usuario
        for i in range(6):
            if i+1 != 6:
                column_label = ttk.Label(content_frame, text=f"Platillo {i+1}", width=column_width)
                column_label.grid(row=0, column=i, padx=5, pady=5)
            else:
                column_label = ttk.Label(content_frame, text="Ingredientes Existentes", width=column_width)
                column_label.grid(row=0, column=i, padx=5, pady=5)

        recetas = []
        for index, row in dataframe.iterrows():
            for receta in row['recetas']:
                if receta not in recetas:
                    recetas.append(receta)
        
        platillos = 0
        for id_receta in recetas:
            if platillos < 5:
                receta = obtener_receta_por_id(id_receta)
                
                label_nombre = ttk.Label(content_frame, text=f"Nombre: {receta['nombre']}", wraplength=150)
                label_nombre.grid(row=1, column=platillos, pady=1)
                
                label_sabor = ttk.Label(content_frame, text=f"Sabor: {receta['tipo']}", wraplength=150)
                label_sabor.grid(row=2, column=platillos, pady=1)
                
                label_ingredientes = ttk.Label(content_frame, text="Ingredientes:", wraplength=150)
                label_ingredientes.grid(row=3, column=platillos, pady=1)
                
                ingredientes = receta['ingredientes']
                row = 4
                for i, ingrediente in enumerate(ingredientes):
                    nombre = ingrediente['nombre']
                    cantidad = ingrediente['cantidad']
                    label_ingrediente = ttk.Label(content_frame, text=f"{nombre}", wraplength=150)
                    label_ingrediente.grid(row=row, column=platillos, columnspan=2, pady=1, sticky="w")
                    row += 1
                    cantidad = float(cantidad) / float(ingredientes_conversion[ingrediente['nombre']])
                    label_ingrediente_cantidad = ttk.Label(content_frame, text=f"Cantidad: {cantidad}", wraplength=150)
                    label_ingrediente_cantidad.grid(row=row, column=platillos, columnspan=2, pady=1, sticky="w")
                    row += 1
                
                label_procedimiento = ttk.Label(content_frame, text='Metodo de Preparación', wraplength=150)
                label_procedimiento.grid(row=row, column=platillos, pady=1)
                row += 1
                procedimientos = receta['metodo_preparacion']
                for i, procedimiento in enumerate(procedimientos):
                    label_procedimiento = ttk.Label(content_frame, text=procedimiento, wraplength=150)
                    label_procedimiento.grid(row=row, column=platillos, columnspan=2, pady=1, sticky='w')
                    row += 1

                platillos += 1
        
        # Configurar el marco de contenido para cambiar de tamaño con el lienzo
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Ajustar la altura de cada fila según el contenido
        for i in range(1, row):
            content_frame.grid_rowconfigure(i, weight=1)
        
        row = 1
        for clave, valor in ingredientes_usuario.items():
            label_nombre = ttk.Label(content_frame, text=f"Nombre: {clave}", wraplength=150)
            label_nombre.grid(row=row, column=5, pady=1)
            row+=1
            cantidad = float(valor) / float(ingredientes_conversion[clave])
            label_cantidad = ttk.Label(content_frame, text=f"Cantidad: {cantidad}", wraplength=150)
            label_cantidad.grid(row=row, column=5, pady=1)
            row+=1

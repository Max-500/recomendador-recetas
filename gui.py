import tkinter as tk
from tkinter import ttk
from main import main
from VentanaIngredientes import VentanaIngredientes

def abrir_mi_refrigerador():
    VentanaIngredientes(ventana_principal)
    

def load_data():
    poblacion_inicial_val = poblacion_variables["Población Inicial"].get()
    poblacion_maxima_val = poblacion_variables["Población Máxima"].get()
    probabilidad_mutacion_individuo_val = poblacion_variables["Probabilidad de Mutación del Individuo"].get()
    probabilidad_mutacion_gen_val = poblacion_variables["Probabilidad de Mutación del Gen"].get()
    ngen_val = poblacion_variables["Número de Generaciones"].get()
    result = main()

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Mi App")

# Crear un estilo de ttk para una apariencia más moderna
style = ttk.Style()
style.theme_use("clam")

# Crear el frame principal
frame_principal = ttk.Frame(ventana_principal, padding="20")
frame_principal.grid(row=0, column=0, sticky="nsew")

boton_refrigerador = ttk.Button(frame_principal, text="Ver Refrigerador", command=abrir_mi_refrigerador)
boton_refrigerador.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

# Crear entradas y etiquetas para los parámetros del algoritmo genético
parametros = [
    ("Población Inicial", 10),
    ("Población Máxima", 20),
    ("Probabilidad de Mutación del Individuo", 0.2),
    ("Probabilidad de Mutación del Gen", 0.5),
    ("Número de Generaciones", 100)
]

poblacion_variables = {}  # Diccionario para mapear nombres de parámetros con variables de control

for i, (texto, valor) in enumerate(parametros, start=2):
    label = ttk.Label(frame_principal, text=texto)
    label.grid(row=i, column=0, pady=5, padx=5, sticky="w")
    poblacion_variables[texto] = tk.StringVar()
    entry = ttk.Entry(frame_principal, textvariable=poblacion_variables[texto])  # Asociar la entrada con la variable de control
    entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
    entry.insert(0, valor)

# Crear botón para iniciar el algoritmo
iniciar = ttk.Button(frame_principal, text="Iniciar", command=load_data)
iniciar.grid(row=len(parametros)+2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Alinear los elementos en el frame principal
frame_principal.grid_rowconfigure(0, weight=1)
frame_principal.grid_rowconfigure(len(parametros)+2, weight=1)
frame_principal.grid_columnconfigure(1, weight=1)

# Ejecutar el bucle principal de la ventana principal
ventana_principal.mainloop()
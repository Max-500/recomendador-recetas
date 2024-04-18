import pandas as pd
import random
import variables
import matplotlib.pyplot as plt
from recetas_completo import recetas, obtener_receta_por_id

def numero_aleatorio():
    while True:
        num = random.randint(1, 100)
        if num != 5:
            return num

sabor = 'Salado'

def main():
    p0 = 10
    pmax = 20
    
    pmut = 0.2
    pmut_gen = 0.5
    
    ngen = 100
    
    df = pd.DataFrame(columns=["recetas", "aptitud"])
    estadisticas_generaciones = pd.DataFrame(columns=['Generacion', 'Mejor', 'Peor', 'Promedio'])
    variables.actualizar_ingredientes_guardados({'pechugas de pollo': 400.0})
    print(variables.ingredientes_guardados)

    # POBLACIÓN INICIAL
    for _ in range(p0):
        recetas = []        
        aux = 0
        while aux < 5:
            x = numero_aleatorio()
            if x not in recetas and x != 5:
                recetas.append(x)
                aux += 1
        individuo = {"recetas": recetas, "aptitud": calcular_aptitud(recetas)}
        df = df._append(individuo, ignore_index=True)
    
    df = df.sort_values(by='aptitud')
    for index in range(ngen):
        mejor, resto = seleccion_mejor_y_resto_individuos(df)
        hijos = cruzas(mejor, resto)
        hijos_mutados = mutaciones(hijos, pmut, pmut_gen)
        df = anadir_poblacion(df, hijos_mutados)
        # Eliminar duplicados
        estadisticas_generaciones = añadir_estadisticas_generacion(df, estadisticas_generaciones, index+1, 'MIN')
        df = df.drop_duplicates(subset=['aptitud'])
        df = df.head(pmax)
    graficar_estadisticas(estadisticas_generaciones)
    return df.head(1)

def calcular_aptitud(data):
    aptitud = []
    
    for id_receta in data:
        receta = obtener_receta_por_id(id_receta)
        requerido = 0
        for ingrediente in receta['ingredientes']:
            if ingrediente['nombre'] in variables.ingredientes_guardados:
                result = float(ingrediente['cantidad']) - float(variables.ingredientes_guardados[ingrediente['nombre']])
                if result < 0:
                    requerido += 0
                else: 
                    requerido += result
            else:
                requerido += float(ingrediente['cantidad'])
                                
        if sabor != receta['tipo']:
            requerido = requerido * 5

        aptitud.append(requerido)
    return sum(aptitud)
        
def seleccion_mejor_y_resto_individuos(df):
    mejor_individuo = df.iloc[0]
    df_resto = df.iloc[1:].copy()
    df_resto = df_resto.sort_values(by='aptitud')
    return mejor_individuo, df_resto

def cruzas(mejor, resto):
    hijos = []
    for _, row in resto.iterrows():
        tamano = min(len(mejor['recetas']), len(row['recetas']))
        punto_corte = random.randint(1, tamano-1)
        
        hijo1 = mejor['recetas'][:punto_corte] + row['recetas'][punto_corte:]
        hijo2 = mejor['recetas'][punto_corte:] + row['recetas'][:punto_corte]
        
        hijos.append(hijo1)
        hijos.append(hijo2)
    return hijos

def mutaciones(hijos, pmut, pmut_gen):
    for hijo in hijos:
        numero_aleatorio_ind = random.uniform(0, 1)
        if numero_aleatorio_ind <= pmut:
            for i in range(len(hijo)):
                numero_aleatorio_gen = random.uniform(0, 1)
                if numero_aleatorio_gen <= pmut_gen:
                    hijo[i] = numero_aleatorio()
    return hijos

def anadir_poblacion(df, hijos):
    for hijo in hijos:
        individuo = {"recetas": hijo, "aptitud": calcular_aptitud(hijo)}
        df = df._append(individuo, ignore_index=True)
    df = df.sort_values(by='aptitud')
    return df

def añadir_estadisticas_generacion(df, estadisticas_generaciones, generacion, modo='MIN'):
    if modo == 'MAX':
        mejor = df['aptitud'].max()
        peor = df['aptitud'].min()
    else:  # 'MIN'
        mejor = df['aptitud'].min()
        peor = df['aptitud'].max()

    promedio = df['aptitud'].mean()
    # Crear un nuevo DataFrame para el registro
    nuevo_registro_df = pd.DataFrame({
        'Generacion': [generacion],
        'Mejor': [mejor],
        'Peor': [peor],
        'Promedio': [promedio]
    })
    # Usar pd.concat para añadir el nuevo registro
    estadisticas_generaciones = pd.concat([estadisticas_generaciones, nuevo_registro_df], ignore_index=True)
    return estadisticas_generaciones

def graficar_estadisticas(df_estadisticas):
    plt.figure(figsize=(10, 6))

    # Graficar cada estadística
    print(df_estadisticas)
    plt.plot(df_estadisticas['Generacion'], df_estadisticas['Mejor'], color='green', label='Mejor')
    plt.plot(df_estadisticas['Generacion'], df_estadisticas['Peor'], color='red', label='Peor')
    plt.plot(df_estadisticas['Generacion'], df_estadisticas['Promedio'], color='blue', label='Promedio')

    # Añadir título y etiquetas
    plt.title('Evolución de la Población')
    plt.xlabel('Generación')
    plt.ylabel('Valor')

    # Añadir leyenda
    plt.legend()

    # Mostrar la gráfica
    plt.show()
main()
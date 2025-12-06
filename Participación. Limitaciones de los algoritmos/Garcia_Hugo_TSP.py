# Participacion Limitaciones de los algoritmos
# Hugo Gabriel Garcia Saldivar ICOM 220530758
# Analisis de algoritmos 2025B

import itertools
import numpy as np

nombres_de_las_ciudades = ["Ciudad A", "Ciudad B", "Ciudad C", "Ciudad D", "Ciudad E", "Ciudad F"]

# Las ciudades se representan con una matriz de adyacencia
matriz_de_distancias_entre_ciudades = np.array([
    # A   B   C   D   E   F
    [0,  10, 15, 20, 25, 30], # Distancias desde Ciudad A
    [10,  0, 35, 25, 15, 20], # Distancias desde Ciudad B
    [15, 35,  0, 30, 10, 45], # Distancias desde Ciudad C
    [20, 25, 30,  0, 50, 15], # Distancias desde Ciudad D
    [25, 15, 10, 50,  0, 10], # Distancias desde Ciudad E
    [30, 20, 45, 15, 10,  0]  # Distancias desde Ciudad F
])

def resolver_problema_del_viajero():
    """
    Función principal que ejecuta 
    el algoritmo para el TSP
    """

    indice_ciudad_origen = 0
    indices_ciudades_a_visitar = [1, 2, 3, 4, 5]
    
    # Variables para almacenar la mejor solución encontrada.
    costo_minimo_encontrado = float('inf')
    mejor_ruta_encontrada = []

    print("INICIO DE EVALUACIÓN DE RUTAS")
    print(f"Origen: {nombres_de_las_ciudades[indice_ciudad_origen]}\n")

    # Generamos todas las permutaciones posibles
    generador_de_permutaciones = itertools.permutations(indices_ciudades_a_visitar)

    contador_rutas = 0
    for permutacion_actual in generador_de_permutaciones:
        contador_rutas += 1
        ruta_actual_evaluada = [indice_ciudad_origen] + list(permutacion_actual) + [indice_ciudad_origen]
        distancia_total_de_la_ruta_actual = 0
        ruta_legible = "" 
        
        # Calculo de distancais
        for i in range(len(ruta_actual_evaluada) - 1):
            ciudad_actual = ruta_actual_evaluada[i]
            siguiente_ciudad = ruta_actual_evaluada[i+1]
            distancia_tramo = matriz_de_distancias_entre_ciudades[ciudad_actual, siguiente_ciudad]
            distancia_total_de_la_ruta_actual += distancia_tramo
            ruta_legible += f"{nombres_de_las_ciudades[ciudad_actual]} -> "

        ruta_legible += nombres_de_las_ciudades[indice_ciudad_origen]

        # Imprimir la ruta evaluada
        print(f"Ruta #{contador_rutas}: {ruta_legible} | Costo Total: {distancia_total_de_la_ruta_actual}")

        if distancia_total_de_la_ruta_actual < costo_minimo_encontrado:
            costo_minimo_encontrado = distancia_total_de_la_ruta_actual
            mejor_ruta_encontrada = ruta_actual_evaluada

    # Resultados 
    print("\nRESULTADO FINAL")
    print(f"Total de rutas evaluadas: {contador_rutas}")
    print(f"Costo Mínimo Encontrado: {costo_minimo_encontrado}") 
    
    print("Mejor Ruta (Secuencia de ciudades):")
    ruta_final_nombres = [nombres_de_las_ciudades[i] for i in mejor_ruta_encontrada]
    print(" -> ".join(ruta_final_nombres))

if __name__ == "__main__":
    resolver_problema_del_viajero()
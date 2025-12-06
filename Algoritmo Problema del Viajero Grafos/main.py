# Hugo Gabriel Garcia Saldivar
# Oswaldo Daniel Maciel Vargas
# Fuerza bruta problema del viajero
import math
import itertools

def distancia_ruta(ruta, grafo):
    distancia_total = 0
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i+1]
        distancia_total = distancia_total + grafo[origen][destino]
    
    # Distancia de regreso al punto de inicio
    distancia_total = distancia_total + grafo[ruta[-1]][ruta[0]]
    return distancia_total

def encontrar_ruta_optima_grafo(grafo):
    mejor_ruta = []
    minima_distancia = float('inf')

    nombre_ciudades = list(grafo.keys())
    punto_inicio = nombre_ciudades[0]
    ciudades_a_visitar = nombre_ciudades[1:]

    permutaciones = list(itertools.permutations(ciudades_a_visitar))

    for perm in permutaciones:
        ruta_actual = [punto_inicio] + list(perm)
        distancia_actual = distancia_ruta(ruta_actual, grafo)
        
        if distancia_actual < minima_distancia:
            minima_distancia = distancia_actual
            mejor_ruta = ruta_actual
            
    mejor_ruta.append(punto_inicio)
    
    return mejor_ruta, minima_distancia


grafo_ciudades = {
    'A': {'B': 12, 'C': 11, 'D': 18, 'E': 20},
    'B': {'A': 12, 'C': 25, 'D': 5, 'E': 9},
    'C': {'A': 11, 'B': 25, 'D': 30, 'E': 11},
    'D': {'A': 18, 'B': 5, 'C': 30, 'E': 9},
    'E': {'A': 20, 'B': 9, 'C': 11, 'D': 9}  
}


mejor_ruta, minima_distancia = encontrar_ruta_optima_grafo(grafo_ciudades)

print("\nLa ruta mas optima encontrada fue:")
print(" -> ".join(map(str, mejor_ruta)))
print(f"\nCon una distancia total de: {minima_distancia}\n\n")
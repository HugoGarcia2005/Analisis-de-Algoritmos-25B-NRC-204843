# Hugo Gabriel Garcia Saldivar
# Fuerza bruta problema del viajero
import math
import itertools

def encontrar_distancia(punto1, punto2):
    distancia = math.sqrt(math.pow(punto1[0]-punto2[0],2)+math.pow(punto1[1]-punto2[1],2)) 
    return distancia

def distancia_ruta(ruta):
    distancia_total = 0
    for i in range(len(ruta)-1):
        distancia_total = distancia_total + encontrar_distancia(ruta[i], ruta[i+1])
    distancia_total = distancia_total + encontrar_distancia(ruta[-1], ruta[0])
    return distancia_total

def encontrar_ruta_mas_corta(ciudades):
    mejor_ruta = []
    minima_distancia = float('inf')

    punto_inicio = ciudades[0]
    ciudades_a_visitar = ciudades[1:]

    permutaciones = list(itertools.permutations(ciudades_a_visitar))
    for perm in permutaciones:
        ruta_actual = [punto_inicio] + list(perm)
        distancia_actual = distancia_ruta(ruta_actual)
        
        if distancia_actual < minima_distancia:
            minima_distancia = distancia_actual
            mejor_ruta = ruta_actual
            
    mejor_ruta.append(punto_inicio)
    
    return mejor_ruta, minima_distancia


ciudades = [(0,0), (1,3), (4,3), (6,1), (3,0), (5,5)]

mejor_ruta, minima_distancia = encontrar_ruta_mas_corta(ciudades)

print(f"El conjunto de las ciudades es: {ciudades}\n")
print("La ruta mas optima encontrada fue:")
print(" -> ".join(map(str, mejor_ruta)))
print(f"\nCon una distancia total de: {minima_distancia}")
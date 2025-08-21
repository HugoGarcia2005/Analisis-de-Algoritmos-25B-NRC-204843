# Participacion - Complejidad Temporal
# Hugo Gabriel Garcia Saldivar 

import random
import time
import matplotlib.pyplot as plt

OPCION_BUBBLE_SORT = 1
OPCION_MERGE_SORT = 2
OPCION_QUICK_SORT = 3
FACTOR_CONVERTIR_MILISEGUNDOS = 1000

def generadorNumeroAleatorios(numerosAGenerar):
    numerosAleatorios = []

    for i in range(numerosAGenerar):
        numeroAleatorio = random.randint(1, 1_000)
        numerosAleatorios.append(numeroAleatorio)
    return numerosAleatorios

def ordenadorNumeros(numerosDesordenados,algoritmoOrdenamiento):
    inicioTiempoEjecucionAlgoritmo = time.perf_counter()

    if algoritmoOrdenamiento == OPCION_BUBBLE_SORT:
        numerosOrdenados = bubbleSort(numerosDesordenados)
    elif algoritmoOrdenamiento == OPCION_MERGE_SORT:
        numerosOrdenados = mergeSort(numerosDesordenados)
    elif algoritmoOrdenamiento == OPCION_QUICK_SORT:
        numerosOrdenados = quickSort(numerosDesordenados)
    else:
        print("Error: Algoritmo no soportado :(")

    finTiempoEjecucionAlgoritmo = time.perf_counter()
    tiempoTotalEjecucionAlgoritmo = (finTiempoEjecucionAlgoritmo - inicioTiempoEjecucionAlgoritmo) * FACTOR_CONVERTIR_MILISEGUNDOS
    return numerosOrdenados, tiempoTotalEjecucionAlgoritmo

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    medio = len(arr) // 2
    izquierda = arr[:medio]
    derecha = arr[medio:]
    izquierda = mergeSort(izquierda)
    derecha = mergeSort(derecha)
    return merge(izquierda, derecha)

def merge(izquierda, derecha):
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

def quickSort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2] 
    izquierda = [x for x in arr if x < pivote]
    medio = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]
    return quickSort(izquierda) + medio + quickSort(derecha)

print("Generando 10 numeros aleatorios")
diezNumerosAleatorios = generadorNumeroAleatorios(10)
print(f"{diezNumerosAleatorios}\n")

# La función ordenador retorna (lista_ordenada, tiempo)
# {tiempoEjecucion:.6f} ajusta en 6 decimales la salida de tiempoEjecucion
arregloOrdenado, tiempoEjecucion = ordenadorNumeros(diezNumerosAleatorios, OPCION_BUBBLE_SORT)

print("=== RESULTADOS BUBBLE SORT ===")
print(f"Arreglo ordenado: {arregloOrdenado}")
print(f"Tiempo de ejecución: {tiempoEjecucion:.6f} ms")

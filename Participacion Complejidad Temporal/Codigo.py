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
        numeroAleatorio = random.randint(1, 10_000)
        numerosAleatorios.append(numeroAleatorio)
    return numerosAleatorios

def medirTiempo(arreglo,algoritmo):
    inicioTiempoEjecucionAlgoritmo = time.perf_counter()
    numerosOrdenados = ordenadorNumeros(arreglo,algoritmo)
    finTiempoEjecucionAlgoritmo = time.perf_counter()
    tiempoTotalEjecucionAlgoritmo = (finTiempoEjecucionAlgoritmo - inicioTiempoEjecucionAlgoritmo) * FACTOR_CONVERTIR_MILISEGUNDOS
    return numerosOrdenados, tiempoTotalEjecucionAlgoritmo    

def ordenadorNumeros(numerosDesordenados,algoritmoOrdenamiento):
    if algoritmoOrdenamiento == OPCION_BUBBLE_SORT:
        numerosOrdenados = bubbleSort(numerosDesordenados)
    elif algoritmoOrdenamiento == OPCION_MERGE_SORT:
        numerosOrdenados = mergeSort(numerosDesordenados)
    elif algoritmoOrdenamiento == OPCION_QUICK_SORT:
        numerosOrdenados = quickSort(numerosDesordenados)
    else:
        print("Error: Algoritmo no soportado :(")
    return numerosOrdenados

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

def generarGraficaComparativa():
    # Tamaños de arreglo a probar: de 50 en 50 hasta 1000
    tamanos = list(range(50, 1001, 50))
    
    # Listas para almacenar los tiempos de cada algoritmo
    tiempos_bubble = []
    tiempos_merge = []
    tiempos_quick = []
    
    print("Generando datos para la gráfica...")
    
    for tamano in tamanos:
        print(f"Procesando arreglo de tamaño: {tamano}")
        
        # Generar arreglo aleatorio
        arreglo = generadorNumeroAleatorios(tamano)
        
        # Medir tiempo de Bubble Sort
        _, tiempo_bubble = medirTiempo(arreglo, OPCION_BUBBLE_SORT)
        tiempos_bubble.append(tiempo_bubble)
        
        # Medir tiempo de Merge Sort
        _, tiempo_merge = medirTiempo(arreglo, OPCION_MERGE_SORT)
        tiempos_merge.append(tiempo_merge)
        
        # Medir tiempo de Quick Sort
        _, tiempo_quick = medirTiempo(arreglo, OPCION_QUICK_SORT)
        tiempos_quick.append(tiempo_quick)
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    
    plt.plot(tamanos, tiempos_bubble, 'r-', label='Bubble Sort', linewidth=2)
    plt.plot(tamanos, tiempos_merge, 'g-', label='Merge Sort', linewidth=2)
    plt.plot(tamanos, tiempos_quick, 'b-', label='Quick Sort', linewidth=2)
    
    plt.xlabel('Tamaño del Arreglo')
    plt.ylabel('Tiempo de Ejecución (ms)')
    plt.title('Comparación de Tiempos de Algoritmos de Ordenamiento')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Mostrar la gráfica
    plt.show()
    
    return tiempos_bubble, tiempos_merge, tiempos_quick


generarGraficaComparativa()


# Hugo Gabriel Garcia Saldivar ICOM 220530758
# Participación. Programación Dinámica (Fibonacci con y sin P.Dinamica)
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from memory_profiler import memory_usage
OPCION_FIBONACCI_NORMAL = 1
OPCION_FIBONACCI_DINAMICO = 2
FACTOR_CONVERTIR_MILISEGUNDOS = 1000

def fibonacci_normal(numero):
    if numero <= 1:
        return numero
    return fibonacci_normal(numero - 1) + fibonacci_normal(numero - 2)

cache = {0: 0, 1: 1}
def fibonacci_dinamico(numero):
    if numero in cache:
        return cache[numero]
    cache[numero] = fibonacci_dinamico(numero - 1) + fibonacci_dinamico(numero - 2)
    return cache[numero]

def funciones_fibonacci(numero, funcion):
    if funcion == OPCION_FIBONACCI_NORMAL:
        return fibonacci_normal(numero)
    elif funcion == OPCION_FIBONACCI_DINAMICO:
        global cache
        cache = {0: 0, 1: 1}
        return fibonacci_dinamico(numero)

def medir_tiempo_funcion(numero_fib, tipo_funcion):
    inicio_tiempo = time.perf_counter()
    funciones_fibonacci(numero_fib, tipo_funcion)
    fin_tiempo = time.perf_counter()
    tiempo_ejecucion = (fin_tiempo - inicio_tiempo) * FACTOR_CONVERTIR_MILISEGUNDOS
    return tiempo_ejecucion

def medir_memoria_funcion(numero_fib, tipo_funcion):
    mem_consumida = memory_usage(
        (funciones_fibonacci, (numero_fib, tipo_funcion)),
        interval=0.01
    )
    return max(mem_consumida)

def generar_grafica_temporal(x_valores, tiempos_normal, tiempos_dinamico):
    plt.figure(figsize=(15, 7))
    plt.plot(x_valores, tiempos_normal, label='Fibonacci Normal', marker='o', linestyle='--', color='darkorange')
    plt.plot(x_valores, tiempos_dinamico, label='Fibonacci Dinamico', marker='o', linestyle='--', color='dodgerblue')
    plt.xlabel("Número 'n' de Fibonacci")
    plt.ylabel("Tiempo de ejecución (milisegundos)")
    plt.title("Complejidad Temporal: Fibonacci Normal vs. Dinámico")
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)

def generar_grafica_espacial(x_valores, memorias_normal, memorias_dinamico):
    plt.figure(figsize=(15, 7))
    plt.plot(x_valores, memorias_normal, label='Fibonacci Normal (Recursivo)', marker='o', linestyle='--', color='crimson')
    plt.plot(x_valores, memorias_dinamico, label='Fibonacci Dinamico (Cache)', marker='o', linestyle='--', color='forestgreen')
    plt.xlabel("Número 'n' de Fibonacci")
    plt.ylabel("Uso de memoria (MiB)")
    plt.title("Complejidad Espacial: Fibonacci Normal vs. Dinámico")
    plt.legend()
    plt.grid(True)

if __name__ == "__main__":
    try:
        numero_maximo = int(input("Ingresa el número máximo de Fibonacci a calcular (ej. 40): "))
        if numero_maximo < 0:
            print("Error: Por favor, ingresa un número no negativo.")
        else:
            x_valores = list(range(0, numero_maximo + 1, 5))
            if numero_maximo not in x_valores:
                x_valores.append(numero_maximo)

            tiempos_fib_normal = []
            tiempos_fib_dinamico = []
            memorias_fib_normal = []
            memorias_fib_dinamico = []

            print("\nCalculando tiempos de ejecución y uso de memoria...")

            for n in x_valores:
                tiempo_n = medir_tiempo_funcion(n, OPCION_FIBONACCI_NORMAL)
                tiempo_d = medir_tiempo_funcion(n, OPCION_FIBONACCI_DINAMICO)
                tiempos_fib_normal.append(tiempo_n)
                tiempos_fib_dinamico.append(tiempo_d)

                memoria_n = medir_memoria_funcion(n, OPCION_FIBONACCI_NORMAL)
                memoria_d = medir_memoria_funcion(n, OPCION_FIBONACCI_DINAMICO)
                memorias_fib_normal.append(memoria_n)
                memorias_fib_dinamico.append(memoria_d)

                print(f"n={n:<3} | T. Normal: {tiempo_n:>8.2f} ms | T. Dinámico: {tiempo_d:>8.4f} ms | M. Normal: {memoria_n:>6.2f} MiB | M. Dinámico: {memoria_d:>6.2f} MiB")

            generar_grafica_temporal(x_valores, tiempos_fib_normal, tiempos_fib_dinamico)
            generar_grafica_espacial(x_valores, memorias_fib_normal, memorias_fib_dinamico)

            print("\nMostrando gráficas. Cierra las ventanas para terminar el programa.")
            plt.show()

    except ValueError:
        print("Error: Entrada no válida. Debes ingresar un número entero.")
    except KeyboardInterrupt:
        print("\nCálculo interrumpido por el usuario.")
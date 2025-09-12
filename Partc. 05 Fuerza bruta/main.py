# Programa para obtener el par mas cercano
# Participacion Hugo Gabriel Garcia Saldivar

import tkinter as tk
from tkinter import ttk
import math
import random

def find_the_distance(point1, point2):
    distance = math.sqrt(math.pow(point1[0]-point2[0],2)+math.pow(point1[1]-point2[1],2)) 
    return distance

def shortest_distance(data_points):
    min_distance = float('inf')
    closest_pair = None
    
    for i in range(len(data_points)):
        for j in range(i + 1, len(data_points)):
            distance = find_the_distance(data_points[i], data_points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (i, j)
    
    return min_distance, closest_pair

def find_closest_pair():
    points = []
    for i in range(5):
        try:
            x = float(entries[i][0].get())
            y = float(entries[i][1].get())
            points.append((x, y))
        except ValueError:
            result_label.config(text="Por favor, complete todos los campos con números válidos")
            return

    min_distance, closest_pair = shortest_distance(points)
    
    if closest_pair:
        result_label.config(text=f"El par más cercano es: P{closest_pair[0]+1} y P{closest_pair[1]+1}\nDistancia: {min_distance:.2f}")

    print(f"El par más cercano es: P{closest_pair[0]+1} y P{closest_pair[1]+1} con una distancia de {min_distance:.2f}")

def clear_fields():
    for i in range(5):
        for j in range(2):
            entries[i][j].delete(0, tk.END)
    result_label.config(text="")

def generate_random_points():
    clear_fields()
    for i in range(5):
        x = random.uniform(0, 40)
        y = random.uniform(0, 40)
        entries[i][0].insert(0, f"{x:.2f}")
        entries[i][1].insert(0, f"{y:.2f}")
    result_label.config(text="Puntos generados aleatoriamente")


root = tk.Tk()
root.title("Encontrar Par de Puntos Más Cercano")
root.geometry("500x300")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

title_label = ttk.Label(main_frame, text="Ingrese las coordenadas de los puntos:", font=('Arial', 12, 'bold'))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

ttk.Label(main_frame, text="Punto", font=('Arial', 10, 'bold')).grid(row=1, column=0, padx=5, pady=5)
ttk.Label(main_frame, text="X", font=('Arial', 10, 'bold')).grid(row=1, column=1, padx=5, pady=5)
ttk.Label(main_frame, text="Y", font=('Arial', 10, 'bold')).grid(row=1, column=2, padx=5, pady=5)

entries = []

for i in range(5):
    row_entries = []
    point_label = ttk.Label(main_frame, text=f"P{i+1}")
    point_label.grid(row=i+2, column=0, padx=5, pady=5)
    
    x_entry = ttk.Entry(main_frame, width=10)
    x_entry.grid(row=i+2, column=1, padx=5, pady=5)
    row_entries.append(x_entry)
    
    y_entry = ttk.Entry(main_frame, width=10)
    y_entry.grid(row=i+2, column=2, padx=5, pady=5)
    row_entries.append(y_entry)
    
    entries.append(row_entries)

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=7, column=0, columnspan=3, pady=20)

find_button = ttk.Button(button_frame, text="Buscar par más cercano", command=find_closest_pair)
find_button.grid(row=0, column=0, padx=10)

clear_button = ttk.Button(button_frame, text="Limpiar datos", command=clear_fields)
clear_button.grid(row=0, column=1, padx=10)

random_button = ttk.Button(button_frame, text="Generar datos aleatorios", command=generate_random_points)
random_button.grid(row=0, column=2, padx=5)

result_label = ttk.Label(main_frame, text="", font=('Arial', 10))
result_label.grid(row=8, column=0, columnspan=3, pady=10)

root.mainloop()
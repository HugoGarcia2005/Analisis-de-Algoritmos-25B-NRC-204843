# Act01 - Busqueda con GUI 
# Hugo Gabriel Garcia Saldivar 

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

arreglo_actual = None
tamanios_lista = [100, 1000, 10000, 100000]
resultados = {"lineal": [], "binaria": []}

def busqueda_lineal(arreglo, elemento):
    for indice in range(len(arreglo)):
        if arreglo[indice] == elemento:
            return indice
    return -1

def busqueda_binaria(arreglo, elemento):
    izquierda, derecha = 0, len(arreglo) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arreglo[medio] < elemento:
            izquierda = medio + 1
        elif arreglo[medio] > elemento:
            derecha = medio - 1
        else:
            return medio
    return -1

def generar_arreglo_ordenado(tamano):
    arreglo = [random.randint(0, 1000000) for _ in range(tamano)]
    arreglo.sort()
    return arreglo

def medir_tiempo(algoritmo, arreglo, elemento):
    inicio = time.perf_counter()
    algoritmo(arreglo, elemento)
    fin = time.perf_counter()
    return (fin - inicio) * 1000 

class AplicacionBusqueda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Comparación de Búsquedas")
        self.ventana.geometry("1000x600+100+100")
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        marco_principal = ttk.Frame(self.ventana, padding=10, width=980, height=580)
        marco_principal.pack(fill=tk.BOTH, expand=False)
        marco_principal.pack_propagate(False) 
        marco_controles = ttk.Frame(marco_principal, padding=10, width=300, height=560)
        marco_controles.pack(side=tk.LEFT, fill=tk.Y)
        marco_controles.pack_propagate(False)
        marco_grafica = ttk.Frame(marco_principal, padding=10, width=650, height=560)
        marco_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        marco_grafica.pack_propagate(False)
        ttk.Label(marco_controles, text="Tamaño de arreglo:").pack(anchor=tk.W)
        self.combo_tamanio = ttk.Combobox(
            marco_controles, 
            values=tamanios_lista, 
            state="readonly"
        )
        self.combo_tamanio.current(0)
        self.combo_tamanio.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            marco_controles, 
            text="Generar Arreglo", 
            command=self.generar_arreglo
        ).pack(fill=tk.X, pady=5)
        
        ttk.Label(marco_controles, text="Valor a buscar:").pack(anchor=tk.W, pady=(10,0))
        self.entrada_valor = ttk.Entry(marco_controles)
        self.entrada_valor.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            marco_controles, 
            text="Búsqueda Lineal", 
            command=lambda: self.realizar_busqueda("lineal")
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            marco_controles, 
            text="Búsqueda Binaria", 
            command=lambda: self.realizar_busqueda("binaria")
        ).pack(fill=tk.X, pady=5)
        
        ttk.Label(marco_controles, text="Resultados:").pack(anchor=tk.W, pady=(10,0))
        self.etiqueta_resultado = ttk.Label(
            marco_controles, 
            wraplength=250,
            relief=tk.SUNKEN, 
            padding=5
        )
        self.etiqueta_resultado.pack(fill=tk.X)
        
        ttk.Button(
            marco_controles, 
            text="Limpiar Gráfica", 
            command=self.limpiar_grafica
        ).pack(fill=tk.X, pady=(20,5))
        
        ttk.Label(marco_controles, text="Datos del Arreglo:").pack(anchor=tk.W, pady=(10,0))
        
        frame_texto = ttk.Frame(marco_controles, height=150)
        frame_texto.pack(fill=tk.BOTH, expand=False)
        frame_texto.pack_propagate(False)
        
        self.texto_datos = tk.Text(
            frame_texto, 
            height=10, 
            width=30,
            state=tk.DISABLED
        )
        scroll = ttk.Scrollbar(frame_texto, command=self.texto_datos.yview)
        self.texto_datos.configure(yscrollcommand=scroll.set)
        self.texto_datos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.figura, self.ejes = plt.subplots(figsize=(6.5, 5)) 
        self.ejes.set_xlabel('Tamaño del arreglo')
        self.ejes.set_ylabel('Tiempo (ms)')
        self.ejes.set_title('Tiempos de Búsqueda')
        self.ejes.set_xticks(range(len(tamanios_lista)))
        self.ejes.set_xticklabels(tamanios_lista)

        self.ejes.set_ylim(0, 10)
        self.ejes.grid(True)
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=marco_grafica)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=False)
        self.canvas_widget.config(width=650, height=560)

    def generar_arreglo(self):
        global arreglo_actual
        try:
            tamano = int(self.combo_tamanio.get())
            arreglo_actual = generar_arreglo_ordenado(tamano)
            self.mostrar_datos()
            self.etiqueta_resultado.config(text=f"Arreglo de {tamano} elementos generado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el arreglo: {str(e)}")
    
    def mostrar_datos(self):
        global arreglo_actual
        self.texto_datos.config(state=tk.NORMAL)
        self.texto_datos.delete(1.0, tk.END)
        
        if arreglo_actual is None:
            self.texto_datos.insert(tk.END, "No hay datos generados")
        else:
            tamano = len(arreglo_actual)
            self.texto_datos.insert(tk.END, f"Total {tamano} elementos: \n\n")

            for i, elemento in enumerate(arreglo_actual):
                self.texto_datos.insert(tk.END, f"{elemento}\n")
                if i % 100 == 0:
                    self.texto_datos.update_idletasks()

        self.texto_datos.config(state=tk.DISABLED)
        self.texto_datos.see(tk.END)
    
    def realizar_busqueda(self, tipo):
        global arreglo_actual, resultados
        
        if arreglo_actual is None:
            messagebox.showwarning("Advertencia", "Primero genera un arreglo")
            return
        
        try:
            valor = int(self.entrada_valor.get())
            tamano = len(arreglo_actual)
            
            if tipo == "lineal":
                tiempo = medir_tiempo(busqueda_lineal, arreglo_actual, valor)
                indice = busqueda_lineal(arreglo_actual, valor)
            else:
                tiempo = medir_tiempo(busqueda_binaria, arreglo_actual, valor)
                indice = busqueda_binaria(arreglo_actual, valor)
            
            resultado = f"Encontrado en índice: {indice}" if indice != -1 else "No encontrado"
            self.etiqueta_resultado.config(
                text=f"Búsqueda {tipo}\n" +
                     f"Resultado: {resultado}\n" +
                     f"Tiempo: {tiempo:.6f} ms\n" +
                     f"Tamaño: {tamano} elementos"
            )
            
            if indice != -1:
                posicion = tamanios_lista.index(tamano)
                if tipo == "lineal":
                    resultados["lineal"].append((posicion, tiempo))
                else:
                    resultados["binaria"].append((posicion, tiempo))
                
                self.actualizar_grafica()
            
        except ValueError:
            messagebox.showerror("Error", "Ingresa un valor numérico válido")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def actualizar_grafica(self):
        self.ejes.clear()
        
        if resultados["lineal"]:
            x, y = zip(*resultados["lineal"])
            puntos_ordenados = sorted(zip(x, y))
            x_ord, y_ord = zip(*puntos_ordenados)
            self.ejes.plot(x_ord, y_ord, 'ro-', label='Búsqueda Lineal') 

        if resultados["binaria"]:
            x, y = zip(*resultados["binaria"])
            puntos_ordenados = sorted(zip(x, y))
            x_ord, y_ord = zip(*puntos_ordenados)
            self.ejes.plot(x_ord, y_ord, 'bs-', label='Búsqueda Binaria')
        
        self.ejes.set_xlabel('Tamaño del arreglo')
        self.ejes.set_ylabel('Tiempo (ms)')
        self.ejes.set_title('Tiempos de Búsqueda')
        self.ejes.set_xticks(range(len(tamanios_lista)))
        self.ejes.set_xticklabels(tamanios_lista)
        self.ejes.set_ylim(0, 10)
        self.ejes.legend()
        self.ejes.grid(True)
        
        self.canvas.draw()
    
    def limpiar_grafica(self):
        global resultados
        resultados = {"lineal": [], "binaria": []}
        self.actualizar_grafica()
        self.etiqueta_resultado.config(text="Gráfica limpiada")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionBusqueda(ventana)
    ventana.mainloop()
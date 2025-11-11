# Act. 5: Técnica Voraz Huffman (Equipo Tr3s)
# Hugo Gabriel Garcia Saldivar
# Oswaldo Daniel Maciel Vargas

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from collections import Counter
import heapq

# =======================
# === LOGICA HUFFMAN ===
# =======================

class NodoHuffman:
    def __init__(self, char, freq, izq=None, der=None):
        self.char = char
        self.freq = freq
        self.izq = izq
        self.der = der
    def __lt__(self, otro):
        return self.freq < otro.freq

def calcular_frecuencias(texto):
    return Counter(texto)

def construir_arbol_huffman(frecuencias):
    cola = [NodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(cola)
    while len(cola) > 1:
        izq = heapq.heappop(cola)
        der = heapq.heappop(cola)
        padre = NodoHuffman(None, izq.freq + der.freq, izq, der)
        heapq.heappush(cola, padre)
    return cola[0] if cola else None

def generar_codigos_huffman(arbol):
    codigos = {}
    def recorrer(nodo, codigo):
        if nodo is None: return
        if nodo.char is not None:
            codigos[nodo.char] = codigo or "0" 
        recorrer(nodo.izq, codigo + "0")
        recorrer(nodo.der, codigo + "1")
    recorrer(arbol, "")
    return codigos

def codificar_texto(texto, mapa_codigos):
    return "".join(mapa_codigos[c] for c in texto)

def decodificar_texto(codificado, arbol):
    if not arbol: return ""
    if arbol.char: return arbol.char * len(codificado)
    nodo, resultado = arbol, ""
    for bit in codificado:
        nodo = nodo.izq if bit == "0" else nodo.der
        if nodo.char:
            resultado += nodo.char
            nodo = arbol
    return resultado

def guardar_comprimido(ruta, texto_codificado):
    salida = os.path.splitext(ruta)[0] + "_comprimido.bin"
    bits_padding = (8 - len(texto_codificado) % 8) % 8
    info_padding = "{:08b}".format(bits_padding)
    texto_codificado_con_padding = info_padding + texto_codificado + ("0" * bits_padding)
    
    array_bytes = bytearray(
        int(texto_codificado_con_padding[i:i+8], 2) 
        for i in range(0, len(texto_codificado_con_padding), 8)
    )
    
    with open(salida, "wb") as f:
        f.write(array_bytes)
    return salida


# =================
# === INTERFAZ  ===
# =================

def update_text_widget(widget, text, append=True):
    """
    Función simple para actualizar un widget de texto.
    (La misma que teníamos en FrontEnd.py)
    """
    widget.config(state=tk.NORMAL)
    if not append:
        widget.delete("1.0", tk.END)
    widget.insert(tk.END, text + "\n")
    widget.see(tk.END)
    widget.config(state=tk.DISABLED)

def create_gui():
    """Crea, estiliza y lanza la ventana principal de la GUI."""
    
    BG_COLOR = "#3E3E3E"       
    FG_COLOR = "#E0E0E0"       
    FRAME_BG = "#2D2D2D"     
    BUTTON_BG = "#555555"    
    BUTTON_ACTIVE = "#666666" 
    DISABLED_BG = "#4A4A4A"   
    DISABLED_FG = "#888888"   
    ENTRY_BG = "#555555"
    TEXT_BG = "#2D2D2D"
    
    root = tk.Tk()
    root.title("Huffman - Equipo Tr3s")
    root.geometry("1000x700") 
    root.config(bg=BG_COLOR)

    style = ttk.Style()
    style.theme_use('clam') 
    style.configure('.', background=BG_COLOR, foreground=FG_COLOR, bordercolor=FRAME_BG)
    style.configure('TFrame', background=BG_COLOR)
    style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR)
    style.configure('TLabelFrame', 
                    background=BG_COLOR, 
                    foreground=FG_COLOR, 
                    bordercolor=BUTTON_BG)
    style.configure('TLabelFrame.Label', 
                    background=BG_COLOR, 
                    foreground=FG_COLOR,
                    font=("Arial", 10, "bold"))
    style.configure('TButton', 
                    background=BUTTON_BG, 
                    foreground=FG_COLOR, 
                    bordercolor=BUTTON_BG,
                    font=("Arial", 10, "bold"))
    style.map('TButton',
        background=[('active', BUTTON_ACTIVE), ('disabled', DISABLED_BG)],
        foreground=[('disabled', DISABLED_FG)]
    )
    style.configure('TEntry', 
                    fieldbackground=ENTRY_BG, 
                    foreground=FG_COLOR, 
                    insertcolor=FG_COLOR, 
                    bordercolor=BUTTON_BG)
    style.map('TEntry',
        fieldbackground=[('disabled', DISABLED_BG)],
        foreground=[('disabled', DISABLED_FG)])

    root.grid_rowconfigure(0, weight=0)  
    root.grid_rowconfigure(1, weight=1)  
    root.grid_columnconfigure(0, weight=1) 

    image_path_var = tk.StringVar()

    frame_controls = ttk.LabelFrame(root, text="Configurar y Ejecutar")
    frame_controls.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
    frame_controls.grid_columnconfigure(0, weight=1) 
    frame_controls.grid_columnconfigure(1, weight=0) 

    frame_path = ttk.Frame(frame_controls, style='TFrame') 
    frame_path.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    ttk.Label(frame_path, text="Selecciona un archivo:").pack(side=tk.LEFT, padx=(0, 5))
    path_entry = ttk.Entry(frame_path, textvariable=image_path_var, state="readonly", width=70)
    path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    browse_button = ttk.Button(frame_path, text="Examinar")
    browse_button.pack(side=tk.LEFT, padx=(5, 0))
    
    frame_config = ttk.Frame(frame_controls, style='TFrame') 
    frame_config.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    clear_button = ttk.Button(frame_config, text="Limpiar")
    clear_button.pack(side=tk.RIGHT, padx=(0, 5))

    start_button = ttk.Button(frame_config, text="Iniciar Compresión")
    start_button.config(state="disabled") 
    start_button.pack(side=tk.RIGHT, padx=(5, 20)) 

    frame_resultados_base = ttk.Frame(root, style='TFrame')
    frame_resultados_base.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_resultados_base.grid_columnconfigure(0, weight=1) 
    frame_resultados_base.grid_columnconfigure(1, weight=1)
    frame_resultados_base.grid_rowconfigure(0, weight=1)

    frame_consola = ttk.LabelFrame(frame_resultados_base, text="Salida de Consola (Frecuencias y Códigos)")
    frame_consola.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
    
    txt_consola = scrolledtext.ScrolledText(
        frame_consola,
        wrap=tk.WORD,
        font=("Courier New", 10), 
        state=tk.DISABLED,
        background=TEXT_BG,
        foreground=FG_COLOR,
        insertbackground=FG_COLOR,
        borderwidth=0,
        highlightthickness=0
    )
    txt_consola.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    frame_comparacion = ttk.LabelFrame(frame_resultados_base, text="Resultados de Compresión")
    frame_comparacion.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

    txt_resultados = tk.Text(
        frame_comparacion,
        font=("Arial", 12, "bold"),
        state=tk.DISABLED,
        wrap=tk.WORD,
        background=TEXT_BG,
        foreground=FG_COLOR,
        insertbackground=FG_COLOR,
        borderwidth=0,
        highlightthickness=0
    )
    txt_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def clear_results_callback():
        """Lógica de 'clear_all' de Huffman.py"""
        print("Limpiando resultados...")
        update_text_widget(txt_consola, "Listo para un nuevo archivo.", append=False)
        update_text_widget(txt_resultados, "", append=False)
    
    clear_button.config(command=clear_results_callback)

    def select_image_callback():
        """Lógica de 'select_file' de Huffman.py + validación de FrontEnd.py"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo .txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path and file_path.endswith(".txt"):
            image_path_var.set(file_path)
            start_button.config(state="normal") 
            clear_results_callback() 
            update_text_widget(txt_consola, f"Archivo cargado: {os.path.basename(file_path)}", append=False)
        elif file_path:
            image_path_var.set("¡Error! Selecciona un archivo .txt")
            start_button.config(state="disabled")
        else:
            start_button.config(state="disabled")
    
    browse_button.config(command=select_image_callback)

    def start_analysis_callback():
        """
        Lógica principal de 'start_compression' de Huffman.py
        Integrada en nuestro layout de FrontEnd.py
        """
        start_button.config(state="disabled")
        clear_button.config(state="disabled")

        ruta = image_path_var.get()
        if not ruta:
            messagebox.showwarning("Error", "Selecciona un archivo .txt primero.")
            start_button.config(state="normal")
            clear_button.config(state="normal")
            return

        update_text_widget(txt_consola, "Leyendo archivo...", append=False)
        root.update_idletasks()

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                texto = f.read()
        except Exception as e:
            messagebox.showerror("Error al leer archivo", str(e))
            start_button.config(state="normal")
            clear_button.config(state="normal")
            return

        if not texto:
            messagebox.showwarning("Archivo vacío", "No hay texto para comprimir.")
            start_button.config(state="normal")
            clear_button.config(state="normal")
            return

        try:
            freqs = calcular_frecuencias(texto)
            update_text_widget(txt_consola, f"Caracteres únicos encontrados: {len(freqs)}")
            update_text_widget(txt_consola, "Construyendo árbol de Huffman...")
            root.update_idletasks()

            arbol = construir_arbol_huffman(freqs)
            
            codigos = generar_codigos_huffman(arbol)
            update_text_widget(txt_consola, "\n--- Códigos de Huffman (Ordenados por Frec.) ---")
            
            for c, code in sorted(codigos.items(), key=lambda x: freqs[x[0]], reverse=True):
                update_text_widget(txt_consola, f"  Freq: {freqs[c]:<7} | Char: {repr(c):<6} | Código: {code}")
            
            update_text_widget(txt_consola, "\n--- Proceso ---")
            root.update_idletasks()

            update_text_widget(txt_consola, "Codificando texto...")
            codificado = codificar_texto(texto, codigos)
            
            update_text_widget(txt_consola, "Decodificando para verificación...")
            decodificado = decodificar_texto(codificado, arbol)
            verificacion = 'Correcta' if decodificado == texto else 'Error'
            update_text_widget(txt_consola, f"Verificación: {verificacion}")
            
            update_text_widget(txt_consola, "Guardando archivo binario...")
            salida = guardar_comprimido(ruta, codificado)
            update_text_widget(txt_consola, f"Archivo guardado en: {os.path.basename(salida)}")
            
            tam_o = os.path.getsize(ruta)
            tam_c = os.path.getsize(salida)
            reduccion = 100 * (1 - tam_c / tam_o) if tam_o > 0 else 0

            update_text_widget(txt_resultados,
                        f"Verificación: {verificacion}\n"
                        f"------------------------\n"
                        f"Tamaño Original:   {tam_o} bytes\n"
                        f"Tamaño Comprimido: {tam_c} bytes\n\n"
                        f"¡Reducción del {reduccion:.2f}%!",
                        append=False)

        except Exception as e:
            messagebox.showerror("Error en Compresión", str(e))
            update_text_widget(txt_consola, f"\nERROR: {e}")
        
        finally:
            start_button.config(state="normal")
            clear_button.config(state="normal")

    start_button.config(command=start_analysis_callback)
    
    update_text_widget(txt_consola, "Por favor, carga un archivo .txt para comprimir.", append=False)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
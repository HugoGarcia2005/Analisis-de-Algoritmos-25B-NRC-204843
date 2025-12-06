# [Act.Codigo] Entrega con Menu Desplegable y Huffman Original
# Equipo Tr3s
# Garcia Saldivar Hugo Gabriel
# Maciel Vargas Oswaldo Daniel

from PIL import Image, ImageDraw, ImageTk
import time 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import shutil 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import heapq

PADDING = 0
OUTPUT_SCALE = 1
ERROR_THRESHOLD = 15 
GIF_DISPLAY_SIZE = (320, 320)

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char 
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequencies_original_image(image):
    """Calcula frecuencias de cada pixel (R,G,B) de la imagen original."""
    pixels = list(image.getdata())
    freqs = {}
    for p in pixels:
        freqs[p] = freqs.get(p, 0) + 1
    return freqs

def build_huffman_tree(freqs):
    priority_queue = [HuffmanNode(char, freq) for char, freq in freqs.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0] if priority_queue else None

def generate_huffman_codes(node, current_code="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is None:
        return

    if node.char is not None:
        code_map[node.char] = current_code
        return

    generate_huffman_codes(node.left, current_code + "0", code_map)
    generate_huffman_codes(node.right, current_code + "1", code_map)
    return code_map

def save_huffman_bin_simple(image, code_map, output_folder):
    """Guarda la imagen comprimida (solo los códigos) en un .bin"""
    bin_path = os.path.join(output_folder, "imagen_huffman_original.bin")
    
    pixels = list(image.getdata())
    
    bit_string = []
    for p in pixels:
        bit_string.append(code_map[p])
    full_bit_string = "".join(bit_string)
    
    extra_padding = 8 - (len(full_bit_string) % 8)
    if extra_padding == 8: extra_padding = 0
    full_bit_string += ("0" * extra_padding)
    
    byte_array = bytearray()
    for i in range(0, len(full_bit_string), 8):
        byte = full_bit_string[i:i+8]
        byte_array.append(int(byte, 2))
        
    with open(bin_path, 'wb') as f:
        f.write(byte_array)
        
    return bin_path, len(full_bit_string)

def weighted_average(hist):
    total = sum(hist)
    value, error = 0, 0
    if total > 0:
        value = sum(i * x for i, x in enumerate(hist)) / total
        error = sum(x * (value - i) ** 2 for i, x in enumerate(hist)) / total
        error = error ** 0.5
    return value, error

def color_from_histogram(hist):
    r, re = weighted_average(hist[:256])
    g, ge = weighted_average(hist[256:512])
    b, be = weighted_average(hist[512:768])
    e = re * 0.2989 + ge * 0.5870 + be * 0.1140
    return (int(r), int(g), int(b)), e

class QuadtreeNode(object):
    def __init__(self, img, box, depth):
        self.box = box
        self.depth = depth
        self.children = None
        self.leaf = False
        image = img.crop(box)
        self.width, self.height = image.size
        hist = image.histogram()
        self.color, self.error = color_from_histogram(hist)

    def is_leaf(self):
        return self.leaf

    def split(self, img):
        l, t, r, b = self.box
        lr = int(l + (r - l) / 2)
        tb = int(t + (b - t) / 2)
        tl = QuadtreeNode(img, (l, t, lr, tb), self.depth + 1)
        tr = QuadtreeNode(img, (lr, t, r, tb), self.depth + 1)
        bl = QuadtreeNode(img, (l, tb, lr, b), self.depth + 1)
        br = QuadtreeNode(img, (lr, tb, r, b), self.depth + 1)
        self.children = [tl, tr, bl, br]

class QuadtreeBase(object):
    def __init__(self, image):
        self.root = None
        self.width, self.height = image.size
        self.max_depth = 0 

    def get_leaf_nodes(self, depth):
        if depth > self.max_depth:
            depth = self.max_depth
        leaf_nodes = []
        def get_leaf_nodes_recursion(node, target_depth):
            if node.is_leaf() or node.depth == target_depth:
                leaf_nodes.append(node)
            elif node.children is not None:
                for child in node.children:
                    get_leaf_nodes_recursion(child, target_depth)
        get_leaf_nodes_recursion(self.root, depth)
        return leaf_nodes

    def _create_image_from_depth(self, depth):
        m = OUTPUT_SCALE
        dx, dy = (PADDING, PADDING)
        image = Image.new('RGB', (int(self.width * m + dx), int(self.height * m + dy)))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width * m, self.height * m), (0, 0, 0))
        leaf_nodes = self.get_leaf_nodes(depth)
        for node in leaf_nodes:
            l, t, r, b = node.box
            box = (l * m + dx, t * m + dy, r * m - 1, b * m - 1)
            draw.rectangle(box, node.color)
        return image

    def create_gif(self, base_name, gif_dir, frames_dir, duration=500, loop=0):
        folder_name = f"{base_name}_frames"
        frames_folder_path = os.path.join(frames_dir, folder_name)
        os.makedirs(frames_folder_path, exist_ok=True)
        print(f"Guardando fotogramas individuales en: '{frames_folder_path}/'")
        gif_file_path = os.path.join(gif_dir, f"{base_name}.gif")
        images = []
        end_product_image = self._create_image_from_depth(self.max_depth)
        for i in range(self.max_depth + 1):
            image = self._create_image_from_depth(i)
            images.append(image)
            try:
                frame_path = os.path.join(frames_folder_path, f"frame_{i:02d}.png")
                image.save(frame_path)
            except Exception as e:
                print(f"Advertencia: No se pudo guardar el fotograma {frame_path}. Error: {e}")
        for _ in range(3):
            images.append(end_product_image)
        print(f"Creando GIF con {len(images)} fotogramas en '{gif_file_path}'...")
        images[0].save(
            gif_file_path, 
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop)
        return gif_file_path

class QuadtreeDivideAndConquer(QuadtreeBase):
    def __init__(self, image, max_depth=10):
        super().__init__(image)
        self.root = QuadtreeNode(image, image.getbbox(), 0)
        self.max_depth = 0 
        self._build_tree_dc(image, self.root, max_depth)

    def _build_tree_dc(self, image, node, max_depth):
        if (node.depth >= max_depth) or (node.error <= ERROR_THRESHOLD):
            if node.depth > self.max_depth:
                self.max_depth = node.depth
            node.leaf = True
            return
        node.split(image)
        for child in node.children:
            self._build_tree_dc(image, child, max_depth)

class QuadtreeDynamicProgramming(QuadtreeBase):
    def __init__(self, image, max_depth=10):
        super().__init__(image)
        self.root = QuadtreeNode(image, image.getbbox(), 0)
        self._build_full_tree_dp(image, self.root, max_depth)
        self._prune_tree_dp(self.root)
        self.max_depth = 0
        self._update_max_depth(self.root)

    def _build_full_tree_dp(self, image, node, max_depth):
        if node.depth < max_depth:
            node.split(image) 
            for child in node.children:
                self._build_full_tree_dp(image, child, max_depth)
        else:
            node.leaf = True

    def _prune_tree_dp(self, node):
        if not node.children:
            return
        for child in node.children:
            self._prune_tree_dp(child)
        if (node.error <= ERROR_THRESHOLD):
            node.leaf = True
            node.children = None
        else:
            node.leaf = False
            
    def _update_max_depth(self, node):
        if node.is_leaf():
            if node.depth > self.max_depth:
                self.max_depth = node.depth
        elif node.children:
            for child in node.children:
                self._update_max_depth(child)

gif_frames_data = []
gif_animation_job = None

def get_unique_output_dir(base_dir_name):
    if not os.path.exists(base_dir_name):
        return base_dir_name
    counter = 1
    while True:
        new_dir_name = f"{base_dir_name}_{counter}"
        if not os.path.exists(new_dir_name):
            return new_dir_name
        counter += 1

def run_huffman_thread(image_path, root, start_button, clear_button):
    """Ejecuta Huffman sobre la imagen original."""
    try:
        print(f"Iniciando Técnica Voraz (Huffman) en imagen original: '{image_path}'...")
        
        OUTPUT_DIR = get_unique_output_dir('huffman_resultados')
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"Directorio de salida: {OUTPUT_DIR}")

        image = Image.open(image_path).convert('RGB')
        
        print("Calculando frecuencias de píxeles...")
        freqs = calculate_frequencies_original_image(image)
        print(f"Colores únicos encontrados: {len(freqs)}")
        
        print("Construyendo árbol de Huffman...")
        tree = build_huffman_tree(freqs)
        codes = generate_huffman_codes(tree)
        
        print("Guardando archivo comprimido...")
        bin_path, total_bits = save_huffman_bin_simple(image, codes, OUTPUT_DIR)
        
        original_bits = image.width * image.height * 24
        file_size = os.path.getsize(bin_path)
        ratio = (original_bits / 8) / file_size if file_size > 0 else 0
        
        msg = (
            f"¡Compresión Voraz Finalizada!\n\n"
            f"Guardado en:\n{OUTPUT_DIR}\n\n"
            f"Archivo: imagen_huffman_original.bin\n"
            f"Peso del archivo: {file_size/1024:.2f} KB\n"
            f"Ratio de Compresión: {ratio:.2f}x"
        )
        messagebox.showinfo("Éxito Huffman", msg)
        print("Proceso Huffman terminado.")

    except Exception as e:
        print(f"Error en Huffman: {e}")
        messagebox.showerror("Error", f"Ocurrió un error en Huffman:\n{e}")
    finally:
        root.after(0, lambda: start_button.config(state="normal"))
        root.after(0, lambda: clear_button.config(state="normal"))

def run_quadtree_thread(image_path, max_n, root, fig, ax, canvas, start_button, clear_button, gif_label):
    """
    Ejecuta el análisis comparativo de Quadtree (D&C y DP).
    Se usa para las opciones 'Divide y Vencerás' y 'Programación Dinámica'.
    """
    try:
        print(f"Iniciando Quadtree (D&C vs DP) con N={max_n}...")
        
        def pre_run_clear():
            ax.clear()
            ax.set_title("Calculando...", color="#E0E0E0")
            ax.set_facecolor("#2D2D2D")
            canvas.draw()
            gif_label.config(text="Generando GIF...")
        
        root.after(0, pre_run_clear)
        
        OUTPUT_DIR = get_unique_output_dir('quadtree_resultados')
        GIF_DIR = os.path.join(OUTPUT_DIR, 'gif')
        FRAMES_DIR = os.path.join(OUTPUT_DIR, 'frames')
        os.makedirs(GIF_DIR, exist_ok=True)
        os.makedirs(FRAMES_DIR, exist_ok=True)

        depths_n = []
        times_dc = []
        times_dp = []

        image = Image.open(image_path).convert('RGB')
        
        print("\n--- TAREA 1: Análisis de Complejidad ---")
        for n in range(1, max_n + 1):
           
            start_time_dc = time.perf_counter()
            _ = QuadtreeDivideAndConquer(image, max_depth=n)
            time_taken_dc = time.perf_counter() - start_time_dc
            
       
            start_time_dp = time.perf_counter()
            _ = QuadtreeDynamicProgramming(image, max_depth=n)
            time_taken_dp = time.perf_counter() - start_time_dp
            
            depths_n.append(n)
            times_dc.append(time_taken_dc)
            times_dp.append(time_taken_dp)
            print(f"N={n} | D&C: {time_taken_dc:.4f}s | DP: {time_taken_dp:.4f}s")

        if depths_n: 
            ax.plot(depths_n, times_dc, marker='o', linestyle='-', label='Divide y Venceras')
            ax.plot(depths_n, times_dp, marker='x', linestyle='--', label='Programacion Dinamica')
            ax.set_xlabel('n (Nivel de Profundidad)')
            ax.set_ylabel('Tiempo (s)')
            ax.set_title('Comparacion de Complejidad Temporal')
            legend = ax.legend()
            legend.get_frame().set_facecolor('#555555')
            for text in legend.get_texts(): text.set_color('#E0E0E0')
            ax.grid(True, color='#555555') 
            root.after(0, lambda: update_matplotlib_canvas(canvas))

        print("\n--- TAREA 2: Generación de GIFs ---")

        quadtree_dc = QuadtreeDivideAndConquer(image, max_depth=max_n)
        gif_path_dc = quadtree_dc.create_gif('quadtree_dc', GIF_DIR, FRAMES_DIR)
        root.after(0, lambda: load_and_play_gif(gif_label, gif_path_dc))

        quadtree_dp = QuadtreeDynamicProgramming(image, max_depth=max_n)
        quadtree_dp.create_gif('quadtree_dp', GIF_DIR, FRAMES_DIR)
        
        print(f"Proceso Quadtree completado. Resultados en: {OUTPUT_DIR}")

    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
    finally:
        root.after(0, lambda: start_button.config(state="normal"))
        root.after(0, lambda: clear_button.config(state="normal"))

def update_matplotlib_canvas(canvas):
    canvas.draw()

def load_and_play_gif(gif_label, gif_path):
    global gif_frames_data, gif_animation_job
    if gif_animation_job:
        gif_label.after_cancel(gif_animation_job)
        gif_animation_job = None  
    gif_frames_data = []
    try:
        gif = Image.open(gif_path)
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.copy()
            frame.thumbnail(GIF_DISPLAY_SIZE, Image.Resampling.LANCZOS) 
            gif_frames_data.append(ImageTk.PhotoImage(frame))
        if gif_frames_data:
            gif_label.config(text="") 
            animate_gif_frame(gif_label, 0)
    except Exception as e:
        print(f"Error al cargar GIF: {e}")

def animate_gif_frame(gif_label, frame_index):
    global gif_frames_data, gif_animation_job
    if not gif_frames_data: return
    gif_label.config(image=gif_frames_data[frame_index])
    next_index = (frame_index + 1) % len(gif_frames_data)
    gif_animation_job = gif_label.after(500, animate_gif_frame, gif_label, next_index)


def create_gui():
    root = tk.Tk()
    root.title("Compresión de Imágenes - Algoritmos")
    root.geometry("1200x800")

    BG_COLOR = "#3E3E3E"       
    FG_COLOR = "#E0E0E0"       
    FRAME_BG = "#2D2D2D"     
    BUTTON_BG = "#555555"    
    BUTTON_ACTIVE = "#666666" 
    DISABLED_BG = "#4A4A4A"   
    DISABLED_FG = "#888888"   
    ENTRY_BG = "#555555"       
    
    root.config(bg=BG_COLOR)

    style = ttk.Style()
    style.theme_use('clam') 
    style.configure('.', background=BG_COLOR, foreground=FG_COLOR, bordercolor=FRAME_BG)
    style.configure('TFrame', background=BG_COLOR)
    style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR)
    style.configure('TLabelFrame', background=BG_COLOR, foreground=FG_COLOR, bordercolor=BUTTON_BG)
    style.configure('TLabelFrame.Label', background=BG_COLOR, foreground=FG_COLOR)
    style.configure('TButton', background=BUTTON_BG, foreground=FG_COLOR, bordercolor=BUTTON_BG)
    style.map('TButton',
        background=[('active', BUTTON_ACTIVE), ('disabled', DISABLED_BG)],
        foreground=[('disabled', DISABLED_FG)]
    )
    style.configure('TEntry', fieldbackground=ENTRY_BG, foreground=FG_COLOR, insertcolor=FG_COLOR, bordercolor=BUTTON_BG)
    
    root.grid_rowconfigure(0, weight=1)  
    root.grid_rowconfigure(1, weight=10) 
    root.grid_columnconfigure(0, weight=2) 
    root.grid_columnconfigure(1, weight=2)
    root.grid_columnconfigure(2, weight=1)

    image_path_var = tk.StringVar()
    n_var = tk.IntVar(value=8) 
    algo_var = tk.StringVar() 

    frame_controls = ttk.LabelFrame(root, text="Configurar y Ejecutar")
    frame_controls.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
    frame_controls.grid_columnconfigure(0, weight=3) 
    frame_controls.grid_columnconfigure(1, weight=2) 
    

    frame_path = ttk.Frame(frame_controls, style='TFrame') 
    frame_path.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    ttk.Label(frame_path, text="Ruta:").pack(side=tk.LEFT, padx=(0, 5))
    path_entry = ttk.Entry(frame_path, textvariable=image_path_var, state="readonly", width=60)
    path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    ttk.Button(frame_path, text="Examinar...", command=lambda: image_path_var.set(filedialog.askopenfilename())).pack(side=tk.LEFT, padx=(5, 0))
    
    frame_config = ttk.Frame(frame_controls, style='TFrame') 
    frame_config.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    ttk.Label(frame_config, text="N:").pack(side=tk.LEFT, padx=(5, 0))
    ttk.Spinbox(frame_config, from_=1, to=12, textvariable=n_var, width=5).pack(side=tk.LEFT, padx=5)
    
    ttk.Label(frame_config, text="Algoritmo:").pack(side=tk.LEFT, padx=(10, 0))
    algo_combo = ttk.Combobox(frame_config, textvariable=algo_var, state="readonly", width=25)
    algo_combo['values'] = ("D&V y PD", "Técnica voraz")
    algo_combo.current(0)
    algo_combo.pack(side=tk.LEFT, padx=5)
    
    clear_button = ttk.Button(frame_config, text="Limpiar")
    clear_button.pack(side=tk.RIGHT, padx=(0, 5))
    start_button = ttk.Button(frame_config, text="Iniciar")
    start_button.pack(side=tk.RIGHT, padx=(5, 10)) 

    frame_graph = ttk.LabelFrame(root, text="Resultados: Gráfica")
    frame_graph.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    fig = plt.Figure(figsize=(5, 4), dpi=100, facecolor=BG_COLOR)
    ax = fig.add_subplot(111, facecolor=FRAME_BG)
    ax.set_title("La grafica aparecerá aquí", color=FG_COLOR)
    ax.set_xlabel("N", color=FG_COLOR)
    ax.set_ylabel("Tiempo (s)", color=FG_COLOR)
    ax.tick_params(colors=FG_COLOR)
    for spine in ax.spines.values(): spine.set_color(BUTTON_BG)
    
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.get_tk_widget().config(bg=BG_COLOR) 
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    frame_gif = ttk.LabelFrame(root, text="Resultados: GIF Generado")
    frame_gif.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
    gif_label = ttk.Label(frame_gif, text="El GIF aparecerá aquí...", anchor="center")
    gif_label.pack(fill=tk.BOTH, expand=True)

    def clear_results():
        ax.clear()
        ax.set_title("La grafica aparecerá aquí", color=FG_COLOR)
        ax.set_facecolor(FRAME_BG) 
        if ax.get_legend(): ax.get_legend().remove()
        canvas.draw()
        global gif_animation_job
        if gif_animation_job: gif_label.after_cancel(gif_animation_job)
        gif_label.config(image='', text="Esperando...")

    clear_button.config(command=clear_results)

    def start_analysis():
        img_path = image_path_var.get()
        n_val = n_var.get()
        selection = algo_var.get()

        if not img_path:
            messagebox.showwarning("Atención", "Selecciona una imagen primero.")
            return

        start_button.config(state="disabled")
        clear_button.config(state="disabled")
        
        if selection == "Técnica voraz":
            t = threading.Thread(
                target=run_huffman_thread,
                args=(img_path, root, start_button, clear_button),
                daemon=True
            )
            t.start()
        else:

            t = threading.Thread(
                target=run_quadtree_thread,
                args=(img_path, n_val, root, fig, ax, canvas, start_button, clear_button, gif_label),
                daemon=True
            )
            t.start()

    start_button.config(command=start_analysis)
    root.mainloop()

if __name__ == '__main__':
    create_gui()
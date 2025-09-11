# Hugo Gabriel Garcia Saldivar
import tkinter as tk

def saludar():
    root.config(bg="red")
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"La alma de {nombre} ha sido vendida por 5 años y 6 meses")
    
def romperContrato():
    root.config(bg="green")
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"    
    lbl.config(text=f"{nombre} rompio su contrato y escapo de cucei")

root = tk.Tk()
root.title("Bienvenido a CUCEI")
root.geometry("970x620")
root.config(bg="lightpink")

lbl = tk.Label(root, text="Ingresa tu nombre para registrarte en CUCEI")
lbl.pack(pady=10)

entrada = tk.Entry(root)
entrada.pack(pady=25)

btn = tk.Button(root, text="Aceptar", command=saludar)
btn.pack(pady=10)

btn = tk.Button(root, text="Romper contrato", command=romperContrato)
btn.pack(pady=10)

root.mainloop()


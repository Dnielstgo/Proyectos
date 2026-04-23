import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes = os.path.join(BASE_DIR, "imagenes")


def cargar_imagen(nombre):
    """Carga una imagen JPG desde la carpeta 'imagenes' y la convierte a formato Tkinter"""
    path = os.path.join(ruta_imagenes, nombre)
    img = Image.open(path)
    img = img.resize((120, 120))
    return ImageTk.PhotoImage(img)

def jugar_vs_pc(eleccion_jugador):
    global puntos_jugador, puntos_pc

    opciones = ["Piedra", "Papel", "Tijera"]
    eleccion_pc = random.choice(opciones)

    lbl_jugador.config(image=imagenes[eleccion_jugador][0])
    lbl_pc.config(image=imagenes[eleccion_pc][1])

    if eleccion_jugador == eleccion_pc:
        resultado = "¡Empate!"
    elif (eleccion_jugador == "Piedra" and eleccion_pc == "Tijera") or \
         (eleccion_jugador == "Papel" and eleccion_pc == "Piedra") or \
         (eleccion_jugador == "Tijera" and eleccion_pc == "Papel"):
        resultado = "¡Ganaste!"
        puntos_jugador += 1
    else:
        resultado = "Perdiste..."
        puntos_pc += 1

    lbl_resultado.config(text=resultado)
    actualizar_marcador()

def seleccionar_jugada_j2(eleccion):
    global eleccion_jugador1, esperando_j2, puntos_jugador, puntos_pc

    eleccion_jugador2 = eleccion

    lbl_jugador.config(image=imagenes[eleccion_jugador1][0])
    lbl_pc.config(image=imagenes[eleccion_jugador2][1])

    if eleccion_jugador1 == eleccion_jugador2:
        resultado = "¡Empate!"
    elif (eleccion_jugador1 == "Piedra" and eleccion_jugador2 == "Tijera") or \
         (eleccion_jugador1 == "Papel" and eleccion_jugador2 == "Piedra") or \
         (eleccion_jugador1 == "Tijera" and eleccion_jugador2 == "Papel"):
        resultado = "Jugador 1 gana!"
        puntos_jugador += 1
    else:
        resultado = "Jugador 2 gana!"
        puntos_pc += 1

    lbl_resultado.config(text=resultado)
    actualizar_marcador()
    esperando_j2 = False

def jugar_vs_jugador1(eleccion):
    global eleccion_jugador1, esperando_j2
    eleccion_jugador1 = eleccion
    lbl_resultado.config(text="Turno Jugador 2...")
    esperando_j2 = True

def actualizar_marcador():
    if modo.get() == 1:
        lbl_marcador.config(text=f"Jugador: {puntos_jugador}  |  PC: {puntos_pc}")
    else:
        lbl_marcador.config(text=f"Jugador 1: {puntos_jugador}  |  Jugador 2: {puntos_pc}")

def reiniciar():
    global puntos_jugador, puntos_pc
    puntos_jugador, puntos_pc = 0, 0
    lbl_jugador.config(image="")
    lbl_pc.config(image="")
    lbl_resultado.config(text="")
    actualizar_marcador()

def salir():
    ventana.destroy()


ventana = tk.Tk()
ventana.title("Piedra, Papel o Tijera")
ventana.geometry("500x550")
ventana.config(bg="lightblue")


puntos_jugador = 0
puntos_pc = 0
eleccion_jugador1 = None
esperando_j2 = False


imagenes = {
    "Piedra": [cargar_imagen("Piedra_1.jpg"), cargar_imagen("Piedra_2.jpg")],
    "Papel": [cargar_imagen("Papel_1.jpg"), cargar_imagen("Papel_2.jpg")],
    "Tijera": [cargar_imagen("Tijera_1.jpg"), cargar_imagen("Tijera_2.jpg")]
}


tk.Label(ventana, text="Jugador 1", font=("Arial", 12), bg="lightblue").pack()
lbl_jugador = tk.Label(ventana, bg="lightblue")
lbl_jugador.pack()

tk.Label(ventana, text="Oponente", font=("Arial", 12), bg="lightblue").pack()
lbl_pc = tk.Label(ventana, bg="lightblue")
lbl_pc.pack()

lbl_resultado = tk.Label(ventana, text="", font=("Arial", 14, "bold"), bg="lightblue")
lbl_resultado.pack(pady=10)

lbl_marcador = tk.Label(ventana, text="Jugador: 0  |  PC: 0", font=("Arial", 12, "bold"), bg="lightblue")
lbl_marcador.pack(pady=5)

modo = tk.IntVar(value=1)
frame_modo = tk.Frame(ventana, bg="lightblue")
frame_modo.pack(pady=10)
tk.Radiobutton(frame_modo, text="Jugador vs PC", variable=modo, value=1, bg="lightblue").grid(row=0, column=0, padx=10)
tk.Radiobutton(frame_modo, text="Jugador 1 vs Jugador 2", variable=modo, value=2, bg="lightblue").grid(row=0, column=1, padx=10)


frame_botones = tk.Frame(ventana, bg="lightblue")
frame_botones.pack(pady=10)

def accion_boton(eleccion):
    if modo.get() == 1:
        jugar_vs_pc(eleccion)
    else:
        global esperando_j2
        if not esperando_j2:
            jugar_vs_jugador1(eleccion)
        else:
            seleccionar_jugada_j2(eleccion)

tk.Button(frame_botones, text="Piedra", command=lambda: accion_boton("Piedra")).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Papel", command=lambda: accion_boton("Papel")).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Tijera", command=lambda: accion_boton("Tijera")).grid(row=0, column=2, padx=10)


frame_extra = tk.Frame(ventana, bg="lightblue")
frame_extra.pack(pady=15)

tk.Button(frame_extra, text="Reiniciar Juego", command=reiniciar, bg="orange").grid(row=0, column=0, padx=10)
tk.Button(frame_extra, text="Salir", command=salir, bg="red", fg="white").grid(row=0, column=1, padx=10)


ventana.mainloop()

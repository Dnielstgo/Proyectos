# Importar bibliotecas necesarias
import tkinter as tk
from tkinter import messagebox
import random
import os

# Lista de valores y palos posibles para las cartas
valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
palos = ['C', 'D', 'H', 'S']

# Función para crear y mezclar la baraja
def crear_baraja():
    baraja = [(valor, palo) for valor in valores for palo in palos]
    random.shuffle(baraja)
    return baraja

# Función para asignar un valor numérico a cada carta
def valor_carta(carta):
    valor = carta[0]
    if valor in ['J', 'Q', 'K']:
        return 10
    elif valor == 'A':
        return 11
    else:
        return int(valor)

# Función que calcula el total de puntos de una mano, ajustando el valor del As si es necesario
def calcular_puntos(mano):
    puntos = sum(valor_carta(carta) for carta in mano)
    ases = sum(1 for carta in mano if carta[0] == 'A')
    while puntos > 21 and ases:
        puntos -= 10
        ases -= 1
    return puntos

# Clase principal para manejar la interfaz gráfica y la lógica del juego
class BlackjackGUI:
    def __init__(self, root):
        # Configura la ventana principal
        self.root = root
        self.root.title("Blackjack Visual")
        self.root.configure(bg='#006400')
        self.root.geometry("1280x720+100+50")
        self.root.resizable(False, False)

        self.mostrar_inicio = True
        self.pantalla_inicio()  # Muestra la pantalla inicial

    # Pantalla inicial del juego
    def pantalla_inicio(self):
        self.frame_inicio = tk.Frame(self.root, bg='#006400')
        self.frame_inicio.pack(expand=True, fill=tk.BOTH)

        # Título del juego
        titulo = tk.Label(self.frame_inicio, text="BlackJack", font=("Georgia", 100, "bold"), bg='#006400', fg='white')
        titulo.pack(expand=True)

        # Autores
        autores = tk.Label(self.frame_inicio, text="Created by Daniela Gallo & María José Viviescas", font=("Georgia", 20), bg='#006400', fg='white')
        autores.pack()

        # Botón para comenzar el juego
        boton_comenzar = tk.Button(self.frame_inicio, text="Comenzar", font=("Georgia", 18), bg='#006400', fg='black', command=self.iniciar_juego)
        boton_comenzar.pack(pady=50)

    # Inicia una nueva partida
    def iniciar_juego(self):
        if self.mostrar_inicio:
            self.frame_inicio.destroy()
            self.mostrar_inicio = False

        # Variables de control
        self.cartas_pedidas = 0
        self.doble_valor_carta = 0

        # Crear frames para mostrar las cartas de la casa y del jugador
        self.frame_casa = tk.Frame(self.root, bg='#006400')
        self.frame_casa.pack(pady=30)
        self.frame_jugador = tk.Frame(self.root, bg='#006400')
        self.frame_jugador.pack(pady=30)

        # Etiqueta para mostrar los puntos
        self.label_puntos = tk.Label(self.root, text="", font=("Georgia", 16), bg='#006400', fg='white')
        self.label_puntos.pack(pady=10)

        # Botones de juego
        self.frame_botones = tk.Frame(self.root, bg='#006400')
        self.frame_botones.pack(pady=20)

        self.boton_pedir = tk.Button(self.frame_botones, text="Pedir carta", font=("Futura", 20), bg='white', fg='black', width=15, command=self.pedir_carta)
        self.boton_pedir.grid(row=0, column=0, padx=20)

        self.boton_plantarse = tk.Button(self.frame_botones, text="Plantarse", font=("Futura", 20), bg='white', fg='black', width=15, command=self.turno_casa)
        self.boton_plantarse.grid(row=0, column=1, padx=20)

        self.reiniciar_manos()  # Baraja cartas y reparte

    # Carga una imagen de carta desde la carpeta "cartas"
    def cargar_imagen(self, carta):
        nombre = carta[0] + carta[1] + "@1x.png"
        ruta = os.path.join("cartas", nombre)
        try:
            return tk.PhotoImage(file=ruta).subsample(3, 3)
        except:
            return None

    # Muestra una mano de cartas en pantalla
    def mostrar_mano(self, frame, mano, ocultar_primera=False):
        for widget in frame.winfo_children():
            widget.destroy()
        for i, carta in enumerate(mano):
            if i == 0 and ocultar_primera:
                img = tk.PhotoImage(file=os.path.join("cartas", "reverso.png")).subsample(3, 3)
            else:
                img = self.cargar_imagen(carta)
            if img:
                label = tk.Label(frame, image=img, bg='#006400')
                label.image = img
                label.pack(side=tk.LEFT, padx=5)

    # Actualiza los puntos en la interfaz
    def actualizar_puntos(self):
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        puntos_c = "??" if self.carta_oculta else calcular_puntos(self.mano_casa)
        self.label_puntos.config(text=f"Puntos jugador: {puntos_j} | Puntos casa: {puntos_c}")

    # Lógica al pedir una carta
    def pedir_carta(self):
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        if puntos_j >= 21:
            return

        self.cartas_pedidas += 1
        usar_doble = False

        # Activar efecto de carta doble en la tercera carta
        if self.cartas_pedidas == 3:
            if messagebox.askyesno("Efecto", "La siguiente carta valdrá el doble. ¿Deseas continuar?"):
                usar_doble = True
            else:
                self.cartas_pedidas -= 1
                return

        carta = self.baraja.pop()
        self.mano_jugador.append(carta)

        # Aplica el valor doble a la carta recién sacada
        if usar_doble:
            self.doble_valor_carta = 1 if carta[0] == 'A' else valor_carta(carta)
        else:
            self.doble_valor_carta = 0

        self.mostrar_mano(self.frame_jugador, self.mano_jugador)
        self.actualizar_puntos()

        puntos_j_final = calcular_puntos(self.mano_jugador) + self.doble_valor_carta

        # Permitir eliminar una carta solo tras la primera carta pedida
        if self.cartas_pedidas == 1 and puntos_j_final < 21:
            self.root.after(300, self.ventana_eliminar_carta)

        # Verifica si el jugador llega a 21 o se pasa
        if puntos_j_final == 21:
            messagebox.showinfo("Blackjack", "¡Tienes 21! Te plantas automáticamente.")
            self.deshabilitar_botones()
            self.root.after(500, self.turno_casa)
        elif puntos_j_final > 21:
            self.root.after(700, self.mostrar_resultado)

    # Ventana emergente para eliminar una carta
    def ventana_eliminar_carta(self):
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        if puntos_j >= 21:
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar carta")
        ventana.configure(bg='#004400')
        ventana.geometry("400x300")
        ventana.transient(self.root)
        ventana.grab_set()

        # Centrar la ventana
        ventana.update_idletasks()
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana.winfo_screenheight() // 2) - (h // 2)
        ventana.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(ventana, text="¿Cuál carta deseas eliminar?", font=("Georgia", 12), bg='#004400', fg='white').pack(pady=10)

        for i, carta in enumerate(self.mano_jugador):
            txt = f"{carta[0]}{carta[1]}"
            tk.Button(ventana, text=txt, command=lambda i=i: self.eliminar_y_cerrar(i, ventana), width=10).pack(pady=5)

    # Elimina una carta seleccionada por el jugador
    def eliminar_y_cerrar(self, indice, ventana):
        eliminada = self.mano_jugador.pop(indice)
        messagebox.showinfo("Carta eliminada", f"Has eliminado: {eliminada[0]}{eliminada[1]}")
        ventana.destroy()
        self.mostrar_mano(self.frame_jugador, self.mano_jugador)
        self.actualizar_puntos()

    # Inicia el turno de la casa
    def turno_casa(self):
        self.carta_oculta = False
        self.mostrar_mano(self.frame_casa, self.mano_casa)
        self.actualizar_puntos()
        self.root.after(1000, self.continuar_turno_casa)

    # Lógica del turno de la casa
    def continuar_turno_casa(self):
        if calcular_puntos(self.mano_casa) == 21:
            messagebox.showinfo("Blackjack", "La casa tiene 21.")
            self.mostrar_resultado()
            return

        while calcular_puntos(self.mano_casa) < 17:
            carta = self.baraja.pop()
            self.mano_casa.append(carta)
            self.mostrar_mano(self.frame_casa, self.mano_casa)
            self.actualizar_puntos()
            self.root.update()
            self.root.after(700)

        self.mostrar_resultado()

    # Muestra el resultado final de la partida
    def mostrar_resultado(self):
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        puntos_c = calcular_puntos(self.mano_casa)

        if puntos_j > 21:
            resultado = "¡Te pasaste! Pierdes."
        elif puntos_c > 21:
            resultado = "¡La casa se pasó! Ganaste."
        elif puntos_j > puntos_c:
            resultado = "¡Ganaste!"
        elif puntos_j < puntos_c:
            resultado = "La casa gana."
        else:
            resultado = "Empate."

        # Limpia la interfaz y muestra el mensaje final
        for widget in self.root.winfo_children():
            widget.destroy()

        resultado_frame = tk.Frame(self.root, bg='#006400')
        resultado_frame.pack(expand=True, fill=tk.BOTH)

        mensaje_final = tk.Label(resultado_frame, text=resultado, font=("Georgia", 60), bg='#006400', fg='white')
        mensaje_final.pack(expand=True)

        boton_reiniciar = tk.Button(resultado_frame, text="Volver a jugar", font=("Georgia", 20), bg='white', command=self.reiniciar)
        boton_reiniciar.pack(pady=20)

    # Desactiva los botones cuando el jugador se planta
    def deshabilitar_botones(self):
        self.boton_pedir.config(state=tk.DISABLED)
        self.boton_plantarse.config(state=tk.DISABLED)

    # Inicializa las manos de jugador y casa
    def reiniciar_manos(self):
        self.baraja = crear_baraja()
        self.mano_jugador = [self.baraja.pop(), self.baraja.pop()]
        self.mano_casa = [self.baraja.pop(), self.baraja.pop()]
        self.carta_oculta = True
        self.cartas_pedidas = 0
        self.doble_valor_carta = 0

        self.mostrar_mano(self.frame_jugador, self.mano_jugador)
        self.mostrar_mano(self.frame_casa, self.mano_casa, ocultar_primera=True)
        self.actualizar_puntos()

        if calcular_puntos(self.mano_jugador) == 21:
            messagebox.showinfo("Blackjack", "¡Blackjack! Te plantas automáticamente.")
            self.deshabilitar_botones()
            self.root.after(800, self.turno_casa)

    # Reinicia todo el juego
    def reiniciar(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.iniciar_juego()

# Ejecutar aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()

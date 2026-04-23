import tkinter as tk
from tkinter import messagebox
import random
import os
from datetime import datetime

# Card values and suits
valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
palos = ['C', 'D', 'H', 'S']

def crear_baraja():
    """Create and shuffle a deck of cards"""
    baraja = [(valor, palo) for valor in valores for palo in palos]
    random.shuffle(baraja)
    return baraja

def valor_carta(carta):
    """Get the numerical value of a card"""
    valor = carta[0]
    if valor in ['J', 'Q', 'K']:
        return 10
    elif valor == 'A':
        return 11
    else:
        return int(valor)

def calcular_puntos(mano):
    """Calculate the total points of a hand, adjusting for Aces"""
    puntos = sum(valor_carta(carta) for carta in mano)
    ases = sum(1 for carta in mano if carta[0] == 'A')
    while puntos > 21 and ases:
        puntos -= 10
        ases -= 1
    return puntos

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Visual")
        self.root.configure(bg='#006400')  # Dark green background
        self.root.geometry("1280x720+100+50")
        self.root.resizable(False, False)
        
        # Game state variables
        self.mostrar_inicio = True
        self.dinero_jugador = 1000
        self.dinero_apostado = 0
        self.estadisticas = {
            'partidas_jugadas': 0,
            'victorias': 0,
            'derrotas': 0,
            'empates': 0,
            'blackjacks': 0,
            'mayor_ganancia': 0,
            'fecha_ultima_partida': None
        }
        self.pantalla_inicio()

    def pantalla_inicio(self):
        """Show the start screen"""
        self.clear_screen()
        
        self.frame_inicio = tk.Frame(self.root, bg='#006400')
        self.frame_inicio.pack(expand=True, fill=tk.BOTH)

        # Game title
        titulo = tk.Label(self.frame_inicio, text="BlackJack", 
                         font=("Georgia", 100, "bold"), bg='#006400', fg='gold')
        titulo.pack(expand=True)

        # Authors
        autores = tk.Label(self.frame_inicio, 
                          text="Created by Daniela Gallo & María José Viviescas", 
                          font=("Georgia", 20), bg='#006400', fg='white')
        autores.pack()

        # Start button
        boton_comenzar = tk.Button(self.frame_inicio, text="Comenzar", 
                                  font=("Georgia", 18), bg='gold', fg='black', 
                                  command=self.iniciar_juego)
        boton_comenzar.pack(pady=20)

        # Stats button
        boton_estadisticas = tk.Button(self.frame_inicio, text="Ver Estadísticas", 
                                      font=("Georgia", 14), bg='white', fg='black', 
                                      command=self.mostrar_estadisticas)
        boton_estadisticas.pack(pady=10)

    def mostrar_estadisticas(self):
        """Show game statistics"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Estadísticas del Juego")
        ventana.geometry("600x500")
        ventana.configure(bg='white')
        
        # Center the window
        ventana.update_idletasks()
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana.winfo_screenheight() // 2) - (h // 2)
        ventana.geometry(f"{w}x{h}+{x}+{y}")

        # Title
        tk.Label(ventana, text="Estadísticas de Blackjack", 
                font=("Georgia", 20, "bold"), bg='white', fg='black').pack(pady=10)

        # Stats frame
        frame_stats = tk.Frame(ventana, bg='white')
        frame_stats.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Stats labels - now with black text
        stats_text = [
            f"Partidas jugadas: {self.estadisticas['partidas_jugadas']}",
            f"Victorias: {self.estadisticas['victorias']}",
            f"Derrotas: {self.estadisticas['derrotas']}",
            f"Empates: {self.estadisticas['empates']}",
            f"Blackjacks conseguidos: {self.estadisticas['blackjacks']}",
            f"Mayor ganancia en una partida: ${self.estadisticas['mayor_ganancia']}",
            f"Última partida: {self.estadisticas['fecha_ultima_partida'] or 'No hay datos'}"
        ]

        for stat in stats_text:
            tk.Label(frame_stats, text=stat, font=("Georgia", 14), 
                    bg='white', fg='black', anchor='w').pack(fill=tk.X, pady=5)

        # Close button
        tk.Button(ventana, text="Cerrar", font=("Georgia", 14), 
                 bg='#006400', fg='white', command=ventana.destroy).pack(pady=20)

    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def iniciar_juego(self):
        """Start a new game"""
        self.clear_screen()
        self.mostrar_inicio = False
        
        # Initialize game state
        self.cartas_pedidas = 0
        self.doble_valor_carta = 0
        self.carta_oculta = True
        
        # Create frames for cards
        self.frame_casa = tk.Frame(self.root, bg='#006400')
        self.frame_casa.pack(pady=20)
        
        self.frame_jugador = tk.Frame(self.root, bg='#006400')
        self.frame_jugador.pack(pady=20)

        # Points display - now with black text on light background
        self.frame_puntos = tk.Frame(self.root, bg='#D2B48C')  # Tan background
        self.frame_puntos.pack(pady=10, fill=tk.X, padx=50)
        
        self.label_puntos = tk.Label(self.frame_puntos, text="", 
                                   font=("Georgia", 16), bg='#D2B48C', fg='black')
        self.label_puntos.pack()

        # Money display - same style as points
        self.frame_dinero = tk.Frame(self.root, bg='#D2B48C')
        self.frame_dinero.pack(pady=10, fill=tk.X, padx=50)
        
        self.label_dinero = tk.Label(self.frame_dinero, 
                                   text=f"Dinero disponible: ${self.dinero_jugador}", 
                                   font=("Georgia", 16), bg='#D2B48C', fg='black')
        self.label_dinero.pack()

        # Buttons frame
        self.frame_botones = tk.Frame(self.root, bg='#006400')
        self.frame_botones.pack(pady=20)

        # Game buttons with improved styling
        self.boton_pedir = tk.Button(self.frame_botones, text="Pedir carta", 
                                    font=("Futura", 20), bg='white', fg='black', 
                                    width=15, command=self.pedir_carta)
        self.boton_pedir.grid(row=0, column=0, padx=20, pady=10)

        self.boton_plantarse = tk.Button(self.frame_botones, text="Plantarse", 
                                       font=("Futura", 20), bg='white', fg='black', 
                                       width=15, command=self.turno_casa)
        self.boton_plantarse.grid(row=0, column=1, padx=20, pady=10)

        self.boton_apostar = tk.Button(self.frame_botones, text="Apostar", 
                                      font=("Futura", 20), bg='gold', fg='black', 
                                      width=15, command=self.ventana_apostar)
        self.boton_apostar.grid(row=1, column=0, padx=20, pady=10)

        self.boton_estadisticas = tk.Button(self.frame_botones, text="Estadísticas", 
                                           font=("Futura", 20), bg='#D2B48C', fg='black', 
                                           width=15, command=self.mostrar_estadisticas)
        self.boton_estadisticas.grid(row=1, column=1, padx=20, pady=10)

        # Initialize hands
        self.reiniciar_manos()

    def ventana_apostar(self):
        """Show betting window"""
        if self.dinero_jugador <= 0:
            messagebox.showinfo("Sin dinero", "No tienes suficiente dinero para apostar.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Apostar")
        ventana.geometry("400x300")
        ventana.configure(bg='#D2B48C')  # Tan background
        
        # Center the window
        ventana.update_idletasks()
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana.winfo_screenheight() // 2) - (h // 2)
        ventana.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(ventana, text="¿Cuánto deseas apostar?", 
                font=("Georgia", 16), bg='#D2B48C', fg='black').pack(pady=10)

        self.entrada_apuesta = tk.Entry(ventana, font=("Georgia", 16))
        self.entrada_apuesta.pack(pady=10)

        tk.Button(ventana, text="Confirmar apuesta", font=("Georgia", 16), 
                 bg='#006400', fg='white', command=lambda: self.confirmar_apuesta(ventana)).pack(pady=20)

    def confirmar_apuesta(self, ventana):
        """Confirm the bet amount"""
        try:
            apuesta = int(self.entrada_apuesta.get())
        except ValueError:
            messagebox.showinfo("Error", "Por favor, ingresa una cantidad válida.")
            return

        if apuesta <= 0:
            messagebox.showinfo("Error", "La apuesta debe ser mayor que cero.")
            return
        elif apuesta > self.dinero_jugador:
            messagebox.showinfo("Error", "No tienes suficiente dinero para esa apuesta.")
            return

        self.dinero_apostado = apuesta
        self.dinero_jugador -= apuesta
        self.label_dinero.config(text=f"Dinero disponible: ${self.dinero_jugador}")
        ventana.destroy()
        self.actualizar_puntos()

    def cargar_imagen(self, carta):
        """Load card image from the 'cartas' folder"""
        nombre = carta[0] + carta[1] + "@1x.png"
        ruta = os.path.join("cartas", nombre)
        try:
            return tk.PhotoImage(file=ruta).subsample(3, 3)
        except:
            return None

    def mostrar_mano(self, frame, mano, ocultar_primera=False):
        """Display a hand of cards"""
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

    def actualizar_puntos(self):
        """Update the points display"""
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        puntos_c = "??" if self.carta_oculta else calcular_puntos(self.mano_casa)
        self.label_puntos.config(text=f"Puntos jugador: {puntos_j} | Puntos casa: {puntos_c}")

    def pedir_carta(self):
        """Player draws a card"""
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        if puntos_j >= 21:
            return

        self.cartas_pedidas += 1
        usar_doble = False

        # Double value effect on third card
        if self.cartas_pedidas == 3:
            if messagebox.askyesno("Efecto", "La siguiente carta valdrá el doble. ¿Deseas continuar?"):
                usar_doble = True
            else:
                self.cartas_pedidas -= 1
                return

        carta = self.baraja.pop()
        self.mano_jugador.append(carta)

        # Apply double value if activated
        if usar_doble:
            self.doble_valor_carta = valor_carta(carta)  # Full double value now
        else:
            self.doble_valor_carta = 0

        self.mostrar_mano(self.frame_jugador, self.mano_jugador)
        self.actualizar_puntos()

        puntos_j_final = calcular_puntos(self.mano_jugador) + self.doble_valor_carta

        # Allow card removal after first card is drawn
        if self.cartas_pedidas == 1 and puntos_j_final < 21:
            self.root.after(300, self.ventana_eliminar_carta)

        # Check for blackjack or bust
        if puntos_j_final == 21:
            self.estadisticas['blackjacks'] += 1
            messagebox.showinfo("Blackjack", "¡Tienes 21! Te plantas automáticamente.")
            self.deshabilitar_botones()
            self.root.after(500, self.turno_casa)
        elif puntos_j_final > 21:
            self.root.after(700, self.mostrar_resultado)

    def ventana_eliminar_carta(self):
        """Show card removal window"""
        if calcular_puntos(self.mano_jugador) + self.doble_valor_carta >= 21:
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar carta")
        ventana.configure(bg='#D2B48C')  # Tan background
        ventana.geometry("400x300")
        ventana.transient(self.root)
        ventana.grab_set()

        # Center the window
        ventana.update_idletasks()
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana.winfo_screenheight() // 2) - (h // 2)
        ventana.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(ventana, text="¿Cuál carta deseas eliminar?", 
                font=("Georgia", 12), bg='#D2B48C', fg='black').pack(pady=10)

        for i, carta in enumerate(self.mano_jugador):
            txt = f"{carta[0]}{carta[1]}"
            tk.Button(ventana, text=txt, bg='white', fg='black',
                     command=lambda i=i: self.eliminar_y_cerrar(i, ventana), 
                     width=10).pack(pady=5)

    def eliminar_y_cerrar(self, indice, ventana):
        """Remove selected card and close window"""
        eliminada = self.mano_jugador.pop(indice)
        messagebox.showinfo("Carta eliminada", f"Has eliminado: {eliminada[0]}{eliminada[1]}")
        ventana.destroy()
        self.mostrar_mano(self.frame_jugador, self.mano_jugador)
        self.actualizar_puntos()

    def turno_casa(self):
        """Dealer's turn"""
        self.carta_oculta = False
        self.mostrar_mano(self.frame_casa, self.mano_casa)
        self.actualizar_puntos()
        self.deshabilitar_botones()
        self.root.after(1000, self.continuar_turno_casa)

    def continuar_turno_casa(self):
        """Dealer draws cards according to rules"""
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

    def mostrar_resultado(self):
        """Show game result and handle winnings"""
        puntos_j = calcular_puntos(self.mano_jugador) + self.doble_valor_carta
        puntos_c = calcular_puntos(self.mano_casa)
        
        # Update game stats
        self.estadisticas['partidas_jugadas'] += 1
        self.estadisticas['fecha_ultima_partida'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if puntos_j > 21:
            resultado = "¡Te pasaste! Pierdes."
            self.estadisticas['derrotas'] += 1
        elif puntos_c > 21:
            resultado = "¡La casa se pasó! Ganaste."
            self.dinero_jugador += self.dinero_apostado * 2
            self.estadisticas['victorias'] += 1
            if self.dinero_apostado * 2 > self.estadisticas['mayor_ganancia']:
                self.estadisticas['mayor_ganancia'] = self.dinero_apostado * 2
        elif puntos_j > puntos_c:
            resultado = "¡Ganaste!"
            self.dinero_jugador += self.dinero_apostado * 2
            self.estadisticas['victorias'] += 1
            if self.dinero_apostado * 2 > self.estadisticas['mayor_ganancia']:
                self.estadisticas['mayor_ganancia'] = self.dinero_apostado * 2
        elif puntos_j < puntos_c:
            resultado = "La casa gana."
            self.estadisticas['derrotas'] += 1
        else:
            resultado = "Empate."
            self.dinero_jugador += self.dinero_apostado  # Return bet on tie
            self.estadisticas['empates'] += 1

        # Show result screen
        self.clear_screen()
        
        resultado_frame = tk.Frame(self.root, bg='#D2B48C')  # Tan background
        resultado_frame.pack(expand=True, fill=tk.BOTH)

        mensaje_final = tk.Label(resultado_frame, text=resultado, 
                               font=("Georgia", 60), bg='#D2B48C', fg='black')
        mensaje_final.pack(expand=True)

        # Stats for this round
        frame_stats_ronda = tk.Frame(resultado_frame, bg='#D2B48C')
        frame_stats_ronda.pack(pady=10)
        
        tk.Label(frame_stats_ronda, 
                text=f"Tus puntos: {puntos_j} | Puntos casa: {puntos_c}", 
                font=("Georgia", 16), bg='#D2B48C', fg='black').pack()
                
        tk.Label(frame_stats_ronda, 
                text=f"Apuesta: ${self.dinero_apostado} | Dinero actual: ${self.dinero_jugador}", 
                font=("Georgia", 16), bg='#D2B48C', fg='black').pack()

        # Buttons frame
        frame_botones_resultado = tk.Frame(resultado_frame, bg='#D2B48C')
        frame_botones_resultado.pack(pady=20)

        # Play again button
        tk.Button(frame_botones_resultado, text="Volver a jugar", font=("Georgia", 20), 
                bg='#006400', fg='white', command=self.iniciar_juego).pack(side=tk.LEFT, padx=10)
                
        # Stats button
        tk.Button(frame_botones_resultado, text="Ver Estadísticas", font=("Georgia", 20), 
                bg='gold', fg='black', command=self.mostrar_estadisticas).pack(side=tk.LEFT, padx=10)
                
        # Return to main menu button
        tk.Button(frame_botones_resultado, text="Menú principal", font=("Georgia", 20), 
                bg='white', fg='black', command=self.pantalla_inicio).pack(side=tk.LEFT, padx=10)

    def deshabilitar_botones(self):
        """Disable game buttons"""
        self.boton_pedir.config(state=tk.DISABLED)
        self.boton_plantarse.config(state=tk.DISABLED)
        self.boton_apostar.config(state=tk.DISABLED)

    def habilitar_botones(self):
        """Enable game buttons"""
        self.boton_pedir.config(state=tk.NORMAL)
        self.boton_plantarse.config(state=tk.NORMAL)
        self.boton_apostar.config(state=tk.NORMAL)

    def reiniciar_manos(self):
        """Reset hands for a new round"""
        self.baraja = crear_baraja()
        self.mano_jugador = [self.baraja.pop(), self.baraja.pop()]
        self.mano_casa = [self.baraja.pop(), self.baraja.pop()]
        self.carta_oculta = True
        self.cartas_pedidas = 0
        self.doble_valor_carta = 0

        self.mostrar_mano(self.frame_jugador, self.mano_jugador)
        self.mostrar_mano(self.frame_casa, self.mano_casa, ocultar_primera=True)
        self.actualizar_puntos()
        self.habilitar_botones()

        # Check for immediate blackjack
        if calcular_puntos(self.mano_jugador) == 21:
            self.estadisticas['blackjacks'] += 1
            messagebox.showinfo("Blackjack", "¡Blackjack! Ganaste automáticamente.")
            self.dinero_jugador += self.dinero_apostado * 2
            if self.dinero_apostado * 2 > self.estadisticas['mayor_ganancia']:
                self.estadisticas['mayor_ganancia'] = self.dinero_apostado * 2
            self.mostrar_resultado()

if __name__ == "__main__":
    root = tk.Tk()
    juego = BlackjackGUI(root)
    root.mainloop()
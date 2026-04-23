import random


#Los valores de las cartas se definen mezclando todos los palos y numeros
def crear_baraja():
    palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    baraja = [(valor, palo) for valor in valores for palo in palos]
    random.shuffle(baraja)
    return baraja


#Retorna el valor de cada carta
def valor_carta(carta):
    valor = carta[0]
    if valor in ['J', 'Q', 'K']:
        return 10
    elif valor == 'A':
        return 11
    else:
        return int(valor)

#Se define que pasa en el dado caso de que haya algun cambio con la carta del As
#Se suman los puntos que se obtienen hasta el momdento
def calcular_puntos(mano):
    puntos = sum(valor_carta(carta) for carta in mano)
    ases = sum(1 for carta in mano if carta[0] == 'A')
    while puntos > 21 and ases:
        puntos -= 10
        ases -= 1
    return puntos

#Arroja los puntos que se obtienen en cada ronda del jugador
def mostrar_mano(mano):
    print(mano)
    print(f"Puntos actuales: {calcular_puntos(mano)}")

#Arroja las cartas del jugador teniendo en cuenta las cartas especiales con nuevas modalidades
def jugar_blackjack():
    baraja = crear_baraja()
    mano_jugador = [baraja.pop(), baraja.pop()]
    mano_casa = [baraja.pop(), baraja.pop()]

    carta_doble_valor = False
    carta_magica_usada = False

    print("\n" + "-" * 40)
    print("Tu mano:")
    mostrar_mano(mano_jugador)

    print("\n" + "-" * 40)
    print("Mano de la casa:")
    print("[??]", mano_casa[1])

    # Turno del jugador
    while True:
        print("\n" + "-" * 40)
        puntos = calcular_puntos(mano_jugador)
        if puntos > 21:
            print("¡Te pasaste de 21! Pierdes.")
            return

#Opcion de solicitar otra carta para seguir sumando puntos
        decision = input("¿Deseas otra carta? (s/n): ").lower()
        if decision == 's':
            carta_nueva = baraja.pop()
            print(f"Recibiste {carta_nueva}")
            mano_jugador.append(carta_nueva)
            print("Tu mano actualizada:")
            mostrar_mano(mano_jugador)
        else:
            print("Te plantas.")
            break

    # Turno de la casa
    print("\n" + "-" * 40)
    print("Turno de la casa:")
    mostrar_mano(mano_casa)
    while calcular_puntos(mano_casa) < 17:
        carta = baraja.pop()
        mano_casa.append(carta)
        print(f"La casa toma: {carta}")
        mostrar_mano(mano_casa)

    puntos_jugador = calcular_puntos(mano_jugador)
    puntos_casa = calcular_puntos(mano_casa)

#Resultados finales tanto de la casa como del jugador
    print("\n" + "-" * 40)
    print("Resultados finales:")
    print(f"Tus puntos: {puntos_jugador}")
    print(f"Puntos de la casa: {puntos_casa}")

    if puntos_casa > 21 or puntos_jugador > puntos_casa:
        print("¡Ganaste!")
    elif puntos_jugador < puntos_casa:
        print("La casa gana.")
    else:
        print("Empate.")

# Bucle para repetir el juego
while True:
    jugar_blackjack()
    print("\n" + "=" * 40)
    otra = input("¿Quieres jugar otra vez? (s/n): ").lower()
    if otra != 's':
        print("¡Gracias por jugar!")
        break

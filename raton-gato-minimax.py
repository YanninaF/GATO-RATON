import time # funcion time sleep : pausar ejecucion x 1seg logrando que sea mas facil de seguir visualemnte
import random # para determinar pos y mov aleaotorio

# Tamaño del tablero
tamano = 5  # definimos el tamano del tablero / matriz 5*5

# Definición del tablero
tablero = [["." for _ in range(tamano)] for _ in range(tamano)] #aqui tablero es el nom de la var q contiene la matriz /tamano es la variable
#que define el tamañó

# Definición de las posiciones iniciales
gato_pos = (0, random.randint(0, tamano - 1))  # El gato se coloca en una posición aleatoria en la fila superior
raton_pos = (tamano - 1, tamano - 1)

# Funciones para mover el gato y el ratón
def mover(pos, direccion):
    x, y = pos
    if direccion == "arriba" and x > 0: #asegura que nos movamos fuera del borde superior del. tab
        x -= 1 # si ambas condiciones son verdaderas decrementar x en 1 mov hacia arriba 
    elif direccion == "abajo" and x < tamano - 1:
        x += 1
    elif direccion == "izquierda" and y > 0:
        y -= 1
    elif direccion == "derecha" and y < tamano - 1:
        y += 1
    return (x, y) #devu nuev pos

# Función para obtener movimientos posibles (evitar moverse fuera del tablero)
def movimientos_posibles(pos): 
    x, y = pos
    movimientos = []
    if x > 0: movimientos.append("arriba")
    if x < tamano - 1: movimientos.append("abajo")
    if y > 0: movimientos.append("izquierda")
    if y < tamano - 1: movimientos.append("derecha")
    return movimientos

# Función para determinar si el juego ha terminado
def juego_terminado(gato_pos, raton_pos):
    return gato_pos == raton_pos

# Función para evaluar el estado del juego
def evaluar_estado(gato_pos, raton_pos):
    if gato_pos == raton_pos:
        return float('-inf')  # El gato atrapa al ratón, máxima penalización para el gato
    else:
        # Distancia Manhattan entre el gato y el ratón
        return abs(gato_pos[0] - raton_pos[0]) + abs(gato_pos[1] - raton_pos[1])

# Algoritmo Minimax
def minimax(gato_pos, raton_pos, profundidad, maximizando):
    if juego_terminado(gato_pos, raton_pos) or profundidad == 0:
        return evaluar_estado(gato_pos, raton_pos)

    if maximizando:  #raton
        max_eval = float('-inf')  #Inicializa max_eval con el valor más bajo posible (-inf).
        for movimiento in movimientos_posibles(raton_pos):
            nueva_pos = mover(raton_pos, movimiento)
            evaluacion = minimax(gato_pos, nueva_pos, profundidad - 1, False)
            max_eval = max(max_eval, evaluacion)  #retorna el max valor
        return max_eval
    else:
        min_eval = float('inf') #Inicializa min_eval con el valor más alto posible (inf).
        for movimiento in movimientos_posibles(gato_pos):
            nueva_pos = mover(gato_pos, movimiento)
            evaluacion = minimax(nueva_pos, raton_pos, profundidad - 1, True)
            min_eval = min(min_eval, evaluacion) #retorna el min valor
            
        return min_eval

# Función para obtener el mejor movimiento usando Minimax
def mejor_movimiento(pos, profundidad, maximizando, es_raton):
    mejor_mov = None
    if maximizando:
        mejor_eval = float('-inf')
        for movimiento in movimientos_posibles(pos):
            nueva_pos = mover(pos, movimiento)
            if es_raton:
                evaluacion = minimax(gato_pos, nueva_pos, profundidad - 1, False)
            else:
                evaluacion = minimax(nueva_pos, raton_pos, profundidad - 1, False)
            if evaluacion > mejor_eval:
                mejor_eval = evaluacion
                mejor_mov = movimiento
    else:
        mejor_eval = float('inf')
        for movimiento in movimientos_posibles(pos):
            nueva_pos = mover(pos, movimiento)
            if es_raton:
                evaluacion = minimax(gato_pos, nueva_pos, profundidad - 1, True)
            else:
                evaluacion = minimax(nueva_pos, raton_pos, profundidad - 1, True)
            if evaluacion < mejor_eval:
                mejor_eval = evaluacion
                mejor_mov = movimiento
    return mejor_mov

# Función para imprimir el tablero de una manera legible
def imprimir_tablero(tablero, gato_pos, raton_pos):
    for x in range(tamano):
        for y in range(tamano):
            if (x, y) == gato_pos:
                print("G", end=" ")
            elif (x, y) == raton_pos:
                print("R", end=" ")
            else:
                print(tablero[x][y], end=" ")
        print()

# Actualizamos el tablero y mostramos
def actualizar_tablero(tablero, gato_pos, raton_pos):
    for x in range(tamano):
        for y in range(tamano):
            tablero[x][y] = "."

    x, y = gato_pos
    tablero[x][y] = "G"

    x, y = raton_pos
    tablero[x][y] = "R"

    imprimir_tablero(tablero, gato_pos, raton_pos)

# Función principal para probar el juego
def jugar(tablero, gato_pos, raton_pos, profundidad, turno_limite):
    raton_turno = True  # Empezamos con el turno del ratón
    turnos = 0  # Contador de turnos

    while not juego_terminado(gato_pos, raton_pos):
        print(f"Gato: {gato_pos}, Ratón: {raton_pos}")

        if raton_turno:
            # Movimiento aleatorio del ratón
            movimientos_aleatorios = movimientos_posibles(raton_pos)
            mov_raton = random.choice(movimientos_aleatorios)
            raton_pos = mover(raton_pos, mov_raton)
            print(f"El ratón se mueve {mov_raton} a {raton_pos}")
            actualizar_tablero(tablero, gato_pos, raton_pos)
        else:
            # Movimiento del gato
            mov_gato = mejor_movimiento(gato_pos, profundidad, False, False)
            gato_pos = mover(gato_pos, mov_gato)
            print(f"El gato se mueve {mov_gato} a {gato_pos}")
            actualizar_tablero(tablero, gato_pos, raton_pos)

        # Esperar 1 segundo antes del siguiente movimiento
        time.sleep(1)

        if juego_terminado(gato_pos, raton_pos):
            print(f"El gato atrapó al ratón en {gato_pos}!")
            break

        # Incrementar el contador de turnos y verificar si se ha alcanzado el límite
        turnos += 1
        if turnos >= turno_limite:
            print("El ratón ha escapado!")
            break

        # Cambiar el turno
        raton_turno = not raton_turno

    print("Juego terminado.")

# Ejecutar el juego con un límite de turnos
turno_limite = 20  # Definimos el límite de turnos
jugar(tablero, gato_pos, raton_pos, 3, turno_limite)


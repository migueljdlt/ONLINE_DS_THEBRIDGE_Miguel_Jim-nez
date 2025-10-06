import numpy as np
import random

def crear_tablero(lado=10):
    tablero=np.full((10,10), " ")
    return tablero
def tipos_de_barco(eslora):
    barcos = {2: "Destructor", 3: "Submarino", 4: "Acorazado"}
    if eslora in barcos:
        return f"{barcos[eslora]} (eslora{eslora})"
    else:
        return f"Ese barco no es militar, aconsejamos su retirada"
def colocar_barco(eslora, tablero):
    tablero_temp = tablero.copy() 
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]
    colocado= False
    intentos=100    
    while not colocado and intentos >0:
        intentos -= 1
        posicion=random.choice(("horizontal", "vertical"))
        if posicion == "horizontal":
            fila= random.randint(0,num_max_filas-1)
            columna=random.randint(0, num_max_columnas - eslora)
            barco=[]
            for i in range(eslora):
                barco.append((fila, columna + i))
        else: #en vertical
            fila=random.randint(0, num_max_filas - eslora)
            columna = random.randint(0, num_max_columnas -1)
            barco=[]
            for i in range(eslora):
                barco.append((fila + i, columna))        
        posicion_valida= True
        for pieza in barco:
            fila, columna = pieza              
            if tablero_temp[pieza] == "O":
                posicion_valida = False 
                break        
        if posicion_valida:
            for pieza in barco:
                tablero_temp[pieza]= "O"
            colocado= True
            return tablero_temp    
    if not colocado:
        print("Posición no válida")
        return False
def crear_flota(tablero):
    tablero_actual= tablero 
    for i in range(3):
        destructor = colocar_barco(2, tablero_actual)
        if destructor is False:
            print("Posición peligrosa para el destructor")
            return None
        else:
            tablero_actual = destructor
    for i in range(2):
        submarino = colocar_barco(3, tablero_actual)
        if submarino is False:
            print("Posición peligrosa para el submarino")
            return None
        else:
            tablero_actual = submarino
    acorazado = colocar_barco(4, tablero_actual)
    if acorazado is False:
        print("Posición peligrosa para el acorazado")
        return None
    else:
        tablero_actual= acorazado
    
    return tablero_actual
tablero_jugador_oculto=crear_flota(crear_tablero(10))
tablero_pc_oculto=crear_flota(crear_tablero(10))
tablero_jugador = tablero_jugador_oculto.copy()
tablero_pc= crear_tablero(10)
def disparar (tablero, coordenada):
    fila, columna = coordenada 
    if tablero[fila, columna]== "O":
        return f"Tocado"
    elif tablero[fila, columna]== "X":
        return f"Inteligencia militar son antónimos"
    elif tablero[fila, columna]== " ":
        return f"Agua"
    elif tablero[fila, columna]== "-":
        return f"Pobres peces"
    else:
        return "Agua"
victoria_jugador= False
victoria_pc= False
while not victoria_jugador and not victoria_pc:
    print("Tu turno")
    print("Tablero")
    print(tablero_jugador)
    print("¿Dónde deseas disparar?")
    fila=int(input("Fila (0-9): "))
    columna= int(input("Columna (0-9): "))
    resultado= disparar(tablero_pc_oculto, (fila, columna))
    print(resultado)
    f"Resultado: {resultado}"  
    if resultado == "Tocado":
        tablero_pc[fila,columna] = "X"
        tablero_pc_oculto[fila, columna] = "X"
    else:
        tablero_pc[fila, columna]= "-"    
    victoria_jugador = not np.any(tablero_pc_oculto == "O")    
    if victoria_jugador:
        break    
    if not victoria_jugador:
        print("Turno de la máquina")
        fila= random.randint(0,9)
        columna=random.randint(0,9)
        resultado_pc= disparar(tablero_jugador_oculto, (fila,columna))
        f' "PC dispara a  ({fila}, {columna})'
        f'Resultado: {resultado_pc}'
        if resultado_pc == "Tocado":
            tablero_jugador[fila,columna] = "X"
            tablero_jugador_oculto[fila, columna] = "X"
        else:
            tablero_jugador[fila, columna]= "-"
        victoria_pc = not np.any(tablero_jugador_oculto == "O")
        print("Tu tablero después del ataque:")
        print(tablero_jugador)
if victoria_jugador:
    print("YOU WIN")
else:
    print("PC WINS")

print("Tablero final enemigo:")
print(tablero_pc_oculto)
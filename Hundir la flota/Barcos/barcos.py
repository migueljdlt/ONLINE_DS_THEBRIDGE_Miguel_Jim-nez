import numpy as np
import random

def tipos_de_barco(eslora):
    barcos = {2: "Destructor", 3: "Submarino", 4: "Acorazado"}
    if eslora in barcos:
        return f'{barcos[eslora]} (eslora{eslora})'
    else:
        return "Ese barco no es militar, aconsejamos su retirada"
def tipos_de_barco(eslora):
    barcos = {2: "Destructor", 3: "Submarino", 4: "Acorazado"}
    if eslora in barcos:
        return "{barcos[eslora]} (eslora{eslora})"
    else:
        return "Ese barco no es militar, aconsejamos su retirada"ç
def colocar_barco(eslora, tablero):
    tablero_temp = tablero.copy() 
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]
    posicion=random.choice(["horizontal", "vertical"])
    colocado= False
    intentos=100    
    while not colocado and intentos >0:
        intentos -= 1
        if posicion == "horizontal":
            fila= random.randint(0,num_max_filas-1)
            columna=random.randint(0, num_max_columnas - eslora)
            barco=[]
            for i in range(eslora):
                barco.append((fila, columna + i))
        else:
            fila=random.randint(0, num_max_filas - eslora)
            columna = random.randint(0, num_max_columnas -1)
            barco=[]
            for i in range(eslora):
                barco.append((fila + i, columna))        
        posicion_valida= True
        for pieza in barco:
            fila, columna = pieza            
            if (fila < 0 or fila >= num_max_filas or 
                columna < 0 or columna >= num_max_columnas):
                posicion_valida = False
                break                
            if tablero_temp[fila, columna] == "O":
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
        resultado = colocar_barco(2, tablero_actual)
        if resultado is False:
            print("Posición peligrosa para el destructor")
            return None
        else:
            tablero_actual = resultado
    for i in range(2):
        resultado = colocar_barco(3, tablero_actual)
        if resultado is False:
            print("Posición peligrosa para el submarino")
            return None
        else:
            tablero_actual = resultado
    resultado = colocar_barco(4, tablero_actual)
    if resultado is False:
        print("Posición peligrosa para el acorazado")
        return None
    else:
        tablero_actual= resultado
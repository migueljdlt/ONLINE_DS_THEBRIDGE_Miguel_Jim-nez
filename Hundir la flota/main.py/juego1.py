while not victoria_jugador and not victoria_pc:
    print("Tu turno")
    print("Tablero")
    print(tablero_jugador)
    print("¿Dónde deseas disparar?")
    fila=int(input("Fila (0-9): "))
    columna= int(input("Columna (0-9): "))
    resultado= disparar(tablero_pc_oculto, (fila, columna))
    print("Resultado: {resultado}")    
    if resultado == "Tocado":
        tablero_pc[fila,columna] = "X"
        tablero_pc_oculto[fila, columna] = "X"
    else:
        tablero_pc[fila, columna]= "-"    
    print("Tablero PC:")
    print(tablero_pc)
    victoria_jugador = not np.any(tablero_pc_oculto == "O")    
    if victoria_jugador:
        break    
    if not victoria_jugador:
        print("Turno de la máquina")
        fila= random.randint(0,9)
        columna=random.randint(0,9)
        resultado_pc= disparar(tablero_jugador_oculto, (fila,columna))
        print("PC dispara a ({fila}, {columna})")
        print("Resultado: "{resultado_pc})
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
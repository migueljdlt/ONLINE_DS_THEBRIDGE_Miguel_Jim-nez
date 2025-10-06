def disparar (tablero, coordenada):
    fila, columna = coordenada 
    if tablero[fila, columna]== "O":
        return "Tocado"
    elif tablero[fila, columna]== "X":
        return "Inteligencia militar son antónimos"
    elif tablero[fila, columna]== " ":
        return "Agua"
    elif tablero[fila, columna]== "-":
        return "Pobres peces"
    else:
        return "Agua"
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

ratio = os.getenv("RATIO")
sensibilidad = os.getenv("SENSIBILIDAD")
r_menor = os.getenv("R_MENOR")
r_mayor = os.getenv("R_MAYOR")

def obtener_dosis(glicemia, carbos):
    fila = glicemia // sensibilidad -1
    columna = carbos // ratio

    if fila == 0:
        dosis = columna
    elif columna == 0:
        if glicemia < 250:
            dosis = 0
        else:
            dosis = fila - 2
    else:
        dosis = fila + columna - 1

    return int(dosis)

if __name__ == "__main__":
    dosis = obtener_dosis(220, 0)


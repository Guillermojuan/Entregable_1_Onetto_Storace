from funciones import iniciar_juego
from readerDeDatos import df, generador_preguntas


# Funcion Recursiva
def correr_juego():
    puntaje_final = iniciar_juego(5, generador_preguntas(df))
    print(f"Su puntaje final es: {puntaje_final}")
    respuesta = input("¿Quieres volver a jugar? (s/n): ").strip().lower()
    #si es distinto de 's' liquida
    if respuesta == 's':
        correr_juego()
    else:
        print("Gracias por jugar.")

if __name__ == '__main__':
    correr_juego()
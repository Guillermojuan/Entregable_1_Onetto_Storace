from funciones import iniciar_juego
from readerDeDatos import df, generador_preguntas
from monadas import temporizador

def correr_juego():
    puntaje_final = iniciar_juego(5, generador_preguntas(df))
    print(f"Su puntaje final es: {puntaje_final}")
    
    respuesta = temporizador(5, input, "¿Queres volver a jugar? (s/n): ")
    
    if respuesta.is_right() and respuesta.value == 's':
        correr_juego()
    elif respuesta.is_left() and respuesta.value == "Timeout":
        print("Demoraste mas de 5 seg. Si querias volver a jugar se mas rapido.")
    else:
        print("Gracias por jugar.")
from typing import List, Generator
from functools import wraps
from readerDeDatos import df, generador_preguntas

# Decorador
def numeradorPregunta(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        numero_pregunta = kwargs.get('numero_pregunta', 1)  # Obtener el número de pregunta o usar 1 por defecto
        print(f"Respondiendo pregunta {numero_pregunta}:")
        return func(*args, **kwargs)
    return wrapper

# Funcion Lambda
verificar_respuesta = lambda entrada: entrada in ['1', '2', '3']

# Llamo al decorador para numerar las preguntas
@numeradorPregunta
def jugar(pregunta_info: dict, numero_pregunta: int = 1) -> bool:
    print(f"Pregunta: {pregunta_info['pregunta']}")
    for i, opcion in enumerate(pregunta_info['opciones'], 1):
        print(f"{i}. {opcion}")
    
    # Validar la respuesta ingresada con lambda function
    while True:
        respuesta_usuario = input("Seleccione la opción correcta (1, 2 o 3): ")
        if verificar_respuesta(respuesta_usuario):
            break
        print("Entrada inválida. Por favor, ingrese 1, 2 o 3.")
    
    if (pregunta_info['opciones'][int(respuesta_usuario) - 1] == pregunta_info['respuesta_correcta']):
        print("¡Respuesta correcta!\n")
        return True
    else:
        print(f"Respuesta incorrecta. La respuesta correcta era: {pregunta_info['respuesta_correcta']}\n")
        


def iniciar_juego(n: int, generador: Generator[dict, None, None]) -> int:
    puntaje_total = 0
    for i in range(1, n + 1):
        pregunta_info = next(generador)
        if jugar(pregunta_info, numero_pregunta=i):  # Pasar el número de la pregunta
            puntaje_total += 10
        print(f"Puntaje actual: {puntaje_total}\n")
    
    return puntaje_total
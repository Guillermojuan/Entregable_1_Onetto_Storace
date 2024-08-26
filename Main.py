import pandas as pd
import random
import itertools
from typing import List, Generator

df = pd.read_csv('Entregable_1_Onetto_Storace\JEOPARDY_CSV.csv', encoding='latin1')

#El juego debe sortear 5 preguntas al azar de las 20 posibles, mostrarle al usuario cada pregunta con sus opciones, 
#y si el usuario acierta suma 10 puntos. Al finalizar, el juego le informa al usuario su puntaje.

def generador_preguntas(df: pd.DataFrame) -> Generator[dict, None, None]:
    while True:
        preguntas_seleccionadas = df.sample(n=5)
        for index, row in preguntas_seleccionadas.iterrows():
            yield {
                'pregunta': row['Question'],
                'respuesta_correcta': row['Answer'],
                'opciones': obtener_opciones(df, row['Answer'])
            }

# Obtener opciones para una pregunta dada
def obtener_opciones(df: pd.DataFrame, respuesta_correcta: str) -> List[str]:
    respuestas_incorrectas = df[df['Answer'] != respuesta_correcta]['Answer'].sample(n=2).tolist()
    opciones = list(itertools.chain([respuesta_correcta], respuestas_incorrectas))
    random.shuffle(opciones)
    return opciones

# Decorador para manejar puntaje
def manejar_puntaje(func):
    puntaje = 0
    def wrapper(*args, **kwargs):
        nonlocal puntaje
        es_correcto = func(*args, **kwargs)
        if es_correcto:
            puntaje += 10
        return puntaje
    return wrapper

# Verificador de respuestas válidas
def verificar_respuesta() -> int:
    while True:
        respuesta_usuario = input("Seleccione la opción correcta (1, 2 o 3): ")
        if respuesta_usuario in ['1', '2', '3']:
            return int(respuesta_usuario) - 1  # Restamos 1 para adaptarlo a los índices (0, 1, 2)
        else:
            print("Entrada inválida. Por favor, ingrese 1, 2 o 3.")

# Función principal del juego
@manejar_puntaje
def jugar(pregunta_info: dict) -> bool:
    print(f"Pregunta: {pregunta_info['pregunta']}")
    for i, opcion in enumerate(pregunta_info['opciones'], 1):
        print(f"{i}. {opcion}")
    
    # Verificamos que la entrada sea válida (1, 2 o 3)
    respuesta_usuario = verificar_respuesta()
    
    return pregunta_info['opciones'][respuesta_usuario] == pregunta_info['respuesta_correcta']

# Recursión para continuar el juego
def iniciar_juego(n: int, generador: Generator[dict, None, None]):
    if n == 0:
        return
    pregunta_info = next(generador)
    puntaje_actual = jugar(pregunta_info)
    print(f"Puntaje: {puntaje_actual}\n")
    iniciar_juego(n - 1, generador)

# Iniciar el juego con 5 preguntas
iniciar_juego(5, generador_preguntas(df))

import random
import pandas as pd
from typing import List, Generator
from itertools import chain

df = pd.read_csv('JEOPARDY_CSV.csv', encoding='latin1') #Poner el relative path del archivo csv

def obtener_opciones(df: pd.DataFrame, respuesta_correcta: str) -> List[str]:
    # Obtener las respuestas incorrectas, sin incluir la respuesta correcta
    respuestas_incorrectas = [respuesta for respuesta in df['Answer'].dropna().sample(n=min(2, len(df['Answer']))) if respuesta != respuesta_correcta]

    # Si no hay suficientes respuestas incorrectas, rellena con respuestas aleatorias
    while len(respuestas_incorrectas) < 2:
        respuestas_incorrectas.append(df['Answer'].sample(1).values[0])

    opciones = list(chain([respuesta_correcta], respuestas_incorrectas))  # Concatenar las respuestas correctas e incorrectas
    random.shuffle(opciones)  # Mezclar las opciones
    return opciones



# Generador
def generador_preguntas(df: pd.DataFrame) -> Generator[dict, None, None]:
    n_preguntas = min(5, len(df))  # Selecciona el número de preguntas disponibles si hay menos de 5
    preguntas_seleccionadas = df.sample(n=n_preguntas)
    
    for _, row in preguntas_seleccionadas.iterrows():
        yield {
            'pregunta': row['Question'],
            'respuesta_correcta': row['Answer'],
            'opciones': obtener_opciones(df, row['Answer'])
        }

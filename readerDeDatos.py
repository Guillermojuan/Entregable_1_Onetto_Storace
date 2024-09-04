import random
import pandas as pd
from typing import List, Generator
from itertools import chain

df = pd.read_csv('JEOPARDY_CSV.csv', encoding='latin1') #Poner el relative path del archivo csv

def obtener_opciones(df: pd.DataFrame, respuesta_correcta: str) -> List[str]:
    respuestas_incorrectas = [respuesta for respuesta in df['Answer'].sample(n=2) if respuesta != respuesta_correcta]
    opciones = list(chain([respuesta_correcta], respuestas_incorrectas)) # Uso de chain para concatenar las listas
    random.shuffle(opciones) # Mezclar las opciones y no siempre caiga la respuesta en el mismo lugar
    return opciones

# Generador
def generador_preguntas(df: pd.DataFrame) -> Generator[dict, None, None]:
    preguntas_seleccionadas = df.sample(n=5)
    for _, row in preguntas_seleccionadas.iterrows():
        yield {
            'pregunta': row['Question'],
            'respuesta_correcta': row['Answer'],
            'opciones': obtener_opciones(df, row['Answer'])
        }

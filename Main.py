import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import pandas as pd
import random
from typing import List, Generator


# PARTE IMPORTANTE PARA CORRER EL PROGRAMA, ES IMPORTANTE QUE EN LA LINEA 23 SE COLOQUE LA RUTA DEL ARCHIVO CSV, EN LA , EN LA LINEA 149 Y 168 LA IMAGEN QUE DICE TRIVIA FOTO

# Puntaje final
puntaje_final = 0

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Leo el CSV con la librería pandas y creamos un DataFrame con la información del archivo
df = pd.read_csv('JEOPARDY_CSV.csv', encoding='latin1') # Importante poner la ruta del archivo correcta

# Generador de preguntas aleatorias
def generador_preguntas(df: pd.DataFrame) -> Generator[dict, None, None]:
    preguntas_seleccionadas = df.sample(n=5)
    for _, row in preguntas_seleccionadas.iterrows():
        yield {
            'pregunta': row['Question'],
            'respuesta_correcta': row['Answer'],
            'opciones': obtener_opciones(df, row['Answer'])
        }

# Función para obtener opciones de respuesta, incluyendo la correcta y algunas incorrectas
def obtener_opciones(df: pd.DataFrame, respuesta_correcta: str) -> List[str]:
    respuestas_incorrectas = [respuesta for respuesta in df['Answer'].sample(n=2) if respuesta != respuesta_correcta]
    opciones = [respuesta_correcta] + respuestas_incorrectas
    random.shuffle(opciones)
    return opciones

# Decorador para manejar el puntaje globalmente
def manejar_puntaje(func):
    def wrapper(*args, **kwargs):
        global puntaje_final
        es_correcto = func(*args, **kwargs)
        if es_correcto:
            puntaje_final += 10
        return es_correcto
    return wrapper

# Función principal del juego, decorada para sumar el puntaje
@manejar_puntaje
def verificar_respuesta(opcion_seleccionada, respuesta_correcta):
    es_correcto = opcion_seleccionada == respuesta_correcta
    mostrar_resultado(es_correcto, respuesta_correcta)
    return es_correcto

# Función para configurar y mostrar la pregunta actual
def jugar(pregunta_info: dict):
    label_pregunta.config(text=pregunta_info['pregunta'])
    for i, boton in enumerate(botones_opciones):
        boton.config(text=pregunta_info['opciones'][i], 
                     command=lambda op=pregunta_info['opciones'][i]: verificar_respuesta(op, pregunta_info['respuesta_correcta']))

# Ventana personalizada para mostrar el resultado de cada pregunta
def mostrar_resultado(es_correcto, respuesta_correcta):
    ventana_resultado = Toplevel(ventana)
    ventana_resultado.title("Resultado")
    centrar_ventana(ventana_resultado, 500, 250)  # Centrar el Toplevel

    ventana_resultado.configure(bg="#2F2F2F")

    # Label de resultado
    texto_resultado = "¡Correcto!" if es_correcto else f"Incorrecto. La respuesta correcta era: {respuesta_correcta}"
    label_resultado = tk.Label(ventana_resultado, text=texto_resultado, font=("Arial", 18), bg="#2F2F2F", fg="white", wraplength=450)
    label_resultado.pack(pady=20)

    # Botón para continuar a la siguiente pregunta
    boton_continuar = tk.Button(ventana_resultado, text="Continuar", font=("Arial", 14), bg="white", command=lambda: cerrar_ventana(ventana_resultado))
    boton_continuar.pack(pady=10)

def cerrar_ventana(ventana_resultado):
    ventana_resultado.destroy()
    try:
        pregunta_info = next(generador)
        jugar(pregunta_info)
    except StopIteration:
        ventana_fin_juego()

# Función para reiniciar el juego
def reiniciar_juego():
    global puntaje_final, generador
    puntaje_final = 0
    generador = generador_preguntas(df)
    iniciar_juego(5, generador)

# Ventana personalizada al finalizar el juego
def ventana_fin_juego():
    ventana_final = Toplevel(ventana)
    ventana_final.title("Fin del Juego")
    centrar_ventana(ventana_final, 500, 250)  # Centrar el Toplevel

    ventana_final.configure(bg="#2F2F2F")

    # Label de felicitación
    label_felicidades = tk.Label(ventana_final, text="¡Ha finalizado el juego!", font=("Arial", 24), bg="#2F2F2F", fg="white")
    label_felicidades.pack(pady=20)

    # Label para mostrar el puntaje final
    label_puntaje = tk.Label(ventana_final, text=f"Su puntaje final es: {puntaje_final} / 50", font=("Arial", 18), bg="#2F2F2F", fg="white")
    label_puntaje.pack(pady=10)

    # Botón para volver a jugar
    boton_reiniciar = tk.Button(ventana_final, text="Volver a Jugar", font=("Arial", 14), bg="white", command=lambda: (ventana_final.destroy(), reiniciar_juego()))
    boton_reiniciar.pack(side=tk.RIGHT, padx=20, pady=20)

    # Botón para cerrar el juego
    boton_cerrar = tk.Button(ventana_final, text="Cerrar", font=("Arial", 14), bg="white", command=ventana.quit)
    boton_cerrar.pack(side=tk.LEFT, padx=20, pady=20)

# Función recursiva que inicia el juego y maneja las rondas
def iniciar_juego(n: int, generador: Generator[dict, None, None]):
    # Ocultar pantalla de inicio
    pantalla_inicio.pack_forget()

    # Mostrar el juego
    frame.pack(expand=True, fill="both")
    
    try:
        pregunta_info = next(generador)
        jugar(pregunta_info)
    except StopIteration:
        ventana_fin_juego()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Juego de Trivia")
ventana.geometry("800x600")
ventana.minsize(800, 600)
centrar_ventana(ventana, 800, 600)  # Centrar la ventana principal

# Inicializar el puntaje final
puntaje_final = 0

# Crear un frame para la pantalla de inicio con el fondo gris oscuro
pantalla_inicio = tk.Frame(ventana, bg="#2F2F2F")
pantalla_inicio.pack(expand=True, fill="both")

# Cargar la imagen de fondo para la pantalla de inicio
imagen_fondo_inicio = Image.open("trivia foto 1.jpg")
imagen_fondo_inicio = ImageTk.PhotoImage(imagen_fondo_inicio)

# Crear un label para mostrar la imagen de fondo en la pantalla de inicio
label_fondo_inicio = tk.Label(pantalla_inicio, image=imagen_fondo_inicio, bg="#2F2F2F")
label_fondo_inicio.place(relwidth=1, relheight=1)

# Crear un label para mostrar el mensaje de bienvenida
label_bienvenida = tk.Label(pantalla_inicio, text="¡Bienvenido a Trivia Mundi!", font=("Arial", 24), bg="#2F2F2F", fg="white")
label_bienvenida.place(relx=0.5, rely=0.4, anchor="center")

# Crear un botón "Jugar" en la pantalla de inicio con fondo blanco
boton_jugar = tk.Button(pantalla_inicio, text="Jugar", font=("Arial", 24), bg="white", command=lambda: iniciar_juego(5, generador))
boton_jugar.place(relx=0.5, rely=0.5, anchor="center")

# Crear un frame para contener todos los widgets del juego con el fondo gris oscuro
frame = tk.Frame(ventana, bg="#2F2F2F")

# Cargar la imagen de fondo para el juego
imagen_fondo = Image.open("trivia foto 1.jpg")
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

# Crear un label para mostrar la imagen de fondo en el juego
label_fondo = tk.Label(frame, image=imagen_fondo, bg="#2F2F2F")
label_fondo.place(relwidth=1, relheight=1)

# Crear un label para mostrar la pregunta con fondo transparente
label_pregunta = tk.Label(frame, text="", font=("Arial", 18), bg="#2F2F2F", fg="white", wraplength=750)
label_pregunta.place(relx=0.5, rely=0.1, anchor="center")

# Crear botones para las opciones
botones_opciones = []
for i in range(3):
    boton = tk.Button(frame, font=("Arial", 14), bg="white", relief="raised")
    boton.place(relx=0.5, rely=0.45 + (i * 0.12), anchor="center", relwidth=0.6, relheight=0.1)
    botones_opciones.append(boton)

# Iniciar el generador de preguntas
generador = generador_preguntas(df)

ventana.mainloop()

from decorador import numeradorPregunta
from funciones import verificar_respuesta, jugar, iniciar_juego
from monadas import temporizador, Right, Left
import pandas as pd
from readerDeDatos import obtener_opciones, generador_preguntas
from recursividad import correr_juego


#Test para el decorador numeradorPregunta
def test_numerador_pregunta(capsys):
    # Creo una función de prueba que use el decorador numeradorPregunta
    @numeradorPregunta
    def mock_function(numero_pregunta):
        return f"Pregunta número {numero_pregunta}"

    #Llamo a la función decorada
    resultado = mock_function(numero_pregunta=3)

    #Capturo la salida de la función
    captured = capsys.readouterr()

    #Verifico que la salida incluyera la numeración correcta
    assert "Respondiendo pregunta 3" in captured.out
    assert resultado == "Pregunta número 3"


#Tests para las funciones
def test_verificar_respuesta():
    #Verifico que la respuesta válida sea aceptada
    assert verificar_respuesta('1') == True
    #Verifico que una respuesta inválida sea rechazada
    assert verificar_respuesta('4') == False

def test_jugar_correcto(monkeypatch):
    #Creo una pregunta de prueba
    pregunta = {
        'pregunta': '¿Cuál es la capital de Francia?',
        'opciones': ['París', 'Londres', 'Madrid'],
        'respuesta_correcta': 'París'
    }

    #Simulo la entrada del usuario, en este caso, seleccionando la opción correcta
    monkeypatch.setattr('builtins.input', lambda _: '1')
    
    #Verifico que la respuesta es correcta
    resultado = jugar(pregunta, numero_pregunta=1)
    assert resultado == True

def test_jugar_incorrecto(monkeypatch):
    #Creo una pregunta de prueba
    pregunta = {
        'pregunta': '¿Cuál es la capital de Francia?',
        'opciones': ['París', 'Londres', 'Madrid'],
        'respuesta_correcta': 'París'
    }

    #Simulo la entrada incorrecta del usuario
    monkeypatch.setattr('builtins.input', lambda _: '2')
    
    #Verifico que la respuesta es incorrecta
    resultado = jugar(pregunta, numero_pregunta=1)
    assert resultado == False

def test_iniciar_juego(monkeypatch):
    #Simulo varias entradas del usuario para varias preguntas
    inputs = iter(['1', '2', '3', '1', '1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    #Creo una pregunta de prueba
    pregunta = {
        'pregunta': '¿Cuál es la capital de Francia?',
        'opciones': ['París', 'Londres', 'Madrid'],
        'respuesta_correcta': 'París'
    }

    #Creo un generador de preguntas
    generador = iter([pregunta, pregunta, pregunta, pregunta, pregunta])
    
    #Simulo el juego completo y verifico que el puntaje es el esperado (30 puntos)
    resultado = iniciar_juego(5, generador)
    assert resultado == 30  # Simula 3 respuestas incorrectas y 2 correctas


# Tests para monadas
def test_either_right():
    #Test para el monad Right, verifico que la instancia sea correcta
    right_value = Right(10)
    assert right_value.is_right()
    assert not right_value.is_left()
    assert right_value.value == 10

def test_either_left():
    #Test para el monad Left, verifico que la instancia sea correcta
    left_value = Left("error")
    assert left_value.is_left()
    assert not left_value.is_right()
    assert left_value.value == "error"

def test_either_bind_right():
    #Verifico el comportamiento de bind cuando se aplica sobre un valor Right
    right_value = Right(10)
    result = right_value.bind(lambda x: Right(x + 5))
    assert result.value == 15

def test_either_bind_left():
    #Verifico que bind no afecta a un valor Left
    left_value = Left("error")
    result = left_value.bind(lambda x: Right(x + 5))
    assert result.value == "error"

def test_temporizador_exito():
    #Test para el temporizador cuando la función termina exitosamente
    def funcion_exitosa():
        return "éxito"
    
    resultado = temporizador(1, funcion_exitosa)
    assert resultado.is_right()
    assert resultado.value == "éxito"

def test_temporizador_timeout():
    #Test para el temporizador cuando la función excede el tiempo límite
    def funcion_lenta():
        import time
        time.sleep(2)
        return "éxito"

    resultado = temporizador(1, funcion_lenta)
    assert resultado.is_left()
    assert resultado.value == "Timeout"


#Tests para readerdedatos
def test_obtener_opciones():
    #Creo un DataFrame con respuestas de prueba
    df = pd.DataFrame({'Answer': ['París', 'Londres', 'Madrid']})
    respuesta_correcta = 'París'
    
    #Verifico que las opciones devueltas incluyan la respuesta correcta y 3 opciones en total
    opciones = obtener_opciones(df, respuesta_correcta)
    assert respuesta_correcta in opciones
    assert len(opciones) == 3

def test_generador_preguntas():
    #Creo un DataFrame de prueba con preguntas y respuestas
    df = pd.DataFrame({
        'Question': ['¿Cuál es la capital de Francia?'],
        'Answer': ['París']
    })

    #Genero preguntas y verifico que la pregunta y las opciones son correctas
    generador = generador_preguntas(df)
    pregunta = next(generador)
    assert pregunta['pregunta'] == '¿Cuál es la capital de Francia?'
    assert pregunta['respuesta_correcta'] == 'París'
    assert len(pregunta['opciones']) == 3  #Asegurar que se devuelvan 3 opciones


# Tests para recursividad
def test_correr_juego(monkeypatch):
    #Simulo el flujo del juego con respuestas correctas y luego una opción de no volver a jugar
    inputs = iter(['1', '1', '1', '1', '1', 'n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    #Verifico que el juego corre sin errores
    correr_juego()

def test_correr_juego_termina_con_timeout(monkeypatch):
    #Simulo el juego pero con timeout en la respuesta final
    inputs = iter(['1', '1', '1', '1', '1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    #Verifico que el juego corre correctamente aunque termine por timeout
    correr_juego()


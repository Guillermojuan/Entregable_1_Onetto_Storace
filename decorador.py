from functools import wraps

# Decorador
def numeradorPregunta(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        numero_pregunta = kwargs.get('numero_pregunta', 1)  # Obtener el número de pregunta o usar 1 por defecto
        print(f"Respondiendo pregunta {numero_pregunta}:")
        return func(*args, **kwargs)
    return wrapper

import threading

def temporizador(timeout, func, *args, **kwargs):
    result = []

    def target():
        try:
            result.append(Right(func(*args, **kwargs)))
        except Exception as e:
            result.append(Left(e))

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return Left("Timeout")
    return result[0] if result else Left("Error")

class Either:
    def __init__(self, value):
        self.value = value

    def is_left(self):
        return isinstance(self, Left)

    def is_right(self):
        return isinstance(self, Right)

    def bind(self, func):
        if self.is_left():
            return self
        return func(self.value)

    def map(self, func):
        if self.is_left():
            return self
        return Right(func(self.value))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

class Left(Either):
    pass

class Right(Either):
    pass
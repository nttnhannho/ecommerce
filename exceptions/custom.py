class CustomException(Exception):
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f'{self._message}'


CustomInternalServerErrors = (
    SyntaxError,
    IndentationError,
    NameError,
    IndexError,
    TypeError,
    ImportError,
    ValueError,
    AttributeError,
    KeyError,
    ZeroDivisionError,
    IOError,
    OSError,
)

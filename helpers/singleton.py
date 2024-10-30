from threading import Lock


class SingletonMeta(type):
    __instances = {}
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[cls] = instance
        return cls.__instances[cls]

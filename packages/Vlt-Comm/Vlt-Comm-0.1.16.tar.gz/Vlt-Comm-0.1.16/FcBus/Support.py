

class NoDataException(Exception):
    def __init__(self, value):
        self.value = value


class ErrorDataException(Exception):
    def __init__(self, value):
        self.value = value


class CommandError(Exception):
    def __init__(self, value):
        self.value = value


class UnsupportPara(Exception):
    def __init__(self, value):
        self.value = value


class UnconfigedException(Exception):
    def __init__(self, value):
        self.value = value
        
        
class TimeOutException(Exception):
    def __init__(self, value):
        self.value = value
        
        
def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
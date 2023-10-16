


class ValuesNotFound(Exception):
    def __init__(self, message) -> None:
        self.message = message


    def __str__(self) -> str:
        return f"{self.message}"
    

class IPError(Exception):
    def __str__(self) -> str:
        return "IP с которого вы пытаететь авторизоваться не добавлен в список разрешенных IP адресов."
    
class Error(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.message = message
        self.code = code
        
    def __str__(self) -> str:
        return f"{self.message} (Код ошибки: {self.code})"
    



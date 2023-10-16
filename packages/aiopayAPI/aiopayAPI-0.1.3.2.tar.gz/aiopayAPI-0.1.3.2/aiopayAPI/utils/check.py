from ..exceptions import ValuesNotFound, Error

class Checker:
    def __init__(self, **params: dict | None) -> None:
        self.params = params


    def check_params(self) -> None: 
        missing_params = [param for param, value in self.params.items() if value is None]
        if missing_params:
            raise ValuesNotFound(f"Не найден обязательный параметр {', '.join(missing_params)}! Укажите его во время инициализации класса PayOk")
                
    

    def status(self, data: dict) -> None:
        try:
            error = data["error_code"]
            text = data["error_text"]
            raise Error(text, error)
        except KeyError:
            pass
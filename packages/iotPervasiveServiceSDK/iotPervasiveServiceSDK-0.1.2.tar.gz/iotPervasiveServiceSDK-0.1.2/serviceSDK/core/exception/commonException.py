class invalidParamsException(Exception):
    def __init__(self, param,value):
        self.message = f"The param '{param}' is {value}"
        super().__init__(self.message)
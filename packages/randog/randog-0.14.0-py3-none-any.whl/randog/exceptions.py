class FactoryConstructionError(Exception):
    _message: str

    @property
    def message(self) -> str:
        return self._message

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

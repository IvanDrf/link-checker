class InternalError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message: object = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return f'Internal error: {self.message}'

        return 'Internal error'

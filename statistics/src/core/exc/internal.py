class InternalError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.message = args[0] if args else None

    def __str__(self) -> str:
        return f'Internal error: {self.message}' if self.message else 'Internal error'

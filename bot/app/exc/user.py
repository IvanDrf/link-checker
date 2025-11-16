class UserError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message: object = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return f'UserError: {self.message}'

        return f'UserError: empty message'

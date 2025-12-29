class RepoError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.message = args[0] if args else None

    def __str__(self) -> str:
        return f'Repo error: {self.message}' if self.message else 'Repo error'

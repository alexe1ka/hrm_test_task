class Alphabet:

    def __init__(self, alphabet) -> None:
        super().__init__()
        self._alphabet = alphabet

    @property
    def alphabet(self):
        return self._alphabet

    def __repr__(self) -> str:
        return f'alphabet: {self._alphabet}'

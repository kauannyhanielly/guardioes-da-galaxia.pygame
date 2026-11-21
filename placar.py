class Placar:
    def __init__(self):
        self.pontos = 0

    @property
    def pontos(self):
        return self._pontos

    @pontos.setter
    def pontos(self, valor):
        self._pontos = max(0, valor)

    def adicionar(self, pontos):
        self.pontos += pontos

    def __str__(self):
        return f"Pontos: {self.pontos}"

    def __lt__(self, outro):
        if not isinstance(outro, Placar):
            return NotImplemented
        return self.pontos < outro.pontos

from inimigo import Inimigo


class Fase:
    # Cada linha guarda o tipo, a altura e as posições horizontais.
    _FORMACOES = {
        1: (
            ("caca", 100, (80, 200, 320, 440, 560, 680)),
        ),
        2: (
            ("ataque", 65, (170, 378, 586)),
            ("caca", 135, (80, 200, 320, 440, 560, 680)),
        ),
        3: (
            ("mae", 35, (350,)),
            ("ataque", 155, (100, 280, 460, 640)),
            ("caca", 220, (60, 155, 250, 345, 440, 535, 630, 725)),
        ),
    }

    def __init__(self, numero):
        if numero not in self._FORMACOES:
            raise ValueError("O número da fase deve ser 1, 2 ou 3.")
        self.numero = numero

    def criar_inimigos(self):
        inimigos = []
        for tipo, y, posicoes_x in self._FORMACOES[self.numero]:
            for x in posicoes_x:
                inimigos.append(Inimigo.criar(tipo, x, y))
        return inimigos

    def terminou(self, inimigos):
        return not any(inimigo.ativo for inimigo in inimigos)

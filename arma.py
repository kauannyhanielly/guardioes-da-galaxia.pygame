import pygame
from projetil import Projetil


class Arma:

    def __init__(self):
        self.municao_maxima = 10
        self._municao = 10
        self.ultimo_recarregamento = pygame.time.get_ticks()

    @property
    def municao(self):
        return self._municao

    @municao.setter
    def municao(self, valor):
        self._municao = max(0, min(valor, self.municao_maxima))

    def disparar(self, x, y):
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_recarregamento >= 500:
            if self.municao < self.municao_maxima:
                self.municao += 1

            self.ultimo_recarregamento = agora

        if self.municao > 0:
            self.municao -= 1

            return Projetil(
                x, y, 1, -8, True
            )

        return None

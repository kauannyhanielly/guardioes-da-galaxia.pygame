import pygame
from entidade import Entidade


class Projetil(Entidade):

    def __init__(self, x, y, dano, velocidade_y, do_jogador):
        super().__init__(x, y, 6, 15)

        self.dano = dano
        self.velocidade_y = velocidade_y
        self.do_jogador = do_jogador
        self.ativo = True

    def atualizar(self):
        self.y += self.velocidade_y

        if self.y < 0 or self.y > 600:
            self.ativo = False

    def desenhar(self, tela):
        if self.ativo:
            if self.do_jogador:
                cor = (0, 255, 0)
            else:
                cor = (255, 0, 0)

            pygame.draw.rect(
                tela,
                cor,
                (self.x, self.y, self.largura, self.altura)
            )

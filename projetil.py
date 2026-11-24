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
        self.rect.y += self.velocidade_y
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.ativo = False

    def desenhar(self, tela):
        if self.ativo:
            cor = (80, 255, 120) if self.do_jogador else (255, 70, 70)
            pygame.draw.rect(tela, cor, self.rect, border_radius=3)
            pygame.draw.rect(tela, (255, 255, 255), self.rect.inflate(-4, -6), border_radius=2)

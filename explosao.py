import math
import pygame
from entidade import Entidade


class Explosao(Entidade):
    """Efeito visual: um clarão com faíscas que some sozinho."""

    DURACAO = 22  # quadros

    def __init__(self, x, y, tamanho=30):
        super().__init__(x - tamanho, y - tamanho, tamanho * 2, tamanho * 2)
        self.tamanho = tamanho
        self.quadro = 0

    def atualizar(self):
        self.quadro += 1
        if self.quadro >= self.DURACAO:
            self.ativo = False

    def desenhar(self, tela):
        if not self.ativo:
            return
        progresso = self.quadro / self.DURACAO
        centro = self.rect.center
        lado = self.tamanho * 2
        camada = pygame.Surface((lado * 2, lado * 2), pygame.SRCALPHA)
        meio = (lado, lado)

        alpha = int(255 * (1 - progresso))
        raio = int(self.tamanho * (0.4 + 0.9 * progresso))
        pygame.draw.circle(camada, (255, 140, 40, alpha // 2), meio, raio)
        pygame.draw.circle(camada, (255, 220, 90, alpha), meio, max(1, int(raio * 0.6)))
        pygame.draw.circle(camada, (255, 255, 255, alpha), meio, max(1, int(raio * 0.25)))

        for i in range(8):
            angulo = i * math.pi / 4 + 0.3
            dist = self.tamanho * (0.5 + 1.3 * progresso)
            ponto = (meio[0] + math.cos(angulo) * dist,
                     meio[1] + math.sin(angulo) * dist)
            pygame.draw.circle(camada, (255, 200, 80, alpha), ponto, 3)

        tela.blit(camada, camada.get_rect(center=centro))

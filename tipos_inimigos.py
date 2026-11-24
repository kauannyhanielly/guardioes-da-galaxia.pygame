import pygame

from inimigo import Inimigo
from recursos import Recursos


class CacaAlienigena(Inimigo):
    tipo = "caca"

    def __init__(self, x, y):
        super().__init__(x, y, 34, 54, 1, 3, 10)
        self.direcao = 1
        self.imagem = Recursos.imagem("alien.png", 42, 66, (80, 220, 100))

    def atualizar(self):
        self.rect.x += self.velocidade * self.direcao
        if self.rect.right >= 800:
            self.rect.right = 800
            self.direcao = -1
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.direcao = 1

    def desenhar(self, tela):
        self.desenhar_imagem(tela)

    def atacar(self):
        return None


class NaveAtaque(Inimigo):
    tipo = "ataque"

    def __init__(self, x, y):
        super().__init__(x, y, 56, 56, 3, 2, 25)
        self.direcao = 1
        self.imagem = Recursos.imagem("nave_ataque.png", 66, 66, (240, 100, 70))
        self.limite_esquerdo = max(0, x - 80)
        self.limite_direito = min(800, self.rect.right + 80)
        self.ultimo_tiro = pygame.time.get_ticks()

    def atualizar(self):
        self.rect.x += self.velocidade * self.direcao
        if self.rect.right >= self.limite_direito:
            self.rect.right = self.limite_direito
            self.direcao = -1
        elif self.rect.left <= self.limite_esquerdo:
            self.rect.left = self.limite_esquerdo
            self.direcao = 1

    def desenhar(self, tela):
        self.desenhar_imagem(tela)

    def atacar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro < 2000:
            return None

        from projetil import Projetil

        self.ultimo_tiro = agora
        return Projetil(self.rect.centerx, self.rect.bottom, 5, 4, False)


class NaveMae(Inimigo):
    tipo = "mae"

    def __init__(self, x, y):
        super().__init__(x, y, 104, 100, 20, 1, 100)
        self.direcao = 1
        self.imagem = Recursos.imagem("nave_mae.png", 120, 118, (165, 95, 240))
        self.ultimo_tiro = pygame.time.get_ticks()

    def atualizar(self):
        if self.rect.y < 50:
            self.rect.y += self.velocidade

        self.rect.x += self.velocidade * self.direcao
        if self.rect.right >= 800:
            self.rect.right = 800
            self.direcao = -1
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.direcao = 1

    def desenhar(self, tela):
        self.desenhar_imagem(tela)

    def atacar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro < 1000:
            return None

        from projetil import Projetil

        self.ultimo_tiro = agora
        return Projetil(self.rect.centerx, self.rect.bottom, 10, 5, False)

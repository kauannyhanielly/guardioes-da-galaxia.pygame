import pygame
from entidade import Entidade
from arma import Arma
from recursos import Recursos


class Jogador(Entidade):
    VIDA_MAXIMA = 100
    LARGURA_TELA = 800
    ALTURA_TELA = 600

    def __init__(self, x, y):
        super().__init__(x, y, 56, 56)
        self.vida = self.VIDA_MAXIMA
        self.velocidade = 5
        self.arma = Arma()
        self.imagem = Recursos.imagem("jogador.png", 84, 84, (60, 140, 255))

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        self._vida = max(0, min(valor, self.VIDA_MAXIMA))

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

    def disparar(self):
        return self.arma.disparar(self.rect.centerx, self.rect.top)

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida == 0:
            self.ativo = False

    def atualizar(self):
        self.mover(pygame.key.get_pressed())
        limites = pygame.Rect(0, 0, self.LARGURA_TELA, self.ALTURA_TELA)
        self.rect.clamp_ip(limites)

    def desenhar(self, tela):
        if self.ativo:
            self.desenhar_imagem(tela)
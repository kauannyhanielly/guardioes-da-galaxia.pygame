from abc import ABC, abstractmethod
import pygame

class Entidade(ABC):

    def __init__(self,x,y,largura,altura):
        self.rect = pygame.Rect(x,y,largura,altura)
        self.ativo = True
        self.imagem = None

    @abstractmethod
    def atualizar(self):
        pass

    @abstractmethod
    def desenhar(self,tela):
        pass

   

    def desenhar_imagem(self, tela):
        """Desenha self.imagem centralizada na área de colisão (self.rect)."""
        if self.imagem is not None:
            tela.blit(self.imagem, self.imagem.get_rect(center=self.rect.center))

from abc import ABC, abstractmethod
import pygame

class Entidade(ABC):

    def __init__(self,x,y,largura,altura):
        self.Rect = pygame.rect(x,y,largura,altura)
        self.ativo = True

    @abstractmethod
    def atualizar(self):
        pass

    @abstractmethod
    def desenhar(self,tela):
        pass

   
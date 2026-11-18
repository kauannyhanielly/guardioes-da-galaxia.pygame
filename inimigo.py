from abc import abstractmethod
from entidade import Entidade

class Inimigo(Entidade):
    _registro = {}

    def __init_subclass__(cls, **kwargs): 
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "tipo"):
            Inimigo._registro[cls.tipo] = cls


    def __init__(self,x,y,largura,altura,vida,velocidade,pontos):
        super().__init__(x,y,largura,altura)
        self.vida = vida
        self.velocidade = velocidade
        self.pontos = pontos

    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self,valor):
        self._vida = max(0,valor)

    def receber_dano(self,dano):
        self.vida -= dano
        if self.vida == 0:
            self.ativo = False

    @classmethod 
    def criar(cls, tipo, x, y):
        return cls._registro[tipo](x, y)

    @abstractmethod
    def atacar(self):
        pass
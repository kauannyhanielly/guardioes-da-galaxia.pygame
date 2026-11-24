import os
import pygame


class Recursos:
    """Carrega e guarda as imagens do jogo (cada uma é carregada uma vez só)."""

    PASTA = os.path.dirname(os.path.abspath(__file__))
    _cache = {}

    @classmethod
    def imagem(cls, nome, largura, altura, cor_reserva, tonalidade=None):
        """Devolve a imagem de 'imagens/nome' cabendo em (largura x altura),
        sem deformar. 'tonalidade' pinta a imagem com uma cor (ex.: (255, 120, 120)).
        Se o arquivo não existir, devolve um quadrado colorido (jogo não quebra)."""
        chave = (nome, largura, altura, tonalidade)
        if chave in cls._cache:
            return cls._cache[chave]

        caminho = os.path.join(cls.PASTA, "imagens", nome)
        try:
            img = pygame.image.load(caminho).convert_alpha()
            escala = min(largura / img.get_width(), altura / img.get_height())
            novo_tamanho = (max(1, int(img.get_width() * escala)),
                            max(1, int(img.get_height() * escala)))
            img = pygame.transform.smoothscale(img, novo_tamanho)
            if tonalidade is not None:
                img.fill(tonalidade + (255,), special_flags=pygame.BLEND_RGBA_MULT)
        except (pygame.error, FileNotFoundError):
            img = pygame.Surface((largura, altura), pygame.SRCALPHA)
            img.fill(cor_reserva)

        cls._cache[chave] = img
        return img


class Sons:
    """Carrega e toca os efeitos sonoros da pasta 'sons'.
    Se não houver placa de som ou o arquivo faltar, o jogo continua mudo."""

    VOLUMES = {
        "tiro": 0.35,
        "tiro_inimigo": 0.2,
        "vazio": 0.4,
        "acerto": 0.4,
        "explosao": 0.6,
        "dano": 0.7,
        "fase": 0.6,
        "vitoria": 0.7,
        "derrota": 0.7,
    }

    def __init__(self):
        self._sons = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            return

        pasta = os.path.join(Recursos.PASTA, "sons")
        for nome, volume in self.VOLUMES.items():
            try:
                som = pygame.mixer.Sound(os.path.join(pasta, nome + ".wav"))
                som.set_volume(volume)
                self._sons[nome] = som
            except (pygame.error, FileNotFoundError):
                pass

    def tocar(self, nome):
        som = self._sons.get(nome)
        if som is not None:
            som.play()

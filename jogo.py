import random
import pygame
from jogador import Jogador
from inimigo import Inimigo
from projetil import Projetil
from fase import Fase
from placar import Placar
import tipos_inimigos  

class Jogo:
    LARGURA = 800
    ALTURA = 600
    TOTAL_FASES = 3
    DANO_COLISAO = 20

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Guardiões da Galáxia - Última Fronteira")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont(None, 28)
        self.fonte_grande = pygame.font.SysFont(None, 64)

        self.estrelas = [
            [random.randint(0, self.LARGURA),
             random.randint(0, self.ALTURA),
             random.choice([1, 2, 3])]
            for _ in range(80)
        ]
        self.reiniciar()

    def reiniciar(self):
       
        self.jogador = Jogador(self.LARGURA // 2 - 33, self.ALTURA - 80)
        self.placar = Placar()
        self.fase = Fase(1)
        self.estado = "jogando" 
        self.iniciar_fase()

    def iniciar_fase(self):
       
        self.entidades = [self.jogador] + self.fase.criar_inimigos()

    @staticmethod
    def colidiu(a, b):
        """Utilitário de colisão entre duas entidades."""
        return a.rect.colliderect(b.rect)

    def inimigos(self):
        return [e for e in self.entidades if isinstance(e, Inimigo)]

    def projeteis(self):
        return [e for e in self.entidades if isinstance(e, Projetil)]

    def adicionar_tiro(self, tiro):
        if tiro is not None:
            self.entidades.append(tiro)

    def tratar_colisoes(self):
        for tiro in self.projeteis():
            if tiro.do_jogador:
                for inimigo in self.inimigos():
                    if tiro.ativo and inimigo.ativo and self.colidiu(tiro, inimigo):
                        inimigo.receber_dano(tiro.dano)
                        tiro.ativo = False
                        if not inimigo.ativo:
                            self.placar.adicionar(inimigo.pontos)
            elif tiro.ativo and self.colidiu(tiro, self.jogador):
                self.jogador.receber_dano(tiro.dano)
                tiro.ativo = False

        for inimigo in self.inimigos():
            if inimigo.ativo and self.colidiu(inimigo, self.jogador):
                self.jogador.receber_dano(self.DANO_COLISAO)
                inimigo.ativo = False

    def atualizar(self):
        
        for e in self.entidades:
            e.atualizar()

   
        for inimigo in self.inimigos():
            self.adicionar_tiro(inimigo.atacar())

        self.tratar_colisoes()

        if not self.jogador.ativo:
            self.estado = "perdeu"

       
        self.entidades = [e for e in self.entidades
                          if e.ativo or e is self.jogador]

        if self.estado == "jogando" and self.fase.terminou(self.inimigos()):
            self.avancar_fase()

        for estrela in self.estrelas:
            estrela[1] += estrela[2]
            if estrela[1] > self.ALTURA:
                estrela[1] = 0
                estrela[0] = random.randint(0, self.LARGURA)

    def avancar_fase(self):
        if self.fase.numero >= self.TOTAL_FASES:
            self.estado = "venceu"
        else:
            self.fase = Fase(self.fase.numero + 1)
            self.iniciar_fase()

    def desenhar(self):
        self.tela.fill((5, 5, 25))
        for x, y, vel in self.estrelas:
            brilho = 120 + vel * 45
            pygame.draw.circle(self.tela, (brilho, brilho, 255), (x, y),
                               1 if vel < 3 else 2)

        for e in self.entidades:
            e.desenhar(self.tela)

        hud = (f"Vida: {self.jogador.vida}    "
               f"Pontos: {self.placar.pontos}    "
               f"Fase: {self.fase.numero}/{self.TOTAL_FASES}")
        self.tela.blit(self.fonte.render(hud, True, (255, 255, 255)), (10, 10))

        if self.estado != "jogando":
            texto = "VITÓRIA!" if self.estado == "venceu" else "FIM DE JOGO"
            msg = self.fonte_grande.render(texto, True, (255, 255, 255))
            dica = self.fonte.render("Aperte R para jogar de novo", True, (200, 200, 200))
            self.tela.blit(msg, msg.get_rect(center=(self.LARGURA // 2, self.ALTURA // 2 - 20)))
            self.tela.blit(dica, dica.get_rect(center=(self.LARGURA // 2, self.ALTURA // 2 + 30)))

        pygame.display.flip()

    def rodar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if self.estado == "jogando" and evento.key == pygame.K_SPACE:
                        self.adicionar_tiro(self.jogador.disparar())
                    elif self.estado != "jogando" and evento.key == pygame.K_r:
                        self.reiniciar()

            if self.estado == "jogando":
                self.atualizar()
            self.desenhar()
            self.relogio.tick(60)

        pygame.quit()
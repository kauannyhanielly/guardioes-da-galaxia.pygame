import random
import pygame
from jogador import Jogador
from inimigo import Inimigo
from projetil import Projetil
from fase import Fase
from placar import Placar
from explosao import Explosao
from recursos import Sons
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
        self.fonte_pequena = pygame.font.SysFont(None, 22)
        self.fonte_grande = pygame.font.SysFont(None, 80)
        self.sons = Sons()

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
        self.flash = 0
        self.iniciar_fase()

    def iniciar_fase(self):
       
        self.entidades = [self.jogador] + self.fase.criar_inimigos()
        self.aviso_ate = pygame.time.get_ticks() + 1800

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
            self.sons.tocar("tiro" if tiro.do_jogador else "tiro_inimigo")

    def explodir(self, entidade, tamanho):
        self.entidades.append(Explosao(entidade.rect.centerx, entidade.rect.centery, tamanho))
        self.sons.tocar("explosao")

    def machucar_jogador(self, dano):
        self.jogador.receber_dano(dano)
        self.flash = 10
        self.sons.tocar("dano")

    def tratar_colisoes(self):
        for tiro in self.projeteis():
            if tiro.do_jogador:
                for inimigo in self.inimigos():
                    if tiro.ativo and inimigo.ativo and self.colidiu(tiro, inimigo):
                        inimigo.receber_dano(tiro.dano)
                        tiro.ativo = False
                        if inimigo.ativo:
                            self.sons.tocar("acerto")
                        else:
                            self.placar.adicionar(inimigo.pontos)
                            self.explodir(inimigo, max(22, inimigo.rect.width // 2 + 8))
            elif tiro.ativo and self.colidiu(tiro, self.jogador):
                self.machucar_jogador(tiro.dano)
                tiro.ativo = False

        for inimigo in self.inimigos():
            if inimigo.ativo and self.colidiu(inimigo, self.jogador):
                self.machucar_jogador(self.DANO_COLISAO)
                inimigo.ativo = False
                self.explodir(inimigo, max(22, inimigo.rect.width // 2 + 8))

    def atualizar(self):
        
        for e in self.entidades:
            e.atualizar()

   
        for inimigo in self.inimigos():
            self.adicionar_tiro(inimigo.atacar())

        self.tratar_colisoes()

        if not self.jogador.ativo:
            self.explodir(self.jogador, 45)
            self.terminar("perdeu")

       
        self.entidades = [e for e in self.entidades
                          if e.ativo or e is self.jogador]

        if self.estado == "jogando" and self.fase.terminou(self.inimigos()):
            self.avancar_fase()

        self.mover_estrelas()
        if self.flash > 0:
            self.flash -= 1

    def mover_estrelas(self):
        for estrela in self.estrelas:
            estrela[1] += estrela[2]
            if estrela[1] > self.ALTURA:
                estrela[1] = 0
                estrela[0] = random.randint(0, self.LARGURA)

    def atualizar_efeitos(self):
        """Depois do fim de jogo: só as explosões e as estrelas continuam animando."""
        for e in self.entidades:
            if isinstance(e, Explosao):
                e.atualizar()
        self.entidades = [e for e in self.entidades if e.ativo or e is self.jogador]
        self.mover_estrelas()
        if self.flash > 0:
            self.flash -= 1

    def terminar(self, resultado):
        self.estado = resultado
        self.sons.tocar("vitoria" if resultado == "venceu" else "derrota")

    def avancar_fase(self):
        if self.fase.numero >= self.TOTAL_FASES:
            self.terminar("venceu")
        else:
            self.sons.tocar("fase")
            self.fase = Fase(self.fase.numero + 1)
            self.iniciar_fase()

    def desenhar_hud(self):
        painel = pygame.Surface((self.LARGURA, 46), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 150))
        self.tela.blit(painel, (0, 0))
        pygame.draw.line(self.tela, (90, 110, 200), (0, 46), (self.LARGURA, 46), 2)

        # vida: barra que muda de cor
        fracao = self.jogador.vida / self.jogador.VIDA_MAXIMA
        cor = (80, 220, 100) if fracao > 0.5 else (240, 200, 60) if fracao > 0.25 else (240, 70, 70)
        self.tela.blit(self.fonte_pequena.render("VIDA", True, (180, 190, 230)), (14, 4))
        pygame.draw.rect(self.tela, (40, 40, 60), (14, 22, 180, 16), border_radius=5)
        if fracao > 0:
            pygame.draw.rect(self.tela, cor, (14, 22, int(180 * fracao), 16), border_radius=5)
        pygame.draw.rect(self.tela, (200, 210, 255), (14, 22, 180, 16), 1, border_radius=5)
        valor = self.fonte_pequena.render(str(self.jogador.vida), True, (255, 255, 255))
        self.tela.blit(valor, (204, 22))

        # pontos (centro)
        rotulo = self.fonte_pequena.render("PONTOS", True, (180, 190, 230))
        pontos = self.fonte.render(f"{self.placar.pontos:06d}", True, (255, 220, 90))
        self.tela.blit(rotulo, rotulo.get_rect(midtop=(self.LARGURA // 2, 4)))
        self.tela.blit(pontos, pontos.get_rect(midtop=(self.LARGURA // 2, 20)))

        # fase (direita)
        rotulo = self.fonte_pequena.render("FASE", True, (180, 190, 230))
        fase = self.fonte.render(f"{self.fase.numero} / {self.TOTAL_FASES}", True, (255, 255, 255))
        self.tela.blit(rotulo, rotulo.get_rect(topright=(self.LARGURA - 14, 4)))
        self.tela.blit(fase, fase.get_rect(topright=(self.LARGURA - 14, 20)))

        # munição (embaixo, à esquerda): um quadradinho por tiro
        arma = self.jogador.arma
        for i in range(arma.municao_maxima):
            cor_tiro = (80, 255, 120) if i < arma.municao else (50, 60, 80)
            pygame.draw.rect(self.tela, cor_tiro, (14 + i * 14, self.ALTURA - 22, 8, 14), border_radius=2)

    def escurecer(self, alpha):
        camada = pygame.Surface((self.LARGURA, self.ALTURA), pygame.SRCALPHA)
        camada.fill((0, 0, 10, alpha))
        self.tela.blit(camada, (0, 0))

    def desenhar(self):
        self.tela.fill((5, 5, 25))
        for x, y, vel in self.estrelas:
            brilho = 120 + vel * 45
            pygame.draw.circle(self.tela, (brilho, brilho, 255), (x, y),
                               1 if vel < 3 else 2)

        for e in self.entidades:
            e.desenhar(self.tela)

        if self.flash > 0:
            camada = pygame.Surface((self.LARGURA, self.ALTURA), pygame.SRCALPHA)
            camada.fill((255, 0, 0, self.flash * 12))
            self.tela.blit(camada, (0, 0))

        self.desenhar_hud()

        agora = pygame.time.get_ticks()
        if self.estado == "jogando" and agora < self.aviso_ate:
            msg = self.fonte_grande.render(f"FASE {self.fase.numero}", True, (255, 255, 255))
            msg.set_alpha(min(255, (self.aviso_ate - agora) // 3))
            self.tela.blit(msg, msg.get_rect(center=(self.LARGURA // 2, self.ALTURA // 2)))

        if self.estado != "jogando":
            self.escurecer(170)
            venceu = self.estado == "venceu"
            texto = "VITÓRIA!" if venceu else "FIM DE JOGO"
            cor = (120, 255, 150) if venceu else (255, 90, 90)
            msg = self.fonte_grande.render(texto, True, cor)
            final = self.fonte.render(f"Pontuação final: {self.placar.pontos}", True, (255, 220, 90))
            dica = self.fonte.render("Aperte R para jogar de novo", True, (200, 200, 220))
            cx = self.LARGURA // 2
            self.tela.blit(msg, msg.get_rect(center=(cx, self.ALTURA // 2 - 50)))
            self.tela.blit(final, final.get_rect(center=(cx, self.ALTURA // 2 + 10)))
            self.tela.blit(dica, dica.get_rect(center=(cx, self.ALTURA // 2 + 50)))

        pygame.display.flip()

    def rodar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if self.estado == "jogando" and evento.key == pygame.K_SPACE:
                        tiro = self.jogador.disparar()
                        if tiro is None:
                            self.sons.tocar("vazio")
                        self.adicionar_tiro(tiro)
                    elif self.estado != "jogando" and evento.key == pygame.K_r:
                        self.reiniciar()

            if self.estado == "jogando":
                self.atualizar()
            else:
                self.atualizar_efeitos()
            self.desenhar()
            self.relogio.tick(60)

        pygame.quit()
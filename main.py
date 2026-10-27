import pygame
import pygame

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Guardiões da Galáxia - Última Fronteira")
relogio = pygame.time.Clock()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((10, 10, 40))   # fundo azul bem escuro
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
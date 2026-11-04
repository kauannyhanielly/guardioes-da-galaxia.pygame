import pygame

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Guardiões da Galáxia - Última Fronteira")
relogio = pygame.time.Clock()

# Jogador: um retângulo azul na parte de baixo da tela
jogador = pygame.Rect(LARGURA // 2 - 25, ALTURA - 80, 50, 40)
velocidade_jogador = 5

# Inimigo: um retângulo vermelho que anda de um lado para o outro
inimigo = pygame.Rect(100, 80, 60, 40)
velocidade_inimigo = 3

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador (setas ou A/D e W/S)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador.x -= velocidade_jogador
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador.x += velocidade_jogador
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        jogador.y -= velocidade_jogador
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        jogador.y += velocidade_jogador

    # Impede o jogador de sair da tela
    jogador.clamp_ip(tela.get_rect())

    # Movimento do inimigo: vai e volta na horizontal
    inimigo.x += velocidade_inimigo
    if inimigo.right >= LARGURA or inimigo.left <= 0:
        velocidade_inimigo = -velocidade_inimigo

    # Desenho
    tela.fill((10, 10, 40))
    pygame.draw.rect(tela, (60, 140, 255), jogador)
    pygame.draw.rect(tela, (220, 50, 50), inimigo)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
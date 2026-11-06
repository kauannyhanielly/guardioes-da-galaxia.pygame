import os
import random
import pygame

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Guardiões da Galáxia - Última Fronteira")
relogio = pygame.time.Clock()

PASTA = os.path.dirname(os.path.abspath(__file__))


def carregar_imagem(nome, largura, altura, cor_reserva):
    """Carrega a imagem da pasta 'imagens'. Se não achar, usa um quadrado colorido."""
    caminho = os.path.join(PASTA, "imagens", nome)
    try:
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.smoothscale(img, (largura, altura))
    except (pygame.error, FileNotFoundError):
        img = pygame.Surface((largura, altura))
        img.fill(cor_reserva)
        return img


# Imagens (ajuste o tamanho se ficar esquisito)
jogador_img = carregar_imagem("jogador.png", 66, 50, (60, 140, 255))
inimigo_img = carregar_imagem("inimigo.png", 70, 60, (220, 50, 50))

# Jogador: começa embaixo, no meio da tela
jogador = jogador_img.get_rect(midbottom=(LARGURA // 2, ALTURA - 20))
velocidade_jogador = 5

# Inimigo: anda de um lado para o outro
inimigo = inimigo_img.get_rect(topleft=(100, 80))
velocidade_inimigo = 3

# Estrelas do fundo: [x, y, velocidade]
estrelas = []
for _ in range(80):
    estrelas.append([random.randint(0, LARGURA),
                     random.randint(0, ALTURA),
                     random.choice([1, 2, 3])])

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador (setas ou W, A, S, D)
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

    # Movimento das estrelas: descem e voltam para o topo
    for estrela in estrelas:
        estrela[1] += estrela[2]
        if estrela[1] > ALTURA:
            estrela[1] = 0
            estrela[0] = random.randint(0, LARGURA)

    # Desenho
    tela.fill((5, 5, 25))
    for x, y, vel in estrelas:
        brilho = 120 + vel * 45
        raio = 1 if vel < 3 else 2
        pygame.draw.circle(tela, (brilho, brilho, 255), (x, y), raio)
    tela.blit(inimigo_img, inimigo)
    tela.blit(jogador_img, jogador)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
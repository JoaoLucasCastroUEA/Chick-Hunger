import pygame
import sys

pygame.init()

# Configurações da janela
largura = 1000
altura = 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("HUD - Imagem no Canto Inferior Esquerdo")

# Carrega a imagem do cursor
imagem_cursor_original = pygame.image.load(r'C:\Users\joaoj\OneDrive\Documentos\GitHub\Chick-Hunger\Assets\mira.png')
tamanho_novo_cursor = (40, 40)  # Defina o tamanho desejado para o cursor
imagem_cursor = pygame.transform.scale(imagem_cursor_original, tamanho_novo_cursor)
pygame.mouse.set_visible(False)  # Torna o cursor padrão invisível

# Carrega a imagem do HUD
imagem_hud_original = pygame.image.load(r'C:\Users\joaoj\OneDrive\Documentos\GitHub\Chick-Hunger\Assets\estilingue.jpeg')
largura_hud_original, altura_hud_original = imagem_hud_original.get_size()

# Ajusta o tamanho da imagem do HUD mantendo a proporção original
razao_aspecto_hud = largura_hud_original / altura_hud_original
nova_altura_hud = int(tamanho_novo_cursor[1] * 1.5)  # Ajuste a altura conforme necessário
nova_largura_hud = int(nova_altura_hud * razao_aspecto_hud)
imagem_hud = pygame.transform.scale(imagem_hud_original, (nova_largura_hud, nova_altura_hud))

# Carrega a imagem de fundo
imagem_fundo = pygame.image.load(r'C:\Users\joaoj\OneDrive\Documentos\GitHub\Chick-Hunger\Assets\brick wall.png')
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Calcula a posição para o canto inferior esquerdo
posicao_hud = (10, altura - nova_altura_hud - 10)

# Configuração do relógio
clock = pygame.time.Clock()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualiza a tela
    tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo na tela
    tela.blit(imagem_cursor, pygame.mouse.get_pos())  # Desenha a imagem do cursor na posição do mouse
    tela.blit(imagem_hud, posicao_hud)  # Desenha a imagem do HUD no canto inferior esquerdo

    pygame.display.flip()

    # Limita a taxa de atualização da tela
    clock.tick(60)

import pygame
import sys
import random

pygame.init()

# Configurações da janela
largura = 1280
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

# Função para gerar galinhas
def gerar_galinha():
    x = largura  # Inicia a galinha à direita da tela
    y = random.choice([200, 400, 600])  # Altura aleatória dentro da tela
    velocidade = random.randint(-5, -1)  # Velocidade aleatória da direita para a esquerda
    return Galinha(x, y, velocidade)

# Função para detectar clique em uma galinha
def verificar_clique_galinha(posicao):
    galinhas_clicadas = [galinha for galinha in grupo_galinhas if galinha.rect.collidepoint(posicao)]

    for galinha in galinhas_clicadas:
        print("Você clicou em uma galinha!")
        galinha.kill()  # Remove a galinha do grupo

# Classe para representar as galinhas
class Galinha(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Cor vermelha para representar as galinhas
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = velocidade

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.right < 0:
            # Remove a galinha se ela sair da tela
            self.kill()

# Grupo de sprites para as galinhas
grupo_galinhas = pygame.sprite.Group()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifica clique do botão esquerdo do mouse
            verificar_clique_galinha(event.pos)
            print(event.pos)

    # Atualiza o grupo de galinhas
    grupo_galinhas.update()

    # Cria uma nova galinha ocasionalmente
    if random.randint(0, 100) < 3:
        galinha = gerar_galinha()
        grupo_galinhas.add(galinha)

    # Atualiza a tela
    tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo na tela
    tela.blit(imagem_cursor, pygame.mouse.get_pos())  # Desenha a imagem do cursor na posição do mouse
    tela.blit(imagem_hud, posicao_hud)  # Desenha a imagem do HUD no canto inferior esquerdo

    pygame.draw.rect(tela, (0, 0 ,0), (0, 250, 1280, 10))
    pygame.draw.rect(tela, (0, 0 ,0), (0, 450, 1280, 10))
    pygame.draw.rect(tela, (0, 0 ,0), (0, 650, 1280, 10))

    # Desenha as galinhas
    grupo_galinhas.draw(tela)

    pygame.display.flip()

    # Limita a taxa de atualização da tela
    clock.tick(60)

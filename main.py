import pygame
import sys
import random
import time

pygame.init()

# Configurações da janela
largura = 1280
altura = 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("HUD - Imagem no Canto Inferior Esquerdo")

galinha_spritesheet = pygame.image.load('Assets/galinha_spritesheet.png')
largura_frame, altura_frame = galinha_spritesheet.get_size()
frame_width = largura_frame // 3  # 3 frames na spritesheet
frame_height = altura_frame

# Separa os frames da spritesheet
frames_galinha = [galinha_spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height)) for i in range(3)]
frames_galinha = [pygame.transform.scale(frame, (55, 55)) for frame in frames_galinha]

# Carregamento da spritesheet do gato
gato_spritesheet = pygame.image.load('Assets/gato_spritesheet.png')
frame_width_gato = gato_spritesheet.get_width() // 4
frame_height_gato = gato_spritesheet.get_height()

# Função para extrair frames da spritesheet do gato
def get_frames_gato():
    frames_gato = []
    for i in range(4):
        frame_gato = gato_spritesheet.subsurface((i * frame_width_gato, 0, frame_width_gato, frame_height_gato))
        frames_gato.append(frame_gato)
    return frames_gato

# Carregamento dos frames do gato
frames_gato = get_frames_gato()
current_frame_gato = 0
frame_change_counter_gato = 0
frame_change_threshold_gato = 13

# Carrega a imagem do cursor
imagem_cursor_original = pygame.image.load('Assets/mira.png')
tamanho_novo_cursor = (40, 40)  # Defina o tamanho desejado para o cursor
imagem_cursor = pygame.transform.scale(imagem_cursor_original, tamanho_novo_cursor)

imagem_cursor_rect = imagem_cursor.get_rect()
pygame.mouse.set_visible(False)  # Torna o cursor padrão invisível

# Carrega a imagem do HUD
imagem_hud_original = pygame.image.load('Assets/estilingue_1.png')
largura_hud_original, altura_hud_original = imagem_hud_original.get_size()

# Ajusta o tamanho da imagem do HUD mantendo a proporção original
razao_aspecto_hud = largura_hud_original / altura_hud_original
nova_altura_hud = int(tamanho_novo_cursor[1] * 1.5)  # Ajuste a altura conforme necessário
nova_largura_hud = int(nova_altura_hud * razao_aspecto_hud)
imagem_hud = pygame.transform.scale(imagem_hud_original, (nova_largura_hud, nova_altura_hud))

# Carrega a imagem de fundo
imagem_fundo = pygame.image.load('Assets/fundo2.png')
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Carrega a imagem para o canto superior direito
# imagem_canto_superior_direito = pygame.image.load('Assets/gato_olhando_para_baixo.png')
# tamanho_imagem_canto_superior_direito = (150, 150)  # Defina o tamanho desejado para a imagem
# imagem_canto_superior_direito = pygame.transform.scale(imagem_canto_superior_direito, tamanho_imagem_canto_superior_direito)
# posicao_canto_superior_direito = (largura - frame_width_gato * 5 - 10, 10 - 10, 10)

# Calcula a posição para o canto inferior esquerdo
posicao_hud = (10, altura - nova_altura_hud - 10)

# Configuração do relógio
clock = pygame.time.Clock()

# Munição
fonte = pygame.font.Font(None, 36)

# Inicializa o valor do texto
municao = 10
pontuacao = 0
vida = 3
game_over = 'Game Over'
# Inicializa o tempo anterior
tempo_anterior = time.time()
tempo_atual = time.time()

# Grupo de sprites para as galinhas
grupo_galinhas = pygame.sprite.Group()

# Classe para representar as galinhas
class Galinha(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.frames = frames_galinha  # Lista de frames da animação
        self.frame_atual = 0  # Índice do frame atual
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = velocidade
        self.tempo_frame = 0.2  # Tempo de exibição de cada frame em segundos
        self.tempo_anterior = time.time()

    def update(self):
        self.rect.x += self.velocidade
        if (self.velocidade < 0 and self.rect.right < 0) or (self.velocidade > 0 and self.rect.left > largura):
            # Remove a galinha se ela sair da tela
            self.rect.y += 200
            self.velocidade *= -1

        if (self.rect.y > 600):
            global vida
            vida -= 1
            print('perdeu')
            self.kill()
        print(self.rect.x)
        if self.velocidade < 0:
            self.image = pygame.transform.flip(self.frames[self.frame_atual], True, False)
        else:
            self.image = self.frames[self.frame_atual]

        tempo_atual = time.time()
        if tempo_atual - self.tempo_anterior > self.tempo_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.tempo_anterior = tempo_atual

def desenhar_texto():
    municao_texto = fonte.render(f"Munição: {municao}", True, (255, 255, 255))
    tela.blit(municao_texto, (largura - 200, altura - 50))

    pontuacao_texto = fonte.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
    tela.blit(pontuacao_texto, (largura - 1200, altura - 680))

    vida_texto = fonte.render(f"Vida: {vida}", True, (255, 255, 255))
    tela.blit(vida_texto, (largura - 1200, altura - 630))

# Função para gerar galinhas
def gerar_galinha():
    lado = random.choice(["direita","esquerda"])  # Escolhe aleatoriamente entre esquerda e direita
    if lado == "direita":
        x = largura# Inicia a galinha à direita da tela
        velocidade = random.randint(-5, -1)  # Velocidade aleatória da direita para a esquerda
    else:
        x = -40 # Inicia a galinha à esquerda da tela
        velocidade = random.randint(1, 5)  # Velocidade aleatória da esquerda para a direita

    y = 200  # Altura aleatória dentro da tela
    return Galinha(x, y, velocidade)

# Função para detectar clique em uma galinha
def verificar_clique_galinha(posicao):
    global municao  # Indica que estamos usando a variável global valor_texto
    global pontuacao

    galinhas_clicadas = [galinha for galinha in grupo_galinhas if galinha.rect.collidepoint(posicao)]

    for galinha in galinhas_clicadas:
        print("Você clicou em uma galinha!")
        galinha.kill()  # Remove a galinha do grupo
        pontuacao += 1
        municao -= 1  # Diminui o valor do texto


# Loop principal
while True:
    # Vê os inputs do jogador
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verifica clique do botão esquerdo do mouse
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Só chama verificar clique se tiver munição
            if municao > 0:
                verificar_clique_galinha(event.pos)

    if vida > 0:
        # Preenche a tela com a cor de fundo
        tela.blit(imagem_fundo, (0, 0))

        # Atualiza o grupo de galinhas
        grupo_galinhas.update()


        # Cria uma nova galinha ocasionalmente
        if random.randint(0, 100) < 1:
            galinha = gerar_galinha()
            grupo_galinhas.add(galinha)

        # Desenha as galinhas
        grupo_galinhas.draw(tela)

        # Desenha o cursor
        tela.blit(imagem_cursor, imagem_cursor_rect)

        # Desenha o HUD
        tela.blit(imagem_hud, posicao_hud)

        fps = clock.get_fps()
        print(f"FPS: {fps}")

        # Desenha a imagem no canto superior direito
        tela.blit(pygame.transform.scale(frames_gato[current_frame_gato], (int(frame_width_gato * 4.7), int(frame_height_gato * 4.7))),
                  (largura - int(frame_width_gato * 4.7) - 150, 0))
        # Desenha o texto na tela
        desenhar_texto()

        imagem_cursor_rect.center = pygame.mouse.get_pos()

        tempo_atual = time.time()


        # verifica se passou 10seg pra aumentar a munição
        if tempo_atual - tempo_anterior > 10:
            municao += 10
            tempo_anterior = tempo_atual

        # Desenha as linhas horizontais
        pygame.draw.rect(tela, (0, 0, 0), (0, 250, 1280, 10))
        pygame.draw.rect(tela, (0, 0, 0), (0, 450, 1280, 10))
        pygame.draw.rect(tela, (0, 0, 0), (0, 650, 1280, 10))

        # Atualiza a animação do gato
        frame_change_counter_gato += 1
        if frame_change_counter_gato >= frame_change_threshold_gato:
            current_frame_gato = (current_frame_gato + 1) % 4
            frame_change_counter_gato = 0


# Se a vida acabar entrar na tela de gameover
    else:
        tela.fill((0, 0, 0))
        game_over_text = fonte.render(f"GameOver", True, (255, 255, 255))
        tela.blit(game_over_text, (200,200))

    # Atualiza a tela
    pygame.display.flip()
    # Limita a taxa de atualização da tela
    clock.tick(60)
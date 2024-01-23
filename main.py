import sys
import random
import time
import pygame

pygame.init()

# Screen settings
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HUD - Image in the Bottom Left Corner")

# Chicken spritesheet
chicken_spritesheet = pygame.image.load('Assets/chicken_spritesheet.png')
frame_width, frame_height = chicken_spritesheet.get_size()
frame_width = frame_width // 3  # 3 frames in the spritesheet
frame_height = frame_height

# Separate frames from the spritesheet
chicken_frames = [chicken_spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height)) for i in range(3)]
chicken_frames = [pygame.transform.scale(frame, (55, 55)) for frame in chicken_frames]

# Load cat spritesheet
cat_spritesheet = pygame.image.load('Assets/cat_spritesheet.png')
frame_width_cat = cat_spritesheet.get_width() // 4
frame_height_cat = cat_spritesheet.get_height()


# Function to extract frames from the cat spritesheet
def get_frames_cat():
    frames_cat = []
    for i in range(4):
        frame_cat = cat_spritesheet.subsurface((i * frame_width_cat, 0, frame_width_cat, frame_height_cat))
        frames_cat.append(frame_cat)
    return frames_cat


# Load cat frames
frames_cat = get_frames_cat()
current_frame_cat = 0
frame_change_counter_cat = 0
frame_change_threshold_cat = 13

# Load cursor image
original_cursor_image = pygame.image.load('Assets/decent_sight.png')
new_cursor_size = (40, 40)
cursor_image = pygame.transform.scale(original_cursor_image, new_cursor_size)

cursor_image_rect = cursor_image.get_rect()
pygame.mouse.set_visible(False)

# Load HUD image
original_hud_image = pygame.image.load('Assets/slingshot_1_copy.png')
original_hud_width, original_hud_height = original_hud_image.get_size()

# Adjust HUD image size while maintaining the original aspect ratio
hud_aspect_ratio = original_hud_width / original_hud_height
new_hud_height = int(new_cursor_size[1] * 1.5)
new_hud_width = int(new_hud_height * hud_aspect_ratio)
hud_image = pygame.transform.scale(original_hud_image, (new_hud_width, new_hud_height))

# Load background image
background_image = pygame.image.load('Assets/background2.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Calculate position for the bottom left corner
hud_position = (10, HEIGHT - new_hud_height - 10)

# Clock setup
clock = pygame.time.Clock()

# Ammunition
font = pygame.font.Font(None, 36)

# Initialize text values
ammunition = 10
score = 0
life = 3
game_over = 'Game Over'

# Initialize previous time
previous_time = time.time()
current_time = time.time()

# Initialize chicken spawn time
current_time_chickens = time.time()
previous_time_chickens = time.time()

# Sprite group for chickens
chicken_group = pygame.sprite.Group()

spawn_probability = 1


# Class to represent chickens
class Chicken(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.frames = chicken_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.frame_time = 0.2
        self.previous_time = time.time()

    def update(self):
        self.rect.x += self.speed
        if (self.speed < 0 and self.rect.right < 0) or (self.speed > 0 and self.rect.left > WIDTH):
            self.rect.y += 200
            self.speed *= -1

        if self.rect.y > 600:
            global life
            life -= 1
            self.kill()
        if self.speed < 0:
            self.image = pygame.transform.flip(self.frames[self.current_frame], True, False)
        else:
            self.image = self.frames[self.current_frame]

        current_time = time.time()
        if current_time - self.previous_time > self.frame_time:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.previous_time = current_time


def draw_text():
    ammunition_text = font.render(f"Ammunition: {ammunition}", True, (255, 255, 255))

    x_ammunition = hud_position[0] + new_hud_width + 10
    y_ammunition = hud_position[1] + 20
    screen.blit(ammunition_text, (x_ammunition, y_ammunition))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 1200, HEIGHT - 680))

    life_text = font.render(f"Life: {life}", True, (255, 255, 255))
    screen.blit(life_text, (WIDTH - 1200, HEIGHT - 630))


# Function to generate chickens
def generate_chicken():
    side = random.choice(["right", "left"])
    if side == "right":
        x = WIDTH
        speed = random.randint(-5, -1)
    else:
        x = -40
        speed = random.randint(1, 5)

    y = 200
    return Chicken(x, y, speed)


# Function to check click on a chicken
def check_click_chicken(position):
    global ammunition
    global score

    clicked_chickens = [chicken for chicken in chicken_group if chicken.rect.collidepoint(position)]

    for chicken in clicked_chickens:
        if ammunition == 0:
            break
        chicken.kill()
        score += 1
        ammunition -= 1


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if ammunition > 0:
                check_click_chicken(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if life <= 0:
                    life = 3
                    ammunition = 10
                    spawn_probability = 1
                    score = 0
                    previous_time_chickens = time.time()
                    current_time_chickens = time.time()
                    previous_time = time.time()
                    current_time = time.time()
                    for chicken in chicken_group:
                        chicken.kill()

    if life > 0:
        screen.blit(background_image, (0, 0))
        chicken_group.update()

        if random.randint(0, 100) < spawn_probability:
            chicken = generate_chicken()
            chicken_group.add(chicken)

        chicken_group.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), (0, 250, 1280, 10))
        pygame.draw.rect(screen, (0, 0, 0), (0, 450, 1280, 10))
        pygame.draw.rect(screen, (0, 0, 0), (0, 650, 1280, 10))

        screen.blit(cursor_image, cursor_image_rect)

        screen.blit(hud_image, hud_position)

        fps = clock.get_fps()
        print(f"FPS: {fps}")

        screen.blit(pygame.transform.scale(frames_cat[current_frame_cat],
                                           (int(frame_width_cat * 4.7), int(frame_height_cat * 4.7))),
                    (WIDTH - int(frame_width_cat * 4.7) - 150, 0))

        draw_text()

        cursor_image_rect.center = pygame.mouse.get_pos()

        current_time = time.time()

        if current_time - previous_time > 10:
            ammunition += 20
            previous_time = current_time

        current_time_chickens = time.time()
        if current_time_chickens - previous_time_chickens > 20:
            spawn_probability += 0.5
            previous_time_chickens = current_time_chickens

        frame_change_counter_cat += 1
        if frame_change_counter_cat >= frame_change_threshold_cat:
            current_frame_cat = (current_frame_cat + 1) % 4
            frame_change_counter_cat = 0

    else:
        screen.fill((0, 0, 0))
        game_over_text = font.render("GameOver", True, (255, 255, 255))

        x_game_over = (WIDTH - game_over_text.get_width()) // 2
        y_game_over = (HEIGHT - game_over_text.get_height()) // 2

        screen.blit(game_over_text, (x_game_over, y_game_over))

        restart_text = font.render("Press R to restart", True, (255, 255, 255))

        x_restart = (WIDTH - restart_text.get_width()) // 2
        y_restart = y_game_over + game_over_text.get_height() + 20

        screen.blit(restart_text, (x_restart, y_restart))

    pygame.display.flip()
    clock.tick(60)

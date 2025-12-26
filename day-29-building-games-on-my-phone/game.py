import pygame
import sys
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 29: Background Update 🎨")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (30, 30, 30)

# Font
font = pygame.font.SysFont(None, 40)

# Player setup
player_size = 40
player = pygame.Rect(WIDTH // 2, HEIGHT - 60, player_size, player_size)

# Enemy setup
enemy_size = 40
num_enemies = 5
enemies = []
for _ in range(num_enemies):
    enemies.append(pygame.Rect(random.randint(0, WIDTH - enemy_size), random.randint(-200, -40), enemy_size, enemy_size))
enemy_speed = 5

# Buttons
button_size = (80, 60)
left_button = pygame.Rect(20, HEIGHT - 70, *button_size)
right_button = pygame.Rect(WIDTH - 100, HEIGHT - 70, *button_size)

# Game variables
score = 0
game_over = False

# Load background image (optional, must be in same folder)
try:
    bg_image = pygame.image.load("background.png")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = None

def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

def draw_gradient():
    for i in range(HEIGHT):
        color = (30, i % 255, 100)  # simple gradient effect
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

def reset_game():
    global player, enemies, score, game_over
    player = pygame.Rect(WIDTH // 2, HEIGHT - 60, player_size, player_size)
    enemies.clear()
    for _ in range(num_enemies):
        enemies.append(pygame.Rect(random.randint(0, WIDTH - enemy_size), random.randint(-200, -40), enemy_size, enemy_size))
    score = 0
    game_over = False

# Background mode: 1=color, 2=gradient, 3=image
bg_mode = 2  

# Game loop
while True:
    # ---- Draw background ----
    if bg_mode == 1:
        screen.fill(GRAY)
    elif bg_mode == 2:
        draw_gradient()
    elif bg_mode == 3 and bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle restart
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
            if restart_btn.collidepoint(mouse_pos):
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        # Handle input
        moving_left, moving_right = False, False
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # left click
            mouse_pos = pygame.mouse.get_pos()
            if left_button.collidepoint(mouse_pos):
                moving_left = True
            if right_button.collidepoint(mouse_pos):
                moving_right = True

        # Player movement
        if keys[pygame.K_LEFT] or moving_left:
            if player.left > 0:
                player.x -= 5
        if keys[pygame.K_RIGHT] or moving_right:
            if player.right < WIDTH:
                player.x += 5

        # Enemy movement
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemy.y = random.randint(-200, -40)
                enemy.x = random.randint(0, WIDTH - enemy_size)
                score += 1

            if player.colliderect(enemy):
                game_over = True

        # Draw objects
        pygame.draw.rect(screen, BLUE, player)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Buttons
        pygame.draw.rect(screen, GREEN, left_button)
        draw_text("←", font, WHITE, left_button.centerx, left_button.centery)
        pygame.draw.rect(screen, GREEN, right_button)
        draw_text("→", font, WHITE, right_button.centerx, right_button.centery)

        # Score
        draw_text(f"Score: {score}", font, WHITE, 10, 10, center=False)

    else:
        # Game Over
        draw_text("GAME OVER", font, RED, WIDTH//2, HEIGHT//2 - 20)
        restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_btn)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)
        draw_text(f"Final Score: {score}", font, WHITE, WIDTH//2, HEIGHT//2 - 70)

    pygame.display.flip()
    clock.tick(30)

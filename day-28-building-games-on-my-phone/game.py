import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 28: Onscreen Buttons + Restart")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# Fonts
font = pygame.font.SysFont(None, 40)

# Player setup
player_size = 40
player = pygame.Rect(WIDTH // 2, HEIGHT - 60, player_size, player_size)

# Enemy setup
enemy_size = 40
num_enemies = 5
enemies = []
for _ in range(num_enemies):
    x = random.randint(0, WIDTH - enemy_size)
    y = random.randint(-150, -40)
    enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))
enemy_speed = 5

# Game variables
score = 0
game_over = False

# Button setup
button_width, button_height = 100, 60
left_button = pygame.Rect(20, HEIGHT - button_height - 10, button_width, button_height)
right_button = pygame.Rect(WIDTH - button_width - 20, HEIGHT - button_height - 10, button_width, button_height)

def draw_text(text, font, color, x, y, center=True):
    """Helper to draw text on screen"""
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

def reset_game():
    global player, enemies, score, game_over
    player = pygame.Rect(WIDTH // 2, HEIGHT - 60, player_size, player_size)
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(0, WIDTH - enemy_size)
        y = random.randint(-150, -40)
        enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))
    score = 0
    game_over = False

# Game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart button after Game Over
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
            if restart_btn.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        # Handle onscreen button presses
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # Left click (or touch)
            mouse_pos = pygame.mouse.get_pos()
            if left_button.collidepoint(mouse_pos) and player.left > 0:
                player.x -= 5
            if right_button.collidepoint(mouse_pos) and player.right < WIDTH:
                player.x += 5

        # Enemy movement
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemy.y = random.randint(-150, -40)
                enemy.x = random.randint(0, WIDTH - enemy_size)
                score += 1

            # Collision detection
            if player.colliderect(enemy):
                game_over = True

        # Draw player + enemies
        pygame.draw.rect(screen, BLUE, player)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Draw buttons
        pygame.draw.rect(screen, DARK_GREEN, left_button)
        pygame.draw.rect(screen, DARK_GREEN, right_button)
        draw_text("◀", font, WHITE, left_button.centerx, left_button.centery)
        draw_text("▶", font, WHITE, right_button.centerx, right_button.centery)

        # Draw score
        draw_text(f"Score: {score}", font, BLACK, 10, 10, center=False)

    else:
        # Game over screen
        draw_text("GAME OVER", font, RED, WIDTH//2, HEIGHT//2 - 20)
        restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_btn)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH//2, HEIGHT//2 - 70)

    pygame.display.flip()
    clock.tick(30)

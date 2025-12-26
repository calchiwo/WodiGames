import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 33: Platforms & Health Demo 🟦🟥")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 36)

# Player setup
player_size = 40
player_speed = 5
player = pygame.Rect(WIDTH//2, HEIGHT-60, player_size, player_size)
player_vel_y = 0
gravity = 1
jump_strength = -15
on_ground = False

# Enemy setup (static)
enemy_size = 40
enemy = pygame.Rect(WIDTH-100, HEIGHT-100, enemy_size, enemy_size)

# Platforms
platforms = [
    pygame.Rect(100, HEIGHT-150, 150, 20),
    pygame.Rect(300, HEIGHT-200, 150, 20),
    pygame.Rect(50, HEIGHT-250, 150, 20),
]

# Health & score
max_health = 3
health = max_health
score = 0

# On-screen buttons
button_size = 60
left_button = pygame.Rect(10, HEIGHT - button_size - 10, button_size, button_size)
right_button = pygame.Rect(WIDTH - button_size - 10, HEIGHT - button_size - 10, button_size, button_size)
jump_button = pygame.Rect(WIDTH//2 - button_size//2, HEIGHT - button_size - 10, button_size, button_size)

# Game variables
game_over = False

# Helper to draw text
def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

# Reset game
def reset_game():
    global player, player_vel_y, health, score, game_over
    player.x = WIDTH//2
    player.y = HEIGHT-60
    player_vel_y = 0
    health = max_health
    score = 0
    game_over = False

# Game loop
while True:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # On-screen button taps
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            if left_button.collidepoint(mouse_pos):
                player.x -= player_speed
            if right_button.collidepoint(mouse_pos):
                player.x += player_speed
            if jump_button.collidepoint(mouse_pos) and on_ground:
                player_vel_y = jump_strength

        # Restart
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
            if restart_btn.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        # Keyboard movement
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_UP] and on_ground:
            player_vel_y = jump_strength

        # Gravity
        player_vel_y += gravity
        player.y += player_vel_y

        # Collision with platforms
        on_ground = False
        for plat in platforms:
            if player.colliderect(plat) and player_vel_y >= 0:
                player.bottom = plat.top
                player_vel_y = 0
                on_ground = True

        # Floor collision
        if player.bottom >= HEIGHT - 60:
            player.bottom = HEIGHT - 60
            player_vel_y = 0
            on_ground = True

        # Collision with enemy
        if player.colliderect(enemy):
            health -= 1
            player.x = WIDTH//2  # Reset player position
            player.y = HEIGHT - 60
            player_vel_y = 0
            if health <= 0:
                game_over = True

        # Score: increase for staying alive each frame
        score += 1

    # Draw player and enemy
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, enemy)

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat)

    # Draw on-screen buttons
    pygame.draw.rect(screen, GREEN, left_button)
    pygame.draw.rect(screen, GREEN, right_button)
    pygame.draw.rect(screen, YELLOW, jump_button)
    draw_text("←", font, WHITE, left_button.centerx, left_button.centery)
    draw_text("→", font, WHITE, right_button.centerx, right_button.centery)
    draw_text("↑", font, WHITE, jump_button.centerx, jump_button.centery)

    # Draw score and health
    draw_text(f"Score: {score}", font, BLACK, 10, 10, center=False)
    draw_text(f"Health: {health}", font, RED, WIDTH - 10, 10, center=False)

    # Game over screen
    if game_over:
        draw_text("GAME OVER", font, RED, WIDTH//2, HEIGHT//2 - 20)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH//2, HEIGHT//2 - 70)
        restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_btn)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(60)

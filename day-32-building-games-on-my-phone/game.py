import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 32: Collision Demo 🟦🟥")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)

# Floor setup
FLOOR_Y = HEIGHT - 100

# Player setup
player_size = 40
player_speed = 5
player = pygame.Rect(100, FLOOR_Y - player_size, player_size, player_size)

# Enemy setup (static on the same floor)
enemy_size = 40
enemy = pygame.Rect(WIDTH - 150, FLOOR_Y - enemy_size, enemy_size, enemy_size)

# On-screen button setup
button_size = 80
left_button = pygame.Rect(10, HEIGHT - button_size - 10, button_size, button_size)
right_button = pygame.Rect(WIDTH - button_size - 10, HEIGHT - button_size - 10, button_size, button_size)

# Game variables
score = 0
game_over = False

# Helper function to draw text
def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

# Reset game function
def reset_game():
    global player, score, game_over
    player.x = 100
    player.y = FLOOR_Y - player_size
    score = 0
    game_over = False

# Game loop
while True:
    screen.fill(WHITE)

    # Draw floor
    pygame.draw.rect(screen, BLACK, (0, FLOOR_Y, WIDTH, 5))

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

        # Restart button
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
            if restart_btn.collidepoint(mouse_pos):
                reset_game()

    # Keyboard controls
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

    # Check collision
    if player.colliderect(enemy) and not game_over:
        game_over = True

    # Draw player and enemy
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, enemy)

    # Draw on-screen buttons
    pygame.draw.rect(screen, GREEN, left_button)
    pygame.draw.rect(screen, GREEN, right_button)
    draw_text("←", font, WHITE, left_button.centerx, left_button.centery)
    draw_text("→", font, WHITE, right_button.centerx, right_button.centery)

    # Draw score
    draw_text(f"Score: {score}", font, BLACK, 10, 10, center=False)

    # Game Over screen
    if game_over:
        draw_text("collision detected ✅", font, RED, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH // 2, HEIGHT // 2 - 70)
        restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_btn)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(60)

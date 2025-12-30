import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 20: Gravity Demo")

# Clock for controlling FPS
clock = pygame.time.Clock()
FPS = 60

# Player properties
player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = 100
y_speed = 0           # Vertical speed
gravity = 0.5         # Gravity acceleration
jump_speed = -10      # Jump velocity
ground_level = HEIGHT - 100  # Ground Y position

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player_y + player_height >= ground_level:
        y_speed = jump_speed

    # Apply gravity
    y_speed += gravity
    player_y += y_speed

    # Ground collision
    if player_y + player_height >= ground_level:
        player_y = ground_level - player_height
        y_speed = 0

    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, ground_level, WIDTH, HEIGHT - ground_level))

    # Draw player
    pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))

    # Update display
    pygame.display.update()

pygame.quit()
sys.exit()

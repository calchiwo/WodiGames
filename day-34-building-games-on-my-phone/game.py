import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 34: Animations Demo 🟦🟥")

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

# Player setup
player_width, player_height = 40, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 60
player_speed = 5
player_vel_y = 0
jump_force = -12
gravity = 0.6
on_ground = True

player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Animation frames (simple colored rects for demo)
walk_frames = [pygame.Surface((player_width, player_height)) for _ in range(2)]
for i, frame in enumerate(walk_frames):
    frame.fill((0, 0, 255 - i*50))  # slightly different shades for demo
jump_frame = pygame.Surface((player_width, player_height))
jump_frame.fill((0, 100, 255))

current_frame = 0
frame_timer = 0

# Platforms
platforms = [pygame.Rect(100, HEIGHT - 150, 400, 20)]

# Enemy setup (static)
enemy_size = 40
enemy = pygame.Rect(WIDTH - enemy_size - 50, HEIGHT - enemy_size - 60, enemy_size, enemy_size)

# Buttons - moved lower
button_size = 80
button_offset = 10  # distance from bottom
left_button = pygame.Rect(10, HEIGHT - button_size - button_offset, button_size, button_size)
right_button = pygame.Rect(WIDTH - button_size - 10, HEIGHT - button_size - button_offset, button_size, button_size)
jump_button = pygame.Rect(WIDTH//2 - button_size//2, HEIGHT - button_size - button_offset, button_size, button_size)

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

# Reset game
def reset_game():
    global player_rect, player_vel_y, score, game_over, on_ground
    player_rect.x = WIDTH // 2
    player_rect.y = HEIGHT - player_height - 60
    player_vel_y = 0
    score = 0
    game_over = False
    on_ground = True

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            if left_button.collidepoint(mouse_pos):
                player_rect.x -= player_speed
            if right_button.collidepoint(mouse_pos):
                player_rect.x += player_speed
            if jump_button.collidepoint(mouse_pos) and on_ground:
                player_vel_y = jump_force
                on_ground = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
            if restart_btn.collidepoint(mouse_pos):
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = jump_force
            on_ground = False

    # Gravity
    player_vel_y += gravity
    player_rect.y += player_vel_y

    # Platform collision
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat) and player_vel_y >= 0:
            player_rect.bottom = plat.top
            player_vel_y = 0
            on_ground = True

    # Floor collision
    if player_rect.bottom > HEIGHT - 60:
        player_rect.bottom = HEIGHT - 60
        player_vel_y = 0
        on_ground = True

    # Enemy collision
    if player_rect.colliderect(enemy):
        game_over = True

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat)

    # Draw player animation
    if not on_ground:
        screen.blit(jump_frame, player_rect.topleft)
    else:
        frame_timer += 1
        if frame_timer % 10 == 0:
            current_frame = (current_frame + 1) % len(walk_frames)
        screen.blit(walk_frames[current_frame], player_rect.topleft)

    # Draw enemy
    pygame.draw.rect(screen, RED, enemy)

    # Draw buttons
    pygame.draw.rect(screen, GREEN, left_button)
    pygame.draw.rect(screen, GREEN, right_button)
    pygame.draw.rect(screen, GREEN, jump_button)
    draw_text("←", font, WHITE, left_button.centerx, left_button.centery)
    draw_text("→", font, WHITE, right_button.centerx, right_button.centery)
    draw_text("↑", font, WHITE, jump_button.centerx, jump_button.centery)

    # Draw score
    draw_text(f"Score: {score}", font, BLACK, 10, 10, center=False)

    # Game over screen
    if game_over:
        draw_text("GAME OVER", font, RED, WIDTH//2, HEIGHT//2 - 20)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH//2, HEIGHT//2 - 70)
        restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_btn)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(60)

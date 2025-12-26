import pygame
import random
import sys

pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 31: Collisions & Gravity")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- Colors ---
WHITE = (255, 255, 255)
BLUE = (50, 120, 255)
RED = (255, 60, 60)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# --- Game Variables ---
gravity = 0.8
jump_strength = -14
player_speed = 6
enemy_speed = 5

# --- Player Setup ---
player_size = 40
player = pygame.Rect(WIDTH//2, HEIGHT-100, player_size, player_size)
player_vel_y = 0
on_ground = True

# --- Enemies ---
enemy_size = 40
enemies = [pygame.Rect(random.randint(0, WIDTH-enemy_size), -i*150, enemy_size, enemy_size) for i in range(5)]

# --- Buttons ---
btn_w, btn_h = 80, 80
left_btn = pygame.Rect(30, HEIGHT-btn_h-30, btn_w, btn_h)
right_btn = pygame.Rect(130, HEIGHT-btn_h-30, btn_w, btn_h)
jump_btn = pygame.Rect(WIDTH-110, HEIGHT-btn_h-30, btn_w, btn_h)

# --- Game State ---
score = 0
game_over = False

# --- Helper Functions ---
def reset_game():
    global player, player_vel_y, on_ground, enemies, score, game_over
    player.x = WIDTH//2
    player.y = HEIGHT-100
    player_vel_y = 0
    on_ground = True
    enemies = [pygame.Rect(random.randint(0, WIDTH-enemy_size), -i*150, enemy_size, enemy_size) for i in range(5)]
    score = 0
    game_over = False

def draw_buttons():
    pygame.draw.rect(screen, GREY, left_btn, border_radius=15)
    pygame.draw.rect(screen, GREY, right_btn, border_radius=15)
    pygame.draw.rect(screen, GREY, jump_btn, border_radius=15)
    screen.blit(font.render("◀", True, BLACK), (left_btn.x+25, left_btn.y+25))
    screen.blit(font.render("▶", True, BLACK), (right_btn.x+25, right_btn.y+25))
    screen.blit(font.render("⬆", True, BLACK), (jump_btn.x+25, jump_btn.y+25))

# --- Main Loop ---
running = True
while running:
    screen.fill(WHITE)
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_game()

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()

    # --- Handle input ---
    move_left = keys[pygame.K_LEFT] or (mouse[0] and left_btn.collidepoint(mx, my))
    move_right = keys[pygame.K_RIGHT] or (mouse[0] and right_btn.collidepoint(mx, my))
    jump_pressed = (keys[pygame.K_SPACE] or (mouse[0] and jump_btn.collidepoint(mx, my)))

    if not game_over:
        # Horizontal movement
        if move_left:
            player.x -= player_speed
        if move_right:
            player.x += player_speed

        # Gravity
        player_vel_y += gravity
        player.y += player_vel_y

        # Ground collision
        ground_y = HEIGHT - 60
        if player.bottom >= ground_y:
            player.bottom = ground_y
            player_vel_y = 0
            on_ground = True
        else:
            on_ground = False

        # Jump
        if jump_pressed and on_ground:
            player_vel_y = jump_strength
            on_ground = False

        # Enemies fall
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemy.x = random.randint(0, WIDTH-enemy_size)
                enemy.y = random.randint(-300, -40)

        # Collision detection
        for enemy in enemies:
            if player.colliderect(enemy):
                game_over = True

        # Scoring
        score += 1

    # --- Draw ---
    pygame.draw.rect(screen, BLUE, player)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    draw_buttons()

    # --- HUD ---
    if not game_over:
        text = font.render(f"Score: {score//10}", True, BLACK)
        screen.blit(text, (20, 20))
    else:
        over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Tap anywhere to restart", True, BLACK)
        screen.blit(over_text, (WIDTH//2 - 100, HEIGHT//2 - 40))
        screen.blit(restart_text, (WIDTH//2 - 170, HEIGHT//2 + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()

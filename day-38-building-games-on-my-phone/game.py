import pygame
import sys

pygame.init()

# Full-screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Day 38 - Obstacles & Bump Blast 🚀")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

GRID_SIZE = 40
GAME_TOP = 80
GAME_BOTTOM = HEIGHT // 2 - 60
GAME_HEIGHT = GAME_BOTTOM - GAME_TOP

# Obstacles
obstacles = [
    pygame.Rect(200, GAME_TOP + 50, GRID_SIZE, GRID_SIZE),
    pygame.Rect(400, GAME_TOP + 150, GRID_SIZE, GRID_SIZE),
    pygame.Rect(600, GAME_TOP + 100, GRID_SIZE, GRID_SIZE),
    pygame.Rect(800, GAME_TOP + 200, GRID_SIZE, GRID_SIZE),
]
obstacle_flash = [0 for _ in obstacles]  # Timer for flash effect

# Player
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = BLUE
        self.speed = GRID_SIZE
        self.score = 0
        self.bump_timer = 0

    def move(self, dx, dy):
        self.rect.x += dx * GRID_SIZE
        self.rect.y += dy * GRID_SIZE
        self.score += 1

    def draw(self, surface):
        color = YELLOW if self.bump_timer > 0 else self.color
        pygame.draw.rect(surface, color, self.rect)
        if self.bump_timer > 0:
            self.bump_timer -= 1

player = Player(WIDTH // 2, GAME_TOP + GAME_HEIGHT // 2)

# Buttons
button_size = 90
button_spacing = 25
button_y_center = HEIGHT // 2 + 80
left_button = pygame.Rect(WIDTH//2 - button_size*2 - button_spacing, button_y_center, button_size, button_size)
right_button = pygame.Rect(WIDTH//2 + button_size + button_spacing, button_y_center, button_size, button_size)
up_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center - button_size - 15, button_size, button_size)
down_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center + button_size + 15, button_size, button_size)

move_left = move_right = move_up = move_down = False
game_over = False

# Text helper
def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    rect = label.get_rect()
    rect.center = (x, y) if center else (x, y)
    screen.blit(label, rect)

def reset_game():
    global player, game_over, obstacle_flash
    player.rect.x = WIDTH // 2
    player.rect.y = GAME_TOP + GAME_HEIGHT // 2
    player.score = 0
    game_over = False
    obstacle_flash = [0 for _ in obstacles]

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not game_over:
                move_left = left_button.collidepoint(pos)
                move_right = right_button.collidepoint(pos)
                move_up = up_button.collidepoint(pos)
                move_down = down_button.collidepoint(pos)
            else:
                restart_btn = pygame.Rect(WIDTH//2 - 100, GAME_TOP + GAME_HEIGHT//2 + 60, 200, 60)
                if restart_btn.collidepoint(pos):
                    reset_game()
        if event.type == pygame.MOUSEBUTTONUP:
            move_left = move_right = move_up = move_down = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update player
    if not game_over:
        dx = dy = 0
        if move_left: dx = -1
        if move_right: dx = 1
        if move_up: dy = -1
        if move_down: dy = 1
        if dx != 0 or dy != 0:
            player.move(dx, dy)

        # Boundary collision
        if player.rect.left < 0 or player.rect.right > WIDTH or player.rect.top < GAME_TOP or player.rect.bottom > GAME_BOTTOM:
            player.bump_timer = 5
            game_over = True

        # Obstacle collisions
        for i, obs in enumerate(obstacles):
            if player.rect.colliderect(obs):
                player.bump_timer = 5
                obstacle_flash[i] = 5  # Flash obstacle
                game_over = True
                break

    # Draw gameplay area with pulsing glow
    glow_alpha = 50 + int(50 * (pygame.time.get_ticks() % 1000) / 1000)
    glow_surf = pygame.Surface((WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (0, 255, 255, glow_alpha), (0, 0, WIDTH, GAME_HEIGHT), 6)
    screen.blit(glow_surf, (0, GAME_TOP))

    # Draw obstacles with flash
    for i, obs in enumerate(obstacles):
        color = ORANGE if obstacle_flash[i] > 0 else RED
        pygame.draw.rect(screen, color, obs)
        if obstacle_flash[i] > 0:
            obstacle_flash[i] -= 1

    # Draw player
    player.draw(screen)

    # Score animation
    score_color = ORANGE if pygame.time.get_ticks() % 500 < 250 else BLACK
    draw_text(f"Score: {player.score}", font, score_color, 10, 10, center=False)

    # Draw buttons with pop effect
    for btn, label, moving in [
        (left_button, "←", move_left), (right_button, "→", move_right),
        (up_button, "↑", move_up), (down_button, "↓", move_down)
    ]:
        pygame.draw.rect(screen, DARK_GREEN, btn, border_radius=12)
        draw_text(label, font, WHITE, btn.centerx, btn.centery)
        if moving:
            pygame.draw.rect(screen, GREEN, btn.inflate(20, 20), border_radius=12, width=3)

    # Game over screen
    if game_over:
        draw_text("GAME OVER", big_font, RED, WIDTH//2, GAME_TOP + GAME_HEIGHT//2 - 30)
        draw_text(f"Final Score: {player.score}", font, BLACK, WIDTH//2, GAME_TOP + GAME_HEIGHT//2 + 10)
        restart_btn = pygame.Rect(WIDTH//2 - 100, GAME_TOP + GAME_HEIGHT//2 + 60, 200, 60)
        pygame.draw.rect(screen, GREEN, restart_btn, border_radius=10)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(15)  # faster for energy

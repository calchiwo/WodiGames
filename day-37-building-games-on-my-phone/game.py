import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Full-screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Day 37: Obstacle Interaction Demo")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
OBSTACLE_COLOR = (200, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# Grid size
GRID_SIZE = 40

# Gameplay area (top region)
GAME_TOP = 80
GAME_BOTTOM = HEIGHT // 2 - 60
GAME_HEIGHT = GAME_BOTTOM - GAME_TOP

# Player class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = BLUE
        self.speed = GRID_SIZE
        self.score = 0

    def move(self, dx, dy):
        self.rect.x += dx * GRID_SIZE
        self.rect.y += dy * GRID_SIZE
        self.score += 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Generate obstacles
NUM_OBSTACLES = 5
obstacles = []
for _ in range(NUM_OBSTACLES):
    ox = random.randint(0, WIDTH//GRID_SIZE - 1) * GRID_SIZE
    oy = random.randint(GAME_TOP//GRID_SIZE, (GAME_BOTTOM//GRID_SIZE) - 1) * GRID_SIZE
    obstacles.append(pygame.Rect(ox, oy, GRID_SIZE, GRID_SIZE))

# Player starts centered in gameplay zone
player = Player(WIDTH // 2, GAME_TOP + GAME_HEIGHT // 2)

# On-screen buttons (center area)
button_size = 90
button_spacing = 25
button_y_center = HEIGHT // 2 + 80

left_button = pygame.Rect(WIDTH//2 - button_size*2 - button_spacing, button_y_center, button_size, button_size)
right_button = pygame.Rect(WIDTH//2 + button_size + button_spacing, button_y_center, button_size, button_size)
up_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center - button_size - 15, button_size, button_size)
down_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center + button_size + 15, button_size, button_size)

# Movement flags
move_left = move_right = move_up = move_down = False
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
    global player, game_over, obstacles
    player.rect.x = WIDTH // 2
    player.rect.y = GAME_TOP + GAME_HEIGHT // 2
    player.score = 0
    game_over = False
    # Regenerate obstacles
    obstacles.clear()
    for _ in range(NUM_OBSTACLES):
        ox = random.randint(0, WIDTH//GRID_SIZE - 1) * GRID_SIZE
        oy = random.randint(GAME_TOP//GRID_SIZE, (GAME_BOTTOM//GRID_SIZE) - 1) * GRID_SIZE
        obstacles.append(pygame.Rect(ox, oy, GRID_SIZE, GRID_SIZE))

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
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
                # Restart button
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
        if move_left:
            dx = -1
        if move_right:
            dx = 1
        if move_up:
            dy = -1
        if move_down:
            dy = 1
        if dx != 0 or dy != 0:
            player.move(dx, dy)

        # Game over if player hits gameplay boundaries
        if (player.rect.left < 0 or player.rect.right > WIDTH or
            player.rect.top < GAME_TOP or player.rect.bottom > GAME_BOTTOM):
            game_over = True

        # Check collisions with obstacles
        for obs in obstacles:
            if player.rect.colliderect(obs):
                game_over = True
                break

    # Draw gameplay area outline
    pygame.draw.rect(screen, (220, 220, 220), (0, GAME_TOP, WIDTH, GAME_HEIGHT), 2)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obs)

    # Draw player
    player.draw(screen)

    # Draw score
    draw_text(f"Score: {player.score}", font, BLACK, 10, 10, center=False)

    # Draw on-screen buttons
    for btn, label in [
        (left_button, "←"), (right_button, "→"),
        (up_button, "↑"), (down_button, "↓")
    ]:
        color = DARK_GREEN
        if ((btn == left_button and move_left) or
            (btn == right_button and move_right) or
            (btn == up_button and move_up) or
            (btn == down_button and move_down)):
            color = GREEN  # Brighten when pressed
        pygame.draw.rect(screen, color, btn, border_radius=12)
        draw_text(label, font, WHITE, btn.centerx, btn.centery)

    # Game over screen
    if game_over:
        draw_text("GAME OVER", big_font, RED, WIDTH//2, GAME_TOP + GAME_HEIGHT//2 - 30)
        draw_text(f"Final Score: {player.score}", font, BLACK, WIDTH//2, GAME_TOP + GAME_HEIGHT//2 + 10)
        restart_btn = pygame.Rect(WIDTH//2 - 100, GAME_TOP + GAME_HEIGHT//2 + 60, 200, 60)
        pygame.draw.rect(screen, GREEN, restart_btn, border_radius=10)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(10)

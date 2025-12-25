import pygame
import sys
import random

pygame.init()

# Full-screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Day 41 - Shooting Game 🚀")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 150)

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# Grid setup
GRID_SIZE = 40
GAME_TOP = 80
GAME_BOTTOM = HEIGHT // 2 - 60
GAME_HEIGHT = GAME_BOTTOM - GAME_TOP

# Player setup
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = GREEN
        self.speed = GRID_SIZE
        self.bump_timer = 0

    def move(self, dx, dy):
        self.rect.x += dx * GRID_SIZE
        self.rect.y += dy * GRID_SIZE

    def draw(self, surface):
        color = YELLOW if self.bump_timer > 0 else self.color
        pygame.draw.rect(surface, color, self.rect)
        if self.bump_timer > 0:
            self.bump_timer -= 1

player = Player(WIDTH // 2, GAME_TOP + GAME_HEIGHT // 2)

# Enemy setup
class Enemy:
    def __init__(self):
        side = random.choice(['top','bottom','left','right'])
        if side == 'top':
            self.rect = pygame.Rect(random.randint(0, WIDTH - GRID_SIZE), GAME_TOP, GRID_SIZE, GRID_SIZE)
            self.vx, self.vy = 0, random.randint(1,2)
        elif side == 'bottom':
            self.rect = pygame.Rect(random.randint(0, WIDTH - GRID_SIZE), GAME_BOTTOM - GRID_SIZE, GRID_SIZE, GRID_SIZE)
            self.vx, self.vy = 0, -random.randint(1,2)
        elif side == 'left':
            self.rect = pygame.Rect(0, random.randint(GAME_TOP, GAME_BOTTOM - GRID_SIZE), GRID_SIZE, GRID_SIZE)
            self.vx, self.vy = random.randint(1,2), 0
        else:  # right
            self.rect = pygame.Rect(WIDTH - GRID_SIZE, random.randint(GAME_TOP, GAME_BOTTOM - GRID_SIZE), GRID_SIZE, GRID_SIZE)
            self.vx, self.vy = -random.randint(1,2), 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

enemies = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000)  # spawn an enemy every second

# Bullet setup
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.vy = -5

    def update(self):
        self.rect.y += self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

bullets = []

# On-screen buttons
button_size = 90
button_spacing = 25
button_y_center = HEIGHT // 2 + 80

left_button = pygame.Rect(WIDTH//2 - button_size*2 - button_spacing, button_y_center, button_size, button_size)
right_button = pygame.Rect(WIDTH//2 + button_size + button_spacing, button_y_center, button_size, button_size)
up_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center - button_size - 15, button_size, button_size)
down_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center + button_size + 15, button_size, button_size)
shoot_button = pygame.Rect(WIDTH//2 - button_size//2, button_y_center, button_size, button_size)

move_left = move_right = move_up = move_down = shoot = False
score = 0
game_over = False

def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

def reset_game():
    global player, enemies, bullets, score, game_over
    player.rect.x = WIDTH // 2
    player.rect.y = GAME_TOP + GAME_HEIGHT // 2
    enemies = []
    bullets = []
    score = 0
    game_over = False

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_EVENT and not game_over:
            enemies.append(Enemy())
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not game_over:
                move_left = left_button.collidepoint(pos)
                move_right = right_button.collidepoint(pos)
                move_up = up_button.collidepoint(pos)
                move_down = down_button.collidepoint(pos)
                shoot = shoot_button.collidepoint(pos)
                if shoot:
                    bullets.append(Bullet(player.rect.centerx-5, player.rect.top))
            else:
                restart_btn = pygame.Rect(WIDTH//2 - 100, GAME_TOP + GAME_HEIGHT//2 + 60, 200, 60)
                if restart_btn.collidepoint(pos):
                    reset_game()
        if event.type == pygame.MOUSEBUTTONUP:
            move_left = move_right = move_up = move_down = shoot = False
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
        if (player.rect.left < 0 or player.rect.right > WIDTH or
            player.rect.top < GAME_TOP or player.rect.bottom > GAME_BOTTOM):
            game_over = True

        # Update bullets
        for b in bullets[:]:
            b.update()
            if b.rect.bottom < GAME_TOP:
                bullets.remove(b)

        # Update enemies
        for e in enemies[:]:
            e.update()
            # Collision with player
            if player.rect.colliderect(e.rect):
                player.bump_timer = 5
                game_over = True
            # Collision with bullets
            for b in bullets[:]:
                if e.rect.colliderect(b.rect):
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1
                    break

    # Draw gameplay area
    pygame.draw.rect(screen, (200, 200, 255), (0, GAME_TOP, WIDTH, GAME_HEIGHT), 4)

    # Draw enemies
    for e in enemies:
        e.draw(screen)

    # Draw bullets
    for b in bullets:
        b.draw(screen)

    # Draw player
    player.draw(screen)

    # Draw score
    draw_text(f"Score: {score}", font, ORANGE, 10, 10, center=False)

    # Draw on-screen buttons
    for btn, label in [
        (left_button, "←"), (right_button, "→"),
        (up_button, "↑"), (down_button, "↓"),
        (shoot_button, "●")
    ]:
        pygame.draw.rect(screen, DARK_GREEN, btn, border_radius=12)
        draw_text(label, font, WHITE, btn.centerx, btn.centery)
        if ((btn == left_button and move_left) or
            (btn == right_button and move_right) or
            (btn == up_button and move_up) or
            (btn == down_button and move_down) or
            (btn == shoot_button and shoot)):
            pygame.draw.rect(screen, GREEN, btn.inflate(15, 15), border_radius=12, width=3)

    # Game over screen
    if game_over:
        draw_text("GAME OVER", big_font, RED, WIDTH//2, GAME_TOP + GAME_HEIGHT//2 - 30)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH//2, GAME_TOP + GAME_HEIGHT//2 + 10)
        restart_btn = pygame.Rect(WIDTH//2 - 100, GAME_TOP + GAME_HEIGHT//2 + 60, 200, 60)
        pygame.draw.rect(screen, GREEN, restart_btn, border_radius=10)
        draw_text("Restart", font, WHITE, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(30)

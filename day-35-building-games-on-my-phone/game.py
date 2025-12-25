import pygame
import sys

pygame.init()

# === Screen setup ===
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 35: Player Class Upgrade 🚀")
clock = pygame.time.Clock()

# === Colors ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# === Fonts ===
font = pygame.font.SysFont(None, 36)

# === Physics ===
GRAVITY = 0.6

# === Platforms ===
platforms = [pygame.Rect(100, HEIGHT - 150, 400, 20)]

# === Buttons ===
button_size = 80
button_y = HEIGHT - button_size - 30
left_button = pygame.Rect(10, button_y, button_size, button_size)
right_button = pygame.Rect(WIDTH - button_size - 10, button_y, button_size, button_size)
jump_button = pygame.Rect(WIDTH // 2 - button_size // 2, button_y, button_size, button_size)


# === PLAYER CLASS ===
class Player:
    """A class representing the player and their movement/animation logic."""

    def __init__(self, x, y):
        self.width, self.height = 40, 50
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel_y = 0
        self.speed = 5
        self.jump_force = -12
        self.on_ground = False

        # Animation setup
        self.walk_frames = [pygame.Surface((self.width, self.height)) for _ in range(2)]
        for i, frame in enumerate(self.walk_frames):
            frame.fill((0, 0, 255 - i * 50))

        self.jump_frame = pygame.Surface((self.width, self.height))
        self.jump_frame.fill((0, 100, 255))

        self.current_frame = 0
        self.frame_timer = 0

    def handle_input(self, move_left, move_right, jump_pressed):
        if move_left:
            self.rect.x -= self.speed
        if move_right:
            self.rect.x += self.speed
        if jump_pressed and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def check_collisions(self, platforms):
        """Check and resolve collisions with platforms and ground."""
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat) and self.vel_y >= 0:
                self.rect.bottom = plat.top
                self.vel_y = 0
                self.on_ground = True

        # Floor collision
        if self.rect.bottom > HEIGHT - 60:
            self.rect.bottom = HEIGHT - 60
            self.vel_y = 0
            self.on_ground = True

    def update(self, move_left, move_right, jump_pressed, platforms):
        self.handle_input(move_left, move_right, jump_pressed)
        self.apply_gravity()
        self.check_collisions(platforms)

        # Simple walking animation
        if not self.on_ground:
            self.current_frame = 0
        else:
            self.frame_timer += 1
            if self.frame_timer % 10 == 0:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)

    def draw(self, surface):
        if not self.on_ground:
            surface.blit(self.jump_frame, self.rect.topleft)
        else:
            surface.blit(self.walk_frames[self.current_frame], self.rect.topleft)


# === Enemy setup ===
enemy = pygame.Rect(WIDTH - 90, HEIGHT - 100, 40, 40)

# === Player instance ===
player = Player(WIDTH // 2, HEIGHT - 100)

# === Game state ===
move_left = move_right = jump_pressed = False
game_over = False


# === Helper Functions ===
def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y)) if center else label.get_rect(topleft=(x, y))
    screen.blit(label, rect)


def draw_ui():
    # Buttons
    pygame.draw.rect(screen, GREEN, left_button)
    pygame.draw.rect(screen, GREEN, right_button)
    pygame.draw.rect(screen, GREEN, jump_button)

    draw_text("←", font, WHITE, *left_button.center)
    draw_text("→", font, WHITE, *right_button.center)
    draw_text("↑", font, WHITE, *jump_button.center)


def reset_game():
    global player, move_left, move_right, jump_pressed, game_over
    player = Player(WIDTH // 2, HEIGHT - 100)
    move_left = move_right = jump_pressed = False
    game_over = False


# === MAIN GAME LOOP ===
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if left_button.collidepoint(pos):
                move_left = True
            if right_button.collidepoint(pos):
                move_right = True
            if jump_button.collidepoint(pos):
                jump_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            move_left = move_right = jump_pressed = False

    # === Game logic ===
    if not game_over:
        player.update(move_left, move_right, jump_pressed, platforms)

        # Check enemy collision
        if player.rect.colliderect(enemy):
            game_over = True

    # === Draw everything ===
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat)

    pygame.draw.rect(screen, RED, enemy)
    player.draw(screen)
    draw_ui()

    if game_over:
        draw_text("GAME OVER", font, RED, WIDTH // 2, HEIGHT // 2 - 20)
        restart_btn = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_btn)
        draw_text("Restart", font, WHITE, *restart_btn.center)

        # Restart logic
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if restart_btn.collidepoint(mouse_pos) and mouse_pressed[0]:
            reset_game()

    pygame.display.flip()
    clock.tick(60)

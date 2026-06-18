import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Lunar Lander Simulation")
clock = pygame.time.Clock()

# Color Palette
SPACE_BLACK = (10, 10, 15)
MOON_GRAY = (140, 140, 145)
LANDER_WHITE = (240, 240, 245)
THRUST_ORANGE = (255, 120, 30)
PAD_GREEN = (50, 220, 90)
TEXT_WHITE = (255, 255, 255)
CRASH_RED = (240, 50, 50)

# Game Font
font = pygame.font.SysFont("Courier", 20, bold=True)


class Lander:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 50
        self.vy = 0.0  # Vertical velocity
        self.vx = 0.0  # Horizontal velocity
        self.gravity = 0.04
        self.thrust = 0.12
        self.fuel = 800
        self.width = 24
        self.height = 24
        self.is_thrusting = False

    def update(self):
        # Always apply gravity downwards
        self.vy += self.gravity

        # Check for keyboard inputs
        keys = pygame.key.get_pressed()
        self.is_thrusting = False

        if self.fuel > 0:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vy -= self.thrust
                self.fuel -= 2
                self.is_thrusting = True
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vx -= self.thrust * 0.5
                self.fuel -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vx += self.thrust * 0.5
                self.fuel -= 1

        # Update absolute positioning matrix coordinates
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        # Draw the main module hull
        lander_rect = pygame.Rect(int(self.x - self.width // 2), int(self.y - self.height // 2), self.width,
                                  self.height)
        pygame.draw.rect(screen, LANDER_WHITE, lander_rect, border_radius=3)

        # Draw support landing legs
        pygame.draw.line(screen, MOON_GRAY, (int(self.x - 12), int(self.y + 12)), (int(self.x - 18), int(self.y + 20)),
                         2)
        pygame.draw.line(screen, MOON_GRAY, (int(self.x + 12), int(self.y + 12)), (int(self.x + 18), int(self.y + 20)),
                         2)

        # Draw engine flame if thrusting engine is firing
        if self.is_thrusting and self.fuel > 0:
            pygame.draw.polygon(screen, THRUST_ORANGE, [
                (int(self.x - 6), int(self.y + 12)),
                (int(self.x + 6), int(self.y + 12)),
                (int(self.x), int(self.y + 12 + random.randint(10, 22)))
            ])


# Target Platform landing coordinates setup configuration
pad_width = 80
pad_x = random.randint(100, WIDTH - 100 - pad_width)
pad_y = HEIGHT - 40
pad_rect = pygame.Rect(pad_x, pad_y, pad_width, 12)

# Initial Setup Instantiation
lander = Lander()
game_state = "FLYING"  # Options: FLYING, LANDED, CRASHED

# Main Physics Engine Loop Execution
running = True
while running:
    clock.tick(60)
    screen.fill(SPACE_BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_state != "FLYING":
            if event.key == pygame.K_SPACE:
                # Full system simulation restart loop
                lander = Lander()
                pad_x = random.randint(100, WIDTH - 100 - pad_width)
                pad_rect.x = pad_x
                game_state = "FLYING"

    if game_state == "FLYING":
        lander.update()

        # Check for lunar surface target landing pad intersection
        lander_bottom = lander.y + 20
        lander_left = lander.x - 18
        lander_right = lander.x + 18

        if lander_bottom >= pad_y:
            # Check if lander completely overlaps horizontally within pad surface area bounds
            if lander_left >= pad_rect.left and lander_right <= pad_rect.right:
                # Check for critical impact landing velocity requirements (Safe limit threshold < 1.5)
                if abs(lander.vy) <= 1.5 and abs(lander.vx) <= 1.0:
                    game_state = "LANDED"
                else:
                    game_state = "CRASHED"
            else:
                # Missed landing target pad entirely
                game_state = "CRASHED"

        # Edge constraint wraps or boundaries checks
        if lander.x < 0 or lander.x > WIDTH or lander.y > HEIGHT:
            game_state = "CRASHED"

    # Draw Environmental Elements
    # Draw Surface Ground Line
    pygame.draw.line(screen, MOON_GRAY, (0, HEIGHT - 28), (WIDTH, HEIGHT - 28), 4)
    # Draw safe Designated green zone targets
    pygame.draw.rect(screen, PAD_GREEN, pad_rect)

    # Draw Lander module vehicle
    lander.draw()

    # Draw HUD (Telemetry Instrument Metrics data)
    fuel_txt = font.render(f"FUEL: {max(0, lander.fuel)}", True, TEXT_WHITE)
    vx_txt = font.render(f"H. VELOCITY: {lander.vx:.2f}", True, TEXT_WHITE)
    # Highlight dangerous vertical speeds in red
    vy_color = CRASH_RED if abs(lander.vy) > 1.5 else PAD_GREEN
    vy_txt = font.render(f"V. VELOCITY: {lander.vy:.2f} (MAX Safe: 1.50)", True, vy_color)

    screen.blit(fuel_txt, (20, 20))
    screen.blit(vx_txt, (20, 45))
    screen.blit(vy_txt, (20, 70))

    # Handle Terminal Overlay Display Screens
    if game_state == "LANDED":
        win_msg = font.render("THE chandrayaan 2 HAS LANDED! Press SPACE to Launch Next Wave", True, PAD_GREEN)
        screen.blit(win_msg, (WIDTH // 2 - 310, HEIGHT // 2))
    elif game_state == "CRASHED":
        lose_msg = font.render("HULL INTEGRITY COMPROMISED! Press SPACE to Restart", True, CRASH_RED)
        screen.blit(lose_msg, (WIDTH // 2 - 280, HEIGHT // 2))

    pygame.display.update()

pygame.quit()
# task - snake game

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Python Game")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()














# task - snake game
import pygame
import random
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)

# 3. Set up the display screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Progressive Speed Snake Game")
clock = pygame.time.Clock()


# 4. Game Variables Setup
def reset_game():
    global snake, snake_dir, food, score, game_over, current_speed
    # Snake starts in the middle
    snake = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
    snake_dir = (GRID_SIZE, 0)  # Starts moving to the right
    food = spawn_food()
    score = 0
    game_over = False
    current_speed = 6  # 🟢 NEW: Starts nice and slow (6 blocks per second)


def spawn_food():
    x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    return [x, y]


# Initialise variables
reset_game()

# 5. Core Game Loop
while True:
    # --- A. EVENT HANDLING (Keyboard Inputs) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
            else:
                # Change direction based on arrows, preventing 180-degree self-collisions
                if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE):
                    snake_dir = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE):
                    snake_dir = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0):
                    snake_dir = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0):
                    snake_dir = (GRID_SIZE, 0)

    # --- B. GAME LOGIC UPDATES ---
    if not game_over:
        # Calculate new position for the snake head
        new_head = [snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1]]

        # Check Collision 1: Walls
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            game_over = True

        # Check Collision 2: Self-collision
        if new_head in snake:
            game_over = True

        if not game_over:
            # Insert the new head position to move forward
            snake.insert(0, new_head)

            # Check Collision 3: Eating Food
            if new_head == food:
                score += 10
                food = spawn_food()  # Don't pop the tail, making the snake grow

                # ⚡ NEW: Increase the speed every time food is eaten!
                # Maximum speed cap is set to 25 so it stays humanly playable.
                if current_speed < 25:
                    current_speed += 1.0  # Adds a noticeable challenge bump
            else:
                snake.pop()  # Remove tail segment to maintain length while traveling

    # --- C. DRAWING GRAPHICS ON SCREEN ---
    screen.fill(COLOR_BLACK)  # Clear screen with black layout

    if game_over:
        # Render Game Over Text
        font = pygame.font.SysFont("Arial", 36)
        text_gameover = font.render(f"GAME OVER! Score: {score}", True, COLOR_WHITE)
        text_restart = font.render("Press SPACE to Play Again", True, COLOR_WHITE)

        screen.blit(text_gameover, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
        screen.blit(text_restart, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2))
    else:
        # Draw Food
        pygame.draw.rect(screen, COLOR_RED, pygame.Rect(food[0], food[1], GRID_SIZE, GRID_SIZE))

        # Draw Snake
        for segment in snake:
            pygame.draw.rect(screen, COLOR_GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        # Draw Score and Speed Dashboard
        font = pygame.font.SysFont("Arial", 20)
        text_score = font.render(f"Score: {score}  |  Speed: {int(current_speed)}", True, COLOR_WHITE)
        screen.blit(text_score, (10, 10))

    # Refresh visual layout
    pygame.display.flip()

    # 🔄 Control Game Speed using the dynamic speed variable
    clock.tick(int(current_speed))

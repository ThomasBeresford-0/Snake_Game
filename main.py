import pygame
import random
from pygame.locals import *
from constants import *

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer for music and sounds
pygame.mixer.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Load background music
pygame.mixer.music.load('background_music.mp3')

# Load sound effects
eat_sound = pygame.mixer.Sound('eat_sound.wav')  # Adjust the filename and path as needed

# Play background music (loop indefinitely)
pygame.mixer.music.play(-1)

# Initialize game variables
INITIAL_SNAKE_X = SCREEN_WIDTH // 2
INITIAL_SNAKE_Y = SCREEN_HEIGHT // 2

snake = [(INITIAL_SNAKE_X, INITIAL_SNAKE_Y)]
snake_direction = K_RIGHT  # Start with right direction
score = 0
food = (random.randint(0, SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE * SNAKE_SIZE,
        random.randint(0, SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE * SNAKE_SIZE)

# Font for displaying text
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    if game_over:
        # Display game over screen
        screen.fill(BLACK)
        game_over_text = font.render("Game Over! Score: {}".format(score), True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(game_over_text, game_over_rect)

        retry_text = font.render("Press 'R' to retry", True, WHITE)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(retry_text, retry_rect)

        quit_text = font.render("Press 'Q' to quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        # Reset variables for new game if retry or quit
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                elif event.key == K_r:
                    score = 0
                    snake = [(INITIAL_SNAKE_X, INITIAL_SNAKE_Y)]
                    snake_direction = K_RIGHT
                    food = (random.randint(0, SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE * SNAKE_SIZE,
                            random.randint(0, SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE * SNAKE_SIZE)
                    game_over = False

        pygame.time.wait(10)  # Small delay to reduce CPU usage

    else:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP and snake_direction != K_DOWN:
                    snake_direction = K_UP
                elif event.key == K_DOWN and snake_direction != K_UP:
                    snake_direction = K_DOWN
                elif event.key == K_LEFT and snake_direction != K_RIGHT:
                    snake_direction = K_LEFT
                elif event.key == K_RIGHT and snake_direction != K_LEFT:
                    snake_direction = K_RIGHT

        # Move snake
        x, y = snake[0]
        if snake_direction == K_UP:
            y -= SNAKE_SIZE
        elif snake_direction == K_DOWN:
            y += SNAKE_SIZE
        elif snake_direction == K_LEFT:
            x -= SNAKE_SIZE
        elif snake_direction == K_RIGHT:
            x += SNAKE_SIZE

        # Check if snake hits boundary
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            game_over = True

        # Check if snake hits itself
        if (x, y) in snake[1:]:
            game_over = True

        # Update snake position
        snake.insert(0, (x, y))
        if x == food[0] and y == food[1]:
            score += 1
            food = (random.randint(0, SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE * SNAKE_SIZE,
                    random.randint(0, SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE * SNAKE_SIZE)
            eat_sound.play()  # Play the eat sound effect when food is eaten
        else:
            snake.pop()

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))  # Red food
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))  # Green snake

        # Display score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(SNAKE_SPEED)

# Stop music when game ends
pygame.mixer.music.stop()

# Quit Pygame
pygame.quit()

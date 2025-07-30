import pygame
import random

# --- Initialization ---
pygame.init()

# --- Screen Settings ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Flappy Bird")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)

# --- Game Variables ---
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
game_over = False
score = 0

# --- Bird Properties ---
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_y_velocity = 0
GRAVITY = 0.5
JUMP_STRENGTH = -8
bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)

# --- Pipe Properties ---
pipe_width = 70
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
pipe_speed = 3
last_pipe_time = pygame.time.get_ticks() - pipe_frequency
pipes = []

def draw_objects():
    """Draws all game elements to the screen."""
    screen.fill(SKY_BLUE)
    # Draw bird
    pygame.draw.rect(screen, YELLOW, bird_rect)
    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

def move_bird():
    """Handles bird movement due to gravity and jumping."""
    global bird_y, bird_y_velocity
    bird_y_velocity += GRAVITY
    bird_y += bird_y_velocity
    bird_rect.y = bird_y

def move_pipes():
    """Moves pipes to the left and removes off-screen pipes."""
    global score
    pipes_to_remove = []
    pipe_passed = False
    
    for pipe in pipes:
        pipe.x -= pipe_speed
        if pipe.right < 0:
            pipes_to_remove.append(pipe)
        
        # Check if bird passed the pipe
        if not pipe_passed and pipe.right < bird_rect.left and pipe.width == pipe_width:
             pipe_passed = True
             score += 1

    for pipe in pipes_to_remove:
        pipes.remove(pipe)
        
def check_collision():
    """Checks for collisions with pipes or screen boundaries."""
    # Check for collision with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    # Check for collision with top/bottom of the screen
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_y_velocity = JUMP_STRENGTH
            if event.key == pygame.K_SPACE and game_over:
                # Reset the game
                bird_y = SCREEN_HEIGHT // 2
                bird_y_velocity = 0
                pipes.clear()
                score = 0
                game_over = False

    if not game_over:
        # --- Bird Movement ---
        move_bird()

        # --- Pipe Generation ---
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > pipe_frequency:
            pipe_height = random.randint(150, SCREEN_HEIGHT - 150)
            top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height - pipe_gap // 2)
            bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap // 2, pipe_width, SCREEN_HEIGHT)
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)
            last_pipe_time = current_time

        # --- Pipe Movement ---
        move_pipes()

        # --- Collision Check ---
        if check_collision():
            game_over = True

        # --- Drawing ---
        draw_objects()

    else:
        # --- Game Over Screen ---
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press Space to Restart", True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.update()


    # --- Frame Rate ---
    clock.tick(60) # Limit frame rate to 60 FPS

pygame.quit()
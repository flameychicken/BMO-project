import pygame
import random
import sys

def run_snake_game():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("BMO Snake Game")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    snake = [(100, 50)]
    direction = (20, 0)
    food = (200, 150)
    score = 0

    def draw():
        screen.fill((0, 0, 0))
        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, 20, 20))
        pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = (0, -20)
                elif event.key == pygame.K_DOWN:
                    direction = (0, 20)
                elif event.key == pygame.K_LEFT:
                    direction = (-20, 0)
                elif event.key == pygame.K_RIGHT:
                    direction = (20, 0)
                elif event.key == pygame.K_ESCAPE:
                    return

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if new_head in snake or not (0 <= new_head[0] < 480 and 0 <= new_head[1] < 320):
            return  # Game over

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = (random.randrange(0, 480, 20), random.randrange(0, 320, 20))
        else:
            snake.pop()

        draw()
        clock.tick(10)
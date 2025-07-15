import pygame
import sys
import os

# Init pygame
pygame.init()
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Virtual BMO")

# Load image
ASSET_PATH = os.path.join("assets", "bmo1.jpg")
try:
    bmo_image = pygame.image.load(ASSET_PATH)
    bmo_image = pygame.transform.scale(bmo_image, (480, 320))
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit(1)

# Display image
def draw_face():
    screen.blit(bmo_image, (0, 0))

# Main loop
running = True
while running:
    draw_face()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
PIZZA_RADIUS = 100
KNIFE_LENGTH = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup the Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knife Hit Game")

# Load Assets
pizza_image = pygame.image.load("pizza.jpg")  # Placeholder for pizza image
pizza_image = pygame.transform.scale(pizza_image, (PIZZA_RADIUS * 2, PIZZA_RADIUS * 2))
knife_image = pygame.image.load("knife.jpg")  # Placeholder for knife image
knife_image = pygame.transform.scale(knife_image, (KNIFE_LENGTH, KNIFE_LENGTH * 3))

# Game Variables
pizza_center = (WIDTH // 2, HEIGHT // 3)
pizza_angle = 0
knives = []  # Stores (angle, x, y) positions of knives
game_over = False

# Main Game Loop
running = True
clock = pygame.time.Clock()


def check_collision(angle):
    for knife in knives:
        if abs((knife[0] - angle) % 360) < 15:
            return True
    return False


while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            new_angle = (pizza_angle + 90) % 360  # Knife enters from bottom
            if check_collision(new_angle):
                game_over = True
            else:
                radian = math.radians(new_angle)
                x = pizza_center[0] + math.cos(radian) * PIZZA_RADIUS
                y = pizza_center[1] - math.sin(radian) * PIZZA_RADIUS
                knives.append((new_angle, x, y))

    if not game_over:
        pizza_angle = (pizza_angle + 2) % 360  # Rotate Pizza

    # Draw Pizza
    rotated_pizza = pygame.transform.rotate(pizza_image, pizza_angle)
    pizza_rect = rotated_pizza.get_rect(center=pizza_center)
    screen.blit(rotated_pizza, pizza_rect.topleft)

    # Draw Knives
    for knife in knives:
        angle, x, y = knife
        rotated_knife = pygame.transform.rotate(knife_image, -angle)
        knife_rect = rotated_knife.get_rect(center=(x, y))
        screen.blit(rotated_knife, knife_rect.topleft)

    # Display Game Over
    if game_over:
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

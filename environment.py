import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

def draw_room(screen):
    # Fill background white
    screen.fill(BLACK)

    wall_thickness = 10

    # Draw top wall (ceiling)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, wall_thickness))

    # Draw bottom wall (floor)
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness))

    # Draw left wall
    pygame.draw.rect(screen, WHITE, (0, 0, wall_thickness, SCREEN_HEIGHT))

    # Draw right wall
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT))

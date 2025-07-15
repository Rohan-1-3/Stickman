import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, STICKMAN_POS_X, STICKMAN_POS_Y
from environment import draw_room
from stickman import Stickman
from utils import sliders, get_stickman_config_from_sliders

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for s in sliders:
            s.update(event)

    stickman_config = get_stickman_config_from_sliders()
    stickman = Stickman(x=STICKMAN_POS_X, y=STICKMAN_POS_Y, config=stickman_config)

    draw_room(screen)
    pygame.draw.rect(screen, (230, 230, 230), (30, 30, 260, 430))  
    for s in sliders:
        s.draw(screen)
    stickman.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, STICKMAN_POS_X, STICKMAN_POS_Y
from environment import draw_room
from stickman import Stickman
from utils import sliders, get_stickman_config_from_sliders

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initial state
simulation_active = False
stickman = Stickman(x=STICKMAN_POS_X, y=STICKMAN_POS_Y, config=get_stickman_config_from_sliders())

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation_active = True
                stickman.is_simulating = True

        # Let sliders update if simulation hasn't started
        if not simulation_active:
            for s in sliders:
                s.update(event)

    # Update stickman config before simulation
    if not simulation_active:
        config = get_stickman_config_from_sliders()
        stickman.config = config
        stickman._parse_config()  # re-parse new values

    # Handle input (arrow key movement)
    keys = pygame.key.get_pressed()
    if stickman.is_simulating:
        stickman.velocity_x = 0
        stickman.velocity_y = 0

        if keys[pygame.K_LEFT]:
            stickman.velocity_x = -stickman.speed
        if keys[pygame.K_RIGHT]:
            stickman.velocity_x = stickman.speed
        if keys[pygame.K_UP]:
            stickman.velocity_y = -stickman.speed
        if keys[pygame.K_DOWN]:
            stickman.velocity_y = stickman.speed

        stickman.update(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Draw environment
    draw_room(screen)

    # Sliders box
    if not simulation_active:
        slider_height = 50
        pygame.draw.rect(screen, (230, 230, 230), (30, 30, 260, len(sliders) * slider_height + 30))
        for s in sliders:
            s.draw(screen)

    # Draw stickman
    stickman.draw(screen)

    # Flip screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
from PSM.PhysicalStateManager import *

# Initialize Physical State Manager with VREP. (Other possibilities are LIVE or NONE)
# At the end of the live cycle poppy returns to its shutdown state so be sure calling
# its __exit__ function
with PhysicalStateManager(SimulationTypes.NONE) as physical_state_manager:

    # for now a game loop so Poppy waits for an ESC to close
    running = True
    pygame.init()
    # pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    my_font = pygame.font.SysFont("arial", 15)
    while running:
        poll_event = pygame.event.poll()

        if poll_event.type == pygame.QUIT:
            running = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                label = my_font.render("Waving!", 1, (255, 255, 0))
                screen.blit(label, (100, 100))
                physical_state_manager.go_to_state(Waving())

    pygame.quit()



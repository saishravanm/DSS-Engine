import sys, pygame


def game_init(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.init()
    pygame.display.flip()

    gameRunning = True
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False

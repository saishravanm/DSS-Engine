import sys, pygame

pygame.init()
surface = pygame.display.set_mode((1920, 1080))
color = (255, 0, 0)


def drawGrid():
    pygame.draw.rect(surface, color, pygame.Rect(0, 0, 100, 100))
    pygame.display.flip()
    
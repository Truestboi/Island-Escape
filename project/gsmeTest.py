import pygame
from pygame.locals import *
import pygameMenu                # This imports classes and other things
from pygameMenu.locals import *

pygame.init()

display_width = 1280
display_height = 720

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Our Game')


def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (
             event.type == KEYDOWN and (
              event.key == K_ESCAPE or
              event.key == K_q
             )):
            pygame.quit()
            quit()



background_image = pygame.image.load("beach.png").convert()

while True:
    event_handler()
    pygameMenu.Menu(surface, window_width, window_height, font, title, *args) # -> Menu object
    screen.blit(background_image, [0, 0])

    pygame.display.update()

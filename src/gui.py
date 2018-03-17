import pygame
import time
import numpy as np

times = []
print_drawing_time = False


def display_screen(screen, gui_clock):
    pygame.display.update()
    # gui_clock.tick(200) # remove this line to boost calculating
    screen.fill((255, 255, 255))    # BACKGROUND
    # actual drawables below
    # rect(50, 50, 50, 50, (255, 0, 0), screen)


def rect(x, y, width, height, color, screen):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))


def draw_image(image, screen):
        # 0 - white, 1 - black
    pixels = image.pixels
    target_pixels = image.compared_picture
    screen.fill((255, 255, 255))    # BACKGROUND
    # displaying the target
    # surf = pygame.surfarray.make_surface(np.array(target_pixels)+10)
    # screen.blit(surf, (0, 0))
    for x in range(image.width):
        for y in range(image.height):
            value = int(pixels[x, y])
            if value != 0:
                screen.set_at((x, y), (value, value, value))

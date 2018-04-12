import pygame
import time
import numpy as np

times = []
print_drawing_time = False
display_target = False
displays = 0


def display(screen, image, scale):
    display_screen(screen, scale)
    draw_image(screen, image, scale)


def display_screen(screen, scale):
    pygame.display.update()
    # gui_clock.tick(200) # remove this line to boost calculating
    screen.fill((255, 255, 255))    # BACKGROUND


def rect(x, y, width, height, color, screen):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))


def draw_image(screen, image, scale):
        # 0 - white, 1 - black
    pixels = image.pixels
    target_pixels = image.compared_picture
    screen.fill((255, 255, 255))    # BACKGROUND

    if display_target:
        surf = pygame.surfarray.make_surface(np.array(target_pixels)+10)
        screen.blit(surf, (0, 0))

    for x in range(image.width):
        for y in range(image.height):
            value = int(pixels[x, y])
            if value <= 255:
                for i in range(scale):
                    for j in range(scale):
                        screen.set_at((scale*x+i, scale*y+j), (value, value, value))
            else:
                for i in range(scale):
                    for j in range(scale):
                        screen.set_at((scale*x+i, scale*y+j), (255, 255, 255))

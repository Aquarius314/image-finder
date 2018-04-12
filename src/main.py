import pygame
import gui
from algorithm import Algorithm
import time


width = 400
height = 400
scale = 2
# 1:    23686, t 153719
# 2:    24597, t 393758 <--
# 5:    21115, t 948539
# 10:   23585, t
# 20:   22303
# 50:   21833
# 100:  19640 for 880it
# 200:  19529 for 450it


def run(screen, clock, alg):
    print("IT'S ON")

    displays = 0
    running = True
    disrupted = False
    capturing = True
    while running and not disrupted:  # main loop
        running = alg.calculate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                disrupted = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    disrupted = True

        if alg.has_best_fitness():
            alg.display_best_fitness()
            pygame.display.set_caption("img" + str(alg.number_of_imgs) + \
                                       " ft" + str(alg.percentage) + \
                                       "% it" + str(alg.iterations))
            if capturing:
                displays += 1
                if displays % 40 == 1:
                    gui.display(screen, alg.get_best_image(), scale)
                    image_file_name = "images/"+str(displays)+"_fitness_"+str(alg.percentage)+".png"
                    pygame.image.save(screen, image_file_name)
                    print("Saved image to " + image_file_name)
            else:
                gui.display(screen, alg.get_best_image(), scale)

        alg.populate_best_images()
        alg.crossover()
    return disrupted

pygame.init()

_clock = pygame.time.Clock()
_screen = pygame.display.set_mode((width*scale, height*scale))
algorithm = Algorithm(width, height)
disr = run(_screen, _clock, algorithm)
pygame.display.set_caption(str(algorithm.percentage) + "% with "
                           + str(algorithm.number_of_imgs) + " after " + str(algorithm.iterations) + " its")
print("FINISHED")
if not disr:
    time.sleep(100000000)
pygame.quit()


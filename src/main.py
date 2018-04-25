import pygame
import gui
from algorithm import Algorithm
import numpy as np
import time
import matplotlib.pyplot as plt

width = 200
height = 200
scale = 3

def run(screen, clock, alg):
    print("IT'S ON")

    fitness_curve = []
    running = True
    disrupted = False
    while running and not disrupted:  # main loop
        running = alg.calculate()
        # alg.calculate()
        # alg.calculate()
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
            gui.display_screen(screen, clock)
            gui.draw_image(alg.get_best_image(), screen, scale)
        current_fitness = (alg.get_best_fitness()/alg.max_fitness)*100
        fitness_curve.append(current_fitness)

        continue_algorithm(alg)

    # display plots
    print(fitness_curve)
    percentages = np.array(fitness_curve[1:])
    label = str(alg.number_of_imgs) + ", time:" + str(alg.total_time) + \
            ", final fitness: " + str(alg.percentage) + ", mutations: " + str(alg.mutations)
    plt.plot(percentages, label=label)
    plt.xlabel("Iterations")
    plt.ylabel("Fitness [%]")
    plt.title("Different mutations rate")
    # plt.show()

    return disrupted


def continue_algorithm(algorithm):
    algorithm.populate_best_images()
    algorithm.crossover()


pygame.init()

_clock = pygame.time.Clock()
_screen = pygame.display.set_mode((width*scale, height*scale))
algorithm1 = Algorithm(width, height, imgs=40, mutations=1)
algorithm3 = Algorithm(width, height, imgs=40, mutations=2)
algorithm4 = Algorithm(width, height, imgs=40, mutations=4)
disr = run(_screen, _clock, algorithm1)
disr = run(_screen, _clock, algorithm3)
disr = run(_screen, _clock, algorithm4)
plt.legend()
plt.show()
# pygame.display.set_caption(str(algorithm.percentage) + "% with "
#                            + str(algorithm.number_of_imgs) + " after " + str(algorithm.iterations) + " its")
print("FINISHED")
# if not disr:
#     time.sleep(100000000)
pygame.quit()


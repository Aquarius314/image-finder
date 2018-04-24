from image import Image
import random
import time
import pygame
import math
import matplotlib.pyplot as plt


class Algorithm:

    best_fitness = -1000000.0
    number_of_imgs = 30
    max_iterations = 500
    number_of_rects = 800
    percentage = 0.00
    target_percentage = 80.00
    total_time = 0

    last_iteration_time = time.time()

    fitness_curve = []

    images = []
    # best_image = None

    def __init__(self, width, height, number_of_imgs):
        self.refresh()
        # self.number_of_rects = int((width+height)/5)
        self.max_fitness = width*height
        self.start_time = time.time()
        self.init_images(width, height)
        self.best_image = self.images[0]
        self.iterations = 0
        self.number_of_imgs = number_of_imgs

    def refresh(self):
        self.best_fitness = -1000000.0
        self.iterations = 0
        self.percentage = 0.00
        self.total_time = 0
        self.fitness_curve = []
        self.images = []

    def init_images(self, width, height):
        for i in range(self.number_of_imgs):
            img = Image(width, height)
            img.put_random_rects(self.number_of_rects)
            self.images.append(img)

    def calculate(self):
        self.iterations += 1
        new_percentage = math.ceil((int(self.best_fitness)/int(self.max_fitness)*100)*100)/100
        percentage_difference = new_percentage - self.percentage
        self.percentage = new_percentage
        time_difference = time.time() - self.last_iteration_time
        self.last_iteration_time = time.time()
        if self.iterations%10 is 0 or self.percentage >= self.target_percentage:
            print("Iterations:", self.iterations)
            pygame.display.set_caption("img" + str(self.number_of_imgs) +
                                       " ft" + str(self.percentage) +
                                       "% it" + str(self.iterations))
            if self.iterations >= self.max_iterations or self.percentage >= self.target_percentage:
                self.total_time = int(time.time()*1000-self.start_time*1000)
                print("Finished after time:", str(self.total_time))
                print("The final fitness was:", str(int(self.best_fitness)))
                return False
            print("Time for 1 iteration: %.2f s after %.2f s, prct improvement: %.2f"
                  % (time_difference, (time.time()-self.start_time), percentage_difference))
        # self.refresh_images()
        self.shake_images()  # ***
        # self.best_fitness = self.get_best_fitness()
        return True

    def shake_images(self):
        for img in self.images:
            img.mutate()

    def refresh_images(self):
        for img in self.images:
            img.refresh()

    def get_fitness(self, img):
        return img.get_fitness()

    def get_best_fitness(self):
        best_of_all = -1000000.0
        for img in self.images:
            fitness = self.get_fitness(img)
            if fitness > best_of_all:
                best_of_all = fitness
                self.best_image = img

        return best_of_all

    def display_best_fitness(self):
        print("Best fitness so far:", self.percentage, "% after iters:",
              self.iterations, "images:", self.number_of_imgs, "rects:", len(self.best_image.rects))

    def has_best_fitness(self):
        fitness = self.get_best_fitness()
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            return True
        else:
            return False

    def get_best_image(self):
        return self.best_image

    def get_first_image(self):
        return self.images[0]

    def populate_best_images(self):
        # sort by fitness desc
        self.images.sort(key=lambda x: x.get_fitness(), reverse=True)

        copy_quarter = True

        if copy_quarter:
            quarter = int(len(self.images)/4)
            for i in range(quarter):
                img = self.images[i]
                self.images[i+1*quarter].overwrite_with(img)
                self.images[i+2*quarter].overwrite_with(img)
                self.images[i+3*quarter].overwrite_with(img)
        else:   # copy only half
            for i in range(int(len(self.images)/2)):
                img = self.images[i]
                self.images[-i-1].overwrite_with(img)

        for i in range(1, len(self.images)):
            self.images[i].mutate()

    def crossover(self):
        min_num_of_rects = 100000
        for img in self.images:
            num_of_rects = len(img.rects)
            if num_of_rects < min_num_of_rects:
                min_num_of_rects = num_of_rects
        mutations = random.randint(int(self.number_of_rects/5) - 5, int(self.number_of_rects/5) + 5)
        for m in range(mutations):
            index = random.randint(0, min_num_of_rects - 1)
            rect1 = self.images[0].rects[index]
            for i in range(len(self.images)-1):
                self.images[i].rects[index] = self.images[i+1].rects[index]
            self.images[-1].rects[index] = rect1

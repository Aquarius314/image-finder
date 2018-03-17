from image import Image
import random
import time
import pygame
import math


class Algorithm:

    best_fitness = -1000000.0
    number_of_imgs = 60
    max_iterations = 10000
    percentage = 0.00
    target_percentage = 98.00

    images = []
    best_image = None

    def __init__(self, width, height):
        self.number_of_rects = int((width+height)/5)
        self.max_fitness = width*height
        self.start_time = time.time()
        self.init_images(width, height)
        self.iterations = 0

    def init_images(self, width, height):
        for i in range(self.number_of_imgs):
            img = Image(width, height)
            img.put_random_rects(self.number_of_rects)
            self.images.append(img)

    def calculate(self):
        self.iterations += 1
        self.percentage = math.ceil((int(self.best_fitness)/int(self.max_fitness)*100)*100)/100
        if self.iterations%10 is 0 or self.percentage >= self.target_percentage:
            print("Iterations:", self.iterations)
            pygame.display.set_caption("img" + str(self.number_of_imgs) +
                                       " ft" + str(self.percentage) +
                                       "% it" + str(self.iterations))
            if self.iterations >= self.max_iterations or self.percentage >= self.target_percentage:
                print("Finished after time:", int(time.time()*1000-self.start_time*1000))
                print("The final fitness was:", str(int(self.best_fitness)))
                return False
        # calculations here

        # self.refresh_images()
        self.shake_images()
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

    def populate_best_images(self):
        # sort by fitness desc
        self.images.sort(key=lambda x: x.get_fitness(), reverse=True)
        # rewrite the worst half
        for i in range(int(len(self.images)/2)):
            img = self.images[i]
            self.images[-i-1].overwrite_with(img)
            if i != 0:  # don't shake the best one
                self.images[i].mutate()
            self.images[-i-1].mutate()

    def crossover(self):
        min_num_of_rects = 100000
        for img in self.images:
            num_of_rects = len(img.rects)
            if num_of_rects < min_num_of_rects:
                min_num_of_rects = num_of_rects
        mutations = random.randint(int(self.number_of_rects) - 5, int(self.number_of_rects) + 5)
        for m in range(mutations):
            index = random.randint(0, min_num_of_rects - 1)
            rect1 = self.images[0].rects[index]
            for i in range(len(self.images)-1):
                self.images[i].rects[index] = self.images[i+1].rects[index]
            self.images[-1].rects[index] = rect1

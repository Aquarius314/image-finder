from image import Image
import random
import time
import pygame
import math


class Algorithm:

    # dobre rezultaty były, potem zmieniłem na noc:
    # 2/3 mutacji pomijana (zamiast 1/2)
    # variation z 4 na 2
    # obrazki z 400 na 600
    # poprawił się wynik pod względem szybkości (gradientu)
    # oby wreszcie pojawiła się stabilność!
    # 94,17 :)

    best_fitness = -1000000000.0
    new_best_fitness = False
    current_fitness = -100000000.0
    number_of_imgs = 100
    max_iterations = 1000000
    number_of_rects = 1400
    percentage = 0.00
    target_percentage = 99.90

    last_iteration_time = time.time()

    images = []
    # best_image = None

    def __init__(self, width, height):
        # self.number_of_rects = int((width+height)/5)
        self.max_fitness = width*height*255
        self.start_time = time.time()
        self.init_images(width, height)
        self.best_image = self.images[0]
        self.iterations = 0

    def init_images(self, width, height):
        for i in range(self.number_of_imgs):
            img = Image(width, height)
            img.put_random_rects(self.number_of_rects)
            self.images.append(img)

    def calculate(self):
        self.iterations += 1
        self.percentage = math.ceil((int(self.current_fitness)/int(self.max_fitness)*100)*100)/100
        time_difference = time.time() - self.last_iteration_time
        self.last_iteration_time = time.time()
        if self.iterations % 100 is 0 or self.percentage >= self.target_percentage:
            pygame.display.set_caption("img" + str(self.number_of_imgs) +
                                       " ft" + str(self.percentage) +
                                       "% it" + str(self.iterations))
            if self.iterations >= self.max_iterations or self.percentage >= self.target_percentage:
                print("Finished after time:", int(time.time()*1000-self.start_time*1000))
                print("The final fitness was:", str(int(self.best_fitness)))
                return False
            print("Iters: %d, time for 1 iteration: %.2f s after %.2f s"
                  % (self.iterations, time_difference, (time.time()-self.start_time)))
            rects_sum = 0
            for img in self.images:
                rects_sum += len(img.rects)
            print("Average number of rects:", str(int(rects_sum/len(self.images))))


        return True

    def shake_images(self):
        for img in self.images:
            img.mutate()

    def refresh_images(self):
        for img in self.images:
            img.refresh()

    def get_best_fitness(self):
        best_of_all = -10000000.0
        for img in self.images:
            fitness = img.get_fitness()
            if fitness > best_of_all:
                best_of_all = fitness
                self.best_image = img

        self.current_fitness = best_of_all
        return best_of_all

    def display_best_fitness(self, disp):
        print("Fitness so far:", self.percentage, "% after iters:",
              self.iterations, "images:", self.number_of_imgs, "rects:", len(self.best_image.rects),
                    " successful iterations:", disp)

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

        copy_quarter = False

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

        return self.images[0]

    def mutate(self):
        for i in range(1, len(self.images)):
            self.images[i].mutate()

    def recover_best_image(self, img):
        # save best image in place of worst image
        self.images[-1] = img
        self.images[-1].refresh()

    def crossover(self):
        min_num_of_rects = len(self.images[0].rects)
        for img in self.images:
            num_of_rects = len(img.rects)
            if num_of_rects < min_num_of_rects:
                min_num_of_rects = num_of_rects
        mutations = random.randint(int(self.number_of_rects/6), int(self.number_of_rects/5))

        image4 = self.images[0]
        for m in range(mutations):
            if min_num_of_rects <= 1:
                continue
            index = random.randint(0, min_num_of_rects - 1)
            rect1 = self.images[0].rects[index]
            for i in range(len(self.images)-1):
                self.images[i].rects[index] = self.images[i+1].rects[index]
            self.images[-1].rects[index] = rect1
        self.images[3] = image4

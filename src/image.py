import numpy as np
import random
import math
import pygame


class Rect:
    min_size = 2
    max_size = 20
    min_color = -10
    max_color = 20
    initial_max_size = 20

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        # self.is_oval = True
        self.is_oval = False
        # self.is_oval = (random.randint(0, 10) % 2 == 0)
        # self.color = random.randint(0, 255)

    def modify(self, img_width, img_height):
        if random.randint(1, 10) != 1:
            return
        lshake = 0  # left, right, up, down shakes
        rshake = 0
        ushake = 0
        dshake = 0
        swidth = 0
        bwidth = 0
        sheight = 0
        bheight = 0

        # mess with the color
        self.color += random.randint(-2, 2)
        self.color = max(self.min_color, self.color)
        self.color = min(self.max_color, self.color)

        # usually a little better when skipping this
        if self.min_size < self.width:
            swidth = self.min_size-1
        if self.width < self.max_size:
            bwidth = self.min_size-1
        if self.min_size < self.height:
            sheight = self.min_size-1
        if self.height < self.max_size:
            bheight = self.min_size-1

        if swidth != 0 or bwidth != 0:
            self.width += random.randint(-swidth, bwidth)
        if sheight != 0 or bheight != 0:
            self.height += random.randint(-sheight, bheight)
        # if self.is_oval:
        #     self.width = self.height

        variation = 2
        if self.x > variation:
            lshake = variation
        if self.x + self.width < img_width - variation:
            rshake = variation
        if self.y > variation:
            ushake = variation
        if self.y + self.height < img_height - variation:
            dshake = variation

        if lshake != 0 or rshake != 0:
            self.x += random.randint(-lshake, rshake)
        if ushake != 0 or dshake != 0:
            self.y += random.randint(-ushake, dshake)


class Image:

    image_loaded = False
    calculated_fitness = 0
    total_sum = 0
    FILE_NAME = 'assets/woman400prepared.png'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.total_sum = self.width*self.height*255
        if not self.image_loaded:
            self.image_loaded = True
            self.image_from_disk = pygame.image.load(self.FILE_NAME)
        self.pixels = []
        self.rects = []
        self.compared_picture = []
        self.refresh()
        self.prepare_picture()

    def prepare_picture(self):
        self.compared_picture = pygame.surfarray.pixels_red(self.image_from_disk)
        # loaded_image =
        # self.compared_picture = loaded_image[:, :]
        self.compared_picture = np.clip(self.compared_picture, 0, 255)
        values = []
        # for i in range(len(self.compared_picture)):
        #     for j in range(len(self.compared_picture[0])):
        #         if self.compared_picture[i, j] not in values:
        #             values.append(self.compared_picture[i, j])
        # print(values)
        # for i in range(len(loaded_image)):
        #     for j in range(len(loaded_image[0])):
        #         col = loaded_image[i, j]
        #         self.compared_picture[i, j] = col

    def draw_smooth_heart(self):
        u = self.width/6
        self.draw_circle_on_compared_image(2*u, 2*u, u)
        self.draw_circle_on_compared_image(4*u, 2*u, u)
        self.draw_rect_on_compared_image(u, 2*u, 4*u, u)
        self.draw_triangle_on_compared_image(u, 3*u, 2*u, 2*u, 1)
        self.draw_triangle_on_compared_image(3*u, 3*u, 2*u, 2*u, 4)

    def draw_circle_on_compared_image(self, x, y, r):
        for i in range(int(x-r), int(x+r)):
            for j in range(int(y-r), int(y+r)):
                if self.distance(i, j, x, y) <= r:
                    self.compared_picture[i, j] = 1

    def draw_triangular_heart(self):
        # heart
        u = int(self.width/8)
        self.draw_triangle_on_compared_image(u, 2*u, u, u, 2)
        self.draw_triangle_on_compared_image(2*u, u, u, u, 2)
        self.draw_triangle_on_compared_image(3*u, u, u, u, 3)
        self.draw_triangle_on_compared_image(2*u, 2*u, u, u, 4)
        self.draw_triangle_on_compared_image(3*u, 2*u, u, u, 1)
        self.draw_triangle_on_compared_image(4*u, 2*u, u, u, 4)
        self.draw_triangle_on_compared_image(4*u, u, u, u, 2)
        self.draw_triangle_on_compared_image(5*u, u, u, u, 3)
        self.draw_triangle_on_compared_image(5*u, 2*u, u, u, 1)
        self.draw_triangle_on_compared_image(6*u, 2*u, u, u, 3)
        self.draw_rect_on_compared_image(u, 3*u, u, u)
        self.draw_rect_on_compared_image(6*u, 3*u, u, u)
        self.draw_triangle_on_compared_image(6*u, 4*u, u, u, 4)
        self.draw_triangle_on_compared_image(5*u, 4*u, u, u, 2)
        self.draw_triangle_on_compared_image(5*u, 5*u, u, u, 4)
        self.draw_triangle_on_compared_image(4*u, 5*u, u, u, 2)
        self.draw_triangle_on_compared_image(4*u, 6*u, u, u, 4)
        self.draw_triangle_on_compared_image(3*u, 6*u, u, u, 1)
        self.draw_triangle_on_compared_image(3*u, 5*u, u, u, 3)
        self.draw_triangle_on_compared_image(2*u, 5*u, u, u, 1)
        self.draw_triangle_on_compared_image(2*u, 4*u, u, u, 3)
        self.draw_triangle_on_compared_image(1*u, 4*u, u, u, 1)
        self.draw_rect_on_compared_image(2*u, 2*u, 4*u, 3*u)
        self.draw_rect_on_compared_image(3*u, 5*u, 2*u, u)

    def draw_triangle_on_compared_image(self, x, y, width, height, corner):
        for i in range(int(x), int(x + width)):
            for j in range(int(y), int(y + height)):
                if corner == 1 and i-x > j-y:
                    self.compared_picture[i, j] = 1
                if corner == 2 and i + j >= int((2*x+2*y+width+height)/2):
                    self.compared_picture[i, j] = 1
                if corner == 3 and i-x < j-y:
                    self.compared_picture[i, j] = 1
                if corner == 4 and i + j < int((2*x+2*y+width+height)/2):
                    self.compared_picture[i, j] = 1

    def draw_rect_on_compared_image(self, x, y, width, height):
        for i in range(int(x), int(x + width)):
            for j in range(int(y), int(y + height)):
                self.compared_picture[i, j] = 1

    def overwrite_with(self, img):
        self.rects.clear()
        for rect in img.rects:
            rect2 = Rect(int(rect.x), int(rect.y), int(rect.width), int(rect.height), int(rect.color))
            self.rects.append(rect2)
        # self.refresh()

    def put_random_rects(self, num):
        self.rects.clear()
        self.pixels = np.zeros((self.width, self.height))
        for i in range(num):
            rect = self.get_rand_rect()
            self.rects.append(rect)
            self.draw_rect(rect)
        self.pixels = np.clip(self.pixels, 0, 255)

    def draw_rect(self, rect):
        if rect.is_oval:
            self.draw_oval(rect)
            return
        col = rect.color
        x1 = rect.x
        x2 = rect.x + rect.width
        y1 = rect.y
        y2 = rect.y + rect.height
        self.pixels[y1:y2, x1:x2] += col

    def draw_oval(self, rect):
        ox = rect.width/2 + rect.x
        oy = rect.height/2 + rect.y
        r = int((rect.width+rect.height)/4)
        for i in range(rect.x, min(rect.x + rect.width, self.width)):
            for j in range(rect.y, min(rect.y + rect.height, self.height)):
                if self.distance(i, j, ox, oy) <= r:
                    self.pixels[i, j] = 1

    def remove_rects(self, quantity):
        removed = 0
        remove = random.randint(quantity, quantity+2)
        for i in range(min(remove, len(self.rects))):
            index = -1
            if index >= 0:
                removed += 1
                self.rects.remove(self.rects[index])
            else:
                break
        return removed

    def add_rects(self, quantity):
        add = random.randint(quantity, quantity+1)
        for i in range(add):
            self.rects.append(self.get_rand_rect())

    def mutate(self):
        # find optimal value of rects to add and remove
        # quantity = max(5, int(len(self.rects)/500))
        quantity = max(20, int(len(self.rects)/50))  # more randomness

        # remove some rects
        removed_rects = self.remove_rects(quantity)

        # modify existing rects (move and resize a bit)
        for rect in self.rects:
            rect.modify(self.width, self.height)

        # add some rects
        self.add_rects(removed_rects)

        # change order of rects in list
        random.shuffle(self.rects)

        # generate image and refresh parameters
        self.refresh()

    def get_rand_rect(self):
        computed_max_size = int(random.randint(1, 4)*(Rect.max_size/4))
        width = random.randint(Rect.min_size, computed_max_size)
        height = random.randint(Rect.min_size, computed_max_size)
        x = random.randint(5, self.width - width - 5)
        y = random.randint(5, self.height - height - 5)
        color = random.randint(Rect.min_color, Rect.max_color)
        return Rect(x, y, width, height, color)

    def refresh(self):
        self.pixels = np.zeros((self.width, self.height))
        for rect in self.rects:
            self.draw_rect(rect)
        self.pixels = np.clip(self.pixels, 0, 255)

    def get_darkness(self): # just the coverage of image
        return self.pixels.sum()

    def distance(self, x1, y1, x2, y2):
        return int(math.sqrt((x1-x2)**2 + (y1-y2)**2))

    def get_fit_in_circle(self):
        radius = self.width/4
        circle_x = self.width/2
        circle_y = self.width/2
        fitness = 0
        for x in range(self.width):
            for y in range(self.height):
                d = self.distance(x, y, circle_x, circle_y)
                if int(self.pixels[x, y]) == 1:
                    if d < radius:
                        fitness += 10
                    else:
                        fitness -= int(d/5)
                else:
                    if d < radius:
                        fitness -= 100
                    else:
                        fitness += 10
        return fitness

    def get_pixels_below(self):
        fitness = 0
        for x in range(self.width):
            for y in range(self.height):
                fitness -= int((x - self.height/2)/10)*self.pixels[x, y]
        return fitness

    def get_fitness(self):
        return self.total_sum - np.sum(np.absolute(self.compared_picture - self.pixels))

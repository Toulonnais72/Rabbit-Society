from opensimplex import OpenSimplex
import random
import math
import time
import numpy as np
from PIL import Image

gen = OpenSimplex(seed = int(time.time()))
# some colors
sand_color = (223, 227, 141)
water_color = (124, 208, 222)
dirt_color = (115, 118, 83)
land_color = (140,200,0)
snow_color = (232,232,233)

class Terrain:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.elevation =[]
        self.biome = []
        self.terrain = []
        self.trees = []
        self.plants = []
        self.f = 1 # self.f = random.random(1,7)
        self.valley_depth = random.uniform(1, 6)
        self.water_level = random.uniform(0.01, 0.2)
        self.beach_level = random.uniform(self.water_level, 0.25)
        self.land_level = random.uniform(self.beach_level,0.7)
        self.dirt_level = random.uniform(self.land_level, 0.85)
        self.snow_level = random.uniform(self.dirt_level, 1.0)
        self.nb_trees = 0
        self.nb_plants = 0
        print("Size (Width, Length)", self.width, self.length)
        print("Sea level:", self.water_level)
        print("Beach level:", self.beach_level)
        print("Land level:", self.land_level)
        print("Dirt level:", self.dirt_level)
        print("Snow_level:", self.snow_level)
        print("Valley depth (5,10):", self.valley_depth)

    def noise(self, x, y):
        return gen.noise2d(x,y)/2 + 0.5

    def choose_biome(self, e):
        if e <= self.water_level:
            return "Water"
        elif e < self.water_level * 1.2:
            return "Beach"
        elif e < self.dirt_level:
            return "Land"
        elif e < self.snow_level:
            return "Dirt"
        else:
            return "Snow"

    def create_plants(self, x, y):
        if self.biome[x][y] == "Land":
            self.trees[x][y] = random.randint(0, 2)
            self.nb_trees += self.trees[x][y]
            self.plants[x][y] = random.randint(0, 2)
            self.nb_plants += self.plants[x][y]

        if self.biome[x][y] == "Beach":
            self.trees[x][y] = 0
            self.plants[x][y] = random.randint(0, 2)
            self.nb_plants += self.plants[x][y]

        if self.biome[x][y] == "Water" or "Snow":
            self.trees[x][y] = 0
            self.plants[x][y] = 0

    def generate(self):
        print("Generating elevations and biome...")
        max_e = 0
        for x in range(self.width):
            list_y = []
            for y in range(self.length):
                nx, ny = x/self.width - 0.5, y/self.length - 0.5
                # Generate elevation using perlin noise ###
                e = self.noise(self.f * nx, self.f * ny) + \
                    0.5 * self.noise(2 * self.f * nx, 2 * self.f * ny) + \
                    0.25 * self.noise(4 * self.f * nx, 4 * self.f * ny)
                # Create Valleys ###
                e_flat = math.pow(e, self.valley_depth)
                if e_flat > max_e: max_e = e_flat
                list_y.append(e_flat)
                # Create Biomes (water, beach, land, snow) ###
            #print(list_y)
            self.elevation.append(list_y)
        print("Scaling the elevations and creating biome...")
        for x in range(self.length):
            list_biome = []
            for y in range(self.width):
                self.elevation[x][y] /= max_e
                list_biome.append(self.choose_biome(self.elevation[x][y]))
            self.biome.append(list_biome)
        print("Planting trees and shrubs...")
        # Create trees ###
        self.trees = [[0]*self.length]*self.width
        self.plants = [[0]*self.length]*self.width
        for x in range(self.width):
            for y in range(self.length):
                self.create_plants(x,y)
        print("Some Statistics about your land:")
        print("Number of snowy cells:", sum(x.count("Snow") for x in self.biome))
        print("Number of cells with beach:", sum(x.count("Beach") for x in self.biome))
        print("Number of cells with water:", sum(x.count("Water") for x in self.biome))
        print("Number of cells with dirt:", sum(x.count("Dirt") for x in self.biome))
        print("Number of cells with grassy land:", sum(x.count("Land") for x in self.biome))
        print("Number of trees:", self.nb_trees)
        print("Number of plants:", self.nb_plants)

    def save_image(self, filename):
        pixels_out = []
        elevation_array = np.zeros((self.width, self.length, 3), dtype = np.uint8)
        biome_array = np.zeros((self.width, self.length, 3), dtype = np.uint8)
        biome_array[:] = water_color #Fill with Blue

        for x in range(self.width):
            for y in range(self.length):
                biome = self.biome[x][y]
                elevat = self.elevation[x][y]
                if biome == "Water":
                    biome_array[x,y] = water_color
                elif biome == "Land":
                    biome_array[x,y] = land_color
                elif biome == "Beach":
                    biome_array[x, y] = sand_color
                elif biome == "Dirt":
                    biome_array[x,y] = dirt_color
                elif biome == "Snow":
                    biome_array[x,y] = snow_color
                elevation_array[x,y] = (int(elevat*255), int(elevat*255), int(elevat*255))
        Image.fromarray(biome_array).convert("RGB").save("./images/" + filename + ".png")  # don't need to convert
        Image.fromarray(elevation_array).convert("RGB").save("./images/height_field"+filename+".jpg")
        '''image_out = Image.new('RGB', (self.width, self.length))
        image_out.putdata(pixels_out)
        image_out.save(filename + '.png')'''




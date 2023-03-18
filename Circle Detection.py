import cv2
import numpy as np
import random

class CircleDetector:
    def __init__(self, image_path, population_size, max_generations):
        self.image_path = image_path
        self.population_size = population_size
        self.max_generations = max_generations
        self.img = cv2.imread(self.image_path, 0)
        self.height, self.width = self.img.shape
        self.population = []
        self.best_fitness = float('inf')
        self.best_individual = None
        self.fitness_values = []

    def initialize_population(self):
        for i in range(self.population_size):
            individual = []
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            r = random.randint(1, min(self.width, self.height)//2)
            individual.append(x)
            individual.append(y)
            individual.append(r)
            self.population.append(individual)

    def evaluate_fitness(self, individual):
        fitness = 0
        for i in range(self.width):
            for j in range(self.height):
                x, y, r = individual
                distance = np.sqrt((i - x)**2 + (j - y)**2)
                fitness += abs(distance - r - self.img[i][j])
        return fitness

    def selection(self):
        fitness_sum = sum(self.fitness_values)
        probabilities = [fitness/fitness_sum for fitness in self.fitness_values]
        selected_indices = np.random.choice(self.population_size, self.population_size//2, replace=False, p=probabilities)
        selected_individuals = [self.population[i] for i in selected_indices]
        return selected_individuals

    def crossover(self, parent1, parent2):
        child1 = []
        child2 = []
        crossover_point = random.randint(0, 2)
        for i in range(crossover_point):
            child1.append(parent1[i])
            child2.append(parent2[i])
        for i in range(crossover_point, 3):
            child1.append(parent2[i])
            child2.append(parent1[i])
        return child1, child2

    def mutation(self, individual):
        mutation_rate = 0.1
        for i in range(3):
            if random.random() < mutation_rate:
                if i == 0:
                    individual[i] = random.randint(0, self.width)
                elif i == 1:
                    individual[i] = random.randint(0, self.height)
                else:
                    individual[i] = random.randint(1, min(self.width, self.height)//2)
        return individual

    def evolve(self):
        self.initialize_population()
        for generation in range(self.max_generations):
            self.fitness_values = [self.evaluate_fitness(individual) for individual in self.population]
            if min(self.fitness_values) < self.best_fitness:
                self.best_fitness = min(self.fitness_values)
                self.best_individual = self.population[self.fitness_values.index(self.best_fitness)]
            selected_individuals = self.selection()
            self.population = []
            for i in range(self.population_size//2):
                parent1 = selected_individuals[i]
                parent2 = selected_individuals[-i-1]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                self.population.append(child1)
                self.population.append(child2)
        return self.best_individual

if __name__ == "__main__":
    detector = CircleDetector("/home/rakib/Documents/4th Kibo RPC/circle.png", 50, 100)
    best_individual = detector.evaluate_fitness
    cv2.imshow('Circle Detected',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

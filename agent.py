import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

import utils


class Agent:

    def __init__(self, generation, n_population):

        self.generation = generation
        self.n_population = n_population
        self.fitness_score = np.zeros(n_population)
        self.population = list()

        self.traveled_distance = np.zeros(self.n_population)

        # Initialize all models
        for i in range(self.n_population):
            model = self.initiate_bird()
            self.population.append(model)
            self.fitness_score[i] *= (-100)

        if utils.LOAD_POP:
            for i in range(self.n_population):
                self.population[i].load_weights("load_population/model_" + str(i) + ".keras")

    def save_population(self):
        for i in range(self.n_population):
            self.population[i].save_weights("saved_population/model_" + str(i) + ".keras")

    def cross_breeding(self, bird_index_0, bird_index_1):
        weights_0 = self.population[bird_index_0].get_weights()
        weights_1 = self.population[bird_index_1].get_weights()
        weights_0_new = weights_0
        weights_1_new = weights_1
        weights_0_new[0] = weights_1[0]
        weights_1_new[0] = weights_0[0]
        return np.asarray([weights_0_new, weights_1_new])

    def predict_action(self, height, dist, pipe_height, model_num):
        # The height, dist and pipe_height must be between 0 to 1 (Scaled by SCREENHEIGHT)
        height = min(utils.SCREEN_HEIGHT, height) / utils.SCREEN_HEIGHT - 0.5
        dist = dist / 450 - 0.5  # Max pipe distance from player will be 450
        pipe_height = min(utils.SCREEN_HEIGHT, pipe_height) / utils.SCREEN_HEIGHT - 0.5
        neural_input = np.asarray([height, dist, pipe_height])
        neural_input = np.atleast_2d(neural_input)
        output_prob = self.population[model_num].predict(neural_input, 1)[0]
        if output_prob[0] <= 0.5:
            # Perform the jump action
            return 1
        return 0

    def genetic_breeding(self, threshold=0.2):
        """Perform genetic updates here"""
        fitness_tot = self.fitness_score.sum()
        for i in range(self.n_population):
            self.fitness_score[i] /= fitness_tot
            if i != 0:
                self.fitness_score[i] += self.fitness_score[i - 1]

        new_weights = list()

        choice = random.uniform(0, 1)

        if choice < threshold:
            for i in range(self.n_population // 2):
                parent_0 = random.uniform(0, 1)
                parent_1 = random.uniform(0, 1)
                index_0 = -1
                index_1 = -1
                for index in range(self.n_population):
                    if self.fitness_score[index] >= parent_0:
                        index_0 = index
                        break
                for index in range(self.n_population):
                    if self.fitness_score[index] >= parent_1:
                        index_1 = index
                        break
                updated_weights = self.cross_breeding(index_0, index_1)
                updated_weights_0 = self.mutate(updated_weights[0])
                updated_weights_1 = self.mutate(updated_weights[1])
                new_weights.append(updated_weights_0)
                new_weights.append(updated_weights_1)
        else:
            ordered_index = self.fitness_score.argsort()[::-1]

            # 10% of the children are direct copies from the best 10% of the parents
            size = int(self.n_population * 0.1)
            for index in ordered_index[range(size)]:
                new_weights.append(self.population[index].get_weights())

            # 30% of the children come from random breeding of the top 30% of the parents
            size = int(self.n_population * 0.3)
            selected_indices = ordered_index[range(size)]
            for index_i in range(size // 2):
                parent_0 = random.uniform(0, 1)
                parent_1 = random.uniform(0, 1)
                index_0 = -1
                index_1 = -1
                for index_j in selected_indices:
                    if self.fitness_score[index_j] >= parent_0:
                        index_0 = index_j
                        break
                for index_j in selected_indices:
                    if self.fitness_score[index_j] >= parent_1:
                        index_1 = index_j
                        break
                updated_weights = self.cross_breeding(index_0, index_1)
                updated_weights_0 = self.mutate(updated_weights[0])
                updated_weights_1 = self.mutate(updated_weights[1])
                new_weights.append(updated_weights_0)
                new_weights.append(updated_weights_1)

            # 60% of the children come from random breeding across all parents
            size = int(self.n_population * 0.6)
            for index_i in range(size // 2):
                parent_0 = random.uniform(0, 1)
                parent_1 = random.uniform(0, 1)
                index_0 = -1
                index_1 = -1
                for index_j in range(self.n_population):
                    if self.fitness_score[index_j] >= parent_0:
                        index_0 = index_j
                        break
                for index_j in range(self.n_population):
                    if self.fitness_score[index_j] >= parent_1:
                        index_1 = index_j
                        break
                updated_weights = self.cross_breeding(index_0, index_1)
                updated_weights_0 = self.mutate(updated_weights[0])
                updated_weights_1 = self.mutate(updated_weights[1])
                new_weights.append(updated_weights_0)
                new_weights.append(updated_weights_1)

            """
            # 10% of the children come from breeding between best 10% and worst 10% of the parents
            size = int(self.n_population * 0.1)
            selected_indices_0 = ordered_index[range(size)]
            selected_indices_1 = self.fitness_score.argsort()[range(size)]
            for index_i in range(batch[3] // 2):
                parent_0 = random.uniform(0, 1)
                parent_1 = random.uniform(0, 1)
                index_0 = -1
                index_1 = -1
                for index_j in selected_indices_0:
                    if self.fitness_score[index_j] >= parent_0:
                        index_0 = index_j
                        break
                for index_j in selected_indices_1:
                    if self.fitness_score[index_j] >= parent_1:
                        index_1 = index_j
                        break
                updated_weights = self.cross_breeding(index_0, index_1)
                updated_weights_0 = self.mutate(updated_weights[0])
                updated_weights_1 = self.mutate(updated_weights[1])
                new_weights.append(updated_weights_0)
                new_weights.append(updated_weights_1)
            """

        for i in range(len(new_weights)):
            weight = new_weights[i]
            self.population[i].set_weights(weight)

        self.generation += 1

        if utils.SAVE_POP:
            self.save_population()
            print("Population saved")

        return self.traveled_distance, self.fitness_score

    @staticmethod
    def initiate_bird():
        bird = Sequential()
        bird.add(Dense(input_dim=3, units=7, name="dense_0"))
        bird.add(Activation("sigmoid", name="activation_0"))
        bird.add(Dense(units=6, name="dense_1"))
        bird.add(Activation("sigmoid", name="activation_1"))
        bird.add(Dense(units=1, name="dense_2"))
        bird.add(Activation("sigmoid", name="activation_2"))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        bird.compile(loss="mse", optimizer=sgd, metrics=["accuracy"])
        return bird

    @staticmethod
    def mutate(weights):
        mutated_weights = weights.copy()
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                if random.uniform(0, 1) > 0.85:
                    change = random.uniform(-0.5, 0.5)
                    mutated_weights[i][j] += change
        return mutated_weights

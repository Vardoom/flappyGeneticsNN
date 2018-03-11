# Flappy Bird Genetic Evolution
This project aims to train an agent in the PyGame environment "Flappy Bird". The training process uses a combination of Neural Network algorithms and Genetic algorithms.

## Algorithm Process
* Each generation contains 50 birds
* At each generation, the breeding process is performed based on fitness scores
* Crossover swaps the first layers of the NN of the selected parents
* Finally, random mutations are performed in order to achieve diversity

## How to use ?
The algorithm loads the trained models from the load_population folder. In order to do this, the LOAD_POP variable must be set to True in the utils.py file.
The algorithm saves the trained models on the saved_population folder. In order to do this, the SAVE_POP variable must be set to True in the utils.py file.
The number of generations and the size of teh population can be changed in the utils.py file.

## Author
* **Paul Vardon** - [Vardoom](https://github.com/Vardoom)

## Disclaimer
* Based on Flappy Bird clone in pygame, https://github.com/sourabhv/FlapPyBird
* Genetic algorithms inspired by https://github.com/ssusnic/Machine-Learning-Flappy-Bird

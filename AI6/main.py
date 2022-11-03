"""
1. (0.1) citirea datelor din fișier și împărțirea setului de date în date de antrenare și de testare
2. (0.1) inițializarea parametrilor (dimensiunea stratului de intrare, ascuns și de ieșire, rata de învățare, numărul maxim de epoci, etc) și a ponderilor

Implementing
initializarea parametirlor (dimensiunea stratului de intrare, ascuns si de iesire)
https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
"""

import math
import random

import pandas as pd

input_layer_size = 0
hidden_layer_size = 0
output_layer_size = 0
learning_rate = 0
max_num_of_ages = 0
weights = []


def read_data():
    df = pd.read_csv('dataset/iris.data')
    df = df.sample(frac=1)  # shuffle
    split_factor = 0.9
    n_train = math.floor(split_factor * df.shape[0])
    n_test = math.ceil((1 - split_factor) * df.shape[0])
    train_data = df.head(n_train)
    test_data = df.tail(n_test)
    print(train_data.to_string())
    print(test_data.to_string())


def initialize_parameters():
    global input_layer_size
    global hidden_layer_size
    global output_layer_size
    global learning_rate
    global max_num_of_ages
    global weights

    input_layer_size = 4
    hidden_layer_size = 4
    output_layer_size = 3
    learning_rate = 0.1
    max_num_of_ages = 50

    weight_len = input_layer_size * hidden_layer_size + hidden_layer_size * output_layer_size
    for i in range(0, weight_len):
        weights.append(random.uniform(0, 1))
    print("Weights:", weights)



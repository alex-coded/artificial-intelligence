import gzip
import pickle

import numpy as np

import parse
import utils
from Network import Network

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_data = parse.parse_data(r'resources/iris.data')
    train_data, test_data = utils.split_data(all_data, 0.1)
    nr_of_epochs = 50
    network = Network([4, 4, 3], 0.5, nr_of_epochs)
    epochs = network.network_training(train_data, test_data, utils.sigmoid_activation)
    best_epoch = min(epochs.values(), key=lambda x: x[1])
    for idx, epoch in enumerate(epochs.values()):
        print("Epoch ", idx, ":", 'error - ', epoch[1], ', (acc, inacc) - ', epoch[2])
    best_epoch_index = [i for i in epochs if epochs[i] == best_epoch][0]
    print("Best epoch results on validation set: epoch", best_epoch_index, ' with result ', best_epoch[1])
    # print("Test on training data ",
    #       best_epoch[0].test_network(train_test_set, utils.sigmoid_activation, utils.softmax_activation))
    # print('Test on training data for the last epoch ', epochs[nr_of_epochs][0].test_network(train_test_set, utils.sigmoid_activation, utils.softmax_activation))
    print("Test on test data ",
          best_epoch[0].test_network_classification(test_data, utils.sigmoid_activation))

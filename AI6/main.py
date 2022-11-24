import util
from Network import Network
from confusion_matrix import *

if __name__ == '__main__':
    data = util.parse(r'resources/iris.data')
    train, test = util.split_data(data, 0.1)
    nr_epochs = 50
    net = Network([4, 4, 3], 0.5, nr_epochs)
    epochs = net.training(train, test, util.sig_activ)  # Dict[int, Tuple[Network, float, Tuple[int, int]]] - numarul epocii, [Network, err, (acc, inacc)]
    best_epoch = min(epochs.values(), key=lambda y: y[1])  # cea mai buna epoca, este epoca cu cea mai mica eroare
    for index, epoch in enumerate(epochs.values()):
        print("Epoch ", index, ":", 'error - ', epoch[1], ', (acc, inacc) - ', epoch[2])
    best_epoch_id = [i for i in epochs if epochs[i] == best_epoch][0]
    # print("EPOCH", epochs[1])
    print("Best epoch results on validation set: epoch", best_epoch_id, ' with result ', best_epoch[1])
    # print("Test on training data ",
    #       best_epoch[0].test_network_classification(train_data, utils.sigmoid_activation, utils.softmax_activation))
    # print('Test on training data for the last epoch ', epochs[nr_of_epochs][0].test_network(train_data, utils.sigmoid_activation, utils.softmax_activation))
    # print("Test on test data ",
    #       best_epoch[0].test_network_classification(test_data, utils.sigmoid_activation))
    plot_matrix(best_epoch[2][2])
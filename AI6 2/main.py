import util
from Network import Network
from confusion_matrix import *
from err_points import *

if __name__ == '__main__':
    data = util.parse(r'resources/iris.data')
    train, test = util.split_input(data, 0.1)
    nr_epochs = 50
    n = Network([4, 4, 3], 0.5, nr_epochs)
    epochs = n.training(train, test, util.sig_activ)  # Dict[int, Tuple[Network, float, Tuple[int, int]]] - numarul epocii, [Network, err, (acc, inacc)]
    best_epoch = min(epochs.values(), key=lambda y: y[1])  # the best epoch is the one with the least error
    for index, epoch in enumerate(epochs.values()):
        print("Epoca ", index, ":", 'eroare - ', epoch[1], ', (acuratete, inacuratete, stare) - ', epoch[2])
    best_epoch_id = [i for i in epochs if epochs[i] == best_epoch][0]
    print("Cea mai  buna epoca din setul de validare este ", best_epoch_id, ' cu rezultatul ', best_epoch[1])
    print("Test on test data ",
          best_epoch[0].test_net_classification(test, util.sig_activ))
    plot_matrix(best_epoch[2][2])
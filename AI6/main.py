import util
from Network import Network
from confusion_matrix import *
from err_points import *

# pip install matplotlib==3.5.0

if __name__ == '__main__':
    data = util.parse(r'resources/iris.data')
    train, test = util.split_input(data, 0.1)
    nr_epochs = 50
    n = Network([4, 4, 3], 0.5, nr_epochs)
    epochs = n.training(train, test, util.sig_activ)  # Dict[int, Tuple[Network, float, Tuple[int, int]]] - numarul epocii, [Network, err, (acc, inacc)]
    best_epoch = min(epochs.values(), key=lambda y: y[1])  # the best epoch is the one with the least error
    epoch_to_err_train = dict()
    for index, epoch in enumerate(epochs.values()):
        print("Epoca ", index, ":", 'eroare - ', epoch[1], ', (acuratete, inacuratete, stare) - ', epoch[2])
        epoch_to_err_train[index] = epoch[1]
    best_epoch_id = [i for i in epochs if epochs[i] == best_epoch][0]
    print("Cea mai  buna epoca din setul de validare este ", best_epoch_id, ' cu rezultatul ', best_epoch[1])
    print("Test on training data ",
          best_epoch[0].test_net_classification(train, util.sig_activ))
    print('Testul pe data de train pe utlima epoca ', epochs[nr_epochs][0].test_net_classification(train, util.sig_activ))
    print("Testul pe setul de date de antrenare ",
          best_epoch[0].test_net_classification(test, util.sig_activ))
    plot_matrix(best_epoch[2][2])
    li = list(zip(epoch_to_err_train.keys(), epoch_to_err_train.values()))
    plt.scatter(*zip(*li))
    plt.show()
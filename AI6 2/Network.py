import numpy as np
import util
from Layer import Layer


class Network:
    nr_of_epochs: int
    layers: list
    l_sizes: list
    learn_rate: float

    def __init__(self, layer_sizes, learning_rate, nr_of_epochs):
        self.l_sizes = layer_sizes
        self.learn_rate = learning_rate
        self.nr_of_epochs = nr_of_epochs
        self.layers = []
        for idx, inp_size in enumerate(layer_sizes[:-1]):
            self.layers += [Layer(inp_size, layer_sizes[idx + 1])]      # the current layers nr of outputs(nodes) is the next layers number of inputs

    def forward_prop(self, training_set, targ, activ_func):
        cur_layer_inp = training_set
        for layer in self.layers:
            activ = layer.get_activation(cur_layer_inp, activ_func)
            layer.l_activ = activ
            cur_layer_inp = layer.l_activ
        comparison_targ = util.nr_to_nr_arr(targ, self.layers[-1].neuron_nr)
        return self.get_out_l_total_err(comparison_targ)

    def create_copy(self):
        copy = Network(self.l_sizes, self.learn_rate, self.nr_of_epochs)
        for idx, layer in enumerate(self.layers):
            l_in_copy = copy.layers[idx]
            l_in_copy.weights = np.copy(layer.weights)
            l_in_copy.biases = np.copy(layer.biases)
        return copy

    def get_out_l_total_err(self, targ):
        err = targ - self.layers[-1].l_activ
        err = (err * err) / 2
        return np.sum(err)

    def compute_last_layer_delta(self, targ):
        out_l = self.layers[-1]
        outp_activ = out_l.l_activ
        return - (targ - outp_activ) * outp_activ * (1 - outp_activ)

    def compute_hidden_layer_delta(self, out_l_delta):
        out_l = self.layers[-1]
        hid_l = self.layers[-2]
        hid_activ = hid_l.l_activ
        return (out_l_delta @ out_l.weights.T) * hid_activ * (1 - hid_activ)

    def backprop(self, training_input, targ):
        out_l = self.layers[-1]
        hid_l = self.layers[-2]

        first_l_inp = training_input.reshape(1, -1)
        last_l_delta = self.compute_last_layer_delta(
            util.nr_to_nr_arr(targ, out_l.neuron_nr))
        out_l.cost_grad_w = hid_l.l_activ.T @ last_l_delta
        out_l.cost_grad_b = last_l_delta
        out_l.weights -= self.learn_rate * out_l.cost_grad_w
        out_l.biases -= self.learn_rate * out_l.cost_grad_b

        hid_l_delta = self.compute_hidden_layer_delta(last_l_delta)
        hid_l.cost_grad_w = first_l_inp.T @ hid_l_delta
        hid_l.cost_grad_b = hid_l_delta
        hid_l.weights -= self.learn_rate * hid_l.cost_grad_w
        hid_l.biases -= self.learn_rate * hid_l.cost_grad_b

    def get_average_total_err(self, data, activ_func):
        total_set_err = 0
        for idx in range(len(data[0])):
            total_set_err += self.forward_prop(data[0][idx], data[1][idx], activ_func)
        return total_set_err / len(data[0])

    def iterative_training(self, training_data, activate):
        for idx in range(len(training_data[0])):
            self.forward_prop(training_data[0][idx], training_data[1][idx],
                              activate)  # targ, layer nr of neurons
            self.backprop(training_data[0][idx], training_data[1][idx])

    def test_net_classification(self, test_data, activ_func):
        m = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        acc = 0
        inacc = 0
        for index in range(len(test_data[0])):
            coordinates = test_data[0][index]
            actual_v = test_data[1][index]
            self.forward_prop(coordinates, actual_v, activ_func)
            predict_prob = self.layers[-1].l_activ
            pred = np.argmax(predict_prob)
            m[actual_v][pred] += 1

            if actual_v == pred:
                acc += 1
            else:
                inacc += 1

        return acc, inacc, m

    def training(self, training_data, validation_data, activ_func):
        epochs = {}
        iteration = 1
        while iteration <= self.nr_of_epochs:
            self.iterative_training(training_data, activ_func)
            curr_epoch_network = self.create_copy()
            epochs[iteration] = (
                curr_epoch_network, curr_epoch_network.get_average_total_err(validation_data,
                                                                                   activ_func,
                                                                                   ),
                curr_epoch_network.test_net_classification(validation_data, activ_func)
            )
            iteration += 1
            util.shuffle(training_data[0], training_data[1])
        return epochs


import math
import numpy as np


class Layer:
    l_activ: np.ndarray
    l_err: np.ndarray
    cost_grad_w: np.ndarray
    cost_grad_b: np.ndarray
    input_nr: int
    neuron_nr: int
    weights: np.ndarray
    biases: np.ndarray

    def __init__(self, nr_nodes_in, nr_nodes_out):
        self.l_err = None
        self.cost_grad_w = None
        self.cost_grad_b = None
        self.l_activ = np.zeros((1, 1))
        self.input_nr = nr_nodes_in
        self.neuron_nr = nr_nodes_out
        self.weights = np.random.normal(0, 1 / math.sqrt(nr_nodes_in), size=(self.input_nr, self.neuron_nr))
        self.biases = np.random.rand(1, self.neuron_nr)

    def activation_for_l(self, output, activation_function):
        activ = []
        for row in output:
            activ += [activation_function(row)]
        self.l_activ = np.row_stack(activ)

    def calc_output(self, input_train):
        return (input_train @ self.weights) + self.biases

    def get_activation(self, training_input, activate):
        output = self.calc_output(training_input)
        return activate(output)



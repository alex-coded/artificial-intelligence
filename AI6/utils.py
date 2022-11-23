import numpy as np


def shuffle_in_unison(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)


def split_data(all_data, test_data_ratio: float):
    shuffle_in_unison(all_data[0], all_data[1])
    nr_of_elements_test = int(len(all_data[0]) * test_data_ratio)
    test_data = all_data[0][:nr_of_elements_test], all_data[1][:nr_of_elements_test]
    train_data = all_data[0][nr_of_elements_test:], all_data[1][nr_of_elements_test:]
    return train_data, test_data


def sigmoid_activation(z: np.ndarray):
    return 1.0 / (1 + np.exp(-z))



def softmax_activation(z: np.ndarray):
    return np.exp(z) / np.sum(np.exp(z))


def number_to_number_array(index, array_len):
    digit_array = [0] * array_len
    digit_array[index] = 1
    return np.array(digit_array)

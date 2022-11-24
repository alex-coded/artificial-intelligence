
import csv
import numpy as np


def shuffle(x, y):
    state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(state)
    np.random.shuffle(y)


def split_input(all_data, ratio_of_test_data: float):
    shuffle(all_data[0], all_data[1])
    nr = int(len(all_data[0]) * ratio_of_test_data)
    test = all_data[0][:nr], all_data[1][:nr]
    train = all_data[0][nr:], all_data[1][nr:]
    return train, test


def sig_activ(z: np.ndarray):
    return 1.0 / (1 + np.exp(-z))


def softmax_activ_func(z: np.ndarray):
    return np.exp(z) / np.sum(np.exp(z))


def nr_to_nr_arr(index, array_len):
    digit_array = [0] * array_len
    digit_array[index] = 1
    return np.array(digit_array)


def parse(file_name):
    attr_arr = []
    classes_arr = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 0:
                break
            attr_arr += [[float(row[0]), float(row[1]), float(row[2]), float(row[3])]]
            classes_arr += [iris_name_to_nr(row[4])]
    return np.array(attr_arr), np.array(classes_arr)


def iris_name_to_nr(iris):
    if iris == "Iris-setosa":
        return 0
    if iris == "Iris-versicolor":
        return 1
    if iris == "Iris-virginica":
        return 2
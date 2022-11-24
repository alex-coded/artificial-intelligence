from matplotlib import pyplot as plt
import numpy as np


def visualize_err_points(data):
    x, y = data.T
    plt.scatter(x, y)
    plt.show()
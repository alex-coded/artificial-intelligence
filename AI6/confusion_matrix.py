import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt


def plot_matrix(array):
        df_cm = pd.DataFrame(array, index=[i for i in ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]],
                             columns=[i for i in ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]])
        plt.figure(figsize=(10, 7))
        sn.heatmap(df_cm, annot=True)
        plt.savefig('confusion_matrix.png')
        plt.show()


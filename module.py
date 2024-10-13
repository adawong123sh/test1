import pandas as pd
import matplotlib.pyplot as plt

import os

import seaborn as sns

df = pd.read_csv("uploads/titanic.csv")

column_x = "Survived"
try:
    sns.countplot(x=column_x, data=df)

    # Сохранение графика в директорию static
    plot_path = os.path.join("static", "plotfff.png")
    plt.savefig(plot_path)
    plt.close()
except Exception:
    print("Error")

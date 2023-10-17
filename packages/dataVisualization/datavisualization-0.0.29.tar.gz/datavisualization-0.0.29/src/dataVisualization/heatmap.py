import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

file = "/Users/ethan/PycharmProjects/data-visualization/Helen/Marimekko charts trial data Q3 2022.xlsx"
df: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name="Sheet2")

labels = pd.read_excel(file, sheet_name="Sheet3")
labels = labels.replace(labels['Beverages'][11], "")

sns.heatmap(df, cmap="Blues_r", yticklabels=False, annot=labels, fmt="")
plt.show()
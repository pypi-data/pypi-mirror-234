import pandas as pd
import matplotlib.container as con
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.container as container
import numpy as np

file = "/Users/ethan/PycharmProjects/data-visualization/Helen/Log charts - followers - trial.xlsx"
dataframe: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name="Trial")
height = dataframe['Followers'].values
labels = dataframe['Brand'].values
y_pos = np.arange(len(labels))

fig, ax = plt.subplots()
ax.bar(y_pos, height)

# Create names on the x-axis
ax.set_xticks(y_pos, labels)
ax.set_yscale('log')

# Show graphic
plt.show()
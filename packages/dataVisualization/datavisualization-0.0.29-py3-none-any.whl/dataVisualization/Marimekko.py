import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as c
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from matplotlib.lines import Line2D

plt.rcParams['font.family'] = 'Arial'

BAR_WIDTH = 0.85
CHART_WIDTH = 11.05
CHART_HEIGHT = 8

file = "/Users/ethan/Library/CloudStorage/GoogleDrive-ethan@susmon.com/.shortcut-targets-by-id/1yv5Tb8aODBZ75uclq_x7pfAUuSR3Ijlb/SusMon/1 Research Reports/Chart Development/Marimekkos (Quantiles)/working data/Quantiles Generation v9.xlsx"
dataframe: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name="1")
dataframe = dataframe.sort_values("Sector")

fig, ax = plt.subplots(1, figsize=(CHART_WIDTH, CHART_HEIGHT))

sectors = sorted(list(set(dataframe["Sector"])))
size = sorted(sorted(list(set(dataframe["Followers"])), reverse=True)[:3])

rows = len(dataframe)


def _totals_as_percentage(df: pd.DataFrame):
    totals = []
    newValues = []
    for s in range(len(sectors)):
        total = 0
        for i in range(rows):
            if dataframe["Sector"][i] == sectors[s]:
                total += dataframe["Total"][i]
        totals.append(total)

    for s in range(len(sectors)):
        for i in range(rows):
            if dataframe["Sector"][i] == sectors[s]:
                newValues.append((dataframe["Total"][i] / totals[s]) * 100)
    df["% Total"] = newValues
    return df


def _label_height(label: str) -> float:
    """
    get the height of the matplotlib.text.Text object with the given label
    :param label: the label value to be measured
    :return: the width of the label as a floating point number
    """
    _chars = {}
    # an empty dict returns false, we can check if our dict has content below if not we add content
    renderer = plt.gcf().canvas.get_renderer()
    for i in list(label):
        my_num = plt.text(0, 0, i, size=8, family='Arial')
        _chars[i] = {"height": my_num.get_window_extent(renderer=renderer).height,
                     "width": my_num.get_window_extent(renderer=renderer).width}
        my_num.remove()

    height = 0.0
    for char in label:
        if _chars[char]['height'] > height:
            height = _chars[char]['height']
    print(height)
    return height


dataframe = _totals_as_percentage(dataframe)

bars = []
colors_li = ['#FFEBB0', '#FFDF91', '#FED272', '#FEC653', '#FDB934', '#FAA438', '#F88F3B', '#F57A3F', '#F36542',
             '#F05046']
legend_labels = ['less than 10%', '10%-19%', '20%-29%', '30%-39%', '40%-49%', '50%-59%', '60%-69%', '70%-79%',
                 '80%-89%', '90%-100%']
financials = dataframe["Financials"].unique()
max_c = max(dataframe['Colour'].values)

if max_c >= 0.5 and max_c <= 1:
    legend_labels = legend_labels
elif max_c >= 0.4 and max_c <= 0.499:
    legend_labels = legend_labels[:-1]
elif max_c >= 0.3 and max_c <= 0.399:
    legend_labels = legend_labels[:-2]
elif max_c >= 0.2 and max_c <= 0.299:
    legend_labels = legend_labels[:-3]
elif max_c >= 0.15 and max_c <= 0.199:
    legend_labels = legend_labels[:-4]
elif max_c >= 0.1 and max_c <= 0.149:
    legend_labels = legend_labels[:-5]
elif max_c >= 0.05 and max_c <= 0.099:
    legend_labels = legend_labels[:-6]
elif max_c >= 0.025 and max_c <= 0.049:
    legend_labels = legend_labels[:-7]
elif max_c >= 0.01 and max_c <= 0.025:
    legend_labels = legend_labels[:-8]
else:
    legend_labels = legend_labels[:-9]

x = [0]

for s in range(len(sectors)):
    done = False
    if s != 0 and not done:
        x.append(size[s] + x[s-1])
        done = True

x_ticks = []
for i in range(len(financials)):
    if i == 0:
        x_ticks.append(financials[i] / 2)
    else:
        x_ticks.append(np.sum(financials[0:i]) + financials[i] / 2)


for s in range(len(sectors)):
    acc = 0
    bars.append([])
    for i in range(rows):
        if dataframe["Sector"][i] == sectors[s]:
            if dataframe['Colour'][i] >= 0.5 and dataframe['Colour'][i] <= 1:
                color = colors_li[9]
            elif dataframe['Colour'][i] >= 0.4 and dataframe['Colour'][i] <= 0.499:
                color = colors_li[8]
            elif dataframe['Colour'][i] >= 0.3 and dataframe['Colour'][i] <= 0.399:
                color = colors_li[7]
            elif dataframe['Colour'][i] >= 0.2 and dataframe['Colour'][i] <= 0.299:
                color = colors_li[6]
            elif dataframe['Colour'][i] >= 0.15 and dataframe['Colour'][i] <= 0.199:
                color = colors_li[5]
            elif dataframe['Colour'][i] >= 0.1 and dataframe['Colour'][i] <= 0.149:
                color = colors_li[4]
            elif dataframe['Colour'][i] >= 0.05 and dataframe['Colour'][i] <= 0.099:
                color = colors_li[3]
            elif dataframe['Colour'][i] >= 0.025 and dataframe['Colour'][i] <= 0.049:
                color = colors_li[2]
            elif dataframe['Colour'][i] >= 0.01 and dataframe['Colour'][i] <= 0.025:
                color = colors_li[1]
            else:
                color = colors_li[0]

            bar = dataframe["Size"][i]
            b = plt.bar(x[s],
                        bar,
                        color=color,
                        bottom=acc,
                        edgecolor='#414042',
                        linewidth=0.5,
                        align='center',
                        width=dataframe['Financials'][i],
                        zorder=3)
            acc = np.add(acc, bar)
            # bars[s].append(b)
for index, container in enumerate(ax.containers):
    labels = [dataframe["Brand"][index]]

    # for i in range(len(labels)):
    #     rect = container[i]
    #     print(rect.get_height())
    #     if rect.get_height() < 2:
    #         labels[i] = ''

    plt.gca().bar_label(
        container,
        labels=labels,
        label_type='center',
        color='black',
        weight='normal',
        size=8)

legend_elements = [
    Line2D([0], [0], marker='o', color='w', label=legend_labels[i], markerfacecolor=colors_li[i], markersize=15) for i
    in range(len(legend_labels))
]

axins = inset_axes(
    plt.gca(),
    width="5%",  # width: 50% of parent_bbox width
    height="50%",  # height: 5%
    loc="lower right",
    bbox_to_anchor=(0.07, 0, 1, 1),
    bbox_transform=plt.gca().transAxes,
    borderpad=0,
)

cbar = plt.gcf().colorbar(cm.ScalarMappable(
    cmap=c.ListedColormap(colors_li)),
    cax=axins,
    # location='bottom',
    aspect=10,
    shrink=0.35,
    ticks=[0, 1],
    orientation='vertical'
)
cbar.ax.set_yticklabels(['Low', 'High'])

ax.get_yaxis().set_visible(False)
ax.set_xticks(x, sectors)
ax.xaxis.grid(False, which='minor')
ax.spines['bottom'].set_color('#414042')
ax.spines['top'].set_color('#414042')
ax.spines['right'].set_color('#414042')
ax.spines['left'].set_color('#414042')
ax.xaxis.tick_top()
ax.xaxis.set_tick_params(which='major', top=False)
ax.set_ylim(ax.get_ylim()[::-1])
plt.show()

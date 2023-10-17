"""
This file is to handle the creation of pie charts for the data-visualisation project
The dataVisualization method to use is dougnut
Inputs: A dataframe with field data (refer to README.md for structure of data)
Is typically called form Main.py
"""
import matplotlib.pyplot as plt
import pandas as pd

import dataVisualization.susmon_colours as sc
from dataVisualization.exceptions import InvalidInputDataError



def _handle_data(dataframe: pd.DataFrame) -> tuple[
    list[str], list[str], list[str]]:
    """
    Data handling so that the data is easier passed to MatPlotLib.pies
    :param dataframe: A dataframe in which the operations will be performed
    :param headers: The Headers to check on the dataframe
    :param colour_list: a list of colors the be used (colors of wedges)
    :param slide: the slide which this chart is for (used for error functionality)
    :return: size_of_groups, percentages, colours
    """
    size_of_groups = []
    percentages = []
    colors = []

    # get the data column names
    headers = dataframe.columns.tolist()
    headers.pop(0)  # remove the Subject col
    for i in range(0, len(headers) - headers.index('Total')):
        # remove the Total col and all cols after it
        # leaving just the data cols
        headers.pop()

    color_list = sc.get_colour_set(headers)

    # trim the dataframe
    dataframe = dataframe[:10]

    # work out how many non-zero data points we have ad ajust colours accordingly
    for i in range(len(headers)):
        if dataframe[headers[i]].values[0] > 0:
            size_of_groups.append(dataframe[headers[i]].values[0])
            colors.append(color_list[i])
    total = sum(size_of_groups)

    # create labels for % amounts and if no non-zero data just leave without creating chart
    if total > 0:
        for value in size_of_groups:
            percentages.append(str(round((value * 100))) + '%')
    else:
        return [], [], []

    # put things in the order we want them to appear on the pie
    size_of_groups.reverse()
    percentages.reverse()
    colors.reverse()

    return size_of_groups, percentages, colors


def _label_correction(texts: list, wedges: list) -> None:
    """
    Modifies the text elements to change the color if the wedge is too dark
    and then removes the label if the value is less than 5%
    :param texts: A list of the label matplotlib.text.Text instances.
    :param wedges: A list of matplotlib.patches.Wedge instances
    """

    for text, wedge in zip(texts, wedges):
        if wedge.properties()['facecolor'] == (0.2549019607843137,
                                               0.25098039215686274,
                                               0.25882352941176473, 1.0):
            text.set_color('white')
        else:
            text.set_color('black')

        if int(text.get_text().split('%')[0]) <= 5:
            text.set_text('')


def doughnut(dataframe: pd.DataFrame) -> plt.Figure:
    """
    creates a doughnut chart and retuns the Figure
    :param dataframe: a Dataframe containing the table data for this chart
    """

    size_of_groups, percentages, colormode = _handle_data(dataframe)

    if len(size_of_groups) == 0:
        # if there is no data to be plotted raise exception
        raise InvalidInputDataError('')

    # plotting the given data on to a pie chart
    wedges, texts = plt.pie(size_of_groups,
                            labels=percentages,
                            labeldistance=0.67,
                            textprops={
                                'fontsize': 15,
                                'weight': 'bold',
                                'rotation_mode': 'anchor',
                                'va': 'center',
                                'ha': 'center'
                            },
                            wedgeprops={
                                'linewidth': 3,
                                'edgecolor': 'white'
                            },
                            colors=colormode,
                            startangle=90)

    _label_correction(texts, wedges)

    # add a circle at the center to transform it in a donut chart
    my_circle = plt.Circle((0, 0), 0.45, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # save the plot as a file
    return plt.gcf()

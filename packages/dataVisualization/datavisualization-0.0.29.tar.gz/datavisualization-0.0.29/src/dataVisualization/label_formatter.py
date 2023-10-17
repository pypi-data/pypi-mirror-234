import matplotlib.pyplot as plt
import matplotlib.container as container
import pandas as pd
import string

_char_length = {}
special_chars = [" ", '\n', '&', '-', 'ē', 'é', '.', "'", 'ä']
file = "/Users/ethan/Library/CloudStorage/GoogleDrive-ethan@susmon.com/.shortcut-targets-by-id/1yv5Tb8aODBZ75uclq_x7pfAUuSR3Ijlb/SusMon/5 Methodology/Company Name Abbreviations v4.xlsb.xlsx"
brand_abbreviations:pd.DataFrame = pd.read_excel(file, sheet_name="Brand Dataset")
company_abbreviations:pd.DataFrame = pd.read_excel(file, sheet_name="Corporate Dataset")
abbreviations = pd.concat([brand_abbreviations, company_abbreviations])
abbreviations = abbreviations.set_index('Company')


def _setup(size):
    renderer = plt.gcf().canvas.get_renderer()
    for i in list(string.printable) + special_chars:
        my_num = plt.text(0, 0, i, size=size, family='Arial')
        _char_length[i] = {"height": my_num.get_window_extent(renderer=renderer).height,
                           "width": my_num.get_window_extent(renderer=renderer).width}
        my_num.remove()


def _label_width(label:str) -> float:
    """
    get the length of a given label
    :param label:
    :return: the length of the label as a float
    """
    length = 0.0
    for char in label:
        length = length + _char_length[char]["width"]
    return length


def _label_height(label:str) -> float:
    """
    get the height of a given label
    :param label:
    :return: the length of the label as a float
    """
    height = 0.0
    for char in label:
        if _char_length[char]["height"] > height:
            height = _char_length[char]["height"]
        if char == '\n':
            height = height * 2
    return height


def _get_center(rect:container):
    bbox_points = rect.get_bbox().get_points()
    return (((bbox_points[0][0] + bbox_points[1][0]) / 2), ((bbox_points[0][1] + bbox_points[1][1]) / 2))


def format_label(ax, rect, label, format) -> bool:
    """
    This function takes a label and tries to make it fit in a given
    container by performing a list of operations in it
    :param ax:
    :param label:
    :return:
    """
    # fill _char_length dictionary
    fit = False
    # while not fit:
    #     fit = _try_horizontal(ax, rect, label)
    #     if fit: break
    #     fit = _try_first_abreviated_horizontal(ax, label)
    #     if fit: break
    #     fit = _try_second_abreviated_horizontal(ax, label)
    #     if fit: break
    #     fit = _try_vertical(ax, label)
    #     if fit: break
    #     fit = _try_first_abreviated_vertical(ax, label)
    #     if fit: break
    #     fit = _try_second_abreviated_vertical(ax, label)
    #     if fit: break
    #     fit = _blank_label(ax, label)
    try:
        row = [label] + abbreviations.loc[label].values.tolist()
    except KeyError:
        fit = True

    rotations = ['horizontal', 'vertical']
    for size in range(format['Values Font Size'], 2, -1):
        _setup(size)
        for lb in row:
            for r in rotations:
                if not fit:
                    if pd.notna(lb):
                        if r == 'horizontal':
                            if _label_width(lb) < rect.get_window_extent().width and _label_height(lb) < rect.get_window_extent().height:
                                fit = True
                                ax.annotate(text=lb,
                                            xy=_get_center(rect),
                                            fontsize=size,
                                            rotation=r,
                                            horizontalalignment='center',
                                            verticalalignment='center')
                        elif r == 'vertical':
                            if _label_width(lb) < rect.get_window_extent().height and _label_height(lb) < rect.get_window_extent().width:
                                fit = True
                                ax.annotate(text=lb,
                                            xy=_get_center(rect),
                                            fontsize=size,
                                            rotation=r,
                                            horizontalalignment='center',
                                            verticalalignment='center')

    # if not horizontal and vertical dont work just remove the label
    if not fit:
        fit = True

    return ax


if __name__ == '__main__':
    print(abbreviations)
    format_label('Carlsberg Group')
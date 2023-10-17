"""
This file handles all of the susmon colours and associates them to hex-decimal values
"""

colours = {'environmental': '#8DC63F', 'social': '#E2E41E', 'governance': '#00B4AA',
           'twitter': '#14BEF0', 'facebook': '#2382CA', 'instagram': '#965096', 'youtube': '#F05046',
           'sustainability': '#FDB934', 'non-sustainability': '#414042',
           'corporate': '#2382CA', 'brand': '#14BEF0', 'followers': '#FDB934'}

def get_colour(name:str) -> str:
    """
    get the color value of a single given name
    :param name: the name to get the associated value for
    :return: the associated color to the given name
    """
    return colours[name]

def get_colour_set(names:list[str]) -> list[str]:
    """
    for each name in the given list of colors return the associated color
    :param names: a list of names of colors
    :return: a list of colors
    """
    cols = []
    for i in names:
        cols.append(colours[i.lower()])
    return cols

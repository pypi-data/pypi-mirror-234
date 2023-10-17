from pathlib import Path

import plotly.graph_objects as go
import susmon_colours
from label_formatter import format_label_char
import pandas as pd

def _get_data_cols(dataframe: pd.DataFrame) -> list[str]:
    """
    Takes a given dataframe and returns the names of data columns,
    these are the columns with data used to make the bars.
    The dataframe should be in te following format:
    Subject | data_cols* | Total | optional cols | ect.
    where data_cols is a variable number of cols that names will be returned
    :param dataframe: the dataframe we want to get the cols from
    :return:
    """
    # get the data column names
    cols = dataframe.columns.tolist()
    cols.pop(0)  # remove the Subject col
    for i in range(0, len(cols) - cols.index('Total')):
        # remove the Total col and all cols after it
        # leaving just the data cols
        cols.pop()
    return cols


def single_layer_sankey(input_file: str, sheet_name: str):
    input_file = Path(input_file).resolve()
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    df.columns = df.iloc[0]
    df = df[1:]

    for index, row in df.iterrows():
        sectors = ['Alcoholic Drinks','Beverages','Consumer Healthcare', 'Food', 'Home Care', 'Personal Care', 'Petcare', 'Tobacco', 'Other FMCG', 'Rest of business']
        sector_values = []
        sector_loc = []
        i = 0
        for s in sectors:
            sector_values.append(row[s])
            if pd.notna(row[s]):
                sector_loc.append((i, s, row[s]))
                i = i + 1
        if len(sector_loc) != 0:
            comp = (len(sector_loc), row['Company'])
            print(sector_loc)
            print(comp)
            source = []
            labels = []
            values = []
            target = [comp[0] for i in range(len(sector_loc))]
            for item in sector_loc:
                source.append(item[0])
                labels.append(item[1])
                values.append(item[2])
            print(source)
            print(target)
            print(values)
            color_list = ['#8DC63F', '#E2E41E', '#00B4AA', '#14BEF0', '#2382CA', '#965096', '#F05046', '#FDB934', '#414042', '#2382CA',
             '#14BEF0']
            colors = []
            for v in labels:
                colors.append(color_list[sectors.index(v)])
            colors.append('#FDB934')
            colors_low = []
            for c in colors:
                splitc = c.strip('#')
                rgb = tuple(int(splitc[i:i+2], 16) for i in (0, 2, 4))
                colors_low.append('rgba' + str(rgb + (0.75,)))

            print('----------')
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=colors
                ),
                link=dict(
                    source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=target,
                    value=values,
                    color = colors_low
                ))])

            fig.update_layout(font_family="Arial", title_text=comp[1] + ' Sales', font_size=12, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig.write_image("../../Helen/tests/" + comp[1] + ".svg")



    fig.write_html("fig1.html")


def format_labels(labels: str, length: int) -> list[str]:
    new_lbs = []
    for lb in labels:
        new_lbs.append(format_label_char(lb, length))
    return new_lbs


def sector_sankey(dataframe: pd.DataFrame, name: str):
    labels = dataframe['Company'].tolist()
    labels = format_labels(labels, 17)
    values = dataframe['Values'].tolist()
    for i in range(len(labels)):
        if '(estimate)' in labels[i]:
            labels[i] = f"<i><b>{labels[i].split('(')[0]}</b></i> {str(round(values[i], 1))}"
        else:
            labels[i] = f"<b>{labels[i]}</b> {str(round(values[i], 1))}"
    source = [i for i in range(len(labels))]
    target = [len(labels) for i in range(len(labels))]
    labels.insert(len(labels), f"<b>{name}</b> {round(sum(values), 1)}")

    colors = {"Alcoholic Drinks": ('rgba(240,80,70,1)', 'rgba(240,80,70,0.75)'),
              "Beverages": ('rgba(150,80,150,1)', 'rgba(150,80,150,0.75)'),
              "Consumer Healthcare": ('rgba(226,228,30,1)', 'rgba(226,228,30,0.75)'),
              "Food": ('rgba(141,198,63,1)', 'rgba(141,198,63,0.75)'),
              "Home Care": ('rgba(20,190,240,1)', 'rgba(20,190,240,0.75)'),
              "Personal Care": ('rgba(160,228,247,1)', 'rgba(160,228,247,0.75)'),
              "Pet Care": ('rgba(35,130,202,1)', 'rgba(35,130,202,0.75)'),
              "Tobacco": ('rgba(0,180,170,1)', 'rgba(0,180,170,0.75)')}
    color = colors[name]
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=color[0]
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=color[1]
        ))])

    fig.update
    fig.update_layout(font_family="Arial", title_text=name + ' Sales', font_size=12)
    fig.write_image("../../Helen/tests/" + name + ".svg")


def corporate_sankey():
    source = [0,1,2,3,4,5,8,9,6,7]
    target = [6,6,6,7,7,7,10,10,10,10]
    values = [28,11,3.9,13,9,1,17.5,20.2,43,23,105.4]
    labels = ['powdered & liquid beverages', 'Milk products','Water', 'Prepared dishes', 'confectionery', 'Ice cream', 'Beverages', 'Food', 'Personal care', 'Pet care', 'Nestle']
    x = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.35, 0.35, 0.35, 0.35, 1]
    y = [0.15, 0.28, 0.335, 0.45, 0.53, 0.575, 0.15, 0.40, 0.65, 0.9, 0.5]
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(66,135,245,1)',
            x=x,
            y=y
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(66,135,245,0.75)'
        ))])
    fig.update
    fig.update_layout(font_family="Arial", title_text='Nestle' + ' Sales', font_size=12)
    fig.show()

def auto_corp_sankey(df: pd.DataFrame):
    layer1_labels = df['Layer 1 labels'].values.tolist()
    layer2_labels = df['Layer 2 labels'].values.tolist()
    layer3_labels = df['Layer 3 labels'].values.tolist()
    print(layer1_labels)
    print(layer2_labels)
    print(layer3_labels)
    layer1_values = df['Layer 1 Values'].values.tolist()
    layer2_values = df['Layer 2 Values'].values.tolist()
    layer3_values = df['Layer 3 Values'].values.tolist()

    routes = {"source": [], "dest": [], 'values': [], 'labels': []}

    snum = 0
    dnum = 0

    for i in range(len(layer1_labels)):
        if pd.notna(layer1_labels[i]):
            routes['source'].append(snum)
            routes['values'].append(layer1_values[i])
            routes['labels'].append(layer1_labels[i])
            snum = snum + 1
    for i in range(len(layer2_labels)):
        if pd.notna(layer2_labels[i]):
            routes['source'].append(snum)
            routes['values'].append(layer2_values[i])
            routes['labels'].append(layer2_labels[i])
            dnum = snum
            print(f'dnum = {dnum}')
            snum = snum + 1
            print(f'snum = {snum}')
            routes['dest'].append(dnum)
        else:
            dnum = snum - 1
            print(f'dnum = {dnum}')
            routes['dest'].append(dnum)
    for i in range(len(layer3_labels)):
        if pd.notna(layer3_labels[i]):
            routes['values'].append(layer3_values[i])
            routes['labels'].append(layer3_labels[i])
            dnum = snum + 1
            routes['dest'].append(dnum)
        # else:
        #     dnum = snum
        #     routes['dest'].append(dnum)
    print(routes)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=routes['labels'],
            color='rgba(66,135,245,1)',
        ),
        link=dict(
            source=routes['source'],
            target=routes['dest'],
            value=routes['values'],
            color='rgba(66,135,245,0.75)'
        ))])
    fig.update
    fig.update_layout(font_family="Arial", title_text='Monster Energy Sales', font_size=12)
    fig.show()

def main():
    df = pd.read_excel("/Users/ethan/PycharmProjects/data-visualization/Helen/Sankey charts trial data.xlsx", 'Monster Energy')
    auto_corp_sankey(df)
    # sectors = ["Alcoholic Drinks", "Beverages", "Consumer Healthcare", "Food", "Home Care", "Personal Care", "Pet Care", "Tobacco"]
    # for s in sectors:
    #     df = pd.read_excel("../../Helen/AUG23 - Sankey trial numbers.xlsx", s)
    #     sector_sankey(df, s)

if __name__ == '__main__':
    main()
# single_layer_sankey("../../Helen/AUG23 - Sankey trial numbers.xlsx", "2022 Company sales by sector")
# two_layer_sankey("../../Helen/AUG23 - Sankey trial numbers.xlsx", "2022 Company sales by sector")
import pandas as pd
import numpy as np
import random as rd
from pathlib import Path
from openpyxl import load_workbook

def get_labels(color):
    if color == 'Sus / Non-Sus':
        return ['Name', 'Sustainability', 'Non-sustainability', 'Total']
    elif color == 'ESG':
        return ['Name', 'Environmental', 'Social', 'Governance', 'Total']
    elif color == 'Corporate / Brand':
        return ['Name', 'Corporate', 'Brand', 'Total']
    elif color == 'Twitter / Facebook / Instagram / YouTube':
        return ['Name', 'Twitter', 'Facebook', 'Instagram', 'YouTube', 'Total']


def fill_cols(data: pd.Series, cols: list[str], rows:int):
    dict = {}
    for col in cols:
        for row in range(int(rows)):
            if col == 'Name' and col not in dict.keys():
                dict[col] = ['Test']
            elif col == 'Name':
                dict[col].append('test')
            elif col == 'Total':
                continue
            elif col not in dict.keys():
                dict[col] = [np.floor(rd.uniform(data['Min'], data['Max']))]
            else:
                dict[col].append(np.floor(rd.uniform(data['Min'], data['Max'])))

    df = pd.DataFrame.from_dict(dict)
    return df


def main():
    input_path = Path('New_Test_Data.xlsx')
    strat_path = Path('testing data strategy.xlsx')

    df = pd.read_excel(strat_path, sheet_name='Bars')
    try:
        # Generating workbook
        ExcelWorkbook = load_workbook(input_path)
        # Generating the writer engine
        writer = pd.ExcelWriter(input_path, engine='openpyxl')
        # Assigning the workbook to the writer engine
        writer.book = ExcelWorkbook

        for i in range(len(df.index)):
            if df.loc[i]['Form'] not in ['0 out tests', 'Param tests', 'Value tests', 'Row tests', 'Visability Test', np.nan, 'Form']:
                print(df.loc[i])
                fill_cols(df.loc[i], get_labels(df.loc[i]['Colour Scheme']), df.loc[i]['Rows']).to_excel(writer, sheet_name='bars-' + str(i), index=False)

        writer.save()
    except TypeError as e:
        print(e.with_traceback())
        writer.close()


    writer.close()

if __name__ == '__main__':
    main()
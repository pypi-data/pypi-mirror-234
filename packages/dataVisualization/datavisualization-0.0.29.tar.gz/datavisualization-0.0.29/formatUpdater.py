import pandas as pd
import numpy as np
import random as rd
from pathlib import Path
from openpyxl import load_workbook

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

        dict = {}

        for i in range(len(df.index)):
            if df.loc[i]['Form'] not in ['0 out tests', 'Param tests', 'Value tests', 'Row tests', 'Visability Test',
                                         np.nan, 'Form']:
                if 'Slide No.' not in dict.keys():
                    dict['Slide No.'] = ['bars-' + str(i)]
                    dict['Slide Title'] = ['test-' + str(i)]
                    dict['Chart Title'] = ['NA']
                    dict['Chart Type'] = ['Stacked Bar']
                    dict['Data Type'] = ['Sus vs. Non-Sus']
                    dict['Data Order'] = ['Sustainability, Non-sustainability']
                    dict['Name'] = ['Name']
                    dict['Chart Width'] = [df.loc[i]['Chart Width']]
                    dict['Name - Font Weight'] = ['Normal']
                    dict['Name - Font Size'] = ['8']
                    dict['Values - Font Weight'] = ['Normal']
                    dict['Values - Font Size'] = ['8']
                    dict['Legend'] = [df.loc[i]['Legend']]
                    dict['Legend Position'] = ['Bottom centre']
                    dict['Gridlines'] = [df.loc[i]['Gridlines']]
                    dict['X - Axis Scale'] = [df.loc[i]['X-Axis Scale']]
                    dict['Segment Values'] = [df.loc[i]['Segment Values']]
                    dict['Total Values Visable'] = [df.loc[i]['Total Values Visable']]
                    dict['Ranking Values'] = ['Sustainability posts, Non-sustainability posts, Brands']
                    dict['Ranking Order'] = ['Ascending, descending']
                    dict['Top X'] = ['No']
                    dict['Denominator'] = ['1']
                    dict['Decimal Places'] = ['0']
                    dict['Total Values - remove 0'] = ['No']
                    dict['Pair Chart'] = ['No']
                    dict['Comment'] = [df.loc[i]['Comment']]
                else:
                    dict['Slide No.'].append('bars-' + str(i))
                    dict['Slide Title'].append('test-' + str(i))
                    dict['Chart Title'].append('NA')
                    dict['Chart Type'].append('Stacked Bar')
                    dict['Data Type'].append('Sus vs. Non-Sus')
                    dict['Data Order'].append('Sustainability, Non-sustainability')
                    dict['Name'].append('Name')
                    dict['Chart Width'].append(df.loc[i]['Chart Width'])
                    dict['Name - Font Weight'].append('Normal')
                    dict['Name - Font Size'].append('8')
                    dict['Values - Font Weight'].append('Normal')
                    dict['Values - Font Size'].append('8')
                    dict['Legend'].append(df.loc[i]['Legend'])
                    dict['Legend Position'].append('Bottom centre')
                    dict['Gridlines'].append(df.loc[i]['Gridlines'])
                    dict['X - Axis Scale'].append(df.loc[i]['X-Axis Scale'])
                    dict['Segment Values'].append(df.loc[i]['Segment Values'])
                    dict['Total Values Visable'].append(df.loc[i]['Total Values Visable'])
                    dict['Ranking Values'].append('Sustainability posts, Non-sustainability posts, Brands')
                    dict['Ranking Order'].append('Ascending, descending')
                    dict['Top X'].append('No')
                    dict['Denominator'].append('1')
                    if df.loc[i]['Max'] >= 1000000:
                        dict['Decimal Places'].append('3')
                    else:
                        dict['Decimal Places'].append('0')
                    dict['Total Values - remove 0'].append('No')
                    dict['Pair Chart'].append('No')
                    dict['Comment'].append(df.loc[i]['Comment'])

            pd.DataFrame.from_dict(dict).to_excel(writer, sheet_name='Format', index=True)
        writer.save()
    except TypeError as e:
        print(e.with_traceback())
        writer.close()


    writer.close()

if __name__ == '__main__':
    main()
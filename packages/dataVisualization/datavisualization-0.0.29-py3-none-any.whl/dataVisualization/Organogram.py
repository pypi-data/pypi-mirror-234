import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go


def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations


nr_vertices = 25
v_label = list(map(str, range(nr_vertices)))
G = Graph.Tree(nr_vertices, 2) # 2 stands for children number
lay = G.layout('rt')

position = {k: lay[k] for k in range(nr_vertices)}
Y = [lay[k][1] for k in range(nr_vertices)]
M = max(Y)

es = EdgeSeq(G) # sequence of edges
E = [e.tuple for e in G.es] # list of edges

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2*M-position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

labels = v_label

fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   ))
fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='bla',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8
                  ))

axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

fig.update_layout(title= 'Tree with Reingold-Tilford Layout',
              annotations=make_annotations(position, v_label),
              font_size=12,
              showlegend=False,
              xaxis=axis,
              yaxis=axis,
              margin=dict(l=40, r=40, b=85, t=100),
              hovermode='closest',
              plot_bgcolor='rgb(248,248,248)'
              )
fig.show()


# # libraries
# import pandas as pd
# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
#
#
# def make_connections(df: pd.DataFrame)->pd.DataFrame:
#     # print(df)
#     rtn = pd.DataFrame(columns=['from', 'to'])
#     sector = df['Sector'].unique().tolist()
#     categories = df['Category'].unique().tolist()
#     for cat in categories:
#         new_link = pd.Series({'from': sector[0], 'to': cat})
#         rtn = pd.concat([rtn, new_link.to_frame().T], ignore_index=True)
#         for i in range(len(df['Corporate'])):
#             row = df.iloc[[i]]
#             corp = df.iloc[[i]]['Corporate'].values[0]
#             print(row['Category'].values[0] == cat)
#             if(row['Category'].values[0] == cat):
#                 new_link = pd.Series({'from': cat, 'to': corp})
#                 rtn = pd.concat([rtn, new_link.to_frame().T], ignore_index=True)
#     print(rtn)
#     return rtn
#
#
# file = "/Users/ethan/PycharmProjects/data-visualization/Helen/dendrogram/Dendrogram trial data.xlsx"
# dataframe: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name="Alcoholic Drinks")
# links = make_connections(dataframe)
# # # Build a dataframe with your connections
# # df = pd.DataFrame({'from': ['A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F'],
# #                    'to': ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', '1', '2']})
#
# # # Build your graph
# # G = nx.from_pandas_edgelist(links, 'from', 'to')
#
#
# # Spring
# orgchart=nx.from_pandas_edgelist(links, source='from', target='to')
# p=nx.drawing.nx_pydot.to_pydot(orgchart)
# nodes = p.get_node_list()
# for node in nodes:
#     node.set_shape('box')
# p.write_png('orgchart.png')
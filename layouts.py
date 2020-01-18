# layouts.py

import dash
import dash_table
# import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

data = 'cubs-2016-baseball.csv'
df_all = pd.read_csv(data)

# df_all['Last'] = df_all['Name']
# df_all['First'] =

#remove pitchers
df = df_all[df_all['Pos'] != 'P'].copy()

hidden_cols=['Rk','OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB']
# all_cols = df.columns
visible_cols =['Pos','Name','Age','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA']

# visible_cols = list(set(all_cols) - set(hidden_cols))

layout = html.Div([
    html.H3('Test App - Export DataTable to Excel'),

    dash_table.DataTable(
        id='table',
        # columns=[{"name": i, "id": i} for i in df.columns],
        columns=[{"name": i, "id": i} for i in visible_cols] +
                [{"name": i, "id": i, 'hideable': True} for i in hidden_cols],
        hidden_columns=hidden_cols,
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        # sort_mode="multi",
        # hidden_columns=['OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB'],
        # page_action='native',
        # page_current= 0,
        # page_size= 10,

        style_header={'backgroundColor': 'rgb(230, 230, 230)',
                      'fontWeight': 'bold'},
        style_data_conditional=[
                {
                'if': {
                'row_index': 'odd'
                },
                'backgroundColor': 'rgb(248, 248, 248)'
                },
            ],
        # style_table={'overflowX': 'scroll'},
        ), # end datatable

    # Download Selection
    html.A(
        'Download *SELECTED* Data',
        id='download-link',
        href="",
        target="_blank"
    ),

    # Download Button
    # html.Div([
    #   html.A(html.Button('Download Data', id='download-button'), id='download-link')
    #   ]),

    html.Div([
    html.P(id='display-value')
    ])
])

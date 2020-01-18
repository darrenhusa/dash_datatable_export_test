# layouts.py

import dash
import dash_table
# import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

data = 'cubs-2016-baseball.csv'
df_all = pd.read_csv(data)
# print(df_all.columns)
# print('')

# remove pitchers
df = df_all[df_all['Pos'] != 'P'].copy()

new = df['Name'].str.split(expand=True)
df['First'] = new[0]
df['Last'] = new[1]

df['BA'] = df['BA'].round(3)

hidden_cols=['Rk','OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB']
# all_cols = df.columns
visible_cols =['Pos','Name','Last','First','Age','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA']

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

        #FIX - does NOT work!!!!!
        # tooltip={'Pos': "Player's position"},

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
    # html.A(
    #     'Download *SELECTED* Data',
    #     id='download-link',
    #     href="",
    #     target="_blank"
    # ),

    html.A(
        'Download Data',
        id='download-link',
        download="rawdata.csv",
        # href="",
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

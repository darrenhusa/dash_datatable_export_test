# layouts.py

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
# import pandas as pd
positions = sorted(['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'IF', 'UT', 'OF'])
# print(positions)
# print('')

# options = [{'label': pos, 'value': pos} for pos in positions]
# print(options)
# print('')
# [{"name": i, "id": i, 'deletable': True} for i in teams]
# data = 'cubs-2016-baseball.csv'
# df_all = pd.read_csv(data)
# # print(df_all.columns)
# # print('')
#
# # remove pitchers
# df = df_all[df_all['Pos'] != 'P'].copy()
#
# new = df['Name'].str.split(expand=True)
# df['First'] = new[0]
# df['Last'] = new[1]
#
# df['BA'] = df['BA'].round(3)

hidden_cols=['Rk','OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB']
# all_cols = df.columns
visible_cols =['Pos','Name','Last','First','Age','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA']

# visible_cols = list(set(all_cols) - set(hidden_cols))

layout = html.Div([
    html.H3('Test App - Export DataTable to Excel'),
    # dcc.Dropdown(
    #     options=[
    #         {'label': "Men's Baseball", 'value': 'MBS'},
    #         {'label': "Men's Basketball", 'value': 'MBB'},
    #         {'label': "Men's Soccer", 'value': 'MSC'}
    #     ],
    #     value='MBS'
    # ),

    dcc.Dropdown(
        id='position_filter',
        options=[{'label': pos, 'value': pos} for pos in positions],
        # [{'label': "C", 'value': 'C'},
        #     {'label': "1B", 'value': '1B'},
        #     {'label': "2B", 'value': '2B'},
        #     {'label': "3B", 'value': '3B'},
        #     {'label': "SS", 'value': 'SS'},
        #     {'label': "LF", 'value': 'LF'},
        #     {'label': "CF", 'value': 'CF'},
        #     {'label': "RF", 'value': 'RF'},
        #     {'label': "IF", 'value': 'IF'},
        #     {'label': "UT", 'value': 'UT'},
        #     {'label': "OF", 'value': 'OF'},
        # ],
        searchable=False,
        placeholder="Filter by Position (Pos)",
        # multi=True,
        value=['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'IF', 'UT', 'OF'],
        # style={'display': 'inline-block', 'width': '30%', 'margin-left': '7%'}
    ),

    dash_table.DataTable(
        id='table',
        # columns=[{"name": i, "id": i} for i in df.columns],
        columns=[{"name": i, "id": i} for i in visible_cols] +
                [{"name": i, "id": i, 'hideable': True} for i in hidden_cols],
        hidden_columns=hidden_cols,

        #NOTE - use a calback to set the data for the datatable as in the dash dashboard below!!!!!
        #https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f#d574
        # data=df.to_dict('rows'),
        # data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",

        #FIX - does NOT work!!!!!
        # tooltip_data={'Pos': "Player's position"},
        # tooltip_data={'property': 'Pos',
        #               'value': "Player's position"},

        # tooltip_data=[{
        #     col: f"0 {col} th row"
        #     for col in ['Pos', 'Name', 'Last', 'First', 'Age']
        #     } ],

        # tooltip_data=[{
        #         col: f"{col} {i} th row"
        #         for col in _df.columns} for i in range(0,_df.shape[0])],
        # tooltip={'Pos': "Player's position"},
        # tooltip={'property': 'Pos',
        #          'value': "Player's position"},
        # tooltip={'property': 'Pos',
        #          'value': 'this is a test tooltip' },
        # column_conditional_tooltips=[
        #     {
        #         'if': {'column_id': 0, "row_index": 0},
        #         "value": "Player's position",
        #         "type": "text"
        #     },
        # ],

        sort_mode="multi",
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
        html.Button('Download Data', id='download-button'),
        id='download-link',
        download="rawdata.csv",
        # href="",
        target="_blank"
    ),

    # Download Button
    # html.Div([
    #   html.A(html.Button('Download Data', id='download-button'), id='download-link')
    #   ]),

    #diagnostic print - shows contents of DataTable
    # with and without filtering
    # removed for production version!
    # html.Div([
    # html.P(id='display-value')
    # ])
])

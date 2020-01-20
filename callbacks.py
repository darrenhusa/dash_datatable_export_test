# callbacks.py

from dash.dependencies import Input, Output, State

from app import app
import urllib.parse
import pandas as pd
import re

def extract_name_components(name):
    pattern = r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)'
    match = re.search(pattern, name)

    if match:
        first = match.group(1)
        last = match.group(2)

    return first, last


data = 'cubs-2016-baseball.csv'
df_all = pd.read_csv(data)
# print(df_all.columns)
# print('')

# remove pitchers
df = df_all[df_all['Pos'] != 'P'].copy()

# https://stackoverflow.com/questions/49247636/python-split-full-name-into-two-variables-with-possibly-multi-word-last-name
# temp = df['Name'].str.split(" ", n=1, expand=True)
# df['First'] = temp[0]
# df['Last'] = temp[1]

# temp = df['Name'].str.split(r'([a-z]+)\s([a-z\s]+)/i', n=1, expand=True)
# df['First'] = temp[0]
# df['Last'] = temp[1]
# df.head()
# print(temp)
# print('')

# df.name.str.replace(r'(\w+),\s*(\w+)', r'\2 \1')
# df['First'], df['Last'] = df['Name'].str.extract(r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)', expand=True)
# temp = df['Name'].str.extract(r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)', expand=True)
# print(temp)
# print('')

# df['First']  = df['Name'].apply(extract_name_components)[0]
# df['Last']  = df['Name'].apply(extract_name_components)[1]

df['First'] = df.apply(lambda row: extract_name_components(row['Name'])[0], axis=1)
df['Last'] = df.apply(lambda row: extract_name_components(row['Name'])[1], axis=1)

# df['First'] = temp[0]
# df['Last'] = temp[1]

# print(df['Name'].str.extract(r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)', expand=True))
# df['First'] = df['Name'].str.extract(r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)', expand=True)[0]
# df['Last'] = df['Name'].str.extract(r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)', expand=True)[1]
# df['temp'] = df['Name'].str.extract(r'(?P<First>[a-zA-Z]+)\s(?P<Last>[a-zA-Z\s]+)', expand=True)
# print(df['Last'], df['First'])
# print(df.temp)
# print('')
# want to remove the trailing special charatcers!!!
# df['temp'] = df['Name'].str.extract(r'([a-z]+)\s([a-z\s]+)/i')
# df['First'],df['Last'] = df['Name'].str.extract(r'([a-z]+)\s([a-z\s]+)/i')
# df.head()
# df['Last'] = df['Name'].str.split(" ", 1)[1]
# print(temp)
# df['First'] = temp.str.split(',', 1)
# df['Last'] = temp[1]
df['BA'] = df['BA'].round(3)
# print(df)
# print(df.head())
# print('')

@app.callback(
    Output('display-value', 'children'),
    [Input('table', 'derived_virtual_data')])
def display_value(data):
    return '{}'.format(data)


@app.callback(Output('table', 'data'),
              [Input('position_filter', 'value')])
def build_and_filter_table(pos):

    # df = pd.DataFrame.from_dict(data)

    # print('build_initial_table...')
    # print(team)
    # print('')
    if pos is None:
        # print('team is None!!!!!')
        return df.to_dict('records')
        # return df.to_dict('rows')

    if pos:
        # print('inside if...')
        if type(pos) == str:
            dff = df[df['Pos'].isin([pos])]
        else:
            dff = df[df['Pos'].isin(pos)]
    # else:
        # print('inside else...')
        # dff = df

    # print(dff)
    # print('')
    # return dff.to_dict('rows')
    return dff.to_dict('records')


@app.callback(
    Output('download-link', 'href'),
    [Input('table', 'derived_virtual_data')])
def update_download_link(derived_virtual_data):
    # df = derived_virtual_data.to_dict('records')

    df = pd.DataFrame.from_dict(derived_virtual_data)

    # print('inside update download link....')
    # print(derived_virtual_data)
    # print('')
    # print('')
    # dff = filter_data(filter_value)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

# @app.callback([Output('table', 'rows')],
#               [Input('team_filter', 'value')],
#               [State('table', 'derived_virtual_data')])
# @app.callback([Output('table', 'data')],
#               [Input('team_filter', 'value'),
#               Input('table', 'derived_virtual_data')])
# def filter_table(team, derived_virtual_data):
#
#     df = pd.DataFrame.from_dict(derived_virtual_data)
#
#     print('inside filter table...')
#     print(team)
#     print('')
#
#     if team:
#         print('inside if...')
#         dff = df[df['Pos'].isin([team])]
#     else:
#         print('inside else...')
#         dff = df
#
#     print(dff)
#     print('')
#     return dff.to_dict('records')
    # return dff.to_dict('rows')

# ccsj version
# should i use the onclick property of the html.button to trigger this action?????
#
# @app.callback(Output('download-link', 'href'),
#              [Input('table_data', 'derived_virtual_data'),
#              Input('download-button', 'onclick')])
# def set_download_link():
#     return '/download'
#
# @app.server.route('/download')
# def download_csv(data):
#     print('inside download as csv...')
#
#     # need to seialize the data string???
#
#     # print(data)
#     # value = flask.request.args.get('value')
#     # create a dynamic csv or file here using `StringIO`
#     # (instead of writing to the file system)
#     strIO = StringIO.StringIO()
#     # strIO.write('You have selected {}'.format(value))
#     strIO.seek(0)
#     return send_file(strIO,
#                      mimetype='text/csv',
#                      attachment_filename='downloadFile.csv',
#                      as_attachment=True)
#

# return everything
# def selected_data_to_csv(selected_data_dict):
#     return pd.DataFrame(selected_data_dict).to_csv()
#
# @app.callback(
#     Output('download-link', 'href'),
#     Output('display-value', 'children'),
#     [
#         Input('table', 'derived_virtual_data'),
#     ])
# def download_selected(selected_data):
#     print(derived_virtual_data)
#     print('')
#     print('inside download selected callback....')
#     if type(selected_data) == dict:
#         print('inside if branch')
#         ret_str = "{}{}".format(
#             "data:text/csv;charset=utf-8,%EF%BB%BF",
#             urllib.parse.quote(
#                 selected_data_to_csv(selected_data), encoding="utf-8"
#             )
#         )
#     else:
#         print('inside else branch')
#         ret_str = ""
#     return ret_str

# from dash =
# ########################################################################
# @app.callback(Output('my-link', 'href'), [Input('my-dropdown', 'value')])
# def update_link(value):
#     return '/dash/urlToDownload?value={}'.format(value)
#
# @app.server.route('/dash/urlToDownload')
# def download_csv():
#     value = flask.request.args.get('value')
#     # create a dynamic csv or file here using `StringIO`
#     # (instead of writing to the file system)
#     strIO = StringIO.StringIO()
#     strIO.write('You have selected {}'.format(value))
#     strIO.seek(0)
#     return send_file(strIO,
#                      mimetype='text/csv',
#                      attachment_filename='downloadFile.csv',
#                      as_attachment=True)

# Callback for excel download
#############################
# @app.callback(
#     Output('download-link', 'href'),
#     [Input('table', 'derived_virtual_data')])
# # def update_link(start_date, end_date):
# # 	return '/cc-travel-report/birst-category/urlToDownload?value={}/{}'.format(dt.strptime(start_date,'%Y-%m-%d').strftime('%Y-%m-%d'),dt.strptime(end_date,'%Y-%m-%d').strftime('%Y-%m-%d'))
# @app.server.route("/")
# def download_datable1_to_excel(table_data):
#     # value = flask.request.args.get('value')
#     #here is where I split the value
#     # value = value.split('/')
#     # start_date = value[0]
#     # end_date = value[1]
#
#     # filename = datestamp + '_birst_category_' + start_date + '_to_' + end_date + '.xlsx'
# 	# Dummy Dataframe
#     # d = {'col1': [1, 2], 'col2': [3, 4]}
#     df = pd.DataFrame(data=table_data)
#
#     buf = io.BytesIO()
#     excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
#     # download_1 = update_first_download(start_date, end_date, None, 'Birst Category')
#     download_1.to_excel(excel_writer, sheet_name="sheet1", index=False)
#     # df.to_excel(excel_writer, sheet_name="sheet1", index=False)
#     excel_writer.save()
#     excel_data = buf.getvalue()
#     buf.seek(0)
#
#     return send_file(
#         buf,
#         mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         attachment_filename='cubs-2016-stats.xlsx',
#         as_attachment=True,
#         cache_timeout=0
#     )

# test-cell-tooltips.py

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as table

import pandas as pd
import textwrap

# url = 'https://github.com/syntagmatic/gapminder-csv/blob/master/gapminder.csv'
# df = pd.read_csv('gapminder.csv')
df = pd.read_csv('cubs-2016-baseball.csv')

# print(dash.__version__)
# print(table.__version__)

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    # {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    # {
    #     'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
    #     'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
    #     'crossorigin': 'anonymous'
    # }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # {
    #     'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
    #     'rel': 'stylesheet',
    #     'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
    #     'crossorigin': 'anonymous'
    # }
]

app = dash.Dash(__name__,
                # external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = False
app.css.config.serve_locally = False
# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

def create_tooltip(cell):
    try:
        num = float(cell)
        return textwrap.dedent(
            '''
            Tooltip for value **{value:+.2f}**.
            | Multiplier | Value |  Percent |
            |-------|-------|---------------|
            | 1     | {value_1:+.2f}     | {value_1:+.2f}% |
            | 2     | {value_2:+.2f}     | {value_2:+.2f}% |
            | 3     | {value_3:+.2f}     | {value_3:+.2f}% |
            '''.format(
                value=num,
                value_1=num,
                value_2=num * 2,
                value_3=num * 3
            )
        )
    except:
        return textwrap.dedent(
            '''
            Tooltip: **{value}**.
            '''.format(value=cell)
        )


app.layout = html.Div([
    table.DataTable(
        columns = [{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('rows'),
        tooltip={
            col: [
                {
                    'type': 'markdown',
                    'value': create_tooltip(df.loc[i, col])
                }
                for i in range(len(df))
            ]
            for col in df.columns
        },

        # tooltips={
        #     col: [
        #         {
        #             'type': 'markdown',
        #             'value': create_tooltip(df.loc[i, col])
        #         }
        #         for i in range(len(df))
        #     ]
        #     for col in df.columns
        # }
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(debug=True)

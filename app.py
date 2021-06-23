import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_table import DataTable
import sys
import pandas as pd

df = pd.read_csv('data\WNBA_RAPM.csv')
dff = df.copy()
yr = 2020
dff=dff[dff['Year']==yr]

# App layout
app = dash.Dash(__name__, prevent_initial_callbacks=True) # this was introduced in Dash version 1.12.0
server = app.server
# Sorting operators (https://dash.plotly.com/datatable/filtering)
def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
        return 'any'

    if df_column.dtype==object:
        return 'text'
    else:
        return 'numeric'

app.layout = html.Div([
    html.H1("WNBA RAPM", style={'text-align': 'center'}),
    html.H3("Select Season", style={'text-align': 'left'}),
    dcc.Dropdown(id="slct_year",
                options=[
                    {"label": "2018", "value": 2018},
                    {"label": "2019", "value": 2019},
                    {"label": "2020", "value": 2020}],
                multi=False,
                value=2020,
                style={'width': "40%"}
                ),
    html.Br(),
    DataTable(id='table',
        columns=[{"name": i, "id": i, 'type':table_type(dff[i])} for i in dff.columns],
        style_header={
        'backgroundColor': '#ff5c33',
        'fontWeight': 'bold'
        },
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns}
        page_current=0,             # page number that user is on
        page_size=15,                # number of rows visible per page
        filter_action="native",
        style_cell={'maxWidth': '400px', 'whiteSpace': 'normal','textAlign':'center'},
        # fill_width=False,
        data=dff.to_dict(orient='records')
    ),
])

@app.callback(Output('table', 'data'),
              [Input('slct_year', 'value')])

def filter_table(yr):
    dff = df.copy()
    dff=dff[dff['Year']==yr]
    return dff.to_dict(orient='records')


if __name__ == '__main__':
    app.run_server(debug=True)
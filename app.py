import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_table import DataTable
import sys
import pandas as pd

df = pd.read_csv('WNBA_RAPM.csv')
dff = df.copy()
yr = 2020
dff=dff[dff['Year']==yr]

# App layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets,
                prevent_initial_callbacks=True)
app.title = 'WNBA Stats'
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
    dcc.Markdown('-Made by [Sravan Pannala] (http://www.twitter.com/SravanNBA/), '
     '[Roger Ramesh](http://www.twitter.com/burner_celtics/) and '
     '[Neema Djavadzadeh](http://www.twitter.com/findingneema23/)'
     , style={'text-align': 'right',"margin-right": "100px"}
    ),
    html.H3("Select Season", style={'text-align': 'left',"margin-left": "100px"}),
    dcc.Dropdown(id="slct_year",
                options=[
                    {"label": "2018", "value": 2018},
                    {"label": "2019", "value": 2019},
                    {"label": "2020", "value": 2020}],
                multi=False,
                value=2020,
                style={'width': "40%","margin-left": "50px"}
                ),
    html.Br(),
    html.Div([
        DataTable(id='table',
            columns=[{"name": i, "id": i, 'type':table_type(dff[i]), 'selectable':True} for i in dff.columns],
            style_header={
            'backgroundColor': '#ff5c33',
            'fontWeight': 'bold'
            },
            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
            sort_mode="single",         # sort across 'multi' or 'single' columns}
            page_current=0,             # page number that user is on
            page_size=15,                # number of rows visible per page
            filter_action="native",
            style_cell={'minWidth': '70px','maxWidth': '200px', 
                'whiteSpace': 'normal','textAlign':'center'},
            style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': 'Player Name'},
                'textAlign': 'left','minWidth': '100px','backgroundColor':'#ffe6b3'
            },
            {
                'if': {'column_id': 'RAPM Rank'},
                'maxWidth': '70px','backgroundColor':'#ffe6b3'
            },
            {
                'if': {'column_id': 'ORAPM Rank'},
                'maxWidth': '70px','backgroundColor':'#ffe6b3'
            },
            {
                'if': {'column_id': 'DRAPM Rank'},
                'maxWidth': '70px','backgroundColor':'#ffe6b3'
            },
            ],
            # fill_width=False,
            data=dff.to_dict(orient='records')
        )],
        style={"margin-left": "100px","margin-right": "100px"}),
])

@app.callback(Output('table', 'data'),
              [Input('slct_year', 'value')])

def filter_table(yr):
    dff = df.copy()
    dff=dff[dff['Year']==yr]
    return dff.to_dict(orient='records')


if __name__ == '__main__':
    app.run_server(debug=True)
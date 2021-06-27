import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table import DataTable
import sys
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../data").resolve()
df = pd.read_csv(DATA_PATH.joinpath("WNBA_RAPM.csv"))  
dff = df.copy()
yr = 2020
dff=dff[dff['Year']==yr]

# App layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP]
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

#nav_item = dbc.NavItem(dbc.NavLink(brand = "Link", href="#"))
default = dbc.NavbarSimple(
        brand= "Home",
        brand_href="#",
        sticky="top",
        className="mb-5",
        
    )


app.layout = html.Div([
    default,html.H1("WNBA RAPM", style={'text-align': 'center'}),
    dcc.Markdown('-Made by [Sravan Pannala] (http://www.twitter.com/SravanNBA/), '
     '[Roger Ramesh]() and '
     '[Neema Djavadzadeh](http://www.twitter.com/findingneema23/)'
     , style={'text-align': 'right',"margin-right": "100px",'font-size':'22px'}
    ),
    
    
    
    html.Div(html.Img(src=app.get_asset_url('wnbalog.png'), style={"height":'10%', "width":"10%", "margin-left": "65px"})),
    
    html.H3("Select Season", style={'text-align': 'left',"margin-left": "100px",'font-size':'16px'}),
    dcc.Dropdown(id="slct_year",
                options=[
                    {"label": "2018", "value": 2018},
                    {"label": "2019", "value": 2019},
                    {"label": "2020", "value": 2020}],
                multi=False,
                value=2020,
                style={'width': "40%","margin-left": "50px",'font-size':'14px'}
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
            export_format="csv",
            data=dff.to_dict(orient='records')
        )],
        style={"margin-left": "100px","margin-right": "100px", 'font-size':'18px'}),
])

@app.callback(Output('table', 'data'),
              [Input('slct_year', 'value')])

def filter_table(yr):
    dff = df.copy()
    dff=dff[dff['Year']==yr]
    return dff.to_dict(orient='records')


if __name__ == '__main__':
    app.run_server(debug=True)
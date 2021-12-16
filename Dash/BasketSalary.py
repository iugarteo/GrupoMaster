import dash
import plotly
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv('2017-18_NBA_salary.csv')

df2 = pd.read_csv('players_stats.csv')
df_EL = df2.loc[df2['League'] == "NBA"]
anyos = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
app.layout = html.Div([
html.H3('Algorithm Type'),
    dcc.Dropdown(
        id='AlgType',
        options=[
            {'label': 'Random Forest', 'value': 'RF'},
            {'label': 'Decision Forest', 'value': 'DF'},
            {'label': 'SVR', 'value': 'SVR'}
        ],
        value='RF'
    ),
html.H3("% Shots:"),
    dcc.Slider(
       id='shots',
       min=0,
       max=1,
       value=0,
       step=None
    ),
html.H3("Age:"),
    dcc.Slider(
       id='Age',
       min=19,
       max=41,
       value=25,
       step=None
    ),
html.H3("Minutos jugados:"),
    dcc.Slider(
       id='mins',
       min=anyos[0],
       max=anyos[-1],
       value=anyos[0],
       marks={str(year): str(year) for year in anyos},
       step=None
    ),
html.H3('Salario minimo'),
    dcc.Input(value='0', type='float', id = 'sal'),
 html.H3('Minimo'),
    dcc.Checklist(
	id = 'minim',
        options=[
            {'label': 'New York City', 'value': 'NYC'}
        ],
        value=[]
    ),

    dcc.Graph(id='graph'),
   ]),
app.layout = html.Div([
html.H3('Graph Type'),
    dcc.Dropdown(
        id='graphType',
        options=[
            {'label': 'Tarta', 'value': 'pie'},
            {'label': 'Barchart', 'value': 'bar'},
            {'label': 'Puntitos', 'value': 'mark'}
        ],
        value='pie'
    ),
html.Div([
html.Div([
html.H3('Equipo'),
    dcc.RadioItems(
        options=[
            {'label': 'Baskonia', 'value': 'CAJ'},
            {'label': 'Barça', 'value': 'FCB'},
            {'label': 'Anadolu EFES', 'value': 'EFE'},
            {'label': 'Olympiacos', 'value': 'OLY'},
            {'label': 'CSKA Moskow', 'value': 'CSKA'},
            {'label': 'Zalgiris', 'value': 'ZAL'},
            {'label': 'Real Madrid', 'value': 'RMB'}
        ],
        id="teams",
        value='CAJ',
    ),],style={'width': '48%', 'display': 'inline-block'}),
    
html.Div([
html.H3('Columna'),
    dcc.RadioItems(
        options=[
            {'label': 'Triples intentados', 'value': '3PA'},
            {'label': 'Triples metidos', 'value': '3PM'},
            {'label': 'Robos', 'value': 'STL'},
            {'label': 'Minutos jugados', 'value': 'MIN'},
            {'label': 'Tiros metidos??', 'value': 'GP'},
            {'label': 'Puntos logrados', 'value': 'PTS'}
        ],
        id="columnas",
        value='3PM',
    ),
    ],
    style={'width': '48%', 'display': 'inline-block'}
    ),
    ]),
    dcc.Graph(id='graph'),
    html.H3("Year:"),
    dcc.Slider(
       id='year',
       min=anyos[0],
       max=anyos[-1],
       value=anyos[0],
       marks={str(year): str(year) for year in anyos},
       step=None
    )
]),
])

@app.callback(
    Output('graph', 'figure'),
    [Input('AlgType', 'value'),
    Input('shots', 'value'),
    Input('min', 'value'),
    Input('sal', 'value'),
    Input('minim', 'value')]
def update_figure(algth, shots, age, minutes):
    df2016 = df_EL.loc[df_EL['Season'] == "2016 - 2017"]
    df_team = df2016.loc[df_EL['Team'] == team]
    fig = px.bar(df_team, x="Player", y=columna, barmode="group")
    return fig
           
    
if __name__ == '__main__':
    app.run_server(debug=True)

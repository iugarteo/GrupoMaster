import dash
import plotly
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv('players_stats.csv')
df_EL = df.loc[df['League'] == "Euroleague"]
df_EL[['Anyo','Anyo2']] = df_EL["Season"].str.split("-",expand=True,)
del df_EL["Season"]
del df_El["Anyo2"]
anyos = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
])

@app.callback(
    Output('graph', 'figure'),
    [Input('teams', 'value'),
    Input('columnas', 'value'),
    Input('year', 'value'),
    Input('graphType', 'value')])
def update_figure(team, columna, year, tipo):
    df2016 = df_EL.loc[df_EL['Season'] == "2016 - 2017"]
    df_team = df2016.loc[df_EL['Team'] == team]
    titulo = "{} from {} players of team {}".format(columna, year, team)
    if(tipo == "pie"):
        pie1_list = df_team[columna]  
        labels = df_team.Player
        return {
            "data": [
                {
                    "values": pie1_list,
                    "labels": labels,
                    "domain": {"x": [0, .5]},
                    "name": columna, ##Esto no se
                    "hoverinfo": "label+percent+name",
                    "hole": .3,
                    "type": tipo
                }, ],
            "layout": {
                "title": titulo,
                "annotations": [
                    {"font": {"size": 20},
                     "showarrow": False,
                     "text": "Players",
                     "x": 0.20,
                     "y": 1
                     },
                ]
            }
        }
    if(tipo == "bar"):
        fig = px.bar(df_team, x="Player", y=columna, barmode="group")
        return fig
           
    if(tipo == "mark"):
        fig = px.scatter(df_team, x="Player", y=columna)
        return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)

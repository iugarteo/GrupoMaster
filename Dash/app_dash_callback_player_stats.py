import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('C:/Users/mendi/Desktop/Eñaut/Uni/Master/Visualizacion de datos/players_stats.csv')
df_EL = df.loc[df['League'] == "Euroleague"]
anyos = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
                id='graphType',
                options=[
                    {'label': 'Tarta', 'value': 'pie'},
                    {'label': 'Barchart', 'value': 'bar'},
                    {'label': 'Puntitos', 'value': 'mark'}
                ],
                value='pie'
            ),
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
        value='CAJ'
    ),
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
        value='3PM'
    ),
    dcc.Graph(id='graph'),
    dcc.Slider(
       id='year',
       min=anyos.min(),
       max=anyos.max(),
       value=min,
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
    if(tipo == "pie"):
        df2016 = df_EL.loc[df_EL['Season'] == year]
        df_team = df2016.loc[df_EL['Team'] == team]
        pie1 = df_team.Player
        pie1_list = df_team[columna]  
        labels = df_team.Player
        titulo = "{} from {} players of team {}", .format()
        return {
            "data": [
                {
                    "values": pie1_list,
                    "labels": labels,
                    "domain": {"x": [0, .5]},
                    "name": columna.label, ##Esto no se
                    "hoverinfo": "label+percent+name",
                    "hole": .3,
                    "type": tipo
                }, ],
            "layout": {
                "title": "3PT made from 2016 players",
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
    
    if(tipo == "mark"
    


if __name__ == '__main__':
    app.run_server(debug=True)
 

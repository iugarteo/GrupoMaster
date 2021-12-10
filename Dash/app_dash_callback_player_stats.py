import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
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
       value="2016 - 2017",
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
    df2016 = df_EL.loc[df_EL['Season'] == year]
    df_team = df2016.loc[df_EL['Team'] == team]
    if(tipo == "pie"):
        pie1 = df_team.Player
        pie1_list = df_team[columna]  
        labels = df_team.Player
        titulo = "{} from {} players of team {}".format(columna.label, year, team.label)
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
        x = df_team.Player
        trace1 = {
          'x': x,
          'y':df_team[columna],
          'name': columna.label,
          'type': tipo
        };
        data = [trace1];
        layout = {
          'xaxis': {'title': titulo},
          'barmode': 'relative',
          'title': titulo
        };
        fig = go.Figure(data = data, layout = layout)
        iplot(fig)
        
    if(tipo == "mark"):
        trace1 =go.Scatter(
            x = df2016.Player,
            y = df2016[columna],
            mode = "markers",
            name = year,
            marker = dict(color = 'rgba(255, 128, 255, 0.8)')
        )
        data = [trace1]
        layout = dict(title = titulo,
                      xaxis= dict(title= 'Field goald attempt',ticklen= 5,zeroline= False), ##No se que poner en estos
                      yaxis= dict(title= 'Field goald made',ticklen= 5,zeroline= False)
                     )
        fig = dict(data = data, layout = layout)
        iplot(fig)
    
if __name__ == '__main__':
    app.run_server(debug=True)
 

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('C:/Users/mendi/Desktop/Eñaut/Uni/Master/Visualizacion de datos/players_stats.csv')
df_EL = df.loc[df['League'] == "Euroleague"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-radio'),
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
])


@app.callback(
    Output('graph-with-radio', 'figure'),
    [Input('teams', 'value')])
def update_figure(selected_team):
    df2016 = df_EL.loc[df_EL['Season'] == "2016 - 2017"]
    df_team = df2016.loc[df_EL['Team'] == selected_team]
    pie1 = df_team.Player
    pie1_list = df_team["3PM"]  # str(2,4) => str(2.4) = > float(2.4) = 2.4
    labels = df_team.Player
    return {
        "data": [
            {
                "values": pie1_list,
                "labels": labels,
                "domain": {"x": [0, .5]},
                "name": "3 pointer made",
                "hoverinfo": "label+percent+name",
                "hole": .3,
                "type": "pie"
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


if __name__ == '__main__':
    app.run_server(debug=True)
 

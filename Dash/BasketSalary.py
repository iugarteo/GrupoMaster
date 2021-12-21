import dash
import plotly
from dash import dcc, State
import numpy as np
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv('2017-18_NBA_salary.csv')
df2 = pd.read_csv('players_stats.csv')
df_EL = df2.loc[df2['League'] == "Euroleague"]
minutosL = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
edadL = [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41]
shotsL = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1]
anyos = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
html.Div([
            
            # R^2
            html.Div([                
                html.H3("R^2"),
                html.H6(id="R2_text")
            ],
            id="R2-score",
            className="mini_container indicator",
            ),
	    # MAE
            html.Div([                
                html.H3("MAE"),
                html.H6(id="MAE_text")
            ],
            id="MAE-score",
            className="mini_container indicator",
            ),

            #RMSE
            html.Div([                
                html.H3("RMSE"),
                html.H6(id="RMSE_text")
            ],
            id="RMSE-score",
            className="mini_container indicator",
            ),],
        id="indicators",    
        ),
    html.Div([
        html.H3("% Shots:"),
        dcc.Slider(
            id='shots',
            min=0,
            max=1,
            value=0,
            step=0.05,
            marks={str(shot): str(shot) for shot in shotsL},
	    tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.H3("Age:"),
        dcc.Slider(
            id='Age',
            min=19,
            max=41,
            value=25,
            step=1,
	    marks={str(edad): str(edad) for edad in edadL},
	    tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.H3("Minutos jugados:"),
        dcc.Slider(
            id='mins',
            min=0,
            max=45,
            value=0,
            step=1,
	    marks={str(minutos): str(minutos) for minutos in minutosL},
	    tooltip={"placement": "bottom", "always_visible": True},
        ),
	html.H3("Salario minimo querido:"),
       html.Div(dcc.Input(id='input-on-submit', type='number')),
    	html.Button('Mostrar threshold', id='submit-val', n_clicks=0),
dcc.Graph(id='graphAlg'),
    ]),
    html.Div([
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
                ), ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Columna'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Triples intentados', 'value': '3PA'},
                        {'label': 'Triples metidos', 'value': '3PM'},
                        {'label': 'Robos', 'value': 'STL'},
                        {'label': 'Minutos jugados', 'value': 'MIN'},
                        {'label': 'Partidos jugados', 'value': 'GP'},
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
    ]), ])


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
    pie1_list = df_team[columna]
    labels = df_team.Player
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
        fig = px.bar(df_team, x="Player", y=columna, barmode="group", title=titulo)
        return fig
@app.callback(
    [Output("R2_text", "children"),
     Output("MAE_text", "children"),
     Output("RMSE_text", "children")],
     Input('submit-val', 'n_clicks'),
     State('input-on-submit', 'value'))
def update_values(n_clicks, minimo):
     r2 = minimo
     mae = minimo
     rmse = minimo
     return r2, mae, rmse
@app.callback(
     Output('graphAlg', 'figure'),
    [Input('AlgType', 'value'),
     Input('shots', 'value'),
     Input('mins', 'value'),
     Input('submit-val', 'n_clicks'),
     Input('Age', 'value')],
     State('input-on-submit', 'value'))
def update_figure2(tipoAlg, tiros, minutos, n_clicks, edad, minimo):
    df_team = df.loc[df['Tm'] == "HOU"]
    maximo = df_team['Salary'].max()
    trace1 = go.Bar(
                x = df_team.Player,
                y = df_team.Salary,
                name = "citations",
                marker = dict(color = 'rgb(128,212,255)',
                             line=dict(color='rgb(0,0,0)',width=0.05)),
                text = df_team.Player)
    data=trace1
    fig = go.Figure(data = data)
    fig.update_layout(
    shapes=[# Top Threshold line
                        {
                            'type': 'line',
                            'xref': 'paper',
                            'x0': 0,
                            'y0': minimo, 
                            'x1': 1,
                            'y1': minimo, 
                            'line': {
                                'color': 'rgb(255, 0, 0)',
                                'width': 1,
                                'dash': 'solid',
                            },
                        },
    ]
)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import plotly
from dash import dcc, State
import numpy as np
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('2017-18_NBA_salary.csv')
df2 = pd.read_csv('players_stats.csv')
df_EL = df2.loc[df2['League'] == "NBA"]
df_EL[['Season', 'Last']] = df_EL.Season.str.split(" - ",expand=True)
del df_EL['Last']
df_EL['Season'] = df_EL['Season'].astype(int)
minutosL = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
edadL = [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41]
shotsL = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1]
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
                {'label': 'Barchart', 'value': 'bar'}
            ],
            value='pie'
        ),
        html.Div([
                html.H3('Equipo'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Los Angeles Lakers', 'value': 'LAL'},
                        {'label': 'Toronto Raptors', 'value': 'TOR'},
                        {'label': 'Utah Jazz', 'value': 'UTA'},
                        {'label': 'Philadelphia 76ers', 'value': 'PHI'},
                        {'label': 'Boston Celtics', 'value': 'BOS'},
                        {'label': 'Golden State Warriors', 'value': 'GSW'},
                        {'label': 'Los Angeles Clippers', 'value': 'LAC'},
                        {'label': 'New Orleans Pelicans', 'value': 'NOP'},
                        {'label': 'Charlotte Bobcats', 'value': 'CHA'},
                        {'label': 'Phoenix Suns', 'value': 'PHX'},
                        {'label': 'Washington Wizards', 'value': 'WAS'},
                        {'label': 'Memphis Grizzlies', 'value': 'MEM'},
                        {'label': 'New York Knicks', 'value': 'NYK'},
                        {'label': 'Dallas Mavericks', 'value': 'DAL'},
                        {'label': 'Milwakee Bucks', 'value': 'MIL'},
                        {'label': 'Cleveland Cavaliers', 'value': 'CLE'},
                        {'label': 'San Antonio Spurs', 'value': 'SAS'},
                        {'label': 'Oklahoma City Thunder', 'value': 'OKC'},
                        {'label': 'Miami Heat', 'value': 'MIA'},
                        {'label': 'Atlanta Hawks', 'value': 'ATL'},
                        {'label': 'Sacramento Kings', 'value': 'SAC'},
                        {'label': 'Portland Trail Blazers', 'value': 'POR'},
                        {'label': 'Orlando Magic', 'value': 'ORL'},
                        {'label': 'Minnesota Timberwolves', 'value': 'MIN'},
                        {'label': 'Indiana Pacers', 'value': 'IND'},
                        {'label': 'Detroit Pistons', 'value': 'DET'}
                    ],
                    id="teams",
                    value='LAL',
                ),

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
            ),
        ]),
        dcc.Graph(id='graph'),
        html.H3("Year:"),
        dcc.Slider(
            id='year',
            min=df_EL['Season'].min(),
            max=df_EL['Season'].max(),
            value=df_EL['Season'].min(),
            marks={str(year): str(year) for year in df_EL['Season']},
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
    df2016 = df_EL.loc[df_EL['Season'] == year]
    df_team = df2016.loc[df_EL['Team'] == team]
    titulo = "Overall stats from {} NBA players".format(year)
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
     [Output('graphAlg', 'figure'),
     Output("R2_text", "children"),
     Output("MAE_text", "children"),
     Output("RMSE_text", "children")],
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
    r2 = minimo
    mae = minimo
    rmse = minimo
    return fig,r2, mae, rmse

if __name__ == '__main__':
    app.run_server(debug=True)

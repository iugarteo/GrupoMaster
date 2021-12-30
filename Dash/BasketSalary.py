import dash
from dash import dcc, State
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import pandas as pd
import warnings
from prediction import get_model, get_prediction, create_table

warnings.filterwarnings("ignore")

df = pd.read_csv('2017-18_NBA_salary.csv')
df2 = pd.read_csv('players_stats.csv')
df_EL = df2.loc[df2['League'] == "NBA"]
df_EL[['Season', 'Last']] = df_EL.Season.str.split(" - ", expand=True)
del df_EL['Last']
df_EL['Season'] = df_EL['Season'].astype(int)
minutosL = [0, 4, 8, 12, 16, 20, 24, 28,
            32, 36, 40, 44, 48]
edadL = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
shotsL = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
perL = [0, 5, 10, 15, 20, 25, 30, 35, 40]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.SKETCHY]


modelo1, scores1 = get_model("RF")
modelo2, scores2 = get_model("DF")
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.Label('Predice tu salario'),
            width={"size": 6, "offset": 3},
            style={'font-size':'35px'},
        )
    ),
    html.Br(),
    html.Div([dbc.Card(dbc.CardBody(
        dbc.Row(
            [
                dbc.Col(html.Div([html.H2('Seleccionar algoritmo'),
                                  dcc.Dropdown(
                                      id='AlgType',
                                      options=[
                                          {'label': 'Random Forest', 'value': 'RF'},
                                          {'label': 'Decision Tree', 'value': 'DF'}
                                      ],
                                      value='RF',
                                      style={'font-size':'18px'}
                                  ),])),
                dbc.Col(# R^2
                    html.Div([
                        html.H2("R^2"),
                        html.H2(id="R2_text")
                    ],
                        id="R2-score",
                        className="mini_container indicator",
                    ),),
                dbc.Col(# MAE
                    html.Div([
                        html.H2("MAE"),
                        html.H2(id="MAE_text")
                    ],
                        id="MAE-score",
                        className="mini_container indicator",
                    ),),
                dbc.Col(# RMSE
                    html.Div([
                        html.H2("RMSE"),
                        html.H2(id="RMSE_text")
                    ],
                        id="RMSE-score",
                        className="mini_container indicator",
                    ),),
            ]
        ))),
    ],
        id="indicators",
    ),
    html.Br(),
    html.Br(),
    html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(html.Div([html.H2("% Tiros acertado:"),
                                                        dcc.Slider(
                                                            id='shots',
                                                            min=0,
                                                            max=100,
                                                            value=0,
                                                            step=1,
                                                            marks={str(shot): str(shot) for shot in shotsL},
                                                            tooltip={"placement": "bottom", "always_visible": True}
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.H2("Edad:"),
                                                        dcc.Slider(
                                                            id='Age',
                                                            min=19,
                                                            max=41,
                                                            value=25,
                                                            step=1,
                                                            marks={str(edad): str(edad) for edad in edadL},
                                                            tooltip={"placement": "bottom", "always_visible": True},
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.H2("Minutos jugados:"),
                                                        dcc.Slider(
                                                            id='mins',
                                                            min=0,
                                                            max=48,
                                                            value=0,
                                                            step=1,
                                                            marks={str(minutos): str(minutos) for minutos in minutosL},
                                                            tooltip={"placement": "bottom", "always_visible": True},
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.H2("PER:"),
                                                        dcc.Slider(
                                                            id='per',
                                                            min=0,
                                                            max=40,
                                                            value=0,
                                                            step=0.1,
                                                            marks={str(per): str(per) for per in perL},
                                                            tooltip={"placement": "bottom", "always_visible": True}
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.H2("Salario minimo requerido (M$):"),
                                                        html.Div([dcc.Input(id='input-on-submit', type='number',placeholder="1 - 99", style={'font-size':'18px'}),
                                                                  html.Button('Mostrar minimo', id='submit-val', n_clicks=0,  style={'font-size':'18px'})]),
                                                        ])), style={'height':'80vh'}), width=5),
                dbc.Col(dbc.Card(dbc.CardBody([html.H2("Salario a cobrar por equipo:"),html.Div(dcc.Graph(id='graphAlg'), )]), style={'height':'80vh'
                                                                                                                                    }), width=7),
            ]
        ),
    ]),
    html.Br(),
    html.Div([
        dbc.Row(
            dbc.Col(
                html.Label('Estadisticas generales NBA'),
                width={"size": 6, "offset": 3},
                style={'font-size':'35px'},
            )
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(html.Div([html.H2('Tipo de grafico'),
                                                        dcc.Dropdown(
                                                            id='graphType',
                                                            options=[
                                                                {'label': 'Tarta', 'value': 'pie'},
                                                                {'label': 'Barras', 'value': 'bar'}
                                                            ],
                                                            value='pie',
                                                            style={'font-size':'18px'}
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.H2('Tipo de partidos'),
                                                        dcc.Dropdown(
                                                            id='stageType',
                                                            options=[
                                                                {'label': 'Regular', 'value': 'Regular_Season'},
                                                                {'label': 'Playoffs', 'value': 'Playoffs'}
                                                            ],
                                                            value='Regular_Season',
                                                            style={'font-size':'18px'}
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Div([
                                                            html.H2('Equipo'),
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
                                                                    {'label': 'Chicago Bulls', 'value': 'CHI'},
                                                                    {'label': 'Brooklyn Nets', 'value': 'BRK'},
                                                                    {'label': 'Denver Nuggets', 'value': 'DEN'},
                                                                    {'label': 'Detroit Pistons', 'value': 'DET'}
                                                                ],
                                                                id="teams",
                                                                value='LAL',
                                                                style={'font-size':'18px'}
                                                            ),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Div([
                                                                html.H2('Tipo estadistica'),
                                                                dcc.RadioItems(
                                                                    options=[
                                                                        {'label': '__Minutos jugados', 'value': 'MIN'},
                                                                        {'label': '__Partidos jugados', 'value': 'GP'},
                                                                        {'label': '__Puntos logrados', 'value': 'PTS'},
                                                                        {'label': '__Triples intentados', 'value': '3PA'},
                                                                        {'label': '__Triples metidos', 'value': '3PM'},
                                                                        {'label': '__Robos', 'value': 'STL'},
                                                                        {'label': '__Perdidas', 'value': 'TOV'},
                                                                        {'label': '__Rebotes', 'value': 'REB'},
                                                                        {'label': '__Asistencias', 'value': 'AST'},
                                                                        {'label': '__Tapones', 'value': 'BLK'}
                                                                    ],
                                                                    id="columnas",
                                                                    value='3PM',
                                                                    style={'font-size':'16px'},
                                                                    labelStyle={'display': 'block'}
                                                                ),

                                                            ]),
                                                        ]),])), style={'height':'80vh'}), width=4),
                dbc.Col(dbc.Card(dbc.CardBody(html.Div([dcc.Graph(id='graph'),
                                                        html.H2("Temporada:"),
                                                        dcc.Slider(
                                                            id='year',
                                                            min=df_EL['Season'].min(),
                                                            max=df_EL['Season'].max(),
                                                            value=df_EL['Season'].min(),
                                                            marks={str(year): str(year) for year in df_EL['Season']},
                                                            step=None,
                                                        )
                                                        ])), style={'height':'80vh'}), width=8)
            ]
        )
    ]), ], style={'background-image': 'url("assets/suelo.jpg")', 'background-position': 'center top', 'background-size': '1920px 1280px'} )


@app.callback(
    Output('graph', 'figure'),
    [Input('teams', 'value'),
     Input('columnas', 'value'),
     Input('year', 'value'),
     Input('graphType', 'value'),
     Input('stageType', 'value')])
def update_figure(team, columna, year, tipo, stage):
    df2016 = df_EL.loc[df_EL['Season'] == year]
    df_team = df2016.loc[df_EL['Team'] == team]
    df_team = df_team.loc[df_EL['Stage'] == stage]
    titulo = "Estadísticas totales del equipo {} en el año {} en {}".format(team, year, stage)
    if tipo == "pie":
        pie1_list = df_team[columna]
        labels = df_team.Player
        return {
            "data": [
                {
                    "values": pie1_list,
                    "labels": labels,
                    "domain": {"x": [0, .5]},
                    "name": columna,
                    "hoverinfo": "label+value+name",
                    "hole": .3,
                    "type": tipo
                }, ],
            "layout": {
                "title": titulo,
                "annotations": [
                    {"font": {"size": 20},
                     "showarrow": False,
                     "text":"",
                     "x": 0.20,
                     "y": 1
                     },
                ]
            }
        }
    if tipo == "bar":
        fig = px.bar(df_team, x="Player", y=columna, color="Player", title=titulo)
        return fig


@app.callback(
    [Output('graphAlg', 'figure'),
     Output("R2_text", "children"),
     Output("MAE_text", "children"),
     Output("RMSE_text", "children")],
    [Input('AlgType', 'value'),
     Input('shots', 'value'),
     Input('mins', 'value'),
     Input('per', 'value'),
     Input('submit-val', 'n_clicks'),
     Input('Age', 'value')],
    State('input-on-submit', 'value'))
def update_figure2(tipoAlg, tiros, minutos, per, n_clicks, edad, minimo):
    if tipoAlg == "RF":
        modelo = modelo1
        scores = scores1
    elif tipoAlg == "DF":
        modelo = modelo2
        scores = scores2
    table = create_table(edad, minutos*82, per, tiros)
    salarios = get_prediction(modelo, table)
    equipos2 = ['Houston Rockets', 'Golden State Warriors', 'Sacramento Kings', 'Chicago Bulls', 'Portland Trail Blazers', 'Dallas Mavericks', 'Boston Celtics', 'Memphis Grizzlies', 'Denver Nuggets', 'New Orleans Hornets', 'Los Angeles Clippers', 'Orlando Magic',
                'Miami Heat', 'Indiana Pacers', 'Los Angeles Lakers', 'Minessota Timberwolves ', 'Phoenix Suns', 'Atlanta hawks', 'Cleveland Cavaliers', 'New York Knicks', 'Charlotte Hornets', 'Milwakee Bucks', 'San Antonio Spurs', 'Utah Jazz',
                'New Orleans Pelicans', 'Washington Wizards', 'Philadelphia 76ers', 'Brooklyn Nets', 'Oklahoma City Thunder', 'Detroit Pistons', 'Toronto Raptors']
    equipos = ['HOU', 'GSW', 'SAC', 'CHI', 'POR', 'DAL', 'BOS', 'MEM', 'DEN', 'TOT', 'LAC', 'ORL',
               'MIA', 'IND', 'LAL', 'MIN', 'PHO', 'ATL', 'CLE', 'NYK', 'CHO', 'MIL', 'SAS', 'UTA',
               'NOP', 'WAS', 'PHI', 'BRK', 'OKC', 'DET', 'TOR']

    trace1 = go.Bar(
        x=equipos2,
        y=salarios,
        marker=dict(color='rgb(128,212,255)', line=dict(color='rgb(0,0,0)', width=0.05)), text=equipos),
    data = trace1
    if not minimo:
        minimo = 0
    fig = go.Figure(data=data)
    fig.update_xaxes(
        tickangle=45)
    fig.update_layout(
        hovermode='x unified',
        width=800,
        height=500,
        shapes=[
            {
                'type': 'line',
                'xref': 'paper',
                'x0': 0,
                'y0': minimo*1000000,
                'x1': 1,
                'y1': minimo*1000000,
                'line': {
                    'color': 'rgb(255, 0, 0)',
                    'width': 1,
                    'dash': 'solid',
                },
            },
        ]
    )
    r2 = scores[1]
    mae = scores[2]
    rmse = scores[0]
    return fig, r2, mae, rmse


if __name__ == '__main__':
    app.run_server(debug=True)

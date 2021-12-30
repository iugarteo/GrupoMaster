import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils import shuffle
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold


def get_model(alg):
    df = pd.read_csv('2017-18_NBA_salary.csv', sep=',')
    df = df.dropna()
    team_val = df.Tm.unique()
    le = preprocessing.LabelEncoder()
    le.fit(team_val)
    df['Tm'] = le.transform(df[['Tm']])
    df = shuffle(df)
    # df_X=df[['NBA_DraftNumber','Age', 'Tm', 'G',  'MP', 'PER', 'TS%','3PAr', 'FTr','ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS','DWS','WS', 'WS/48','OBPM', 'DBPM', 'BPM','VORP']]
    df_X = df[['Age', 'Tm', 'MP', 'PER', 'TS%']]
    df_Y = df[['Salary']]
    x_train, x_test, y_train, y_test = train_test_split(df_X, df_Y, test_size=0.2, random_state=42)
    if alg == "RF":
        model = RandomForestRegressor()
        max_depth = [2, 5, 8, 10]
        n_estimators = [10, 50, 100]
        param_grid = dict(max_depth=max_depth, n_estimators=n_estimators)
        grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=KFold(),
                            scoring='neg_mean_absolute_percentage_error')
        grid_results = grid.fit(df_X, np.ravel(df_Y))
        model = RandomForestRegressor(max_depth=grid_results.best_params_['max_depth'],
                                      n_estimators=grid_results.best_params_['n_estimators'])
        model.fit(x_train, np.ravel(y_train))
        rfr_predict = model.predict(x_test)
        scores = model_metrics(y_test, rfr_predict)
    elif alg == "DF":
        model = DecisionTreeRegressor()
        max_depth = [2, 5, 8, 10]
        param_grid = dict(max_depth=max_depth)
        grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=KFold(),
                            scoring='neg_mean_absolute_percentage_error')
        grid_results = grid.fit(df_X, np.ravel(df_Y))
        model = DecisionTreeRegressor(max_depth=grid_results.best_params_['max_depth'])
        model.fit(x_train, np.ravel(y_train))
        dt_predict = model.predict(x_test)
        scores = model_metrics(y_test, dt_predict)
    else:
        model = LinearRegression()
        model.fit(x_train, np.ravel(y_train))
        lr_predict = model.predict(x_test)
        scores = model_metrics(y_test, lr_predict)
    return model, scores


def model_metrics(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    return [mse, r2, mae]


def get_prediction(model, table):
    predict = model.predict(table)
    return predict


def create_table(age, minutes, per, shoot):
    teams = ['HOU', 'GSW', 'SAC', 'CHI', 'POR', 'DAL', 'BOS', 'MEM', 'DEN', 'TOT', 'LAC', 'ORL',
     'MIA', 'IND', 'LAL', 'MIN', 'PHO', 'ATL', 'CLE', 'NYK', 'CHO', 'MIL', 'SAS', 'UTA',
     'NOP', 'WAS', 'PHI', 'BRK', 'OKC', 'DET', 'TOR']
    table = pd.DataFrame()
    table['Age'] = None
    table['Tm'] = None
    table['MP'] = None
    table['PER'] = None
    table['TS%'] = None
    for x in teams:
        nueva_fila = {'Age': age, 'Tm': x, 'MP': minutes, 'PER': per, 'TS%': shoot}
        table = table.append(nueva_fila, ignore_index=True)
    team_val = teams
    le = preprocessing.LabelEncoder()
    le.fit(team_val)
    table['Tm'] = le.transform(table[['Tm']])
    return table

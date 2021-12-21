import numpy as np
import pandas as pd
import utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
import shap

class Dashboard(object):
    def __init__(self):
        self.df = pd.read_csv('data/diabetes.csv')
        X = self.df.iloc[:,:-1]
        y = self.df.iloc[:,-1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0, stratify=y)
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.model = None
        self.y_pred = None
        self.explainer = None       
    
    def update_model(self, algorithm_name):
        algorithm = utils.algorithms[algorithm_name]
        self.model = algorithm.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)
        self.explainer = shap.TreeExplainer(self.model)           

    def get_indicators(self):
        accuracy = accuracy_score(self.y_test, self.y_pred)
        f1score = f1_score(self.y_test, self.y_pred)
        rocauc = roc_auc_score(self.y_test, self.y_pred)
        return accuracy, f1score, rocauc
    
    def get_instances(self):
        options = []
        value = 0
        for i, instance in enumerate(self.y_test):
            option = {
                'label': "Instance "+ str(i)+ " (Real="+ str(instance) + " Pred="+ str(self.y_pred[i]) + ")",
                'value': str(i) 
            }        
            options.append(option)    
        return options, value    
    
    def get_shap_values(self, instance_number):  
        if instance_number == None:
            return dict()     
        i_shap = self.explainer.shap_values(self.X_test.iloc[int(instance_number)])      
        if len(i_shap) == 2:
            i_shap = i_shap[1]
        else:
            i_shap = i_shap[0]
        dic = {}
        for i, shap in enumerate(i_shap):
            dic[self.df.columns[i]] = shap            
        return dic     

    def get_variable_names(self):
        variables = []
        for col in self.X_test.columns:
            var = {
                'label': col,
                'value': col
            }
            variables.append(var)
        return variables

    def get_columns(self, column_names):
        columns = self.df[column_names]
        return columns

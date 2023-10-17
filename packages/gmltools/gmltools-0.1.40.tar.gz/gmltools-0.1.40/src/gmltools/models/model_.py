import numpy as np
import pandas as pd
#MODELS
#CLASSIFICATION
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
#REGRESSION
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from lineartree import LinearForestRegressor, LinearBoostRegressor
from  lightgbm import LGBMRegressor
from sklearn.svm import SVR



#PREPROCESSING
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
#OPTIMIZERS
from sklearn.model_selection import GridSearchCV
from .bayes import ModelOptimizer
from sklearn.model_selection import RandomizedSearchCV
from ..model_selection import ForecastGridSearchCV, ForecastRandomizedSearchCV
#INFO
from .models_info import (
    rf_default_params_clf,
    rf_default_params_reg,
    xgb_default_params_clf,
    xgb_default_params_reg,
    lr_default_params_clf,
    lr_default_params_reg,
    mlp_default_params_clf,
    mlp_default_params_reg,
    knn_default_params_clf,
    knn_default_params_reg,
    dt_default_params_clf,
    dt_default_params_reg,
    svr_default_params_reg,
    lgbm_default_params_reg,
    lb_default_params_reg
)
#import compute_sample_weight
from sklearn.utils.class_weight import compute_sample_weight
import joblib
import os
from openpyxl import load_workbook
import time
from typing import Union, List, Dict, Any, Optional
from sklearn.ensemble import VotingClassifier



#---------------------------------------------------------------------------


class SelectSearchCV:

    """
    This class is used to perform a grid search, random search or bayesian search for a model. It is used in the model method of the classes that are the ones that call this function
    """

    def __init__(self, X_train, y_train, pipe, scoring, X_test=None, y_test=None, sample_weight=None,cv:int=10,n_jobs:int=-1):
        """
        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        y_train : pandas series
            Training labels.
        pipe : sklearn pipeline
            Pipeline for the model.
        scoring : str
            Scoring metric for the model.
        sample_weight : str, optional
            If the sample weight is balanced. The default is None.
        cv : int, optional
            Number of folds for the cross validation. The default is 10.
        n_jobs : int, optional
            Number of jobs for the cross validation. The default is -1.
        """
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.pipe = pipe
        self.scoring = scoring
        self.cv = cv
        self.n_jobs = n_jobs
        self._model=""
        if sample_weight=='balanced' : #If the sample weight is balanced
            self.weight = compute_sample_weight(
            class_weight='balanced',
            y=y_train)
        else:
            self.sample_weight = sample_weight


    #grid search
    def _grid_search(self,grid_params:dict):
        """
        This method performs a grid search for a model.

        Parameters
        ----------
        grid_params : dict
            Dictionary with the parameters for the grid search.

        Limitations
        ----------
        grid_params = {MODEL__parameter: [list of values],...}

        """
        print("Grid search is running")
        self._model = GridSearchCV(
            estimator = self.pipe, 
            param_grid = grid_params, 
            cv = self.cv, 
            n_jobs = self.n_jobs, 
            scoring = self.scoring,
            verbose=2
        )

    def _forecast_grid_search(self,grid_params:dict):
        print("Forecast Grid search is running")
        self._model = ForecastGridSearchCV(
            estimator = self.pipe,
            param_grid = grid_params,
            cv = self.cv,
            n_jobs = self.n_jobs,
            scoring = self.scoring,
            verbose = 2
        )
    #random search
    def _random_search(self,random_params:dict,n_iter:int):
        """
        This method performs a random search for a model.

        Parameters
        ----------
        random_params : dict
            Dictionary with the parameters for the random search.
        n_iter : int
            Number of iterations for the random search.
        
        Limitations
        ----------
        random_params = {MODEL__parameter: [list of values],...}

        """
        print("Random search is running")
        self._model = RandomizedSearchCV(
            estimator = self.pipe, 
            param_distributions = random_params, 
            cv = self.cv, 
            n_jobs = self.n_jobs, 
            scoring = self.scoring,
            verbose=2,
            n_iter = n_iter
        )

    def _forecast_random_search(self,random_params:dict,n_iter:int):

        print("Forecast Random search is running")
        self._model = ForecastRandomizedSearchCV(
            estimator = self.pipe,
            param_distributions = random_params,
            cv = self.cv,
            n_jobs = self.n_jobs,
            scoring = self.scoring,
            verbose = 2,
            n_iter = n_iter
        )
    #bayes search
    def _bayes_search(self,bayes_pbounds:dict,bayes_int_params:List[int],bayes_n_iter:int):
        """
        This method performs a bayesian search for a model.

        Parameters
        ----------
        bayes_pbounds : dict
            Dictionary with the parameters for the bayesian search.
            bayes_pbounds = {MODEL__parameter: (min, max),...}
        bayes_int_params : list
            List of parameters that are integer.
            bayes_int_params = [...,...]
        """
        print("Bayesian search is running")
        optimizer = ModelOptimizer(scoring=self.scoring,cv=self.cv)
        params_bayes = optimizer.optimize_model(pbounds=bayes_pbounds, X_train_scale=self.X_train, 
                                    y_train=self.y_train, model=self.pipe, 
                                    int_params=bayes_int_params,n_iter=bayes_n_iter)
        hyper_params = { (k):(int(np.round(v, 0)) if k in bayes_int_params else round(v, 2)) for k, v in params_bayes.items()}
        self._model = self.pipe.set_params(**hyper_params)

    def select_automatic(self, grid_params:dict, random_params:dict, random_n_iter:int, bayes_pbounds:dict, bayes_int_params:List[str], bayes_n_iter:int):
        """
        This method selects the search method to be used

        Parameters
        ----------
        grid_params : dict, optional
            Dictionary with the parameters to be used in the grid search. The default is None.
        random_params : dict, optional
            Dictionary with the parameters to be used in the random search. The default is None.
        random_n_iter : int, optional
            Number of iterations to be used in the random search. The default is None.
        bayes_pbounds : dict, optional
            Dictionary with the parameters to be used in the bayesian search. The default is None.
        bayes_int_params : list, optional
            List of parameters to be used in the bayesian search. The default is None.
        bayes_n_iter : int, optional
            Number of iterations to be used in the bayesian search. The default is None.
        
        """
        if grid_params is not None and grid_params["Search"]=="Forecast":
            self.params = grid_params.copy()
            del grid_params["Search"]
            self._forecast_grid_search(grid_params)
        elif grid_params is not None and grid_params["Search"]=="Normal":
            self.params = grid_params.copy()
            del grid_params["Search"]
            self._grid_search(grid_params)
        elif random_params is not None and random_params["Search"]=="Forecast":
            self.params = random_params.copy()
            del random_params["Search"]
            self._forecast_random_search(random_params,random_n_iter)
        elif random_params is not None and random_params["Search"]=="Normal":
            self.params = random_params.copy()
            del random_params["Search"]
            self._random_search(random_params,random_n_iter)
        elif bayes_pbounds is not None:
            self._bayes_search(bayes_pbounds,bayes_int_params,bayes_n_iter)

        
    

    def fit(self, X_prev=None,columns_lags:List[int]=None, column_rolled_lags:List[int]=None,lags:List[int]=None,rolled_lags:List[int]=None, rolled_metrics:List[int]=None, column_rolled_lags_initial:List[int]=None):
        """
        This method fits the model when previously the search has been performed with the grid_search, random_search or bayes_search methods

        Parameters
        ----------
        X_prev : pandas dataframe, optional
            DataFrame con previsiones. The default is None.
        columns_lags : list, optional
            List of columns to lag. The default is None.
        column_rolled_lags : list, optional
            List of columns to lag. The default is None. 
            The position column of the lags   
        lags : list, optional
            List of lags. The default is None.
            Is used in autoregressive models
        rolled_lags : list, optional
            List of lags. The default is None.
        rolled_metrics : list, optional
            List of metrics. The default is None.
            "mean","std","max","min"
        column_rolled_lags_initial : list, optional
            List of columns to lag. The default is None.
            The initial lag where the rolling window starts/finish. The default is None.

        """
        if self.sample_weight is not None:
            if self.pipe.steps[-1][0]=='XGB':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, XGB__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train, XGB__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, XGB__sample_weight=self.sample_weights)

            elif self.pipe.steps[-1][0]=='LGBM':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, LGBM__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train, LGBM__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, LGBM__sample_weight=self.sample_weights)

            elif self.pipe.steps[-1][0]=='RF':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, RF__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train, RF__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, RF__sample_weight=self.sample_weights)
            elif self.pipe.steps[-1][0] == 'KNN':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, KNN__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train,  KNN__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

                else:
                    self._model.fit(self.X_train, self.y_train, KNN__sample_weight=self.sample_weights)

            elif self.pipe.steps[-1][0] == 'LR':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, LR__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train,  LR__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, LR__sample_weight=self.sample_weights)
                    
            elif self.pipe.steps[-1][0] == 'MLP':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, MLP__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train,  LR__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, DT__sample_weight=self.sample_weights)

            elif self.pipe.steps[-1][0] == 'DT':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, DT__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train,  DT__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, DT__sample_weight=self.sample_weights)

            elif self.pipe.steps[-1][0] == 'SVR':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, SVR__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train,   SVR__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, SVR__sample_weight=self.sample_weights)

                
            elif self.pipe.steps[-1][0] == 'LF':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, LF__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train,  LF__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(self.X_train, self.y_train, LF__sample_weight=self.sample_weights)


            elif self.pipe.steps[-1][0] == 'LB':
                if self.params["Search"]=="Forecast":
                    if self.y_test is None and self.X_test is None:
                        self._model.fit(X=self.X_train, y_train=self.y_train, LB__sample_weight=self.sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                    else:
                        self._model.fit(X=self.X_train, y_train=self.y_train, LB__sample_weight=self.sample_weights, X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

                else:
                    self._model.fit(self.X_train, self.y_train, LB__sample_weight=self.sample_weights)
        else:
            if self.params["Search"]=="Forecast":
                if self.y_test is None and self.X_test is None:
                    self._model.fit(X=self.X_train, y_train=self.y_train, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
                else:
                    self._model.fit(X=self.X_train, y_train=self.y_train,  X_prev = X_prev, X_test=self.X_test, y_test=self.y_test, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags, rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            else:
                self._model.fit(self.X_train, self.y_train)

        return self._model


    
    
    
# def train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None,cv=10,random_n_iter=10, X_prev=None, columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):

#     #Arguments assertion not needed because they are already checked in the model method of the classes that are the ones that call this function
#     """
#     This function performs a grid search or a bayesian search for the hyperparameters of the model. It is used in the for the deployment 
#     of the model in ecah model method of the model classes.

#     Parameters
#     ----------
#     X_train : pandas
#         Training data.
#     y_train : pandas
#         Training labels.
#     bayes_pbounds : dict, optional
#         Dictionary with the bounds for the bayesian search. The default is None.
#     grid_params : dict, optional
#         Dictionary with the grid search parameters. The default is None.
#     random_params : dict, optional
#         Dictionary with the random search parameters. The default is None.
#     n_jobs : int, optional
#         Number of jobs for the grid search. The default is -1.
#     pipe : sklearn pipeline
#         Pipeline for the model.
#     scoring : str
#         Scoring metric for the grid search.
#     bayes_int_params : list, optional
#         List of parameters that are integers. The default is None.
#     bayes_n_iter : int, optional
#         Number of iterations for the bayesian search. The default is 10.
#     sample_weight : pandas, optional
#         Sample weights for the grid search. The default is None.
#     cv : int, optional
#         Number of folds for the grid search. The default is 10.
#         For time series use TimeSeriesSplit or BlockTimeSeriesSplit
#     random_n_iter : int, optional
#         Number of iterations for the random search. The default is 10.
#     """
#     #For Grid Search optimizartion,its done when the bayes_pbounds and random_params are None
#     if bayes_pbounds is None and random_params is None : 
#         print("Grid search is running")
#     #apply the grid search
#         model_ = GridSearchCV(
#             estimator = pipe, 
#             param_grid = grid_params, 
#             cv = cv, 
#             n_jobs = n_jobs, 
#             scoring = scoring,
#             verbose=2
#         )
#     #For Bayesian Search optimization, its done when the bayes_pbounds is not None and random_params is None
#     elif bayes_pbounds is not None and random_params is None: 
#         print("Bayesian search is running")
#         optimizer = ModelOptimizer(scoring=scoring,cv=cv)
#         params_bayes = optimizer.optimize_model(pbounds=bayes_pbounds, X_train_scale=X_train, 
#                                     y_train=y_train, model=pipe, 
#                                     int_params=bayes_int_params,n_iter=bayes_n_iter)
#         hyper_params = { (k):(int(np.round(v, 0)) if k in bayes_int_params else round(v, 2)) for k, v in params_bayes.items()}
#         model_ = pipe.set_params(**hyper_params)
#     #For Random Search optimization, its done when the bayes_pbounds is None and random_params is not None
#     else: 
#         print("Random search is running")
#         model_ = RandomizedSearchCV(
#             estimator = pipe, 
#             param_distributions = random_params, 
#             cv = cv, 
#             n_jobs = n_jobs, 
#             scoring = scoring,
#             verbose=2,
#             return_train_score=True,
#             n_iter=random_n_iter
#         )

#     if sample_weight is not None : #Sample weight are for XGBoost ando some other models but not fo all
#         if sample_weight=='balanced' : #If the sample weight is balanced
#             sample_weights = compute_sample_weight(
#             class_weight='balanced',
#             y=y_train)
#         else:
#             sample_weights=sample_weight
#         if pipe.steps[-1][0]=='XGB':
#             model_.fit(X_train, y_train, XGB__sample_weight=sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#         elif pipe.steps[-1][0]=='LGBM':
#             model_.fit(X_train, y_train, LGBM__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#         elif pipe.steps[-1][0]=='RF':
#             model_.fit(X_train, y_train, RF__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#         elif pipe.steps[-1][0] == 'KNN':
#             model_.fit(X_train, y_train, KNN__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#         elif pipe.steps[-1][0] == 'LR':
#             model_.fit(X_train, y_train, LR__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#         elif pipe.steps[-1][0] == 'MLP':
#             model_.fit(X_train, y_train, MLP__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#         elif pipe.steps[-1][0] == 'DT':
#             model_.fit(X_train, y_train, DT__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#     else :
#         model_.fit(X_train, y_train, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
#     return model_


class Classification:
    """
    This class contains all the classification models. Consideres relevant.
    Its up to suggestions for other models to be added.
    """
    #Global Attributes
    RandomForest_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    XGBoost_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    LogisticRegression_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    DecisionTree_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    KNN_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    MLP_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"

    def __init__(self, model_name, X_train=None, y_train=None, cv=10):
        self.model = None
        self.model_name = model_name
        self.X_train = X_train
        self.y_train = y_train
        self.cv = cv
    def RandomForest_Classifier(self, ordinal_cat_cols:List[str]=None,
                                scoring='accuracy', class_weight=None,
                                grid_params:dict={'RF__n_estimators': [100, 200],
                                            'RF__max_depth': [None, 10, 20],
                                            'RF__min_samples_split': [2, 5],
                                            'RF__max_features': ['sqrt', None]},
                                random_params:dict=None,
                                random_n_iter:int=10,
                                bayes_pbounds:dict=None,
                                bayes_int_params:List[str]=None, 
                                bayes_n_iter:int=30,
                                criterion='gini',
                                sample_weight=None,
                                random_state:int=None,
                                n_jobs:int=-1):
        """
        This function performs a Random Forest classification model with grid search or bayesian optimization.


        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        
        y_train : pandas dataframe
            Training labels.
        
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal. The default is None.
        
        scoring : str, optional
            Scoring function for model evaluation. The default is 'accuracy'.
        
        balanced : str, optional
            If 'balanced', class weights are balanced. The default is None.

        grid_param_grid : dict, optional
            Dictionary of parameters for grid search. The default is {'RFC__n_estimators': [100, 200], 'RFC__max_depth': [None, 10, 20],
                                                    'RFC__min_samples_split': [2, 5], 'RFC__max_features': ['sqrt', None]}.             
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        criterion : str, optional
            Criterion for splitting. The default is 'gini'.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model : sklearn model
            Trained model with grid seach
        """
        print(" INFO: Agurments params must start as 'RF__param'" + '\n' "INFO: Default params in Documentation for Random Forest are: ", rf_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'criterion = {criterion}',
            f'bayes_n_iter = {bayes_n_iter}', f'class_weigth = {class_weight}', f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}',
            f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert class_weight is None or class_weight is 'balanced' , "In case of balanced class weights, balanced must be 'balanced'"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameters"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #RFC should be in every key of grid_param_grid
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('RF__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'RF__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('RF__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'RF__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('RF__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'RF__'"
            assert all(key == 'Search' or key.startswith('RF__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'RF__'"
    
        #Preprocess the data automatically
        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('RF', RandomForestClassifier(criterion=criterion,random_state=random_state,n_jobs=n_jobs,class_weight=class_weight))]) # Model always the last step
        #Select Grid Search, Random Search or Bayesian Optimization
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()
        
        #generate a dictionary with all the parameters used in the model
        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), "Class_Weights":str(class_weight), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape),
                                    'scoring':str(scoring), 'cv':str(self.cv), 'criterion':str(criterion), 'sample_weight':str(sample_weight)}
        

    
    def XGBoost_Classifier( self, ordinal_cat_cols:list=None,
                            scoring='accuracy', eval_metric='merror',
                            objective='multi:softmax', grid_params:dict={},
                            random_params:dict=None, random_n_iter:int=10,
                            bayes_pbounds:dict=None,bayes_int_params:List[str]=None, 
                            bayes_n_iter:int=30, random_state:int=None,
                            sample_weight=None, n_jobs=-1):  
        """
        This method performs a XGBoost classification model with grid search or bayesian optimization.


        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        
        y_train : pandas dataframe
            Training labels.
        
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal. The default is None.
        
        scoring : str, optional
            Scoring function for model evaluation. The default is 'accuracy'.
        
        eval_metric : str, optional
            Evaluation metric. The default is 'merror'.
        
        objective : str, optional
            Objective function. The default is 'multi:softmax'.

        grid_param_grid : dict, optional
            Dictionary of parameters for grid search. 
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.

        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.

        sample_weight : str, optional
            If 'balanced', class weights are balanced. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model : sklearn model
            Trained model with grid seach or bayesian optimization

        """
        print(" INFO: Agurments params must start as 'XGB__param'" + '\n' "INFO: Default params for XGBoost in Documentation are: ", xgb_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'eval_metric = {eval_metric}',f'objective = {objective}',
            f'bayes_n_iter = {bayes_n_iter}', f'sample_weigth = {sample_weight}', f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}',
            f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert sample_weight is None or sample_weight is 'balanced' or isinstance(sample_weight, compute_sample_weight) , "In case of balanced class weights, balanced must be 'balanced'"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameters"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #XGB__ is the prefix for every hyperparameter of this model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('XGB__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'XGB__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('XGB__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'XGB__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('XGB__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'XGB__'"
            assert all(key == 'Search' or key.startswith('XGB__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'XGB__'"


        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('XGB', XGBClassifier(
                                random_state=random_state,
                                n_jobs=n_jobs, 
                                verbosity=0,
                                eval_metric=eval_metric,
                                objective=objective))]) # Model always the last step
        #Select Grid Search, Random Search or Bayesian Optimization
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()
        
        #generate a dictionary with all the parameters used in the model
        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 
                                    'scoring':str(scoring), 'cv':str(self.cv), 'eval_metric':str(eval_metric), 'sample_weight':str(sample_weight), "objective":str(objective)}

    
    def LogisticRegression_Classifier(self,  ordinal_cat_cols:List[str]=None, scoring='accuracy',
                                    grid_params = {'LR__C': [0.1, 1, 10],
                                    'LR__penalty': ['l1', 'l2', 'elasticnet'],
                                    'LR__multi_class': ['ovr', 'multinomial'],   
                                    'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},
                                    random_params:dict=None, random_n_iter:int=10,
                                    bayes_pbounds:dict=None, bayes_int_params:List[str]=None, 
                                    bayes_n_iter:int=30, random_state:int=None, class_weight=None, sample_weight=None,
                                    n_jobs:int=-1 , tol:float=0.0001, max_iter:int=1000):
        """
        This method performs a Logistic Regression classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.
        
        y_train : pandas dataframe
            Training set labels.
        
        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.
        
        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.
        
        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is 
            {'LR__C': [0.1, 1, 10], 'LR__penalty': ['l1', 'l2', 'elasticnet'],
            'LR__multi_class': ['ovr', 'multinomial'], 'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}.

        cv : int, optional
            Number of folds for cross validation. The default is 10.

        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.

        random_n_iter : int, optional   
            Number of iterations for random search. The default is 10.
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        class_weight : str, optional
            If 'balanced', class weights will balanced. The default is None.

        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        tol : float, optional
            Tolerance for stopping criteria. The default is 0.0001.
        
        max_iter : int, optional
            Maximum number of iterations. The default is 1000.
        
        Returns
        -------
        model_ : trained model
            Trained model with grid seach or bayesian optimization

        """

        print(" INFO: Agurments params must start as 'LR__param'" + '\n' "INFO: Default params in Documentaction for Logistic Regression are: ", lr_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'bayes_n_iter = {bayes_n_iter}',
            f'class_weigth = {class_weight}', f'max_iter = {max_iter}' f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}',
            f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert class_weight is None or class_weight is 'balanced' , "In case of balanced class weights, balanced must be 'balanced'"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #LR__ is the prefix for every hyperparameter in this model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('LR__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'LR__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('LR__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'LR__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('LR__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'LR__'"
            assert all(key == 'Search' or key.startswith('LR__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LR__'"

        
        #Preprocessing
        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('LR', LogisticRegression(
                                    max_iter=max_iter,
                                    tol=tol, #default 1e-4
                                    class_weight=class_weight, #is used to handle the imbalance dataset
                                    random_state=random_state,
                                    n_jobs=n_jobs, 
                                    verbose=0,
                                    warm_start=False,
                                    fit_intercept=True,
                                    intercept_scaling=1,
                                    dual=False))]) # Model always the last step
        #Select Grid Search, Random Search or Bayesian Optimization
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()
        
        #generate a dictionary with all the parameters used in the model
        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), "Class Weight":str(class_weight), 'random_state':str(random_state),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 
                                    'scoring':str(scoring), 'cv':str(self.cv), 'tol':str(tol), 'sample_weight':str(sample_weight), "max_iter":str(max_iter)}
  
        
    
    def MLP_Classifier(self,ordinal_cat_cols=None, scoring='accuracy',
                       grid_params={'MLP__alpha': [1e-9,1e-7,1e-5,0.001,0.01],
                        'MLP__hidden_layer_sizes':[(5,),(10,),(15,),(20,),(25,)]},
                        random_params=None, random_n_iter=10,
                        bayes_pbounds=None, bayes_int_params=None, bayes_n_iter=30, 
                        random_state=None, n_jobs=-1, solver='lbfgs',
                        activation='logistic', tol=1e-4, max_iter=450, early_stopping=False,
                       learning_rate='constant',learning_rate_init=0.001,verbose=True, sample_weight=None):
        
        """
        This method performs a Multi Layer Perceptron classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.
        
        y_train : pandas dataframe
            Training set labels.
        
        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.
        
        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.
        
        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
            {'MLP__alpha': [1e-9,1e-7,1e-5,0.001,0.01],
            'MLP__hidden_layer_sizes':[(5,),(10,),(15,),(20,),(25,)]}.

        cv : int, optional
            Number of folds for cross validation. The default is 10.
        
        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.
        
        random_n_iter : int, optional
            Number of iterations for random search. The default is 10.
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.
        
        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        solver : str, optional
            The solver for weight optimization. The default is 'lbfgs'.
        
        activation : str, optional
            Activation function for the hidden layer. The default is 'logistic'.
        
        tol : float, optional
            Tolerance for stopping criteria. The default is 1e-4.
        
        max_iter : int, optional
            Maximum number of iterations. The default is 450.

        early_stopping : bool, optional
            Whether to use early stopping to terminate training when validation score is not improving. The default is False.

        learning_rate : str, optional
            Learning rate schedule for weight updates. The default is 'constant'.
        
        learning_rate_init : float, optional
            The initial learning rate used. The default is 0.001.
        
        verbose : bool, optional
            Whether to print progress messages to stdout. The default is True.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.

        """

        print(" INFO: Agurments params must start as 'MLP__param'" + '\n' "INFO: Default params in Documentation for MultiLayer Perceptron are: ", mlp_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'solver = {solver}',f'activation = {activation}',
        f'bayes_n_iter = {bayes_n_iter}', f'tol = {tol}', f'max_iter = {max_iter}' , f'learning_rate = {learning_rate}', f'learning_rate_init = {learning_rate_init}',
        f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}',
        f'random_state = {random_state}', f'n_jobs = {n_jobs}', f'early_stopping = {early_stopping}', f'verbose = {verbose}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_params must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #MLP__ is the prefix for every hyperparameter in MLPClassifier
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('MLP__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'MLP__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('MLP__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'MLP__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('MLP__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'MLP__'"
            assert all(key == 'Search' or key.startswith('MLP__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'MLP__'"

        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('MLP', MLPClassifier(solver=solver, # Update function
                                                    activation=activation, # Logistic sigmoid activation function
                                                    max_iter=max_iter, # Maximum number of iterations
                                                    tol=tol, # Tolerance for the optimization
                                                    random_state=random_state,
                                                    verbose = verbose,
                                                    early_stopping=early_stopping,
                                                    learning_rate=learning_rate,
                                                    learning_rate_init=learning_rate_init
                                                    ))]) # Model always the last step
        #Select Grid Search, Random Search or Bayesian Optimization
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()
        
        #generate a dictionary with all the parameters used in the model
        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), "Early Stopping":str(early_stopping), 'random_state':str(random_state),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape),
                                    'scoring':str(scoring), 'cv':str(self.cv), 'tol':str(tol), 'sample_weight':str(sample_weight), "max_iter":str(max_iter), "Learning Rate":str(learning_rate), "Learning Rate Init":str(learning_rate_init)}
        
        


    #do the same for knn_classifier
    def KNN_Classifier(self,ordinal_cat_cols=None, scoring='accuracy',
                        grid_params={'KNN__n_neighbors': [3,10,25,60]},
                        random_params=None, random_n_iter=10,  bayes_pbounds=None,
                        bayes_int_params=None, bayes_n_iter=30, sample_weight=None, n_jobs=-1):
          
        """
        This method performs a K-Nearest Neighbors classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.

        y_train : pandas dataframe
            Training set labels.

        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.

        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.

        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
            {'KNN__n_neighbors': [3,10,25,60]}.
        
        cv : int, optional
            Number of folds for cross validation. The default is 10.
        
        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.

        random_n_iter : int, optional
            Number of iterations for random search. The default is 10.

        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.

        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        p : int, optional
            Power parameter for the Minkowski metric. The default is 2.
        
        metric : str, optional
            The distance metric to use for the tree. The default is 'minkowski'.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.

        """

        print(" INFO: Agurments params must start as 'KNN__param'" + '\n' "INFO: Default params in Documentation for Random Forest are: ", knn_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'bayes_n_iter = {bayes_n_iter}',
               f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'n_jobs = {n_jobs}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #KNN_ is the prefix for every hyperparameter in the KNN model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('KNN__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'KNN__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('KNN__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'KNN__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('KNN__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'KNN__'"
            assert all(key == 'Search' or key.startswith('KNN__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'KNN__'"
        
        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('KNN', KNeighborsClassifier(n_jobs=n_jobs))]) # Model always the last step
        #Select Grid Search, Random Search or Bayesian Optimization
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()
        
        #generate a dictionary with all the parameters used in the model
        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 
                                    'scoring':str(scoring), 'cv':str(self.cv),  'sample_weight':str(sample_weight)}



    

    #do the same for a decision tree
    def DecisionTree_Classifier(self, ordinal_cat_cols=None, scoring='accuracy',
                            grid_params={'DT__max_depth': [3,5,7,10],
                                'DT__min_samples_split': [2,3,4],
                                'DT__min_samples_leaf': [4,5,6],
                                'DT__max_features': ['auto','sqrt','log2',None]},
                            cv=10, random_params=None, random_n_iter=10, bayes_pbounds=None, 
                            bayes_int_params=None, bayes_n_iter=30, class_weight=None, sample_weight=None, random_state=None, n_jobs=-1):
            
        """
        This method performs a Decision Tree classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.

        y_train : pandas dataframe
            Training set labels.

        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.

        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.

        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
        
        cv : int, optional
            Number of folds for cross validation. The default is 10.

        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.

        random_n_iter : int, optional
            Number of iterations for random search. The default is 10.
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.
        
        """

        print(" INFO: Agurments params must start as 'DT__param'" + '\n' "INFO: Default params in Documentation for Decision Tree are: ", dt_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
        f'bayes_n_iter = {bayes_n_iter}', f'class_weigth = {class_weight}', f'bayes_pbounds = {bayes_pbounds}', 
        f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_param_grid must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #DT__ is the prefix for every hyperparameter in the Decision Tree model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('DT__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'DT__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('DT__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'DT__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('DT__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'DT__'"
            assert all(key == 'Search' or key.startswith('DT__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'DT__'"

        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('DT', DecisionTreeClassifier(random_state=random_state,class_weight=class_weight))]) # Model always the last step
        #Select Grid Search, Random Search or Bayesian Optimization
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()
        
        #generate a dictionary with all the parameters used in the model
        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), "Class Weight": class_weight, 'random_state':str(random_state),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape),
                                    'scoring':str(scoring), 'cv':str(self.cv),  'sample_weight':str(sample_weight)}
        


    def Voting_Classifier(self, models:list, ordinal_cat_cols=None, scoring='accuracy',
                          voting='hard', weights=None, grid_params:dict=None, n_jobs=-1,random_params=None, random_n_iter=10, bayes_pbounds=None, bayes_int_params=None, bayes_n_iter=30):
        
        """

        Voting classifier is a meta-estimator that fits base classifiers each on the whole dataset.
        It, then, averages the individual predictions to form a final prediction.

        Parameters
        ----------
        models : list
            List of models to be used in the voting classifier.

        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.

        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.

        voting : str, optional
            If 'hard', uses predicted class labels for majority rule voting.
            Elif soft, predicts the class label based on the argmax of the sums of the predicted probabilities, which is recommended for an ensemble of well-calibrated classifiers.

        weights : list, optional
            Sequence of weights (float or int) to weight the occurrences of predicted class labels (hard voting) or class probabilities before averaging (soft voting). Uses uniform weights if None.
        """

        print("INFO: Arguments in grids_params an similars must start as 'Voting__modelname__ .. of list of model tuple like [('knn',KNNeigbors()), ...]'")
        print("INFO: Default params in Documentation for Voting Classifier in 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html'")
        print("\n"+ "INFO: Default params RUN for this model are: ", f'models = {models}',f'scoring = {scoring}', f'voting = {voting}', f'weights = {weights}',
        f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'n_jobs = {n_jobs}')
        assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert isinstance(models, list), "models must be a list of models"
        assert all(isinstance(m, tuple) and len(m) == 2 for m in models), "models must be a list of tuples (name, model)"
        assert all(isinstance(m[0], str) for m in models), "models must be a list of tuples (name, model)"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_param_grid must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #assert that every gird _params contains __name__ after Voting
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
            assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('Voting__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'Voting__modelname__'"

        elif random_params is not None:
            assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
            assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('Voting__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'Voting__modelname__'"

        elif bayes_pbounds is not None:
            assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
            assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
            assert all(key == 'Search' or key.startswith('Voting__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'Voting__modelname__'"
            assert all(key == 'Search' or key.startswith('Voting__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'Voting__modelname__'"



    
        preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols)
        pipe=Pipeline(steps=[('Prep', preprocessor),
                            ('Voting', VotingClassifier(estimators=models, voting=voting, weights=weights, n_jobs=n_jobs))])
        
        select_searchcv=SelectSearchCV(self.X_train, self.y_train, pipe, scoring, sample_weight=None,cv=self.cv,n_jobs=n_jobs)
        select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        self.model=select_searchcv.fit()

        self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
        
        self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols),
                                    'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape),
                                    'scoring':str(scoring), 'cv':str(self.cv),  }

    





    #save model
    def save(self, return_best_metrics:bool=True):
        """
        Saves the model to a file. And saves the cv results if exists grid search or random search as an excel file.

        Parameters
        ----------
        model_name : str
            Name of the model.
            The model is stored in the models folder. with the model name provided

        Returns
        -------
        None.

        """
        assert self.model is not None , "Model not trained yet"
        #create folder if not exists where the model will be saved
        path = f'./models/{self.model_name}'
        if not os.path.exists(path):
            os.makedirs(path)

        joblib.dump(self.model, os.path.join(path, self.model_name+'.joblib'))
        #save cv results if exists grid search or random search
        if hasattr(self.model, 'cv_results_'):
            df = pd.DataFrame(self.model.cv_results_)
            df.sort_values('rank_test_score', inplace=True)
            df.to_excel(os.path.join(path, self.model_name+'_cv_results.xlsx'), index=False)

            #save the best register of the cv_results in a second sheet of excel file called summary_models.xlsx
            df_best = pd.DataFrame(df.iloc[0]).T
            df_best["Search conditions"]=str(self._overall_dict_params)
            df_best['model_name'] = self.model_name
            #set model_name the firts column and Search conditions the second column
            cols = df_best.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df_best = df_best[cols]

            # save in the second sheet
            file_path = './models/summary_models.xlsx'
            if os.path.isfile(file_path):
                df_summary = pd.read_excel(file_path, sheet_name='Sheet2')
                df_summary = pd.concat([df_summary, df_best], axis=0, ignore_index=True)
                df_summary.to_excel(file_path, index=False, sheet_name='Sheet2')
            else:
                df_best.to_excel(file_path, index=False, sheet_name='Sheet2')
            if return_best_metrics:
                return df_best

    def load(self):

        """
        Loads a model from a file.

        Parameters
        ----------
        model_name : str
            Name of the model.
            The model is stored in the models folder. with the model name provided.
            To load a model, the model must be saved before. And when instantiating the class, 
            its not mandatory to pass the X_train and y_train arguments.

        Returns
        -------
        None.

        """
        assert self.model_name in os.listdir('./models'), "Model not found"
        assert self.model_name+'.joblib' in os.listdir(f'./models/{self.model_name}'), "Model not found"
        path = f'./models/{self.model_name}/{self.model_name}'+'.joblib'
        self.model = joblib.load(path)
        return self.model
    
    @staticmethod
    def _automatic_preprocessor( X_train, ordinal_cat_cols:List[str]=None):
        #Arguments assertion not needed because they are already checked in the model method of the classes that are the ones that call this function
        """
        This function performs a preprocessor for the data. It automatically detects the categorical and numeric variables and performs the following steps:
            - Numeric variables: imputation by scaling. STANDARD SCALER
            - Categorical variables: imputation by encoding. ONE HOT ENCODER
            - Ordinal categorical variables: imputation by encoding. ORDINAL ENCODER

        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal.

        Returns
        -------
        preprocessor : sklearn preprocessor
            Preprocessor for the data. Used fo the pipelines for every model.

        """
        num_cols = X_train.select_dtypes(include=np.number).columns.values.tolist() #Detects the numeric variables
        cat_cols = X_train.select_dtypes(include=['category']).columns.values.tolist() #detects the categorical variables

        if ordinal_cat_cols is None:
            cat_cols_onehot = cat_cols
            ordinal_cat_cols = []
        else:
            for col in ordinal_cat_cols:
                cat_cols.remove(col)
            cat_cols_onehot = cat_cols

        # Prepare the categorical variables by encoding the categories    
        categorical_transformer_onehot = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))])
        categorical_transformer_ordinal = Pipeline(steps=[('ordinal', OrdinalEncoder())])
        # Prepare the numeric variables by imputing by scaling
        numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

        preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_transformer, num_cols), #numeric variables
            ('cat_onehot', categorical_transformer_onehot, cat_cols_onehot), #categorical variables
            ('cat_ordinal', categorical_transformer_ordinal, ordinal_cat_cols)]) #ordinal categorical variables
        
        return preprocessor
    
    @staticmethod
    def _not_none_search(*args):
        """
        This function returns a list of the arguments that are not None. Is used to store the not none parameters of the seleted search  of the model in the dictionary self._overall_dict
        """
        search_list=['grid_params', 'random_params', 'random_n_iter', 'bayes_pbounds', 'bayes_int_params', 'bayes_n_iter']
        return [(search_list[i],value_var) for i, value_var in enumerate(args) if value_var is not None]
        #add the variable name to the value
    
#-------------------------------------------------------------------------------------------------------------------REGRESSION-------------------------------------------------------------------------------------------------------------#
class Regression:
    """
    This class contains all regression models that are considered relevant.
    Its up to add more models in the future thta could be suggested by the user.
    """

    RandomForest_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    XGBoost_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    LogisticRegression_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    DecisionTree_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    KNN_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    MLP_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"

    def __init__(self,model_name:str, X_train=None, y_train=None, X_test=None, y_test=None, X_prev=None, cv=10):
        self.model = None
        self.model_name = model_name
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.X_prev = X_prev
        self.cv = cv

    def RandomForest_Regressor(self,  ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error', criterion="friedman_mse",
                            grid_params={'RF__n_estimators': [100, 200, 300, 400, 500],
                                'RF__max_depth': [3,5,7,10],
                                'RF__min_samples_split': [2,3,4],
                                'RF__min_samples_leaf': [4,5,6],
                                'RF__max_features': ['auto','sqrt','log2',None]}, 
                            random_params=None, random_n_iter = 10, bayes_pbounds=None, 
                            bayes_int_params=None, bayes_n_iter = 30, sample_weight=None, random_state=None, n_jobs=-1, 
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a Random Forest regression model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For Time Series, cv must be a TimeSeriesSplit object or BlockTimeSeriesSplit object.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list, optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list, optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
               Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """
            

            print(" INFO: Agurments params must start as 'RF__param'" + '\n' "INFO: Default params in Documentation for Random Forest are: ", rf_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}', 
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameters"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #RF__ is the prefix for every hyperparameter in the model
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('RF__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'RF__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('RF__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'RF__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('RF__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'RF__'"
                assert all(key == 'Search' or key.startswith('RF__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'RF__'"

            #Preprocess the data automatically
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('RF', RandomForestRegressor(criterion=criterion,random_state=random_state,n_jobs=n_jobs))]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'criterion':str(criterion), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)

    
    def XGB_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'XGB__n_estimators': [100, 200, 300, 400, 500],
                                'XGB__max_depth': [3,5,7,10],
                                'XGB__learning_rate': [0.01,0.05,0.1,0.15,0.2],
                                'XGB__min_child_weight': [1,3,5,7],
                                'XGB__gamma': [0.0,0.1,0.2,0.3,0.4],
                                'XGB__colsample_bytree': [0.3,0.4,0.5,0.7]}, 
                            random_params=None, random_n_iter=10, bayes_pbounds=None, bayes_int_params=None,
                            bayes_n_iter=30, sample_weight=None, random_state=None,verbosity=1, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a XGBoost regression model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For Time Series, cv must be a TimeSeriesSplit object or BlockTimeSeriesSplit object.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.

            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.


            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional   
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.

            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'XGB__param'" + '\n' "INFO: Default params in Documentation for XGBoost are: ", xgb_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # XGB__ is the prefix for every hyperparameters
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('XGB__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'XGB__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('XGB__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'XGB__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('XGB__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'XGB__'"
                assert all(key == 'Search' or key.startswith('XGB__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'XGB__'"

            #Preprocess the data automatically
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('XGB', XGBRegressor(random_state=random_state,n_jobs=n_jobs,verbosity=verbosity))]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)


    
    def Linear_Regression(self,  ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'LR__fit_intercept': [True, False],
                                'LR__normalize': [True, False],
                                'LR__copy_X': [True, False]}, 
                            random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a Linear Regression model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, use TimeSeriesSplit.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.


            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.


            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.

            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'LR__param'" + '\n' "INFO: Default params in Documentation for Linear Regression are: ", lr_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_param_grid must be a dictionary of parameters"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #LR is the prefix for every hyperparameter of the Linear Regression
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LR__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'LR__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LR__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'LR__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LR__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'LR__'"
                assert all(key == 'Search' or key.startswith('LR__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LR__'"
           
            
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('LR', LinearRegression())]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)

    
    def KNN_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'KNN__n_neighbors': [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99],
                                'KNN__weights': ['uniform', 'distance'],
                                'KNN__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                                'KNN__leaf_size': [10,20,30,40,50,60,70,80,90,100],
                                'KNN__p': [1,2]}, 
                            random_params=None, random_n_iter=10, bayes_pbounds=None, bayes_int_params=None,
                            bayes_n_iter=30, sample_weight=None ,random_state=None, n_jobs=-1, 
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a KNN Regressor model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, use TimeSeriesSplit or BlockTimeSeriesSplit.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.
            
            Returns
            -------
            self.model : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'KNN__param'" + '\n' "INFO: Default params in Documentation for KNN Regressor are: ", knn_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #KNN_ is the prefix for every hyperparameter in KNN
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('KNN__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'KNN__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('KNN__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'KNN__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('KNN__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'KNN__'"
                assert all(key == 'Search' or key.startswith('KNN__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'KNN__'"

            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('KNN', KNeighborsRegressor())]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)
    


    
    def DecisionTree_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'DT__criterion': ["squared_error", "friedman_mse", "absolute_error", "poisson"],
                                'DT__max_depth': [None,2,3,4,5],
                                'DT__min_samples_split': [2,3,4,],
                                'DT__max_features': ['auto', 'sqrt', 'log2'],
                                'DT__min_impurity_decrease': [0.0,0.1,0.2]}, 
                            random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a Decision Tree Regressor model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.

            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.
            
            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.

            Returns
            -------
            self.model : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'DT__param'" + '\n' "INFO: Default params in Documentation for Decision Tree Regressor are: ", dt_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # DT__ is the prefix for every hyperparameter in the Decision Tree Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('DT__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'DT__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('DT__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'DT__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('DT__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'DT__'"
                assert all(key == 'Search' or key.startswith('DT__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'DT__'"

            
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('DT', DecisionTreeRegressor(random_state=random_state))]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)

    
    def MLP_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'MLP__hidden_layer_sizes': [(3,),(5,)],
                                'MLP__activation': ['identity', 'logistic', 'tanh', 'relu'],
                                'MLP__solver': ['lbfgs', 'sgd', 'adam'],
                                'MLP__alpha': [0.0001,0.001,0.01,0.1,1,10,100],
                                'MLP__max_iter': [200]},
                            random_params=None, random_n_iter=10,bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None,random_state=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            """
            Trains a MLP Regressor model.

            Parameters
            ----------
            X_train : pandas dataframe
                Training data.
            
            y_train : pandas dataframe
                Training target.
            
            ordinal_cat_cols : list, optional
                List of ordinal categorical columns. The default is None.
            
            scoring : str, optional
                Scoring metric. The default is 'neg_mean_squared_error'.

            grid_params : dict, optional
                Grid search parameters. The default is {'MLP__hidden_layer_sizes': [(100,),(200,),(300,),(400,),(500,),(600,),(700,),(800,),(900,),(1000,)],
                'MLP__activation': ['identity', 'logistic', 'tanh', 'relu'],
                'MLP__solver': ['lbfgs', 'sgd', 'adam'],
                'MLP__alpha': [0.0001,0.001,0.01,0.1,1,10,100],
                'MLP__max_iter': [200,400,600,800,1000,1200,1400,1600,1800,2000],
            
            cv : int, optional
                Cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object or 
                a BlockTimeSeriesSplit object.
            
            random_params : dict, optional
                Random search parameters. The default is None.
            
            random_n_iter : int, optional
                Random search number of iterations. The default is 10.

            bayes_pbounds : dict, optional
                Bayesian optimization parameters. The default is None.
            
            bayes_int_params : list, optional
                Bayesian optimization integer parameters. The default is None.

            bayes_n_iter : int, optional
                Bayesian optimization number of iterations. The default is 30.

            random_state : int, optional
                Random state. The default is None.

            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional

                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.
        
            Returns
            -------
            None.

            """
            

            print(" INFO: Agurments params must start as 'MLP__param'" + '\n' "INFO: Default params in Documentation for MultiLayer Perceptron are: ", mlp_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'bayes_n_iter = {bayes_n_iter}' ,
            f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}',
            f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #MLP__ is the prefix for every hyperparameter in the MLP Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('MLP__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'MLP__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('MLP__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'MLP__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('MLP__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'MLP__'"
                assert all(key == 'Search' or key.startswith('MLP__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'MLP__'"

            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('MLP', MLPRegressor(random_state=random_state))]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
        
            print(self.model.best_params_)


    def SVR_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'SVR__kernel':['linear','poly','rbf'],
                                'SVR__C': [0.00001,0.0001,0.001,0.01,0.1,1,10,100,1000],
                                'SVR__gamma':[0.0001,0.001,0.01,0.1,1,10]}, 
                            random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            

            
            """
            This method performs a Decision Tree Regressor model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
            
            categories : list[str], optional
                Categories for OneHotEncoder Interpretation. The default is 'auto'.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.

            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.
            
            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.
            
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'SVR__param'" + '\n' "INFO: Default params in Documentation for SVR Regressor are: ", svr_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # DT__ is the prefix for every hyperparameter in the Decision Tree Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('SVR__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'SVR__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('SVR__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'SVR__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('SVR__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'SVR__'"
                assert all(key == 'Search' or key.startswith('SVR__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'SVR__'"
            
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('SVR', SVR())]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
            
            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)
            
            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)



    def LinearForest_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'LF__n_estimators': [100,200,300,400,500],
                                'LF__max_depth': [None,2,3,4,5],
                                'LF__min_samples_split': [2,3,4,],
                                'LF__max_features': ['auto', 'sqrt', 'log2'],
                                'LF__min_impurity_decrease': [0.0,0.1,0.2]},
                            random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
        
            """
            This method performs a Decision Tree Regressor model with grid search or bayesian optimization.

            Parameters
            ----------
            X_train : pandas
                Training set.
            
            y_train : pandas 
                Training set labels.

            categories : list[str], optional
                Categories for OneHotEncoder Interpretation. The default is 'auto'.
            
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.

            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
            
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.

            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.

            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.

            random_state : int, optional
                Random state. The default is None.

            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.

            Returns
            -------
            model_ : sklearn model
                Trained model.

            """

            print(" INFO: Agurments params must start as 'LF__param'" + '\n' "INFO: Default params in Documentation for Linear Forest Regressor are: ", rf_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # DT__ is the prefix for every hyperparameter in the Decision Tree Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LF__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'LF__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LF__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'LF__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LF__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'LF__'"
                assert all(key == 'Search' or key.startswith('LF__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LF__'"

            
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('LF', LinearForestRegressor(base_estimator=LinearRegression(), random_state=random_state, n_jobs=n_jobs))]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)

            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)



    def LinearBoost_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error', criterion='mse',
                            grid_params={'LB__n_estimators': [10,100,200,300,400,500],
                                'LB__loss':["linear", "square", "absolute", "exponential"],
                                'LB__max_depth': [None,2,3,4,5],
                                'LB__min_samples_split': [2,3,4],
                                'LB__max_features': ['auto', 'sqrt', 'log2'],
                                'LB__min_impurity_decrease': [0.0,0.1,0.2]},
                            random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
        
            """
            This method performs Linear Boosting Regressor from the following Library
            https://github.com/cerlymarco/linear-tree/blob/main/lineartree/lineartree.py

            Parameters
            ----------
            X_train : pandas
                Training set.
            
            y_train : pandas 
                Training set labels.

            categories : list[str], optional
                Categories for OneHotEncoder Interpretation. The default is 'auto'.
            
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.

            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
            
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.

            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.

            bayes_int_params : list, optional   
                List of parameters for bayesian optimization that are integers. The default is None.
            
            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.

            random_state : int, optional
                Random state. The default is None.

            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.
            
            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.

            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.

            
            Returns
            -------
            model_ : sklearn model
                Trained model.

            """

            print(" INFO: Agurments params must start as 'LB__param'" + '\n' "INFO: Default params in Documentation for Linear Boosting Regressor are: ", lb_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # DT__ is the prefix for every hyperparameter in the Decision Tree Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LB__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'LB__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LB__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'LB__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LB__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'LB__'"
                assert all(key == 'Search' or key.startswith('LB__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LB__'"



            
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('LB', LinearBoostRegressor(base_estimator=LinearRegression(), criterion=criterion, random_state=random_state))]) # Model always the last step
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)

            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)


    def LightGBM_Regressor(self, ordinal_cat_cols=None, categories='auto', scoring='neg_mean_squared_error',
                            grid_params={'LGBM__n_estimators': [100,200,300,400,500],
                                    'LGBM__boosting_type': ['gbdt', 'dart', 'goss', 'rf'],
                                    'LGBM__objective': [None],
                                    'LGBM__num_leaves': [31, 127, 255],
                                    'LGBM__max_depth': [-1,2,3,4,5],
                                    'LGBM__learning_rate': [0.1,0.001],
                                    'LGBM__subsample_for_bin': [200000, 500000],
                                    'LGBM__min_split_gain':[0.0],
                                    'LGBM__min_child_weight': [0.001],
                                    'LGBM__min_child_samples':[20],
                                    'LGBM__subsample':[1.0],
                                    'LGBM__subsample_freq':[0], 
                                    'LGBM__colsample_bytree':[1.0]},
                            random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
        
            """
            This method performs a LightGBM Regressor model with grid search random search or  bayesian optimization.
            Bayesian optimization for forescating recusrive lgas option is not available yet.
            https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html

            Parameters
            ----------
            X_train : pandas
                Training set.

            y_train : pandas
                Training set labels.

            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.

            categories : list[str], optional
                Categories for OneHotEncoder Interpretation. The default is 'auto'.

            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.

            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.

            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.

            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.    
            
            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.

            random_state : int, optional
                Random state. The default is None.

            n_jobs : int, optional
                Number of jobs. The default is -1.

            columns_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recursive. The default is None.

            column_rolled_lags : list[int], optional
                List of columns iloc position to apply lags for Forecasting Recusrive Rolling. The default is None.

            lags : list[int], optional
                Value Number of lags to apply for Forecasting Recursive. The default is None.

            rolled_lags : list[int], optional
                Value  Number of lags to apply for Forecasting Recursive Rolling. The default is None.

            rolled_metrics : list, optional 
                List of metrics to apply for Forecasting Recursive Rolling. The default is None.
            
            column_rolled_lags_initial : int, optional
                Int where from prevoiuosly register rolled lags starts computing. The default is None. Ususally use 1.

            Returns
            -------
            model_ : sklearn model
                Trained model.

            """


            print(" INFO: Agurments params must start as 'LGBM__param'" + '\n' "INFO: Default params in Documentation for LightGBM Regressor are: ", lgbm_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert self.X_train is not None and self.y_train is not None, "X_train and y_train must be provided, when initializing the class"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # DT__ is the prefix for every hyperparameter in the Decision Tree Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert 'Search' in grid_params.keys(), "In case of grid search, grid_params must contain 'Search'"
                assert grid_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LGBM__') for key in grid_params.keys()), "In case of grid search, grid_param_grid keys other than 'Search' must start with 'LGBM__'"

            elif random_params is not None:
                assert 'Search' in random_params.keys(), "In case of random search, random_params must contain 'Search'"
                assert random_params["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LGBM__') for key in random_params.keys()), "In case of random search, random_params keys other than 'Search' must start with 'LGBM__'"

            elif bayes_pbounds is not None:
                assert 'Search' in bayes_pbounds.keys(), "In case of bayesian optimization, bayes_pbounds must contain 'Search'"
                assert bayes_pbounds["Search"] in ["Forecast","Normal"], "In case of grid search, grid_params['Search'] must be 'Forecast' or 'Normal'"
                assert all(key == 'Search' or key.startswith('LGBM__') for key in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds keys other than 'Search' must start with 'LGBM__'"
                assert all(key == 'Search' or key.startswith('LGBM__') for key in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LGBM__'"

            
            preprocessor=self._automatic_preprocessor(self.X_train,ordinal_cat_cols,categories=categories)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('LGBM', LGBMRegressor(random_state=random_state))])
            #Select Grid Search, Random Search or Bayesian Optimization
            select_searchcv=SelectSearchCV(X_train=self.X_train, y_train=self.y_train,X_test=self.X_test,y_test=self.y_test, pipe=pipe, scoring=scoring, sample_weight=sample_weight,cv=self.cv,n_jobs=n_jobs)
            select_searchcv.select_automatic(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self.model=select_searchcv.fit(X_prev=self.X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            #generate a dictionary with all the parameters used in the model
            self._search_not_none_params = self._not_none_search(grid_params, random_params, random_n_iter, bayes_pbounds, bayes_int_params, bayes_n_iter)
            self._recursive_not_none_params = self._not_none_recursive(columns_lags, column_rolled_lags,lags,rolled_lags, rolled_metrics, column_rolled_lags_initial)

            self._overall_dict_params = {'X_vars': str(self.X_train.columns), "SearchParams": str(self._search_not_none_params), 'ordinal_cat_cols':str(ordinal_cat_cols), 'random_state':str(random_state),
                                        'n_jobs':str(n_jobs), 'Shape X_train': str(self.X_train.shape),'Shape y_train':str(self.y_train.shape), 'Shape X_prev':str([self.X_prev.shape if self.X_prev is not None else None]),
                                        'scoring':str(scoring), 'cv':str(self.cv), 'sample_weight':str(sample_weight), 'Recursive Params': str(self._recursive_not_none_params)}
            print(self.model.best_params_)
            

    def save(self,return_best_metrics:bool=True):
        """
        Saves the model to a file. And saves the cv results if exists grid search or random search as an excel file.

        Parameters
        ----------
        model_name : str
            Name of the model.
            The model is stored in the models folder. with the model name provided

        Returns
        -------
        None.

        """
        assert self.model is not None , "Model not trained yet"
        #create folder if not exists where the model will be saved
        path = f'./models/{self.model_name}'
        if not os.path.exists(path):
            os.makedirs(path)

        joblib.dump(self.model, os.path.join(path, self.model_name+'.joblib'))
        #save cv results if exists grid search or random search
        if hasattr(self.model, 'cv_results_'):
            df = pd.DataFrame(self.model.cv_results_)
            df.sort_values('rank_test_score', inplace=True)
            if hasattr(self.cv, 'is_timeseriesinitialsplit'):
                #rename the split columns
                try:
                    new_column_names_score = self.cv.get_test_days(self.X_train)
                    new_column_names_pred = ["y_pred_" + date for date in self.cv.get_test_days(self.X_train)]
                except:
                    new_column_names_score = self.cv.get_test_days(self.X_train,self.X_test)
                    new_column_names_pred = ["y_pred_" + date for date in self.cv.get_test_days(self.X_train,self.X_test)]

                df.rename(columns=dict(zip(df.filter(regex='split').filter(regex='_test_score').columns, new_column_names_score)), inplace=True)
                df.rename(columns=dict(zip(df.filter(regex='split').filter(regex='_y_pred').columns, new_column_names_pred)), inplace=True)
            df.to_excel(os.path.join(path, self.model_name+'_cv_results.xlsx'), index=False)

            #save the best register of the cv_results in a second sheet of excel file called summary_models.xlsx
            df_best = pd.DataFrame(df.iloc[0]).T
            df_best["Search conditions"]=str(self._overall_dict_params)
            df_best['model_name'] = self.model_name
            #set model_name the firts column and Search conditions the second column
            cols = df_best.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df_best = df_best[cols]

            # save in the second sheet
            file_path = './models/summary_models.xlsx'
            if os.path.isfile(file_path):
                df_summary = pd.read_excel(file_path, sheet_name='Sheet2')
                df_summary = pd.concat([df_summary, df_best], axis=0,ignore_index=True)
                df_summary.to_excel(file_path, index=False, sheet_name='Sheet2')
            else:
                df_best.to_excel(file_path, index=False, sheet_name='Sheet2')
            if return_best_metrics:
                self.results = df_best
                return df_best
            

    def load(self):

        """
        Loads a model from a file.

        Parameters
        ----------
        model_name : str
            Name of the model.
            The model is stored in the models folder. with the model name provided
            To load a model, the model must be saved before. And when instantiating the class, 
            its not mandatory to pass the X_train and y_train arguments.

        Returns
        -------
        None.

        """
        assert self.model_name in os.listdir('./models'), "Model not found"
        assert self.model_name+'.joblib' in os.listdir(f'./models/{self.model_name}'), "Model not found"
        path = f'./models/{self.model_name}/{self.model_name}'+'.joblib'
        self.model = joblib.load(path)
        return self.model
    
    @staticmethod
    def _automatic_preprocessor(X_train, ordinal_cat_cols:List[str]=None,categories:List[str]='auto'):
        #Arguments assertion not needed because they are already checked in the model method of the classes that are the ones that call this function
        """
        This function performs a preprocessor for the data. It automatically detects the categorical and numeric variables and performs the following steps:
            - Numeric variables: imputation by scaling. STANDARD SCALER
            - Categorical variables: imputation by encoding. ONE HOT ENCODER
            - Ordinal categorical variables: imputation by encoding. ORDINAL ENCODER

        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal.

        Returns
        -------
        preprocessor : sklearn preprocessor
            Preprocessor for the data. Used fo the pipelines for every model.

        """
        num_cols = X_train.select_dtypes(include=np.number).columns.values.tolist() #Detects the numeric variables
        cat_cols = X_train.select_dtypes(include=['category']).columns.values.tolist() #detects the categorical variables

        if ordinal_cat_cols is None:
            cat_cols_onehot = cat_cols
            ordinal_cat_cols = []
        else:
            for col in ordinal_cat_cols:
                cat_cols.remove(col)
            cat_cols_onehot = cat_cols

        # Prepare the categorical variables by encoding the categories    
        categorical_transformer_onehot = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', drop='first',categories=categories))])
        categorical_transformer_ordinal = Pipeline(steps=[('ordinal', OrdinalEncoder())])
        # Prepare the numeric variables by imputing by scaling
        numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

        preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_transformer, num_cols), #numeric variables
            ('cat_onehot', categorical_transformer_onehot, cat_cols_onehot), #categorical variables
            ('cat_ordinal', categorical_transformer_ordinal, ordinal_cat_cols)]) #ordinal categorical variables
        
        return preprocessor
    
    @staticmethod
    def _not_none_search(*args):
        """
        This function returns a list of the arguments that are not None. Is used to store the not none parameters of the seleted search  of the model in the dictionary self._overall_dict
        """
        search_list=['grid_params', 'random_params', 'random_n_iter', 'bayes_pbounds', 'bayes_int_params', 'bayes_n_iter']
        return [(search_list[i],value_var) for i, value_var in enumerate(args) if value_var is not None]
        #add the variable name to the value
    @staticmethod
    def _not_none_recursive(*args):
        """
        This function returns a list of the arguments that are not None. Is used to store the not none parameters of the  the recursive parameters of the model in the dictionary self._overall_dict
        """
        recursive_list=['columns_lags', 'column_rolled_lags','lags','rolled_lags', 'rolled_metrics', 'column_rolled_lags_initial']
        return [(recursive_list[i],value_var) for i, value_var in enumerate(args) if value_var is not None]
            
        


    
    
            

            

            
            
                                
    


        


    

    

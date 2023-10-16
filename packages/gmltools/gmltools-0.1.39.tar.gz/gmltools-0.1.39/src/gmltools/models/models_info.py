
























#---------------------------------------------------------------------PARAMETERS---------------------------------------------------------------------#
# CLASSIFICATION MODELS DEFAULT PARAMETERS
rf_default_params_clf={"n_estimators": 100,
"criterion": "gini",
"max_depth": None,
"min_samples_split": 2,
"min_samples_leaf": 1,
"min_weight_fraction_leaf": 0.0,
"max_features": "sqrt",
"max_leaf_nodes": None,
"min_impurity_decrease": 0.0,
"bootstrap": True,
"oob_score": False,
"n_jobs": None,
"random_state": None,
"verbose": 0,
"warm_start": False,
"class_weight": None,
"ccp_alpha": 0.0,
"max_samples": None
}


xgb_default_params_clf ={
    'base_score': 0.5,
    'booster': 'gbtree',
    'colsample_bylevel': 1,
    'colsample_bynode': 1,
    'colsample_bytree': 1,
    'gamma': 0,
    'gpu_id': -1,
    'importance_type': 'gain',
    'interaction_constraints': '',
    'learning_rate': 0.1,
    'max_delta_step': 0,
    'max_depth': 6,
    'min_child_weight': 1,
    'missing': None,
    'monotone_constraints': '()',
    'n_estimators': 100,
    'n_jobs': 1,
    'num_parallel_tree': 1,
    'random_state': 0,
    'reg_alpha': 0,
    'reg_lambda': 1,
    'scale_pos_weight': 1,
    'subsample': 1,
    'tree_method': 'exact',
    'validate_parameters': 1,
    'verbosity': None
}

lr_default_params_clf={
    'penalty': 'l2',
    'dual': False,
    'tol': 0.0001,
    'C': 1.0,
    'fit_intercept': True,
    'intercept_scaling': 1,
    'class_weight': None,
    'random_state': None,
    'solver': 'lbfgs',
    'max_iter': 100,
    'multi_class': 'auto',
    'verbose': 0,
    'warm_start': False,
    'n_jobs': None,
    'l1_ratio': None
}

mlp_default_params_clf={
    'hidden_layer_sizes': (100,),
    'activation': 'relu',
    'solver': 'adam',
    'alpha': 0.0001,
    'batch_size': 'auto',
    'learning_rate': 'constant',
    'learning_rate_init': 0.001,
    'power_t': 0.5,
    'max_iter': 200,
    'shuffle': True,
    'random_state': None,
    'tol': 0.0001,
    'verbose': False,
    'warm_start': False,
    'momentum': 0.9,
    'nesterovs_momentum': True,
    'early_stopping': False,
    'validation_fraction': 0.1,
    'beta_1': 0.9,
    'beta_2': 0.999,
    'epsilon': 1e-08,
    'n_iter_no_change': 10,
    'max_fun': 15000
}

knn_default_params_clf={
    'n_neighbors': 5,
    'weights': 'uniform',
    'algorithm': 'auto',
    'leaf_size': 30,
    'p': 2,
    'metric': 'minkowski',
    'metric_params': None,
    'n_jobs': None}


dt_default_params_clf={
    'criterion': 'gini',
    'splitter': 'best',
    'max_depth': None,
    'min_samples_split': 2,
    'min_samples_leaf': 1,
    'min_weight_fraction_leaf': 0.0,
    'max_features': None,
    'random_state': None,
    'max_leaf_nodes': None,
    'min_impurity_decrease': 0.0,
    'class_weight': None,
    'ccp_alpha': 0.0
}


# REGRESSION MODELS DEFAULT PARAMETERS

rf_default_params_reg = {
    "n_estimators": 100,
    "criterion": "squared_error",
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "min_weight_fraction_leaf": 0.0,
    "max_features": 1.0,
    "max_leaf_nodes": None,
    "min_impurity_decrease": 0.0,
    "bootstrap": True,
    "oob_score": False,
    "n_jobs": None,
    "random_state": None,
    "verbose": 0,
    "warm_start": False,
    "ccp_alpha": 0.0,
    "max_samples": None
}

#XBGBOOST REGRESSOR DEFAULT PARAMETERS BUT THERE ARE MORE PARAMETERS TO TUNE
xgb_default_params_reg={
    'base_score': 0.5,
    'booster': 'gbtree',
    'colsample_bylevel': 1,
    'colsample_bynode': 1,
    'colsample_bytree': 1,
    'gamma': 0,
    'gpu_id': -1,
    'importance_type': 'gain',
    'interaction_constraints': '',
    'learning_rate': 0.1,
    'max_delta_step': 0,
    'max_depth': 6,
    'min_child_weight': 1,
    'missing': None,
    'monotone_constraints': '()',
    'n_estimators': 100,
    'n_jobs': 1,
    'num_parallel_tree': 1,
    'random_state': 0,
    'reg_alpha': 0,
    'reg_lambda': 1,
    'scale_pos_weight': 1,
    'subsample': 1,
    'tree_method': 'auto',
    'validate_parameters': 1,
    'verbosity': None,
    'lambda': 1,
    'alpha': 0,
    'refresh_leaf': 1,
    'process_type': 'default',
    'grow_policy': 'depthwise',
    'max_bins': 256,
    'predictor': 'auto',
}

lr_default_params_reg={
    'fit_intercept': True,
    'copy_X': True,
    'n_jobs': None,
    'positive': False
}

mlp_default_params_reg = {
    "hidden_layer_sizes": (100,),
    "activation": "relu",
    "solver": "adam",
    "alpha": 0.0001,
    "batch_size": "auto",
    "learning_rate": "constant",
    "learning_rate_init": 0.001,
    "power_t": 0.5,
    "max_iter": 200,
    "shuffle": True,
    "random_state": None,
    "tol": 0.0001,
    "verbose": False,
    "warm_start": False,
    "momentum": 0.9,
    "nesterovs_momentum": True,
    "early_stopping": False,
    "validation_fraction": 0.1,
    "beta_1": 0.9,
    "beta_2": 0.999,
    "epsilon": 1e-08,
    "n_iter_no_change": 10,
    "max_fun": 15000
}


knn_default_params_reg = {
    "n_neighbors": 5,
    "weights": "uniform",
    "algorithm": "auto",
    "leaf_size": 30,
    "p": 2,
    "metric": "minkowski",
    "metric_params": None,
    "n_jobs": None
}

dt_default_params_reg = {
    "criterion": "squared_error",
    "splitter": "best",
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "min_weight_fraction_leaf": 0.0,
    "max_features": None,
    "random_state": None,
    "max_leaf_nodes": None,
    "min_impurity_decrease": 0.0,
    "ccp_alpha": 0.0
}



svr_default_params_reg = {
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
    'degree': 3,
    'gamma': ['scale','auto', 0.001, 0.01, 0.1, 10],
    'coef0': 0.0,
    'tol': 1e-3,
    'C':[0.0001,0.001,0.01,0.1,1,10],
    'epsilon': 0.1,
    'shrinking': True,
    'cache_size': 200,
    'verbose': False,
    'max_iter': -1
}


lb_default_params_reg = {
    "n_estimators": 10,
    "criterion": ["linear", "square", "absolute", "exponential"],
    "max_depth": 3,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "min_weight_fraction_leaf": 0.0,
    "max_features": None,
    "max_leaf_nodes": None,
    "min_impurity_decrease": 0.0,
    "random_state": None,
    "ccp_alpha": 0.0,
}


lgbm_default_params_reg = {
    'n_estimators': [100,200,300,400,500],
    'boosting_type': ['gbdt', 'dart', 'goss', 'rf'],
    'objective': [None],
    'num_leaves': [31, 127, 255],
    'max_depth': [-1,2,3,4,5],
    'learning_rate': [0.1,0.001],
    'subsample_for_bin': [200000, 500000],
    'min_split_gain':[0.0],
    'min_child_weight': [0.001],
    'min_child_samples':[20],
    'subsample':[1.0],
    'subsample_freq':[0], 
    'colsample_bytree':[1.0],
}



lgbm_default_params_reg = {
    'n_estimators': [100,200,300,400,500],
    'boosting_type': ['gbdt', 'dart', 'goss', 'rf'],
    'objective': [None],
    'num_leaves': [31, 127, 255],
    'max_depth': [-1,2,3,4,5],
    'learning_rate': [0.1,0.001],
    'subsample_for_bin': [200000, 500000],
    'min_split_gain':[0.0],
    'min_child_weight': [0.001],
    'min_child_samples':[20],
    'subsample':[1.0],
    'subsample_freq':[0], 
    'colsample_bytree':[1.0],
}












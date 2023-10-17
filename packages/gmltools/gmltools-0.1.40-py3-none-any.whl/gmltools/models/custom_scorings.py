import numpy as np
from sklearn.metrics import make_scorer
# Definir la función de pérdida personalizada
#MEAN_SQUARED_ERROR
def neg_mean_squared_error_exptimeweights(y_true, y_pred):
    diff = np.abs(y_true - y_pred)
    alpha = 0.05
    weights = np.exp(-alpha * np.arange(len(diff)))
    return -np.mean(weights * np.square(diff))

def neg_mean_squared_error_powertimeweights_2(y_true, y_pred):
    diff = np.abs(y_true - y_pred)
    alpha = 2
    weights = np.power(np.arange(len(diff)), alpha)
    weights= (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
    return -np.mean(weights * np.square(diff))

def neg_mean_squared_error_powertimeweights_2_5(y_true, y_pred):
    diff = np.abs(y_true - y_pred)
    alpha = 2.5
    weights = np.power(np.arange(len(diff)), alpha)
    weigts = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
    return -np.mean(weights * np.square(diff))

def neg_mean_squared_error_powertimeweights_2_9(y_true, y_pred):
    diff = np.abs(y_true - y_pred)
    alpha = 2.9
    weights = np.power(np.arange(len(diff)), alpha)
    weights = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
    return -np.mean(weights * np.square(diff))

def neg_mean_squared_error_powertimeweights_1_5(y_true, y_pred):
    diff = np.abs(y_true - y_pred)
    alpha = 1.5
    weights = np.power(np.arange(len(diff)), alpha)
    weights = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
    return -np.mean(weights * np.square(diff))

def neg_mean_squared_error_lineal(y_true, y_pred):
    diff = np.abs(y_true - y_pred)
    alpha = 1
    weights = np.power(np.arange(len(diff)), alpha)
    weights = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
    mse_custom = -np.mean(weights * np.square(diff))
    return -np.mean(weights * np.square(diff))


#scoring = make_scorer(neg_mean_squared_error_exptimeweights, greater_is_better=False)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error, median_absolute_error
import numpy as np
#import numbers
from traceback import format_exc
import time
from sklearn.base import clone


SCORERS = {
    'neg_mean_absolute_error': mean_absolute_error,
    'neg_mean_squared_error': mean_squared_error,
    'neg_root_mean_squared_error': lambda y_true, y_pred: np.sqrt(mean_squared_error(y_true, y_pred)),}





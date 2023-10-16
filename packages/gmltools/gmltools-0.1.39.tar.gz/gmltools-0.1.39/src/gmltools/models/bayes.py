from bayes_opt import BayesianOptimization, UtilityFunction
from sklearn.model_selection import cross_val_score
import numpy as np


class ModelOptimizer:
    """
    Class for optimizing model hyperparameters using Bayesian Optimization.
    Functions based on code from: https://towardsdatascience.com/bayesian-optimization-with-python-85c66df711ec

    Methods:
        black_box_function: Black box function for optimization algorithm.
        optimize_model: Optimize model hyperparameters.

    Attributes:
        optimizer: Optimizer object.
        best_optimizer: Best optimizer object.
        scoring: Scoring function.


    """
    def __init__(self, scoring, cv=10):
        """
        Parameters
        ----------
        scoring : str
            Scoring function.
        cv : int, optional
            Number of folds. The default is 10.
            For Time Series data, use TimeSeriesSplit or BlockTimeSeriesSplit.
        
        Returns
        -------
        None.
        """
        self.optimizer = None
        self.best_optimizer = None
        self.scoring = scoring
        self.cv = cv

    def black_box_function(self, X_train_scale, y_train, model, **params):
        """
        Black box function for optimization algorithm

        Parameters
        ----------
        X_train_scale : array-like
            Training data.
        y_train : array-like
            Target values.
        model : object
            Model object.
        **params : dict
            Dictionary with hyperparameters.
        
        Returns
        -------
        f.mean() : float
            Mean of cross validation scores obtained from the black box function.
        """
        model = model.set_params(**params)
        f = cross_val_score(model, X_train_scale, y_train,
                            scoring=self.scoring, cv=self.cv)
        
        return f.mean()

    def optimize_model(self, pbounds, X_train_scale, y_train, model, int_params, n_iter=25):
        """
        Optimize model hyperparameters

        Parameters
        ----------
        pbounds : dict
            Dictionary with parameter names as keys and a tuple with the
            lower and upper bounds as values.
        X_train_scale : array-like
            Training data.
        y_train : array-like
            Target values.
        model : object
            Model object.
        int_params : list
            List of parameters that should be forced to be integers.
        n_iter : int, optional
            Number of iterations. The default is 25.

        Returns
        -------
        optimizer.max["params"] : dict
            Dictionary with optimized hyperparameters. 
        """
        def opt_function(**params):
            """
            Function wrapper

            Parameters
            ----------
            **params : dict
                Dictionary with hyperparameters.
            
            Returns
            -------
            f.mean() : float
                Mean of cross validation scores obtained from the black box function.
            """
            return self.black_box_function(X_train_scale,
                                           y_train,
                                           model,
                                           **params)
        # create optimizer
        optimizer = BayesianOptimization(f = None,
                                         pbounds=pbounds,
                                         verbose=2,
                                         random_state=None)

        # declare acquisition function used for getting new values of the
        # hyperparams
        utility = UtilityFunction(kind = "ucb", kappa = 1.96, xi = 0.01)

        # Optimization for loop.
        for i in range(n_iter):
            # Get optimizer to suggest new parameter values to try using the
            # specified acquisition function.
            next_point = optimizer.suggest(utility)
            # Force degree from float to int.
            for int_param in int_params:
                next_point[int_param] = int(next_point[int_param])
            # Evaluate the output of the black_box_function using 
            # the new parameter values.
            target = opt_function(**next_point)
            try:
                # Update the optimizer with the evaluation results. 
                # This should be in try-except to catch any errors!
                optimizer.register(params = next_point, target = target)
            except:
                pass
                   
        print("Best result: {}.".format(optimizer.max["params"]))

        self.optimizer = optimizer
        self.best_optimizer = optimizer.max

        return optimizer.max["params"]
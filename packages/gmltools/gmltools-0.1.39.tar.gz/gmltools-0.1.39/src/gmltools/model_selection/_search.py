import pandas as pd
from sklearn.model_selection import ParameterGrid
from joblib import Parallel, delayed
#from sklearn.metrics import SCORERS, make_scorer
from itertools import product
import time
import numbers
from joblib import logger
from collections import defaultdict
#import clone
import numpy as np
from sklearn.base import clone,is_classifier
from traceback import format_exc
from sklearn.utils.validation import _check_fit_params, indexable, check_is_fitted
from sklearn.model_selection._validation import _warn_or_raise_about_fit_failures, _aggregate_score_dicts, _insert_error_scores, _num_samples, _normalize_score_results
from sklearn.model_selection._search import _estimator_has
from numpy.ma import MaskedArray
from abc import ABCMeta, abstractmethod
from sklearn.base import MetaEstimatorMixin, BaseEstimator
from sklearn.model_selection._search import ParameterSampler
from sklearn.utils.metaestimators import available_if
import warnings
from functools import partial
from sklearn.utils._tags import _safe_tags
from scipy.stats import rankdata
from sklearn.exceptions import NotFittedError
from ._scorer import SCORERS
from sklearn.utils.metaestimators import _safe_split
from ..model_prediction._forecast import RecursivePredictor
import copy
from sklearn.model_selection._split import check_cv


class ForecastBaseSearchCV(MetaEstimatorMixin, BaseEstimator, metaclass=ABCMeta):
    """Abstract base class for hyper parameter search with cross-validation."""
    
    @abstractmethod
    def __init__(
        self,
        estimator,
        *,
        scoring=None,
        n_jobs=None,
        refit=True,
        cv=None,
        verbose=0,
        pre_dispatch="2*n_jobs",
        error_score=np.nan,
        return_train_score=True,
    ):

        self.scoring = scoring
        self.estimator = estimator
        self.n_jobs = n_jobs
        self.refit = refit
        self.cv = cv
        self.verbose = verbose
        self.pre_dispatch = pre_dispatch
        self.error_score = error_score
        self.return_train_score = return_train_score


    @property
    def _estimator_type(self):
        return self.estimator._estimator_type


    def _more_tags(self):
    # allows cross-validation to see 'precomputed' metrics
        return {
            "pairwise": _safe_tags(self.estimator, "pairwise"), #check import
            "_xfail_checks": {
                "check_supervised_y_2d": "DataConversionWarning not caught"
            },
        }

    @available_if(_estimator_has("score_samples"))
    def score_samples(self, X):
        """Call score_samples on the estimator with the best found parameters.

        Only available if ``refit=True`` and the underlying estimator supports
        ``score_samples``.

        .. versionadded:: 0.24

        Parameters
        ----------
        X : iterable
            Data to predict on. Must fulfill input requirements
            of the underlying estimator.

        Returns
        -------
        y_score : ndarray of shape (n_samples,)
            The ``best_estimator_.score_samples`` method.
        """
        check_is_fitted(self)
        return self.best_estimator_.score_samples(X)
    
    @available_if(_estimator_has("transform"))
    def transform(self, X):
        """Call transform on the estimator with the best found parameters.

        Only available if the underlying estimator supports ``transform`` and
        ``refit=True``.

        Parameters
        ----------
        X : indexable, length n_samples
            Must fulfill the input assumptions of the
            underlying estimator.

        Returns
        -------
        Xt : {ndarray, sparse matrix} of shape (n_samples, n_features)
            `X` transformed in the new space based on the estimator with
            the best found parameters.
        """
        check_is_fitted(self)
        return self.best_estimator_.transform(X)

    @available_if(_estimator_has("inverse_transform"))
    def inverse_transform(self, Xt):
        """Call inverse_transform on the estimator with the best found params.

        Only available if the underlying estimator implements
        ``inverse_transform`` and ``refit=True``.

        Parameters
        ----------
        Xt : indexable, length n_samples
            Must fulfill the input assumptions of the
            underlying estimator.

        Returns
        -------
        X : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Result of the `inverse_transform` function for `Xt` based on the
            estimator with the best found parameters.
        """
        check_is_fitted(self)
        return self.best_estimator_.inverse_transform(Xt)
    
    @available_if(_estimator_has("predict"))
    def predict(self, X):
        """Call predict on the estimator with the best found parameters.

        Only available if ``refit=True`` and the underlying estimator supports
        ``predict``.

        Parameters
        ----------
        X : indexable, length n_samples
            Must fulfill the input assumptions of the
            underlying estimator.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            The predicted labels or values for `X` based on the estimator with
            the best found parameters.
        """
        check_is_fitted(self)
        return self.best_estimator_.predict(X)

    @property
    def n_features_in_(self):
        """Number of features seen during :term:`fit`.

        Only available when `refit=True`.
        """
        # For consistency with other estimators we raise a AttributeError so
        # that hasattr() fails if the search estimator isn't fitted.
        try:
            check_is_fitted(self)
        except NotFittedError as nfe:
            raise AttributeError(
                "{} object has no n_features_in_ attribute.".format(
                    self.__class__.__name__
                )
            ) from nfe

        return self.best_estimator_.n_features_in_

    @property
    def classes_(self):
        """Class labels.

        Only available when `refit=True` and the estimator is a classifier.
        """
        _estimator_has("classes_")(self)
        return self.best_estimator_.classes_



    def _run_search(self, evaluate_candidates):
        """Repeatedly calls `evaluate_candidates` to conduct a search.

        This method, implemented in sub-classes, makes it possible to
        customize the scheduling of evaluations: GridSearchCV and
        RandomizedSearchCV schedule evaluations for their whole parameter
        search space at once but other more sequential approaches are also
        possible: for instance is possible to iteratively schedule evaluations
        for new regions of the parameter search space based on previously
        collected evaluation results. This makes it possible to implement
        Bayesian optimization or more generally sequential model-based
        optimization by deriving from the BaseSearchCV abstract base class.
        For example, Successive Halving is implemented by calling
        `evaluate_candidates` multiples times (once per iteration of the SH
        process), each time passing a different set of candidates with `X`
        and `y` of increasing sizes.

        Parameters
        ----------
        evaluate_candidates : callable
            This callback accepts:
                - a list of candidates, where each candidate is a dict of
                  parameter settings.
                - an optional `cv` parameter which can be used to e.g.
                  evaluate candidates on different dataset splits, or
                  evaluate candidates on subsampled data (as done in the
                  SucessiveHaling estimators). By default, the original `cv`
                  parameter is used, and it is available as a private
                  `_checked_cv_orig` attribute.
                - an optional `more_results` dict. Each key will be added to
                  the `cv_results_` attribute. Values should be lists of
                  length `n_candidates`

            It returns a dict of all results so far, formatted like
            ``cv_results_``.

            Important note (relevant whether the default cv is used or not):
            in randomized splitters, and unless the random_state parameter of
            cv was set to an int, calling cv.split() multiple times will
            yield different splits. Since cv.split() is called in
            evaluate_candidates, this means that candidates will be evaluated
            on different splits each time evaluate_candidates is called. This
            might be a methodological issue depending on the search strategy
            that you're implementing. To prevent randomized splitters from
            being used, you may use _split._yields_constant_splits()

        Examples
        --------

        ::

            def _run_search(self, evaluate_candidates):
                'Try C=0.1 only if C=1 is better than C=10'
                all_results = evaluate_candidates([{'C': 1}, {'C': 10}])
                score = all_results['mean_test_score']
                if score[0] < score[1]:
                    evaluate_candidates([{'C': 0.1}])
        """
        raise NotImplementedError("_run_search not implemented.")

    def _check_refit_for_multimetric(self, scores):
        """Check `refit` is compatible with `scores` is valid"""
        multimetric_refit_msg = (
            "For multi-metric scoring, the parameter refit must be set to a "
            "scorer key or a callable to refit an estimator with the best "
            "parameter setting on the whole data and make the best_* "
            "attributes available for that metric. If this is not needed, "
            f"refit should be set to False explicitly. {self.refit!r} was "
            "passed."
        )

        valid_refit_dict = isinstance(self.refit, str) and self.refit in scores

        if (
            self.refit is not False
            and not valid_refit_dict
            and not callable(self.refit)
        ):
            raise ValueError(multimetric_refit_msg)


    @staticmethod
    def _select_best_index(refit, refit_metric, results):
        """Select index of the best combination of hyperparemeters."""
        if callable(refit):
            # If callable, refit is expected to return the index of the best
            # parameter set.
            best_index = refit(results)
            if not isinstance(best_index, numbers.Integral):
                raise TypeError("best_index_ returned is not an integer")
            if best_index < 0 or best_index >= len(results["params"]):
                raise IndexError("best_index_ index out of range")
        else:
            best_index = results[f"rank_test_{refit_metric}"].argmin()
        return best_index

    def _check_refit_for_multimetric(self, scores):
        """Check `refit` is compatible with `scores` is valid"""
        multimetric_refit_msg = (
            "For multi-metric scoring, the parameter refit must be set to a "
            "scorer key or a callable to refit an estimator with the best "
            "parameter setting on the whole data and make the best_* "
            "attributes available for that metric. If this is not needed, "
            f"refit should be set to False explicitly. {self.refit!r} was "
            "passed."
        )

        valid_refit_dict = isinstance(self.refit, str) and self.refit in scores

        if (
            self.refit is not False
            and not valid_refit_dict
            and not callable(self.refit)
        ):
            raise ValueError(multimetric_refit_msg)




    def fit(self, X, y_train, X_test=None, y_test=None, *, X_prev=None, lags=None, columns_lags=None, column_rolled_lags=None, column_rolled_lags_initial=None, rolled_metrics=None, rolled_lags=None, groups=None, **fit_params):

        print("Para Forecast Day-Ahead > 1 aplica X=X_train, y_train=y_train, X_test=X_test, y_test=y_test. Para Forecast Day-ahead = 1 aplica X, y_train=y")
        #estimator must exist due to requirements of sklearn 
        estimator=self.estimator
        refit_metric = "score"
        # Genera todos los splits de validación cruzada

        #------------------------------------------------------------------------------------
        # cv_copy=copy.deepcopy(self.cv)
        # if X_test is not None:

        #     n_splits=cv_copy.get_n_splits(X, X_test)
        #     cv_splits = cv_copy.split(X, X_test)   
        #     cv_orig=cv_splits         
        # else:
        #     cv_orig = check_cv(cv_copy, y_train, classifier=is_classifier(estimator))
        #     n_splits=cv_copy.get_n_splits(X,y_train,groups)
        #-----------------------------------------------------------------------------------
        if X_test is not None:
            n_splits=self.cv.get_n_splits(X, X_test)
            cv_splits=self.cv.split(X, X_test)

        else:
            n_splits=self.cv.get_n_splits(X,y_train,groups)
            cv_splits = self.cv.split(X, y_train, groups)

        #Para cuadno se hace recursive prediction con datos de day-ahead > 1, se utiliza un id
        if 'id' in X.columns and 'id':
            #assert that X_test exists as a dataframe
            assert isinstance(X_test, pd.DataFrame), "X_test must be a dataframe"
            assert 'id' in X_test.columns, "X_test must have an id column"
            assert isinstance(y_test, pd.DataFrame) or isinstance(y_test,pd.Series), "y_test must be a Series or a DataFrame"
            a,b=np.unique(X_test.id,return_counts=True)
            self.registers_per_day_format=b[0]
            assert len(np.unique(b))==1
            X_test = X_test.drop(columns=['id'])
            X = X.drop(columns=['id'])
            self.id=True
            print(f"Day-ahead = {int(b[0]/self.cv.increment_size)} Detected")
        #Para day-ahead = 1 no hace falta id
        else:
            print("Day-ahead = 1 Detected")
            self.registers_per_day_format=self.cv.increment_size
            self.id=False
        #assret that all values in b are the same value
        if X_test is not None:
            assert all(X_test.columns == X.columns), "X_test and X must have the same columns names"

        # Crea todas las combinaciones posibles de hiperparámetros
        hyperparameter_combinations = list(ParameterGrid(self.param_grid))

        #numero de splits
        #n_splits=self.cv.get_n_splits(X, X_test)

        # Si scoring es un string, obtén la función de scoring correspondiente
        if isinstance(self.scoring, str):
            if self.scoring not in SCORERS:
                raise ValueError(f"Invalid scoring: {self.scoring}. It should be a valid scorer or a callable.")
            self.scoring = SCORERS[self.scoring]
            scorers=self.scoring

        elif callable(self.scoring):
            scorers=self.scoring
        #Make arrays indexable for cross-validation
        X, y_train, groups = indexable(X, y_train, groups)
        #Check and validate the parameters passed during `fit`
        fit_params = _check_fit_params(X, fit_params)

        #DEFINE OPTIMIZATION

        base_estimator = clone(self.estimator)

        parallel = Parallel(n_jobs=self.n_jobs, pre_dispatch="2*n_jobs",verbose=self.verbose)
        #KEYWARDS FOR FIT AND SCORE FUNCTION
        fit_and_score_kwargs = dict(
            scorer=scorers, #from self.scoring
            fit_params=fit_params, #check from fit
            return_train_score=self.return_train_score, #check from __init__
            return_n_test_samples=True, #check
            return_times=True, #check
            return_parameters=False, #check
            error_score=self.error_score, #check from __init__
            verbose=self.verbose, #check from __init__
        )

        #RESULTTS OF FITTING SCORES ETC STORED IN RESULTS DICT
        results={}
        #PARALLEL PROCESSING OF OPTIMIZATION
        with parallel:
            all_candidate_params = []
            all_out = []
            all_more_results = defaultdict(list)
            
            def evaluate_candidates(candidate_params,cv=None, more_results=None):

                # if X_test is None:
                #     cv = cv or cv_orig
                #     cv_splits = cv.split(X, y_train, groups)
                # else:
                #     cv_splits = cv_orig

                
                #cv = cv or cv_orig
                candidate_params = list(candidate_params)
                n_candidates = len(candidate_params)

                if self.verbose > 0:
                    print(f"Fitting {n_splits} candidates for each {n_candidates}, totalling {n_candidates * n_splits} fits")

                else:
                    pass

                # Ejecuta el proceso de optimización y validación cruzada en paralelo
                
                out = parallel(delayed(_fit_and_score)(model=clone(base_estimator),
                                                        X=X,
                                                        X_test=X_test, 
                                                        y_train=y_train, 
                                                        y_test=y_test, 
                                                        train=train, 
                                                        test=test,
                                                        parameters=parameters, 
                                                        split_progress=(split_idx,n_splits), 
                                                        candidate_progress=(cand_idx, n_candidates),
                                                        is_id=self.id,
                                                        X_prev=X_prev,
                                                        lags=lags,  
                                                        rolled_lags=rolled_lags,  
                                                        column_lags=columns_lags, 
                                                        column_rolled_lags=column_rolled_lags, 
                                                        column_rolled_lags_initial=column_rolled_lags_initial,
                                                        rolled_metrics=rolled_metrics,
                                                        **fit_and_score_kwargs,
                                                        ) 
                    for (cand_idx, parameters), (split_idx, (train,test)) in product(enumerate(candidate_params), enumerate(cv_splits))
                )

                #check the output of _fit_and_score
                if len(out) < 1:
                        raise ValueError(
                            "No fits were performed. "
                            "Was the CV iterator empty? "
                            "Were there no candidates?"
                        )
                elif len(out) != n_candidates * n_splits:
                    raise ValueError(
                        "cv.split and cv.get_n_splits returned "
                        "inconsistent results. Expected {} "
                        "splits, got {}".format(n_splits, len(out) // n_candidates)
                    )

                _warn_or_raise_about_fit_failures(out, self.error_score) #check import

                # For callable self.scoring, the return type is only know after
                # calling. If the return type is a dictionary, the error scores
                # can now be inserted with the correct key. The type checking
                # of out will be done in `_insert_error_scores`.
                if callable(self.scoring):
                    _insert_error_scores(out, self.error_score) #check import

                all_candidate_params.extend(candidate_params)
                all_out.extend(out)

                if more_results is not None:
                    for key, value in more_results.items():
                        all_more_results[key].extend(value)

                nonlocal results
                results = self._format_results(
                    all_candidate_params, n_splits, all_out, lags, all_more_results
                )

                return results

        #run de evaluations
        self._run_search(evaluate_candidates)

        # multimetric is determined here because in the case of a callable
        # self.scoring the return type is only known after calling. If the
        first_test_score = all_out[0]["test_scores"]
        self.multimetric_ = isinstance(first_test_score, dict)

        # check refit_metric now for a callabe scorer that is multimetric
        if callable(self.scoring) and self.multimetric_:
            self._check_refit_for_multimetric(first_test_score)
            refit_metric = self.refit


        # For multi-metric evaluation, store the best_index_, best_params_ and
        # best_score_ iff refit is one of the scorer names
        # In single metric evaluation, refit_metric is "score"
        if self.refit or not self.multimetric_:
            self.best_index_ = self._select_best_index(
                self.refit, refit_metric, results
            )
            if not callable(self.refit):
                # With a non-custom callable, we can select the best score
                # based on the best index
                self.best_score_ = results[f"mean_test_{refit_metric}"][
                    self.best_index_
                ]
            self.best_params_ = results["params"][self.best_index_]

        if self.refit:
            # we clone again after setting params in case some
            # of the params are estimators as well.
            self.best_estimator_ = clone(
                clone(base_estimator).set_params(**self.best_params_)
            )
            refit_start_time = time.time()
            if y_train is not None:
                self.best_estimator_.fit(X, y_train, **fit_params)
            else:
                self.best_estimator_.fit(X, **fit_params)
            refit_end_time = time.time()
            self.refit_time_ = refit_end_time - refit_start_time

            if hasattr(self.best_estimator_, "feature_names_in_"):
                self.feature_names_in_ = self.best_estimator_.feature_names_in_

        # Store the only scorer not as a dict for single metric evaluation
        self.scorer_ = scorers

        self.cv_results_ = results
        self.n_splits_ = n_splits

        return self


    
    def _format_results(self, candidate_params, n_splits, out, lags, more_results=None):
            n_candidates = len(candidate_params)
            out = _aggregate_score_dicts(out) #check import

            results = dict(more_results or {})
            for key, val in results.items():
                # each value is a list (as per evaluate_candidate's convention)
                # we convert it to an array for consistency with the other keys
                results[key] = np.asarray(val)

            def _store(key_name, array, weights=None, splits=False, rank=False):
                """A small helper to store the scores/times to the cv_results_"""
                # When iterated first by splits, then by parameters
                # We want `array` to have `n_candidates` rows and `n_splits` cols.

                # Crear el array original
    
                if "y_pred" in key_name:
                # Cambiar la forma del array a (4, 222, 24)
                    # print(type(array))
                    # print(len(array))
                    # print(array)
                    array=np.array(array)
                    #reshaped_array = array.reshape(n_candidates, n_splits, self.cv.increment_size)
                    reshaped_array = array.reshape(n_candidates, n_splits, self.registers_per_day_format)

                    # Crear un array de objetos con listas en lugar de los valores individuales
                    array = np.empty((n_candidates, n_splits), dtype=object)

                    for i in range(n_candidates):
                        for j in range(n_splits):
                            array[i, j] = list(reshaped_array[i, j])
                else:
                    array = np.array(array, dtype=np.float64).reshape(n_candidates, n_splits)
                if splits:
                    for split_idx in range(n_splits):
                        # Uses closure to alter the results
                        results["split%d_%s" % (split_idx, key_name)] = array[:, split_idx]
                        
                try:
                    array_means = np.average(array, axis=1, weights=weights)
                    results["mean_%s" % key_name] = array_means
    
                    if key_name.startswith(("train_", "test_")) and np.any(
                        ~np.isfinite(array_means)
                    ):
                        warnings.warn(
                            f"One or more of the {key_name.split('_')[0]} scores "
                            f"are non-finite: {array_means}",
                            category=UserWarning,
                        )

                    # Weighted std is not directly available in numpy
                    array_stds = np.sqrt(
                        np.average(
                            (array - array_means[:, np.newaxis]) ** 2, axis=1, weights=weights
                        )
                    )
                    results["std_%s" % key_name] = array_stds
                except:
                    pass

                if rank:
                    # When the fit/scoring fails `array_means` contains NaNs, we
                    # will exclude them from the ranking process and consider them
                    # as tied with the worst performers.
                    if np.isnan(array_means).all():
                        # All fit/scoring routines failed.
                        rank_result = np.ones_like(array_means, dtype=np.int32)
                    else:
                        min_array_means = np.nanmin(array_means) - 1
                        array_means = np.nan_to_num(array_means, nan=min_array_means)
                        rank_result = rankdata(-array_means, method="min").astype(
                            np.int32, copy=False
                        )
                    results["rank_%s" % key_name] = rank_result

            _store("fit_time", out["fit_time"])
            _store("score_time", out["score_time"])
            #_store("y_preds", out["y_preds"])
            #_store("y_reals", out["y_reals"])
            # Use one MaskedArray and mask all the places where the param is not
            # applicable for that candidate. Use defaultdict as each candidate may
            # not contain all the params
            param_results = defaultdict(
                partial(
                    MaskedArray,
                    np.empty(
                        n_candidates,
                    ),
                    mask=True,
                    dtype=object,
                )
            )

            
            for cand_idx, params in enumerate(candidate_params):
                for name, value in params.items():
                    # An all masked empty array gets created for the key
                    # `"param_%s" % name` at the first occurrence of `name`.
                    # Setting the value at an index also unmasks that index
                    param_results["param_%s" % name][cand_idx] = value

            results.update(param_results)
            # Store a list of param dicts at the key 'params'
            results["params"] = candidate_params
            #results["y_preds"] = str(out["y_preds"])
            #results["y_reals"] = str(out["y_reals"])
            test_scores_dict = _normalize_score_results(out["test_scores"])
            if lags is not None:
                y_pred_scores_dict = _normalize_score_results(out["y_pred"])
            if self.return_train_score:
                train_scores_dict = _normalize_score_results(out["train_scores"])

            for scorer_name in test_scores_dict:
                # Computed the (weighted) mean and std for test scores alone
                _store(
                    "test_%s" % scorer_name,
                    test_scores_dict[scorer_name],
                    splits=True,
                    rank=True,
                    weights=None,
                )
                if self.return_train_score:
                    _store(
                        "train_%s" % scorer_name,
                        train_scores_dict[scorer_name],
                        splits=True,
                    )
                if lags is not None:
                    _store(
                    "y_pred_%s" % scorer_name,
                    y_pred_scores_dict[scorer_name],
                    splits=True,
                )


            return results



# Definición de una función _fit_and_score a modo de ejemplo (reemplazar por tu implementación)
def _fit_and_score(model, X, X_test, y_train, y_test, train, test, parameters, fit_params, split_progress, candidate_progress, scorer, verbose, is_id,
                   return_train_score=False, return_parameters=False, return_times=False, return_n_test_samples=False,
                   return_estimator=False, error_score=np.nan, X_prev=None,
                   lags=None, column_lags=None, column_rolled_lags=None, column_rolled_lags_initial=None, rolled_metrics=None, rolled_lags=None,):
    
    """
    This function is used in the ForecastBaseSearchCV class to fit and score the model, it is called in the _run_search function

    Parameters
    ----------
    model : estimator object 
        This is the estimator object that will be fitted and scored

    X : pd.DataFrame
        This is the training data

    X_test : pd.DataFrame
        This is the test data. test Data as argument could be None or a DataFrame
    
    y_train : pd.Series
        This is the training target

    y_test : pd.Series
        This is the test target. test target as argument could be None or a Series. 
    
    train : list
        This is the train index

    test : list
        This is the test index

    parameters : dict
        This is the dictionary of parameters that will be used to fit the model

    fit_params : dict
        This is the dictionary of parameters that will be used to fit the model

    split_progress : tuple
        This is a tuple that contains the current split and the total number of splits

    candidate_progress : tuple
        This is a tuple that contains the current candidate and the total number of candidates

    scorer : dict
        This is the dictionary of scorers that will be used to score the model. It comes from previous SCORER in _score.py 

    verbose : int
        This is the verbosity level
    
    is_id : bool
        This is a boolean that indicates if the model is being fitted for day-ahead > 1 or day-ahead = 1

    return_train_score : bool
        This is a boolean that indicates if the train score will be returned

    return_parameters : bool
        This is a boolean that indicates if the parameters will be returned

    return_times : bool
        This is a boolean that indicates if the times will be returned

    return_n_test_samples : bool
        This is a boolean that indicates if the number of test samples will be returned

    return_estimator : bool
        This is a boolean that indicates if the estimator will be returned

    error_score : numeric
        This is the numeric value that will be returned if an error occurs

    X_prev : pd.DataFrame
        This is an option for using different data for training and for testing.

    lags : list
        This is a list of lags that will be used to create the lagged features

    column_lags : list
        This is a list of columns that will be used to create the lagged features

    column_rolled_lags : list
        This is a list of columns that will be used to create the rolled lagged features

    column_rolled_lags_initial : list 
        This is a list of columns that will be used to create the initial rolled lagged features

    rolled_metrics : list
        This is a list of metrics that will be used to create the rolled lagged features

    rolled_lags : list
        This is a list of lags that will be used to create the rolled lagged features

    Returns
    -------
    result : dict
    """
    if not isinstance(error_score, numbers.Number) and error_score != "raise":
        raise ValueError(
            "error_score must be the string 'raise' or a numeric value. "
            "(Hint: if using 'raise', please make sure that it has been "
            "spelled correctly.)"
        )

    #VERBOSING AND PROGRESS
    progress_msg = ""
    if verbose > 2:
        if split_progress is not None:
            progress_msg = f" {split_progress[0]+1}/{split_progress[1]}"
        if candidate_progress and verbose > 9:
            progress_msg += f"; {candidate_progress[0]+1}/{candidate_progress[1]}"

    if verbose > 1:
        if parameters is None:
            params_msg = ""
        else:
            sorted_keys = sorted(parameters)  # Ensure deterministic o/p
            params_msg = ", ".join(f"{k}={parameters[k]}" for k in sorted_keys)
    if verbose > 9:
        start_msg = f"[CV{progress_msg}] START {params_msg}"
        print(f"{start_msg}{(80 - len(start_msg)) * '.'}")

    # Adjust length of sample weights
    fit_params = fit_params if fit_params is not None else {}
    fit_params = _check_fit_params(X, fit_params, train)

    #SETTING THE PARAMETERS FOR FITTING MODEL
    if parameters is not None:
        # clone after setting parameters in case any parameters
        # are estimators (like pipeline steps)
        # because pipeline doesn't clone steps in fit
        cloned_parameters = {}
        for k, v in parameters.items():
            cloned_parameters[k] = clone(v, safe=False)

        model = model.set_params(**cloned_parameters)
    #TIME START OF FITTING
    start_time = time.time()

    #TRY FITTING THE MODEL
    result = {}
    if X_prev is None:
        #SI EXISTE ID ES PARA DAY AHEAD > 1
        if is_id:
            X_train, y_train = _safe_split(model, X, y_train, train)
            X_test, y_test = _safe_split(model, X_test, y_test, test)
        #SI NO EXISTE ID ES PARA DAY AHEAD = 1
        else:
            #ESTA COPIA ES IMPORTANTE PARA HACER EL FORECAST THE DAY_AHEAD=1, sin hacer copia en el y_train y el X_train, falla. EN cambio para el DAY-AHEAD > 1 no hace falta
            y_train_=y_train.copy()
            X_=X.copy()
            X_train, y_train = _safe_split(model, X, y_train, train)
            X_test, y_test = _safe_split(model, X_, y_train_, test, train)
            
    #Si se utiliza X_prev
    else:
        if is_id:
            X_train, y_train = _safe_split(model, X, y_train, train)
            X_test, y_test = _safe_split(model, X_prev, y_test, test)
        else:
            y_train_=y_train.copy()
            X_=X.copy()
            X_prev_=X_prev.copy()
            X_train, y_train = _safe_split(model, X, y_train, train)
            X_test, y_test = _safe_split(model, X_prev_, y_train, test, train)

    #X_test, y_test = _safe_split(model, X_test, y_test, test,train)
    if 'id' in X_test.columns:
        X_test = X_test.drop(columns=['id'])
    elif 'id' in X_train.columns:
        X_train = X_train.drop(columns=['id'])
    try:
        
        model.fit(X_train, y_train,**fit_params)
        
    except Exception as e:
        # Note fit time as time until error
        fit_time = time.time() - start_time
        score_time = 0.0
        if error_score == "raise":
            raise
        elif isinstance(error_score, numbers.Number):
            if isinstance(scorer, dict):
                test_scores = {name: error_score for name in scorer}
                if return_train_score:
                    train_scores = test_scores.copy()
            else:
                test_scores = error_score
                if return_train_score:
                    train_scores = error_score
        result["fit_error"] = format_exc()

    else:
        result["fit_error"] = None
        #CURRENT TIME - START TIME IS THE FIT TIME
        fit_time = time.time() - start_time
        #compute prediction
        try:
            assert all(X_test.columns == X_train.columns), "X_test and X must have the same columns names"
            recursive_predictor=RecursivePredictor(X_train,  y_train, X_test, model, lags, column_lags, column_rolled_lags, column_rolled_lags_initial, rolled_metrics, rolled_lags)
            #recursive_predictor=RecursivePredictor(X.iloc[train],  y_train.iloc[train], X_test.iloc[test], model, lags, column_lags, column_rolled_lags, column_rolled_lags_initial, rolled_metrics, rolled_lags)
            y_pred_test=recursive_predictor.predict_rec()
            if return_train_score:
                y_pred_train=model.predict(X_train)
                #y_pred_train=model.predict(X.iloc[train])
        except (ValueError, TypeError, KeyError, IndexError) as e:
            assert all(X_test.columns == X_train.columns), "X_test and X must have the same columns names"
            raise Exception("An error occurred while predicting RecursivePredictor.") from e
        #y_pred=model.predict(X_test.iloc[test]) (Esto estaba antes de antes)

        try:
            #se pone negativo el scorer porque se ordena maximizando, el scorer procede del SCORER PROPIO
            test_scores = -scorer(y_test.values ,y_pred_test)
        except Exception as e:
            raise Exception(f"An error occurred while scoring{(y_test.values, y_pred_test, y_test.shape, y_pred_test.shape,scorer)}") from e
        #test_scores = scorer(y_test.iloc[test],y_pred_train, **fit_and_score_kwargs)
        if return_train_score:
            train_scores = -scorer(y_train.values, y_pred_train)
            #train_scores = scorer(y_train.iloc[train], y_pred_train, **fit_and_score_kwargs)
        score_time = time.time() - start_time - fit_time

    if verbose > 1:
        #SCORE TIME AND FIT TIME
        total_time = score_time + fit_time
        end_msg = f"[CV{progress_msg}] END "
        result_msg = params_msg + (";" if params_msg else "")
        if verbose > 2:
            if isinstance(test_scores, dict):
                for scorer_name in sorted(test_scores):
                    result_msg += f" {scorer_name}: ("
                    if return_train_score:
                        scorer_scores = train_scores[scorer_name]
                        result_msg += f"train={scorer_scores:.3f}, "
                    result_msg += f"test={test_scores[scorer_name]:.3f})"
            else:
                result_msg += ", score="
                if return_train_score:
                    result_msg += f"(train={train_scores:.3f}, test={test_scores:.3f})"
                else:
                    result_msg += f"{test_scores:.3f}"
        result_msg += f" total time={logger.short_format_time(total_time)}"

        # Right align the result_msg
        end_msg += "." * (80 - len(end_msg) - len(result_msg))
        end_msg += result_msg
        print(end_msg)

    #RETURNS
    result["test_scores"] = test_scores
    if return_train_score:
        result["train_scores"] = train_scores
    result["y_pred"] =np.array(y_pred_test.tolist())

    if return_n_test_samples:
        result["n_test_samples"] = _num_samples(X_test)
    if return_times:
        result["fit_time"] = fit_time
        result["score_time"] = score_time
    if return_parameters:
        result["parameters"] = parameters
    if return_estimator:
        result["estimator"] = model
    return result





class ForecastGridSearchCV(ForecastBaseSearchCV):
    """Exhaustive search over specified parameter values for an estimator.

    Important members are fit, predict.

    GridSearchCV implements a "fit" and a "score" method.
    It also implements "score_samples", "predict", "predict_proba",
    "decision_function", "transform" and "inverse_transform" if they are
    implemented in the estimator used.

    The parameters of the estimator used to apply these methods are optimized
    by cross-validated grid-search over a parameter grid.

    Read more in the :ref:`User Guide <grid_search>`.

    Parameters
    ----------
    estimator : estimator object
        This is assumed to implement the scikit-learn estimator interface.
        Either estimator needs to provide a ``score`` function,
        or ``scoring`` must be passed.

    param_grid : dict or list of dictionaries
        Dictionary with parameters names (`str`) as keys and lists of
        parameter settings to try as values, or a list of such
        dictionaries, in which case the grids spanned by each dictionary
        in the list are explored. This enables searching over any sequence
        of parameter settings.

    scoring : str, callable, list, tuple or dict, default=None
        Strategy to evaluate the performance of the cross-validated model on
        the test set.

        If `scoring` represents a single score, one can use:

        - a single string (see :ref:`scoring_parameter`);
        - a callable (see :ref:`scoring`) that returns a single value.

        If `scoring` represents multiple scores, one can use:

        - a list or tuple of unique strings;
        - a callable returning a dictionary where the keys are the metric
          names and the values are the metric scores;
        - a dictionary with metric names as keys and callables a values.

        See :ref:`multimetric_grid_search` for an example.

    n_jobs : int, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

        .. versionchanged:: v0.20
           `n_jobs` default changed from 1 to None

    refit : bool, str, or callable, default=True
        Refit an estimator using the best found parameters on the whole
        dataset.

        For multiple metric evaluation, this needs to be a `str` denoting the
        scorer that would be used to find the best parameters for refitting
        the estimator at the end.

        Where there are considerations other than maximum score in
        choosing a best estimator, ``refit`` can be set to a function which
        returns the selected ``best_index_`` given ``cv_results_``. In that
        case, the ``best_estimator_`` and ``best_params_`` will be set
        according to the returned ``best_index_`` while the ``best_score_``
        attribute will not be available.

        The refitted estimator is made available at the ``best_estimator_``
        attribute and permits using ``predict`` directly on this
        ``GridSearchCV`` instance.

        Also for multiple metric evaluation, the attributes ``best_index_``,
        ``best_score_`` and ``best_params_`` will only be available if
        ``refit`` is set and all of them will be determined w.r.t this specific
        scorer.

        See ``scoring`` parameter to know more about multiple metric
        evaluation.

        See :ref:`sphx_glr_auto_examples_model_selection_plot_grid_search_digits.py`
        to see how to design a custom selection strategy using a callable
        via `refit`.

        .. versionchanged:: 0.20
            Support for callable added.

    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

        - None, to use the default 5-fold cross validation,
        - integer, to specify the number of folds in a `(Stratified)KFold`,
        - :term:`CV splitter`,
        - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass, :class:`StratifiedKFold` is used. In all
        other cases, :class:`KFold` is used. These splitters are instantiated
        with `shuffle=False` so the splits will be the same across calls.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validation strategies that can be used here.

        .. versionchanged:: 0.22
            ``cv`` default value if None changed from 3-fold to 5-fold.

    verbose : int
        Controls the verbosity: the higher, the more messages.

        - >1 : the computation time for each fold and parameter candidate is
          displayed;
        - >2 : the score is also displayed;
        - >3 : the fold and candidate parameter indexes are also displayed
          together with the starting time of the computation.

    pre_dispatch : int, or str, default='2*n_jobs'
        Controls the number of jobs that get dispatched during parallel
        execution. Reducing this number can be useful to avoid an
        explosion of memory consumption when more jobs get dispatched
        than CPUs can process. This parameter can be:

            - None, in which case all the jobs are immediately
              created and spawned. Use this for lightweight and
              fast-running jobs, to avoid delays due to on-demand
              spawning of the jobs

            - An int, giving the exact number of total jobs that are
              spawned

            - A str, giving an expression as a function of n_jobs,
              as in '2*n_jobs'

    error_score : 'raise' or numeric, default=np.nan
        Value to assign to the score if an error occurs in estimator fitting.
        If set to 'raise', the error is raised. If a numeric value is given,
        FitFailedWarning is raised. This parameter does not affect the refit
        step, which will always raise the error.

    return_train_score : bool, default=False
        If ``False``, the ``cv_results_`` attribute will not include training
        scores.
        Computing training scores is used to get insights on how different
        parameter settings impact the overfitting/underfitting trade-off.
        However computing the scores on the training set can be computationally
        expensive and is not strictly required to select the parameters that
        yield the best generalization performance.

        .. versionadded:: 0.19

        .. versionchanged:: 0.21
            Default value was changed from ``True`` to ``False``

    Attributes
    ----------
    cv_results_ : dict of numpy (masked) ndarrays
        A dict with keys as column headers and values as columns, that can be
        imported into a pandas ``DataFrame``.

        For instance the below given table

        +------------+-----------+------------+-----------------+---+---------+
        |param_kernel|param_gamma|param_degree|split0_test_score|...|rank_t...|
        +============+===========+============+=================+===+=========+
        |  'poly'    |     --    |      2     |       0.80      |...|    2    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'poly'    |     --    |      3     |       0.70      |...|    4    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'rbf'     |     0.1   |     --     |       0.80      |...|    3    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'rbf'     |     0.2   |     --     |       0.93      |...|    1    |
        +------------+-----------+------------+-----------------+---+---------+

        will be represented by a ``cv_results_`` dict of::

            {
            'param_kernel': masked_array(data = ['poly', 'poly', 'rbf', 'rbf'],
                                         mask = [False False False False]...)
            'param_gamma': masked_array(data = [-- -- 0.1 0.2],
                                        mask = [ True  True False False]...),
            'param_degree': masked_array(data = [2.0 3.0 -- --],
                                         mask = [False False  True  True]...),
            'split0_test_score'  : [0.80, 0.70, 0.80, 0.93],
            'split1_test_score'  : [0.82, 0.50, 0.70, 0.78],
            'mean_test_score'    : [0.81, 0.60, 0.75, 0.85],
            'std_test_score'     : [0.01, 0.10, 0.05, 0.08],
            'rank_test_score'    : [2, 4, 3, 1],
            'split0_train_score' : [0.80, 0.92, 0.70, 0.93],
            'split1_train_score' : [0.82, 0.55, 0.70, 0.87],
            'mean_train_score'   : [0.81, 0.74, 0.70, 0.90],
            'std_train_score'    : [0.01, 0.19, 0.00, 0.03],
            'mean_fit_time'      : [0.73, 0.63, 0.43, 0.49],
            'std_fit_time'       : [0.01, 0.02, 0.01, 0.01],
            'mean_score_time'    : [0.01, 0.06, 0.04, 0.04],
            'std_score_time'     : [0.00, 0.00, 0.00, 0.01],
            'params'             : [{'kernel': 'poly', 'degree': 2}, ...],
            }

        NOTE

        The key ``'params'`` is used to store a list of parameter
        settings dicts for all the parameter candidates.

        The ``mean_fit_time``, ``std_fit_time``, ``mean_score_time`` and
        ``std_score_time`` are all in seconds.

        For multi-metric evaluation, the scores for all the scorers are
        available in the ``cv_results_`` dict at the keys ending with that
        scorer's name (``'_<scorer_name>'``) instead of ``'_score'`` shown
        above. ('split0_test_precision', 'mean_train_precision' etc.)

    best_estimator_ : estimator
        Estimator that was chosen by the search, i.e. estimator
        which gave highest score (or smallest loss if specified)
        on the left out data. Not available if ``refit=False``.

        See ``refit`` parameter for more information on allowed values.

    best_score_ : float
        Mean cross-validated score of the best_estimator

        For multi-metric evaluation, this is present only if ``refit`` is
        specified.

        This attribute is not available if ``refit`` is a function.

    best_params_ : dict
        Parameter setting that gave the best results on the hold out data.

        For multi-metric evaluation, this is present only if ``refit`` is
        specified.

    best_index_ : int
        The index (of the ``cv_results_`` arrays) which corresponds to the best
        candidate parameter setting.

        The dict at ``search.cv_results_['params'][search.best_index_]`` gives
        the parameter setting for the best model, that gives the highest
        mean score (``search.best_score_``).

        For multi-metric evaluation, this is present only if ``refit`` is
        specified.

    scorer_ : function or a dict
        Scorer function used on the held out data to choose the best
        parameters for the model.

        For multi-metric evaluation, this attribute holds the validated
        ``scoring`` dict which maps the scorer key to the scorer callable.

    n_splits_ : int
        The number of cross-validation splits (folds/iterations).

    refit_time_ : float
        Seconds used for refitting the best model on the whole dataset.

        This is present only if ``refit`` is not False.

        .. versionadded:: 0.20

    multimetric_ : bool
        Whether or not the scorers compute several metrics.

    classes_ : ndarray of shape (n_classes,)
        The classes labels. This is present only if ``refit`` is specified and
        the underlying estimator is a classifier.

    n_features_in_ : int
        Number of features seen during :term:`fit`. Only defined if
        `best_estimator_` is defined (see the documentation for the `refit`
        parameter for more details) and that `best_estimator_` exposes
        `n_features_in_` when fit.

        .. versionadded:: 0.24

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Only defined if
        `best_estimator_` is defined (see the documentation for the `refit`
        parameter for more details) and that `best_estimator_` exposes
        `feature_names_in_` when fit.

        .. versionadded:: 1.0

    See Also
    --------
    ParameterGrid : Generates all the combinations of a hyperparameter grid.
    train_test_split : Utility function to split the data into a development
        set usable for fitting a GridSearchCV instance and an evaluation set
        for its final evaluation.
    sklearn.metrics.make_scorer : Make a scorer from a performance metric or
        loss function.

    Notes
    -----
    The parameters selected are those that maximize the score of the left out
    data, unless an explicit score is passed in which case it is used instead.

    If `n_jobs` was set to a value higher than one, the data is copied for each
    point in the grid (and not `n_jobs` times). This is done for efficiency
    reasons if individual jobs take very little time, but may raise errors if
    the dataset is large and not enough memory is available.  A workaround in
    this case is to set `pre_dispatch`. Then, the memory is copied only
    `pre_dispatch` many times. A reasonable value for `pre_dispatch` is `2 *
    n_jobs`.

    Examples
    --------
    >>> from sklearn import svm, datasets
    >>> from sklearn.model_selection import GridSearchCV
    >>> iris = datasets.load_iris()
    >>> parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    >>> svc = svm.SVC()
    >>> clf = GridSearchCV(svc, parameters)
    >>> clf.fit(iris.data, iris.target)
    GridSearchCV(estimator=SVC(),
                 param_grid={'C': [1, 10], 'kernel': ('linear', 'rbf')})
    >>> sorted(clf.cv_results_.keys())
    ['mean_fit_time', 'mean_score_time', 'mean_test_score',...
     'param_C', 'param_kernel', 'params',...
     'rank_test_score', 'split0_test_score',...
     'split2_test_score', ...
     'std_fit_time', 'std_score_time', 'std_test_score']
    """

    _required_parameters = ["estimator", "param_grid"]

    def __init__(
        self,
        estimator,
        param_grid,
        *,
        scoring=None,
        n_jobs=None,
        refit=True,
        cv=None,
        verbose=0,
        pre_dispatch="2*n_jobs",
        error_score=np.nan,
        return_train_score=False,
    ):
        super().__init__(
            estimator=estimator,
            scoring=scoring,
            n_jobs=n_jobs,
            refit=refit,
            cv=cv,
            verbose=verbose,
            pre_dispatch=pre_dispatch,
            error_score=error_score,
            return_train_score=return_train_score,
        )
        self.param_grid = param_grid

    def _run_search(self, evaluate_candidates):
        """Search all candidates in param_grid"""
        evaluate_candidates(ParameterGrid(self.param_grid))




class ForecastRandomizedSearchCV(ForecastBaseSearchCV):
    """Randomized search on hyper parameters.

    RandomizedSearchCV implements a "fit" and a "score" method.
    It also implements "score_samples", "predict", "predict_proba",
    "decision_function", "transform" and "inverse_transform" if they are
    implemented in the estimator used.

    The parameters of the estimator used to apply these methods are optimized
    by cross-validated search over parameter settings.

    In contrast to GridSearchCV, not all parameter values are tried out, but
    rather a fixed number of parameter settings is sampled from the specified
    distributions. The number of parameter settings that are tried is
    given by n_iter.

    If all parameters are presented as a list,
    sampling without replacement is performed. If at least one parameter
    is given as a distribution, sampling with replacement is used.
    It is highly recommended to use continuous distributions for continuous
    parameters.

    Read more in the :ref:`User Guide <randomized_parameter_search>`.

    .. versionadded:: 0.14

    Parameters
    ----------
    estimator : estimator object
        An object of that type is instantiated for each grid point.
        This is assumed to implement the scikit-learn estimator interface.
        Either estimator needs to provide a ``score`` function,
        or ``scoring`` must be passed.

    param_distributions : dict or list of dicts
        Dictionary with parameters names (`str`) as keys and distributions
        or lists of parameters to try. Distributions must provide a ``rvs``
        method for sampling (such as those from scipy.stats.distributions).
        If a list is given, it is sampled uniformly.
        If a list of dicts is given, first a dict is sampled uniformly, and
        then a parameter is sampled using that dict as above.

    n_iter : int, default=10
        Number of parameter settings that are sampled. n_iter trades
        off runtime vs quality of the solution.

    scoring : str, callable, list, tuple or dict, default=None
        Strategy to evaluate the performance of the cross-validated model on
        the test set.

        If `scoring` represents a single score, one can use:

        - a single string (see :ref:`scoring_parameter`);
        - a callable (see :ref:`scoring`) that returns a single value.

        If `scoring` represents multiple scores, one can use:

        - a list or tuple of unique strings;
        - a callable returning a dictionary where the keys are the metric
          names and the values are the metric scores;
        - a dictionary with metric names as keys and callables a values.

        See :ref:`multimetric_grid_search` for an example.

        If None, the estimator's score method is used.

    n_jobs : int, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

        .. versionchanged:: v0.20
           `n_jobs` default changed from 1 to None

    refit : bool, str, or callable, default=True
        Refit an estimator using the best found parameters on the whole
        dataset.

        For multiple metric evaluation, this needs to be a `str` denoting the
        scorer that would be used to find the best parameters for refitting
        the estimator at the end.

        Where there are considerations other than maximum score in
        choosing a best estimator, ``refit`` can be set to a function which
        returns the selected ``best_index_`` given the ``cv_results``. In that
        case, the ``best_estimator_`` and ``best_params_`` will be set
        according to the returned ``best_index_`` while the ``best_score_``
        attribute will not be available.

        The refitted estimator is made available at the ``best_estimator_``
        attribute and permits using ``predict`` directly on this
        ``RandomizedSearchCV`` instance.

        Also for multiple metric evaluation, the attributes ``best_index_``,
        ``best_score_`` and ``best_params_`` will only be available if
        ``refit`` is set and all of them will be determined w.r.t this specific
        scorer.

        See ``scoring`` parameter to know more about multiple metric
        evaluation.

        .. versionchanged:: 0.20
            Support for callable added.

    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

        - None, to use the default 5-fold cross validation,
        - integer, to specify the number of folds in a `(Stratified)KFold`,
        - :term:`CV splitter`,
        - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass, :class:`StratifiedKFold` is used. In all
        other cases, :class:`KFold` is used. These splitters are instantiated
        with `shuffle=False` so the splits will be the same across calls.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validation strategies that can be used here.

        .. versionchanged:: 0.22
            ``cv`` default value if None changed from 3-fold to 5-fold.

    verbose : int
        Controls the verbosity: the higher, the more messages.

        - >1 : the computation time for each fold and parameter candidate is
          displayed;
        - >2 : the score is also displayed;
        - >3 : the fold and candidate parameter indexes are also displayed
          together with the starting time of the computation.

    pre_dispatch : int, or str, default='2*n_jobs'
        Controls the number of jobs that get dispatched during parallel
        execution. Reducing this number can be useful to avoid an
        explosion of memory consumption when more jobs get dispatched
        than CPUs can process. This parameter can be:

            - None, in which case all the jobs are immediately
              created and spawned. Use this for lightweight and
              fast-running jobs, to avoid delays due to on-demand
              spawning of the jobs

            - An int, giving the exact number of total jobs that are
              spawned

            - A str, giving an expression as a function of n_jobs,
              as in '2*n_jobs'

    random_state : int, RandomState instance or None, default=None
        Pseudo random number generator state used for random uniform sampling
        from lists of possible values instead of scipy.stats distributions.
        Pass an int for reproducible output across multiple
        function calls.
        See :term:`Glossary <random_state>`.

    error_score : 'raise' or numeric, default=np.nan
        Value to assign to the score if an error occurs in estimator fitting.
        If set to 'raise', the error is raised. If a numeric value is given,
        FitFailedWarning is raised. This parameter does not affect the refit
        step, which will always raise the error.

    return_train_score : bool, default=False
        If ``False``, the ``cv_results_`` attribute will not include training
        scores.
        Computing training scores is used to get insights on how different
        parameter settings impact the overfitting/underfitting trade-off.
        However computing the scores on the training set can be computationally
        expensive and is not strictly required to select the parameters that
        yield the best generalization performance.

        .. versionadded:: 0.19

        .. versionchanged:: 0.21
            Default value was changed from ``True`` to ``False``

    Attributes
    ----------
    cv_results_ : dict of numpy (masked) ndarrays
        A dict with keys as column headers and values as columns, that can be
        imported into a pandas ``DataFrame``.

        For instance the below given table

        +--------------+-------------+-------------------+---+---------------+
        | param_kernel | param_gamma | split0_test_score |...|rank_test_score|
        +==============+=============+===================+===+===============+
        |    'rbf'     |     0.1     |       0.80        |...|       1       |
        +--------------+-------------+-------------------+---+---------------+
        |    'rbf'     |     0.2     |       0.84        |...|       3       |
        +--------------+-------------+-------------------+---+---------------+
        |    'rbf'     |     0.3     |       0.70        |...|       2       |
        +--------------+-------------+-------------------+---+---------------+

        will be represented by a ``cv_results_`` dict of::

            {
            'param_kernel' : masked_array(data = ['rbf', 'rbf', 'rbf'],
                                          mask = False),
            'param_gamma'  : masked_array(data = [0.1 0.2 0.3], mask = False),
            'split0_test_score'  : [0.80, 0.84, 0.70],
            'split1_test_score'  : [0.82, 0.50, 0.70],
            'mean_test_score'    : [0.81, 0.67, 0.70],
            'std_test_score'     : [0.01, 0.24, 0.00],
            'rank_test_score'    : [1, 3, 2],
            'split0_train_score' : [0.80, 0.92, 0.70],
            'split1_train_score' : [0.82, 0.55, 0.70],
            'mean_train_score'   : [0.81, 0.74, 0.70],
            'std_train_score'    : [0.01, 0.19, 0.00],
            'mean_fit_time'      : [0.73, 0.63, 0.43],
            'std_fit_time'       : [0.01, 0.02, 0.01],
            'mean_score_time'    : [0.01, 0.06, 0.04],
            'std_score_time'     : [0.00, 0.00, 0.00],
            'params'             : [{'kernel' : 'rbf', 'gamma' : 0.1}, ...],
            }

        NOTE

        The key ``'params'`` is used to store a list of parameter
        settings dicts for all the parameter candidates.

        The ``mean_fit_time``, ``std_fit_time``, ``mean_score_time`` and
        ``std_score_time`` are all in seconds.

        For multi-metric evaluation, the scores for all the scorers are
        available in the ``cv_results_`` dict at the keys ending with that
        scorer's name (``'_<scorer_name>'``) instead of ``'_score'`` shown
        above. ('split0_test_precision', 'mean_train_precision' etc.)

    best_estimator_ : estimator
        Estimator that was chosen by the search, i.e. estimator
        which gave highest score (or smallest loss if specified)
        on the left out data. Not available if ``refit=False``.

        For multi-metric evaluation, this attribute is present only if
        ``refit`` is specified.

        See ``refit`` parameter for more information on allowed values.

    best_score_ : float
        Mean cross-validated score of the best_estimator.

        For multi-metric evaluation, this is not available if ``refit`` is
        ``False``. See ``refit`` parameter for more information.

        This attribute is not available if ``refit`` is a function.

    best_params_ : dict
        Parameter setting that gave the best results on the hold out data.

        For multi-metric evaluation, this is not available if ``refit`` is
        ``False``. See ``refit`` parameter for more information.

    best_index_ : int
        The index (of the ``cv_results_`` arrays) which corresponds to the best
        candidate parameter setting.

        The dict at ``search.cv_results_['params'][search.best_index_]`` gives
        the parameter setting for the best model, that gives the highest
        mean score (``search.best_score_``).

        For multi-metric evaluation, this is not available if ``refit`` is
        ``False``. See ``refit`` parameter for more information.

    scorer_ : function or a dict
        Scorer function used on the held out data to choose the best
        parameters for the model.

        For multi-metric evaluation, this attribute holds the validated
        ``scoring`` dict which maps the scorer key to the scorer callable.

    n_splits_ : int
        The number of cross-validation splits (folds/iterations).

    refit_time_ : float
        Seconds used for refitting the best model on the whole dataset.

        This is present only if ``refit`` is not False.

        .. versionadded:: 0.20

    multimetric_ : bool
        Whether or not the scorers compute several metrics.

    classes_ : ndarray of shape (n_classes,)
        The classes labels. This is present only if ``refit`` is specified and
        the underlying estimator is a classifier.

    n_features_in_ : int
        Number of features seen during :term:`fit`. Only defined if
        `best_estimator_` is defined (see the documentation for the `refit`
        parameter for more details) and that `best_estimator_` exposes
        `n_features_in_` when fit.

        .. versionadded:: 0.24

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Only defined if
        `best_estimator_` is defined (see the documentation for the `refit`
        parameter for more details) and that `best_estimator_` exposes
        `feature_names_in_` when fit.

        .. versionadded:: 1.0

    See Also
    --------
    GridSearchCV : Does exhaustive search over a grid of parameters.
    ParameterSampler : A generator over parameter settings, constructed from
        param_distributions.

    Notes
    -----
    The parameters selected are those that maximize the score of the held-out
    data, according to the scoring parameter.

    If `n_jobs` was set to a value higher than one, the data is copied for each
    parameter setting(and not `n_jobs` times). This is done for efficiency
    reasons if individual jobs take very little time, but may raise errors if
    the dataset is large and not enough memory is available.  A workaround in
    this case is to set `pre_dispatch`. Then, the memory is copied only
    `pre_dispatch` many times. A reasonable value for `pre_dispatch` is `2 *
    n_jobs`.

    Examples
    --------
    >>> from sklearn.datasets import load_iris
    >>> from sklearn.linear_model import LogisticRegression
    >>> from sklearn.model_selection import RandomizedSearchCV
    >>> from scipy.stats import uniform
    >>> iris = load_iris()
    >>> logistic = LogisticRegression(solver='saga', tol=1e-2, max_iter=200,
    ...                               random_state=0)
    >>> distributions = dict(C=uniform(loc=0, scale=4),
    ...                      penalty=['l2', 'l1'])
    >>> clf = RandomizedSearchCV(logistic, distributions, random_state=0)
    >>> search = clf.fit(iris.data, iris.target)
    >>> search.best_params_
    {'C': 2..., 'penalty': 'l1'}
    """

    _required_parameters = ["estimator", "param_distributions"]

    def __init__(
        self,
        estimator,
        param_distributions,
        *,
        n_iter=10,
        scoring=None,
        n_jobs=None,
        refit=True,
        cv=None,
        verbose=0,
        pre_dispatch="2*n_jobs",
        random_state=None,
        error_score=np.nan,
        return_train_score=False,
    ):
        self.param_distributions = param_distributions
        self.n_iter = n_iter
        self.random_state = random_state
        super().__init__(
            estimator=estimator,
            scoring=scoring,
            n_jobs=n_jobs,
            refit=refit,
            cv=cv,
            verbose=verbose,
            pre_dispatch=pre_dispatch,
            error_score=error_score,
            return_train_score=return_train_score,
        )

    def _run_search(self, evaluate_candidates):
        """Search n_iter candidates from param_distributions"""
        evaluate_candidates(
            ParameterSampler(
                self.param_distributions, self.n_iter, random_state=self.random_state
            )
        )


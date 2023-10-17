from sklearn import metrics as mtrs
from typing import Optional, Tuple, Union, Sequence, Callable, cast
from scipy.stats import norm, binom_test
from statsmodels.stats import contingency_tables as cont_tab
import matplotlib.pyplot as plt
import numpy as np
from sklearn.inspection import permutation_importance
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import seaborn as sns
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import math
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.pipeline import Pipeline
from scipy import stats
from sklearn.calibration import calibration_curve
import os
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    brier_score_loss,
    precision_score,
    recall_score,
    accuracy_score,
    balanced_accuracy_score,
    roc_auc_score,
)
from sklearn.metrics import (

    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
    r2_score,
    
    



)
#------------------------------------------FUNCTIONS AND UTILS FOR THE CLASSES--------------------------------------------------------
def namestr(obj,glob=globals()):
    """
    This function returns the name of an object variable as a string and is used in the Canalysis class and 
    analysis class to get the name of the model or regressor object.

    Parameters
    ----------
    obj : object
        Object to get the name of
    glob : dict, optional
        Dictionary of global variables, by default globals().
        Whereever is used globals() should be set in the workspace where the function is called.
        That is because globals() returns the global variables of the workspace where the function is called.
        and the names of vars are in the workspace where the function is called.
    """

    return [name for name in glob if glob[name] is obj and name not in ["_","__","___"]][0]


def y_probas_one_vs_others(y_proba)->list:
    """
    This function is used in the Canalysis class to calculate the y_probas for the one vs others method,
    when multiclass classification is used.

    Parameters
    ----------
    y_proba : numpy.ndarray
        Array of probabilities for each class
    
    Returns
    -------
    y_probas : list
    """
    y_probas=[]
    for i in range(y_proba.shape[1]):
        y_proba_2=np.zeros((y_proba.shape[0],2))
        y_proba_2[:,0]=y_proba[:,i]
        y_proba3=np.delete(y_proba, i, axis=1)
        y_proba_2[:,1]=y_proba3.sum(axis=1)
        y_probas.append(y_proba_2)
    return y_probas


def y_one_vs_others(y):
    """
    This function is used in the Canalysis class to calculate the y for the one vs others method,
    when multiclass classification is used. This generates one series for each class. Where for every class
    his name is mantained while the others are replaced by 'others'. That is how the one vs others method works.

    Parameters
    ----------
    y : pandas.core.series.Series
        Target variable of the model. 
    
    """
    cats=y.cat.categories
    replaced_y=[]
    for cat_ in cats:
        y_train_2=y.copy()
        y_train_2=y_train_2.astype(str)
        y_train_2[y_train_2 != str(cat_)] = 'others'
        y_train_2=y_train_2.astype('category')
        replaced_y.append(y_train_2)
        del y_train_2
    return replaced_y

def generar_subplots(num_plots, col=3, figsize=(12, 4)):
    """
    This function is used in the Canalysis class to generate subplots for the plots of the metrics.
    It is used for Roc-Auc, calibration curve, accuracy across thresholds.

    Parameters
    ----------
    num_plots : int
        Number of plots to generate
    col : int, optional
        Number of columns of the subplots, by default 3
    figsize : tuple, optional
        Size of the figure, by default (12, 4)
    Returns
    -------
    fig : matplotlib.figure.Figure

    """
    num_filas = (num_plots + 2) // col
    num_subplots_ultima_fila = num_plots - (num_filas-1)*col
    fig, axs = plt.subplots(num_filas, col, figsize=(figsize[0],figsize[1]*num_filas))
    for i in range(num_subplots_ultima_fila, col):
        axs[num_filas-1, i].remove()
    return fig, axs




def forecast_bias(y_true,y_pred):
    """ Forecast Bias (FB).

    Parameters
    ----------
    y_true : TimeSeries
        Actual values.
    y_pred : TimeSeries
        Predicted values

    Returns
    -------
    float
        The Forecast Bias (OPE)
    """
    y_true_sum, y_pred_sum = np.sum(y_true), np.sum(y_pred)
    return ((y_true_sum - y_pred_sum) / y_true_sum) * 100.

def root_mean_squared_error(y_true, y_pred, sample_weight=None, multioutput='uniform_average'):
    return np.sqrt(mean_squared_error(y_true, y_pred,sample_weight=sample_weight, multioutput=multioutput))


CLF_METRIC_FUNCS_SUMMARY = {
    'Confusion matrix': confusion_matrix,
    'Confusion matrix normalized': confusion_matrix,
    'Accuracy': accuracy_score,
    'Balanced accuracy': balanced_accuracy_score, 
    'Precision': precision_score,
    'Recall': recall_score,
    'F1-Score': f1_score,
    'ROC-AUC': roc_auc_score
}

# Metrics for the model comparison function
CLF_METRIC_FUNCS_COMPARISON = {
    'Accuracy':accuracy_score,
    'Balanced accuracy': balanced_accuracy_score, 
    'Brier Loss':brier_score_loss, 
    'Precision':precision_score, 
    'Recall':recall_score, 
    'F1-Score': f1_score, 
    'ROC-AUC': roc_auc_score
}

REG_METRIC_FUNCS_SUMMARY = {

    'RMSE': root_mean_squared_error,
    'MSE': mean_squared_error,
    'MAE': mean_absolute_error,
    'R2' : r2_score,
    'MAPE': mean_absolute_percentage_error,
    '% BIAS': forecast_bias,
}

#-------------------------------------------------------------------CLASSES---------------------------------------------------------------------
# Classification analysis class
class Canalysis:
    """
    Class to calculate classification metrics analysis.
    """
    def __init__(self,model, X_train, y_train, X_test, y_test, X_val=None, y_val=None):
        """
        Class to calculate classification metrics analysis.

        Parameters
        ----------
        model : sklearn model or list of models
            One Model to analyze: For one model all methods are available.
            List of models: Not all methods are supported. Supported methods are:
                - plot_roc_auc
                - plot_calibration_curve
                - plot_accuracy_across_thresholds
                -plot_histograms
        X_train : pandas.core.frame.DataFrame
            Training set of the model
        y_train : pandas.core.series.Series
            Target variable of the training set
        X_test : pandas.core.frame.DataFrame
            Test set of the model
        y_test : pandas.core.series.Series  
            Target variable of the test set
        *args : pandas.core.frame.DataFrame, pandas.core.series.Series
            Validation set of the model and target variable of the validation set
             
        """

        assert isinstance(X_train, pd.core.frame.DataFrame), 'X_train must be a pandas DataFrame'
        assert isinstance(y_train, pd.core.series.Series), 'y_train must be a pandas Series'
        assert isinstance(X_test, pd.core.frame.DataFrame), 'X_test must be a pandas DataFrame'
        assert isinstance(y_test, pd.core.series.Series), 'y_test must be a pandas Series'
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        if X_val is not None and y_val is not None:
            assert isinstance(X_val, pd.core.frame.DataFrame), 'X_val must be a pandas DataFrame'
            assert isinstance(y_val, pd.core.series.Series), 'y_val must be a pandas Series'
            self.X_val = X_val
            self.y_val = y_val



    def confusion_matrix(self, train_or_test_or_val:str, labels:list, sample_weight=None, normalize:bool=True):
        """
        Calculate confusion matrix and classification metrics.
        For Multiclass uses Macro average, for binary uses binary average.

        Parameters
        ----------
        train_or_test : str, optional
            Whether to calculate metrics on training or test set, by default 'train'
        labels : list
            List of labels. Vector of output categories
        sample_weight : list, optional
            Weights assigned to output samples in training process, by default None.
            ([int, int, ...])
        normalize : bool, optional
            normalize classification metrics when possible, by default True.

        Returns
        -------
        None
            Print confusion matrix and classification metrics
        """
        assert not isinstance(self.model, list), 'model must be a single model, not a list. Comparison of models is only supported for plot_roc_curve(), plot_calibration_curve() and plot_accuracy_across_thresholds()'
        assert isinstance(train_or_test_or_val, str), 'train_or_test must be a string'
        assert train_or_test_or_val.lower() in ['train', 'test','val'], 'train_or_test_or_val must be either "train" or "test or "val"'
        # Check if train or test
        if train_or_test_or_val.lower() == 'train':
            y_true = self.y_train
            y_pred = self.model.predict(self.X_train)
        elif train_or_test_or_val.lower() == 'test':
            y_true = self.y_test
            y_pred = self.model.predict(self.X_test)
        elif train_or_test_or_val.lower() == 'validation':
            #assert self.X_validation exists
            assert hasattr(self, 'X_val'), 'X_validation does not exist. Please provide X_val and y_val in the constructor'
            assert hasattr(self, 'y_val'), 'y_validation does not exist. Please provide X_val and y_val in the constructor'
            y_true = self.y_val
            y_pred = self.model.predict(self.X_val)

        # Calculate confusion matrix
        print('Confusion Matrix and Statistics\n\t   Prediction')
        # if labels is None:
        #     labels = list(y_true.unique())
        cm = mtrs.confusion_matrix(y_true, y_pred, labels=labels, sample_weight=sample_weight, normalize=None)
        cm_df = pd.DataFrame(cm, columns=labels)
        cm_df = pd.DataFrame(labels, columns=['Reference']).join(cm_df)
        print(cm_df.to_string(index=False))
        # Calculate metrics depending on type of classification, multiclass or binary
        try:   
            if len(y_true.unique()) == 2: # binary
                average = 'binary'
            else: # multiclass
                average = 'macro'     
        except:
            if len(np.unique(y_true)) == 2: # binary
                average = 'binary'
            else: # multiclass
                average = 'macro'
                
        # Calculate accuracy
        acc = mtrs.accuracy_score(y_true, y_pred, normalize=normalize, sample_weight=sample_weight)
        # Calculate No Information Rate
        combos = np.array(np.meshgrid(y_pred, y_true)).reshape(2, -1)
        noi = mtrs.accuracy_score(combos[0], combos[1], normalize=normalize, sample_weight=sample_weight)
        # Calculate p-value Acc > NIR
        res = binom_test(cm.diagonal().sum(), cm.sum(), max(pd.DataFrame(cm).apply(sum,axis=1)/cm.sum()),'greater')
        # Calculate P-value mcnemar test
        MCN_pvalue = cont_tab.mcnemar(cm).pvalue
        # Calculate Kappa
        Kappa = mtrs.cohen_kappa_score(y_true, y_pred, labels=labels, sample_weight=sample_weight)
        # Obtain positive label
        pos_label = labels[0]
        # Calculate precision
        precision = mtrs.precision_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate recall 
        recall = mtrs.recall_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate F1 score
        F_score = mtrs.f1_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate balanced accuracy
        Balanced_acc = mtrs.balanced_accuracy_score(y_true, y_pred, sample_weight=sample_weight)
        if average == 'binary': # binary
            # Calculate sensitivity, specificity et al
            TP = cm[1,1]
            TN = cm[0,0]
            FP = cm[0,1]
            FN = cm[1,0]
            sens = TP / (TP + FN)
            spec = TN / (TN + FP)
            Prevalence = (TP + FN) / (TP + TN + FP + FN)
            Detection_rate = TP / (TP + TN + FP + FN)
            Detection_prevalence = (TP + FP) /  (TP + TN + FP + FN)
            
            
            # print all the measures
            out_str = '\nAccuracy: ' + str(round(acc,3)) + '\n' + \
            'No Information Rate: ' + str(round(noi,3)) + '\n' + \
            'P-Value [Acc > NIR]: ' + str(round(res,3)) + '\n' + \
            'Kappa: ' + str(round(Kappa,3)) + '\n' + \
            'Mcnemar\'s Test P-Value: ' + str(round(MCN_pvalue,3)) + '\n' + \
            'Sensitivity: ' + str(round(sens,3)) + '\n' + \
            'Specificity: ' + str(round(spec,3)) + '\n' + \
            'Precision: ' + str(round(precision,3)) + '\n' + \
            'Recall: ' + str(round(recall,3)) + '\n' + \
            'Prevalence: ' + str(round(Prevalence,3)) + '\n' + \
            'Detection Rate: ' + str(round(Detection_rate,3)) + '\n' + \
            'Detection prevalence: ' + str(round(Detection_prevalence,3)) + '\n' + \
            'Balanced accuracy: ' + str(round(Balanced_acc,3)) + '\n' + \
            'F1 Score: ' + str(round(F_score,3)) + '\n' + \
            'Positive label: ' + str(pos_label) 
        else: # multiclass
                    # print all the measures
            out_str = '\n Overall Multiclass Score Using Macro' + '\n'  + \
            '\nAccuracy: ' + str(round(acc,3)) + '\n' + \
            'No Information Rate: ' + str(round(noi,3)) + '\n' + \
            'P-Value [Acc > NIR]: ' + str(round(res,3)) + '\n' + \
            'Kappa: ' + str(round(Kappa,3)) + '\n' + \
            'Mcnemar\'s Test P-Value: ' + str(round(MCN_pvalue,3)) + '\n' + \
            'Precision: ' + str(round(precision,3)) + '\n' + \
            'Recall: ' + str(round(recall,3)) + '\n' + \
            'Balanced accuracy: ' + str(round(Balanced_acc,3)) + '\n' + \
            'F1 Score: ' + str(round(F_score,3))  + '\n' + '\n' + \
            'Individual Class Scores' 
            
            # Calculate metrics for each class
            for i in range(len(labels)):
                labels_index = [i for i in range(len(labels))]
                labels_index.remove(i)
                # Calculate sensitivity, specificity et al
                TP = cm[i,i]
                cm2=np.delete(cm,i,0)
                TN = np.delete(cm2,i,1).sum()
                FP = np.delete(cm[:,i],i).sum()
                FN = np.delete(cm[i],i).sum()
                rec = TP / (TP + FN)
                spec_2 = TN / (TN + FP)
                prec= TP / (TP + FP)
                # print all the measures
                out_str += '\n' + 'Class: ' + str(labels[i]) + '\n' + \
                'Recall: ' + str(round(rec,3)) + '\n' + \
                'Specificity: ' + str(round(spec_2,3)) + '\n' + \
                'Precision: ' + str(round(prec,3)) + '\n' + \
                'F1 Score: ' + str(round((2*prec*rec)/(prec+rec),3)) + '\n' 
        print(out_str)

    #generate a permutation importance plot
    def permutation_importance(self,n_repeats:int=10,random_state=None,figsize=(12, 4)):
        """
        Generate a permutation importance plot. Is used
        to determine the importance of each feature in the model.

        Parameters
        ----------
        n_repeats : int, optional
            Number of times to permute a feature. The default is 10.

        random_state : int, optional
            Random state for the permutation. The default is None.

        figsize : tuple, optional
            Size of the figure. The default is (12, 4).

        Returns
        -------
        None.
            Plot is generated.
        """
        assert not isinstance(self.model, list), 'model must be a single model, not a list. Comparison of models is only supported for plot_roc_curve(), plot_calibration_curve() and plot_accuracy_across_thresholds()'
        assert n_repeats > 0, "n_repeats must be greater than 0 for permutation importance"
        assert random_state is None or isinstance(random_state, int), "random_state must be an integer or None"
        assert isinstance(figsize, tuple) and len(figsize) == 2, "figsize must be a tuple and figsize must be a tuple of length 2"
        importances = permutation_importance(self.model, 
                                    self.X_train, self.y_train,
                                    n_repeats=n_repeats,
                                    random_state=random_state)
        
        fig = plt.figure(2, figsize=figsize) 
        plt.bar(self.X_train.columns, importances.importances_mean, yerr=importances.importances_std,color='black', alpha=0.5)
        plt.xlabel('Feature')
        plt.ylabel('Permutation Importance')
        plt.xticks(rotation=90)
        plt.grid()
        plt.show()

    def get_metrics_summary(self, model_name:str, threshold=0.5, average:str='macro', save=False)-> pd.DataFrame:
        """
        Prints a summary of the metrics of a model for a given threshold
        and returns them in a DataFrame

        Parameters
        ------------
        model_name : str
            The name of the model to use
        threshold : float, optional
            The threshold to use to convert the probabilities to binary values, by default 0.5.
            If the model is a multiclass classifier, this parameter is ignored.

        Returns
        -----------
        pd.DataFrame
            A DataFrame with the metrics (accuracy, balanced accuracy, precision, recall, f1-score, roc-auc)

        Limitations
        -----------
        The data_dict dictionary should have the following structure, with the keys being the set names
        and the values being dictionaries with the keys 'data' and 'target' containing the data and target.

        data_dict = {
            'train': {
                'data': X_train,
                'target': y_train
            },
            'test': {
                'data': X_test,
                'target': y_test
            },
            'validation': {
                'data': X_val,
                'target': y_val
            }
        }

        """
        assert not isinstance(self.model, list), 'model must be a single model, not a list. Comparison of models is only supported for plot_roc_curve(), plot_calibration_curve() and plot_accuracy_across_thresholds()'
        assert isinstance(model_name,str), "model_name must be a string"

        data_dict={'Train': {'data': self.X_train,'target': self.y_train},
            'Test': {'data': self.X_test, 'target': self.y_test} }
        #add validation if it exists
        if hasattr(self, 'X_val') and hasattr(self, 'y_val'):
            data_dict['Val']={'data': self.X_val, 'target': self.y_val}

        if len(data_dict[[key for key in data_dict.keys()][0]]['target'].cat.categories) > 2:
            threshold = None

        # Get the predicted probabilities and predictions
        predictions_dict = {}
        for dataset_type in data_dict.keys():
            # Get the predicted probabilities
            if len(data_dict[[key for key in data_dict.keys()][0]]['target'].cat.categories) == 2:
                predictions_proba = self.model.predict_proba(data_dict[dataset_type]['data'])[:, 1]
                # Get the predictions and store them in a dictionary
                predictions = np.array([1 if i > threshold else 0 for i in predictions_proba])
                predictions_dict[dataset_type] = predictions
            else:
                #predictions_proba = model.predict_proba(data_dict[dataset_type]['data'])
                # Get the predictions and store them in a dictionary
                #predictions = np.array([np.argmax(i) for i in predictions_proba])
                predictions_dict[dataset_type] = self.model.predict(data_dict[dataset_type]['data'])

        # Calculate and print the metrics for each set
        metrics_dict = {
            'Model': model_name,
            'Threshold': threshold
        }
        if data_dict[[key for key in data_dict.keys()][0]]['target'].cat.categories.size > 2:
                print("Multiclass Problem with labels: ", data_dict[[key for key in data_dict.keys()][0]]['target'].cat.categories)
        else:
            print("Binary Problem with: ", data_dict[[key for key in data_dict.keys()][0]]['target'].cat.categories)
        # Iterate over the metrics
        for metric in CLF_METRIC_FUNCS_SUMMARY.keys():
            # Print a separator
            #if multi_class print ("multiclass")
            print('='*40)
            # Iterate over the sets
            for dataset_type, predictions in predictions_dict.items():
                # Calculate the metric for the set
                if metric == 'Confusion matrix':
                    # Calculate the confusion matrix 
                    metric_score = confusion_matrix(
                        data_dict[dataset_type]['target'], predictions
                    )
                    cm_df = pd.DataFrame(metric_score, columns=data_dict[dataset_type]['target'].cat.categories)
                    cm_df = pd.DataFrame(data_dict[dataset_type]['target'].cat.categories, columns=['Reference']).join(cm_df)
                    print(f'{metric} {dataset_type}: \n               Predicted \n{cm_df.to_string(index=False)}')
                elif metric == 'Confusion matrix normalized':
                    # Calculate the normalized confusion matrix and round the values
                    metric_score = confusion_matrix(
                        data_dict[dataset_type]['target'], predictions, normalize='true'
                    )
                    metric_score = np.round(metric_score, 3)
                    cm_df = pd.DataFrame(metric_score, columns=data_dict[dataset_type]['target'].cat.categories)
                    cm_df = pd.DataFrame(data_dict[dataset_type]['target'].cat.categories, columns=['Reference']).join(cm_df)
                    # Round it to 5 decimals
                    print(f'{metric} {dataset_type}: \n               Predicted \n{cm_df.to_string(index=False)}')
                else:
                    # Calculate the other metrics 
                    # For multiclass problems, calculate the metrics for each class
                    if data_dict[[key for key in data_dict.keys()][0]]['target'].cat.categories.size > 2: 
                        if metric in ['Precision', 'Recall', 'F1-Score']:
                    
                            metric_score = CLF_METRIC_FUNCS_SUMMARY[metric](
                                data_dict[dataset_type]['target'], predictions, 
                                average=average
                            )

                        elif metric == 'ROC-AUC': # For ROC-AUC uses OVR strategy, it could be OVO
                            predictions_proba = self.model.predict_proba(data_dict[dataset_type]['data'])
                            metric_score = CLF_METRIC_FUNCS_SUMMARY[metric](
                                data_dict[dataset_type]['target'], predictions_proba, multi_class='ovr',
                                average=average
                            )
                        else: # For accuracy and balanced accuracy
                            metric_score = CLF_METRIC_FUNCS_SUMMARY[metric](
                                data_dict[dataset_type]['target'], predictions
                            )
                            # Store the metric in the dictionary
                        metrics_dict[f'{metric} {dataset_type}'] = metric_score
                        print(f'{metric} {dataset_type}: {metric_score}')
    
                    #For binary problems
                    else: 
                        metric_score = CLF_METRIC_FUNCS_SUMMARY[metric](
                            data_dict[dataset_type]['target'], predictions
                        )
                        print(f'{metric} {dataset_type}: {metric_score}')
                        # Store the metric in the dictionary
                        metrics_dict[f'{metric} {dataset_type}'] = metric_score
        metrics_dict["N_Vars"]=len(self.model.feature_names_in_)
        metrics_dict["Vars"]=str(self.model.feature_names_in_)
        try:
            metrics_dict["best_params"] = str(self.model.best_params_)
        except:
            metrics_dict["best_params"] = None


        if save:
            # Save the metrics as a csv
            metrics_df = pd.DataFrame(metrics_dict, index=[0])
            metrics_df.to_csv(f'{model_name}_metrics_summary.csv', index=False)
            file_path = './models/train_test_summary_models.xlsx'
            if os.path.isfile(file_path):
                df_summary = pd.read_excel(file_path, sheet_name='Sheet2')
                df_summary = pd.concat([df_summary, df_best], axis=0, ignore_index=True)
                df_summary.to_excel(file_path, index=False, sheet_name='Sheet2')
            else:
                df_best.to_excel(file_path, index=False, sheet_name='Sheet2')
            if return_best_metrics:
                return df_best


        # Return the metrics as a DataFrame
        return pd.DataFrame(metrics_dict,index=[0])
    
    #--------------------------------------------Several Models ROC HISTOGRAMS CALIBRATED COMPARISON--------------------------------------------#
    def plot_roc_curve(self,train_or_test_or_val:str,glob,seek_binary=None,model_names=None, figsize=(14,4)):
        """
        Plots the ROC curve for the model or models in the class
        Parameters
        ----------
        train_or_test_or_val : str
            "train" or "test" or "val" to plot the ROC curve for the train, test or validation set
        glob : globals()
            The globals() of the notebook. It is used to get the model names.
        seek_binary : str, optional
            If the dataset is binary, you can specify the name of the class you want to plot the ROC curve for. The default is None.
        model_names : list, optional
            instead of using the glob, you can specify the model names you want to plot the ROC curve for. The default is None.
        figsize : tuple, optional
            The size of the figure. The default is (14,4).

        Returns
        -------
        None.
            plots the ROC curve for the model or models in the class
        """

        assert train_or_test_or_val.lower() in ["train","test","val"], f"train_or_test_or_val must be 'train' or 'test' or 'val' not {train_or_test_or_val}"

        sns.set()
        #Set the X and Y deppending on the train_or_test_or_val
        if train_or_test_or_val.lower()=="train":
            X=self.X_train
            Y=self.Y_train
        elif train_or_test_or_val.lower()=="test":
            X=self.X_test
            Y=self.Y_test
        elif train_or_test_or_val.lower()=="val":
            X=self.X_val
            Y=self.Y_val
        #If self model is not a list, turn it into a list for the for loop to work
        if type(self.model)!=list:
            fits=[self.model]
        else:
            fits=self.model
        #For Binary problems
        if len(Y.cat.categories)==2:
            assert seek_binary != None, f"You must specify the seek_binary category if the target has only 2 categories {Y.cat.categories}"
            seekcol=np.where(Y.cat.categories==seek_binary)[0][0]
            noseek=np.delete(Y.cat.categories,seekcol)[0]
            noseekcol=np.where(Y.cat.categories==noseek)[0][0]
        if len(Y.cat.categories)==2 or len(fits)==1: #Si solo hay una clase o solo hay un modelo
            figure, ax = plt.subplots(1, 1)
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate (Recall)')
            plt.plot([0,1],[0,1], 'k--') #Diagonal discontinua
            plt.xlim([-0.01,1.02])
            plt.ylim([-0.01,1.02])
            figure.set_figheight(figsize[1])
            figure.set_figwidth(figsize[0])  
            aucs_=pd.Series(dtype='float64')
        else: #Si hay mas de una clase o mas de un modelo
            num_graphs=len(fits)+len(Y.cat.categories) #Number of graphs to plot
            fig,axs=generar_subplots(num_graphs,figsize=figsize)
            #for each axs plot the xlabel and ylabel set the title the limits and the grid
            for i, ax in enumerate(axs.flat):
                ax.set_xlabel('False Positive Rate')
                ax.set_ylabel('True Positive Rate (Recall)')
                ax.plot([0,1],[0,1], 'k--') #Diagonal discontinua
                ax.set_xlim([-0.01,1.02])
                ax.set_ylim([-0.01,1.02])
                aucs_=pd.Series(dtype='float64')
                
        fit_plot=[] #List of the fits that have been plotted
        for k,fit in enumerate(fits):
            class_plot=[] #List of the classes that have been plotted
            Xvars=X[fit.feature_names_in_]  #Get the X variables used in the model
            if model_names is None: #If model_names is not specified, get the model name from the globals()
                model_name=namestr(fit,glob)
            else: #If model_names is specified, get the model name from the model_names list
                model_name=model_names[k]
            
            if len(Y.cat.categories)==2: #For binary classification
                y_proba=fit.predict_proba(Xvars)[:,seekcol]
                fpr,tpr,threshold=mtrs.roc_curve(Y.replace({seek_binary:1,noseek:0}),y_proba)
                auc_=round(mtrs.auc(fpr, tpr),3)
                aucs_[model_name]=auc_
                print('Area under the ROC curve of', model_name,':', auc_)
                plt.plot(fpr,tpr,linewidth=2,label=model_name)
            else: #For multiclass classification
                y_proba=fit.predict_proba(Xvars) #Get the probabilities
                y_all=y_one_vs_others(Y) #Get the y_all one vs others
                y_probas=y_probas_one_vs_others(y_proba) #Get the y_probas one vs others
                x=1
                if len(fits)==1: #If there is only one model
                    for i,class_ in enumerate(Y.cat.categories):
                        fpr , tpr , threshold = mtrs.roc_curve(y_all[i],y_probas[i][:,0],pos_label=str(class_))
                        auc_=round(mtrs.auc(fpr, tpr),3)
                        aucs_[model_name +'_class_'+str(class_)]=auc_
                        print('Area under the ROC curve of', model_name + '_class_'+str(class_),':', auc_)
                        plt.plot(fpr,tpr,linewidth=1.5,label=model_name + '_class_'+str(class_))
                        plt.legend(loc='lower right')
                else: #If there are more than one model and multiclass
                    
                    for i, ax in enumerate(axs.flat):
                        if x==0:
                            break
                        for j,class_ in enumerate(Y.cat.categories):
                            if j not in class_plot: #for classes, each class in a different graph
                                fpr , tpr , threshold = mtrs.roc_curve(y_all[j],y_probas[j][:,0],pos_label=str(class_))
                                auc_=round(mtrs.auc(fpr, tpr),3)
                                aucs_[model_name+'_class_'+str(class_)]=auc_
                                ax.plot(fpr,tpr,linewidth=1.5,label=model_name+'_class_'+str(class_))
                                #ax.legend(loc='lower right')
                                ax.title.set_text(f"Class {class_}")
                                plt.tight_layout()
                                class_plot.append(j)
                                print('Area under the ROC curve of', model_name+'_class_'+str(class_),':', auc_)
                                break

                            if i>len(Y.cat.categories)-1: #for the fits, all the classes in the same graph
                                if i not in fit_plot:
                                    fpr , tpr , threshold = mtrs.roc_curve(y_all[j],y_probas[j][:,0],pos_label=str(class_))
                                    auc_=round(mtrs.auc(fpr, tpr),3)
                                    aucs_[model_name+'_'+str(class_)]=auc_
                                    ax.plot(fpr,tpr,linewidth=1.5,label=model_name+'_class_'+str(class_))
                                    ax.title.set_text(f"Model {model_name}")
                                    plt.tight_layout()
                                    if j==len(Y.cat.categories)-1:
                                        fit_plot.append(i)
                                        x=0
                                        break
                        ax.legend(loc='lower right')
            del class_plot #Delete the class_plot list that is marker of the classes plotted per model, for manage the draw of the subplots.
        if model_names is None: #For the title
            plt.suptitle(f'ROC {[namestr(fit,glob) for fit in fits]}')
        else: #For the title
            plt.suptitle(f'ROC {model_names}')
        plt.tight_layout()
        #print the unique values of auc
        print("The Best Area Under the Curve is: ",aucs_.sort_values(ascending=False).index[0] ,aucs_.sort_values(ascending=False)[0])

    #CALIBRATED CURVES
    def plot_calibrated_curve(self,train_or_test_or_val,glob,n_bins=10, seek_binary=None,model_names=None, figsize=(14,4)):
        sns.set()
        assert train_or_test_or_val.lower() in ["train","test","val"], f"train_or_test_or_val must be 'train' or 'test' or 'val' not {train_or_test_or_val}"

        #Set the X and Y deppending on the train_or_test_or_val
        if train_or_test_or_val.lower()=="train":
            X=self.X_train
            Y=self.Y_train
        elif train_or_test_or_val.lower()=="test":
            X=self.X_test
            Y=self.Y_test
        elif train_or_test_or_val.lower()=="val":
            X=self.X_val
            Y=self.Y_val
        #If self model is not a list, turn it into a list for the for loop to work
        if type(self.model)!=list:
            fits=[self.model]
        else:
            fits=self.model
        #For binary classification
        if len(Y.cat.categories)==2:
            assert seek_binary is not None , f"You must specify the seek_binary category if the target has only 2 categories {Y.cat.categories}"
            seekcol=np.where(Y.cat.categories==seek_binary)[0][0]
            noseek=np.delete(Y.cat.categories,seekcol)[0]
            noseekcol=np.where(Y.cat.categories==noseek)[0][0]
        if len(Y.cat.categories)==2 or len(fits)==1: #Si solo hay una clase o solo hay un modelo
            figure, ax = plt.subplots(1, 1)
            plt.xlabel('Predicted probability')
            plt.ylabel('True probability in each bin')
            plt.plot([0,1],[0,1], 'k--') #Diagonal discontinua
            plt.xlim([-0.01,1.02])
            plt.ylim([-0.01,1.02])
            figure.set_figheight(figsize[1])
            figure.set_figwidth(figsize[0])  
            aucs_=pd.Series(dtype='float64')
        else: #Si hay mas de una clase o mas de un modelo
            num_graphs=len(fits)+len(Y.cat.categories)
            fig,axs=generar_subplots(num_graphs,figsize=figsize)
            #for each axs plot the xlabel and ylabel set the title the limits and the grid
            for i, ax in enumerate(axs.flat):
                ax.set_xlabel('Predicted probability')
                ax.set_ylabel('True probability in each bin')
                ax.plot([0,1],[0,1], 'k--') #Diagonal discontinua
                ax.set_xlim([-0.01,1.02])
                ax.set_ylim([-0.01,1.02])
                aucs_=pd.Series(dtype='float64')
                
        fit_plot=[] #List of the fits plotted is used to implement the log of the fits plotted over the classes
        for k,fit in enumerate(fits):
            class_plot=[]
            Xvars=X[fit.feature_names_in_] 
            #The model name used for label and titles is the name 
            if model_names is None: 
                model_name=namestr(fit,glob)
            else:
                model_name=model_names[k]
            if len(Y.cat.categories)==2: #For binary classification
                y_proba=fit.predict_proba(Xvars)[:,seekcol]
                fpr,tpr,threshold=mtrs.roc_curve(Y.replace({seek_binary:1,noseek:0}),y_proba)
                point_y,point_x=calibration_curve(y_all[i], y_probas[i][:,0], n_bins=n_bins, pos_label=str(class_))
                plt.plot(fpr,tpr,linewidth=2,label=model_name)
            else: #For multiclass classification
                y_proba=fit.predict_proba(Xvars) #Get the probabilities
                y_all=y_one_vs_others(Y) #Get the y_all one vs others
                y_probas=y_probas_one_vs_others(y_proba) #Get the y_probas one vs others
                x=1 #This is a break marker for the for loop used in this logic. Intialization is 1 to enter the for loop
                if len(fits)==1: #If there is only one model
                    for i,class_ in enumerate(Y.cat.categories):
                        point_y,point_x=calibration_curve(y_all[i], y_probas[i][:,0], n_bins=n_bins, pos_label=str(class_))
                        plt.plot(point_x,point_y,marker="o",label=model_name+'_class_'+str(class_))
                        plt.legend(loc='lower right')
                else: #If there are more than one model and multiclass
                    #plot the roc for each axs[i,j] pass to flat
                    for i, ax in enumerate(axs.flat):
                        if x==0: #This is a mrker to break the for loop used in this logic
                            break
                        for j,class_ in enumerate(Y.cat.categories):
                            if j not in class_plot: #for classes, each class in a different graph
                                point_y,point_x=calibration_curve(y_all[j], y_probas[j][:,0], n_bins=n_bins, pos_label=str(class_))
                                ax.plot(point_x,point_y,marker="o",label=model_name+'_class_'+str(class_))
                                ax.legend(loc='lower right')
                                ax.title.set_text(f"Class {class_}")
                                plt.tight_layout()
                                class_plot.append(j)
                                break
                            if i>len(Y.cat.categories)-1: #for the fits, all the classes in the same graph
                                if i not in fit_plot:
                                    point_y,point_x=calibration_curve(y_all[j], y_probas[j][:,0], n_bins=n_bins, pos_label=str(class_))
                                    ax.plot(point_x,point_y,marker="o",label=model_name+'_class_'+str(class_))
                                    #show legend out of the plot
                                    if  len(Y.cat.categories)>6: #Si las clases son mas de 6, la leyenda se muestra fuera del grafico.
                                        ax.legend(loc='best', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
                                    else:
                                        ax.legend(loc='lower right')
                                    ax.title.set_text(f"Model {model_name}")
                                    plt.tight_layout()
                                    if j==len(Y.cat.categories)-1: #This is a marker to break the for loop used in this logic
                                        fit_plot.append(i)
                                        x=0
                                        break           
            del class_plot
        if model_names is None: #The suptitle is the name of the models automatically given by the namestr function
            plt.suptitle(f'Calibrated Plots {[namestr(fit,glob) for fit in fits]}')
        else: #The suptitle is the name of the models given by the user
            plt.suptitle(f'Calibrated Plots {model_names}')
        plt.tight_layout()


    #HISTOGRAM PLOTS
    def plot_histograms(self,train_or_test_or_val:str,glob,model_names=None,seek_binary=None):
        sns.set()
        assert train_or_test_or_val.lower() in ["train","test","val"], f"train_or_test_or_val must be 'train' or 'test' or 'val' not {train_or_test_or_val}"
        #Set the X and Y deppending on the train_or_test_or_val
        if train_or_test_or_val.lower()=="train":
            X=self.X_train
            Y=self.Y_train
        elif train_or_test_or_val.lower()=="test":
            X=self.X_test
            Y=self.Y_test
        elif train_or_test_or_val.lower()=="val":
            X=self.X_val
            Y=self.Y_val
        #If self model is not a list, turn it into a list for the for loop to work
        if type(self.model)!=list:
            fits=[self.model]
        else:
            fits=self.model
        #If model_names is None, get the model names automatically, if not, get the model names from the user
        if model_names is None:
            model_name=[namestr(fit,glob) for fit in fits]
        else:
            model_name=model_names
        #Set the ssek positive class For binary classification
        if len(Y.cat.categories)==2:
            assert seek_binary in Y.cat.categories, f"The selected seek category {seek_binary} is not an option, the options are: {Y.cat.categories}"
            seekcol=np.where(Y.cat.categories==seek_binary)[0][0]
            noseek=np.delete(Y.cat.categories,seekcol)[0]
            noseekcol=np.where(Y.cat.categories==noseek)[0][0]
            print(f"Probability of class {str(seek_binary)}")
        #Set the name of the output to be plotted in the graph
        try:
            output_name=Y.name
        except:
            outputname="target"
        # For binary
        if len(Y.cat.categories)==2: 
            for k,fit in enumerate(fits):
                Xvars=X[fit.feature_names_in_]
                df = pd.DataFrame(Y)
                df['prob_est'] = fit.predict_proba(Xvars)[:,seekcol]
                sns.set(style ="ticks")
                d = {'color': ['r', 'b']}
                g = sns.FacetGrid(df,  col=output_name, hue=output_name,hue_kws=d, margin_titles=True)
                bins = np.linspace(0, 1, 10)
                g.map(plt.hist, "prob_est", bins=bins)
                plt.subplots_adjust(top=0.8)
                plt.suptitle(model_name[k])
        #For multiclass
        else:
            for i,class_ in enumerate(Y.cat.categories): 
                for k,fit in enumerate(fits):
                    Xvars=X[fit.feature_names_in_]
                    y_proba=fit.predict_proba(Xvars)
                    y_probas=y_probas_one_vs_others(y_proba)
                    y_all=y_one_vs_others(Y)
                    df = pd.DataFrame(y_all[i])
                    df['prob_est']= y_probas[i][:,1]
                    d = {'color': ['r', 'b']}
                    g = sns.FacetGrid(df,  col=output_name, hue=output_name,hue_kws=d, margin_titles=True)
                    bins = np.linspace(0, 1, 10)
                    g.map(plt.hist, "prob_est", bins=bins)
                    plt.subplots_adjust(top=0.8)
                    plt.suptitle(model_name[k]+'_class_'+str(class_))


    def plot_accuracy_cutoff(self,train_or_test_or_val,glob,seek_binary=None,model_names=None, figsize=(14,4)):
        sns.set()
        assert train_or_test_or_val.lower() in ["train","test","val"], f"train_or_test_or_val must be 'train' or 'test' or 'val' not {train_or_test_or_val}"
        #Set the X and Y deppending on the train_or_test_or_val
        if train_or_test_or_val.lower()=="train":
            X=self.X_train
            Y=self.y_train
        elif train_or_test_or_val.lower()=="test":
            X=self.X_test
            Y=self.y_test
        elif train_or_test_or_val.lower()=="val":
            X=self.X_val
            Y=self.y_val
        #If self model is not a list, turn it into a list for the for loop to work
        if type(self.model)!=list:
            fits=[self.model]
        else:
            fits=self.model
        if len(Y.cat.categories)==2:
            assert seek_binary != None, f"You must specify the seek_binary category if the target has only 2 categories {Y.cat.categories}"
            seekcol=np.where(Y.cat.categories==seek_binary)[0][0]
            noseek=np.delete(Y.cat.categories,seekcol)[0]
            noseekcol=np.where(Y.cat.categories==noseek)[0][0]
        if len(Y.cat.categories)==2 or len(fits)==1: #Si solo hay una clase o solo hay un modelo
            figure, ax = plt.subplots(1, 1)
            plt.xlabel("Thresholds")
            plt.ylabel("Acurracy Scores")
            plt.xlim([-0.01,1.02])
            plt.ylim([-0.01,1.02])
            figure.set_figheight(figsize[1])
            figure.set_figwidth(figsize[0])  
        else: #Si hay mas de una clase o mas de un modelo
            num_graphs=len(fits)+len(Y.cat.categories)
            fig,axs=generar_subplots(num_graphs,figsize=figsize)
            #for each axs plot the xlabel and ylabel set the title the limits and the grid
            for i, ax in enumerate(axs.flat):
                ax.set_xlabel("Thresholds")
                ax.set_ylabel("Acurracy Scores")
                ax.set_xlim([-0.01,1.02])
                ax.set_ylim([-0.01,1.02])   
        fit_plot=[]
        for k, fit in enumerate(fits):
            if model_names is None:
                model_name=namestr(fit,glob)
            else:
                model_name=model_names[k]
            class_plot=[]
            Xvars=X[fit.feature_names_in_]  
            if len(Y.cat.categories)==2: #For binary classification
                y_proba=fit.predict_proba(Xvars)[:,seekcol]
                fpr,tpr,threshold=mtrs.roc_curve(Y.replace({seek_binary:1,noseek:0}),y_proba)
                y_true = Y == 1
                accuracy_scores = []
                for thresh in thresholds:
                    accuracy_scores.append(mtrs.accuracy_score(y_true, [1 if m > thresh else 0 for m in fit.predict_proba(Xvars)[:,seekcol]]))
                accuracy_scores = np.array(accuracy_scores)
                plt.plot(thresholds, accuracy_scores,label=model_name)
            else: #For multiclass classification #OVR IS APPLIED
                y_proba=fit.predict_proba(Xvars)
                y_all=y_one_vs_others(Y)
                y_probas=y_probas_one_vs_others(y_proba)
                x=1
                if len(fits)==1: #If there is only one model
                    for i,class_ in enumerate(Y.cat.categories):
                        fpr , tpr , threshold = mtrs.roc_curve(y_all[i],y_probas[i][:,0],pos_label=str(class_))
                        y_true = y_all[j] == class_
                        accuracy_scores = []
                        for thresh in thresholds:
                            accuracy_scores.append(mtrs.accuracy_score(y_true, [1 if m > thresh else 0 for m in y_probas[j][:,0]]))
                        accuracy_scores = np.array(accuracy_scores)
                        plt.plot(thresholds, accuracy_scores,label=model_name+'_class_'+str(class_))
                        plt.legend(loc='lower right')
                else: #If there are more than one model and multiclass
                    for i, ax in enumerate(axs.flat):
                        if x==0:
                            break
                        for j,class_ in enumerate(Y.cat.categories):
                            if j not in class_plot: #for classes, each class in a different graph
                                fpr, tpr, thresholds = mtrs.roc_curve(y_all[j], y_probas[j][:,0],pos_label=str(class_))
                                y_true = y_all[j] == class_
                                accuracy_scores = []
                                for thresh in thresholds:
                                        accuracy_scores.append(mtrs.accuracy_score(y_true, [1 if m > thresh else 0 for m in y_probas[j][:,0]]))
                                accuracy_scores = np.array(accuracy_scores)
                                ax.plot(thresholds, accuracy_scores,label=model_name+'_class_'+str(class_))
                                ax.legend(loc='lower right')
                                ax.title.set_text(f"Class {class_}")
                                plt.tight_layout()
                                class_plot.append(j)
                                break
                            if i>len(Y.cat.categories)-1: #for the fits, all the classes in the same graph
                                if i not in fit_plot:
                                    fpr, tpr, thresholds = mtrs.roc_curve(y_all[j], y_probas[j][:,0], pos_label=str(class_))
                                    y_true = y_all[j] == class_
                                    accuracy_scores = []
                                    for thresh in thresholds:
                                            accuracy_scores.append(mtrs.accuracy_score(y_true, [1 if m > thresh else 0 for m in y_probas[j][:,0]]))

                                    accuracy_scores = np.array(accuracy_scores)

                                    ax.plot(thresholds, accuracy_scores,label=model_name+'_class_'+str(class_))
                                    ax.legend(loc='lower right')
                                    ax.title.set_text(f"Model {model_name}")
                                    plt.tight_layout()
                                    if j==len(Y.cat.categories)-1:
                                        fit_plot.append(i)
                                        x=0
                                        break
                        ax.legend(loc='lower right')
            del class_plot
        if model_names is None:
            plt.suptitle(f'Accuracy across possible Thresholds {[namestr(fit,glob) for fit in fits]}')
        else:
            plt.suptitle(f'Accuracy across possible Thresholds {model_names}')
        plt.tight_layout()




class Ranalysis:
    """
    Class to perform analysis of regression models.
    """
    def __init__(self,model_name:str, model, X_train, y_train, X_test = None, y_test = None,X_val=None, y_val=None, X_prev = None):
        self.model_name = model_name
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        if X_test is not None and y_test is not None:
            assert isinstance(X_test, pd.core.frame.DataFrame), 'X_test must be a pandas DataFrame'
            assert isinstance(y_test, pd.core.series.Series), 'y_test must be a pandas Series'
            self.X_test = X_test
            self.y_test = y_test
        if X_val is not None and y_val is not None:
            assert isinstance(X_val, pd.core.frame.DataFrame), 'X_val must be a pandas DataFrame'
            assert isinstance(y_val, pd.core.series.Series), 'y_val must be a pandas Series'
            self.X_val = X_val
            self.y_val = y_val
        if X_prev is not None:
            assert isinstance(X_prev,pd.core.frame.DataFrame)
            self.X_prev = X_prev
    #residual analysis of the models
    def residual_analysis(self, train_or_test_or_val:str, remove_vars:list=None, figsize=(20, 10), bins:int=30, smooth_order:int=5, save:bool=True):
        """
        Generate a residual analysis plot. Is used to determine if the model is overfitting or underfitting.
        Studying the variance and the bias of the residuals.

        Parameters
        ----------
        train_or_test : str
            Whether to use the training or test data.

        figsize : tuple, optional
            Size of the figure. The default is (1400, 1000).
        
        bins : int, optional
            Number of bins for the histogram. The default is 30.
        
        smooth_order : int, optional
            Order of the smoothing polynomial. The default is 5.
        
        Returns
        -------
        None.
            Plot is generated.
        """
        sns.set()
        #assertions
        assert train_or_test_or_val.lower() in ['train', 'test','val'], "train_or_test must be either 'train' or 'test'"
        assert isinstance(figsize, tuple) and len(figsize) == 2, "figsize must be a tuple and figsize must be a tuple of length 2"
        assert isinstance(bins, int) and bins > 0, "bins must be an integer greater than 0"
        assert isinstance(smooth_order, int) and smooth_order > 0, "smooth_order must be an integer greater than 0"
        # Create the residuals
        assert train_or_test_or_val.lower() in ['train','test','val'], "train_or_test must be 'train', 'test' or 'val'"
        assert remove_vars is None or isinstance(remove_vars, list), "remove_vars must be a list"
        df=pd.DataFrame(columns=['y_true', 'y_pred'])
        if train_or_test_or_val.lower() == 'train': # If train is selected
            y_pred = self.model.predict( self.X_train)
            y_true = self.y_train
            if isinstance(remove_vars,list):
                columns_var = self.X_train.columns.to_list()
                for var in remove_vars:
                    columns_var.remove(var)
                df[columns_var] = self.X_train.drop(columns=remove_vars)
            else:
                df[self.X_train.columns] = self.X_train
        elif train_or_test_or_val.lower() == 'test':
            assert hasattr(self, 'X_test'), 'X_test does not exist. Please provide X_test and y_test in the constructor'
            assert hasattr(self, 'y_test'), 'y_test does not exist. Please provide X_test and y_test in the constructor'
            y_pred = self.model.predict( self.X_test)
            y_true =  self.y_test
            if isinstance(remove_vars,list):
                columns_var = self.X_test.columns.to_list()
                for var in remove_vars:
                    columns_var.remove(var)
                df[columns_var] = self.X_test.drop(columns=remove_vars)
            else:
                df[self.X_test.columns] = self.X_test
        elif  train_or_test_or_val.lower() == 'val':
            assert hasattr(self, 'X_val'), 'X_validation does not exist. Please provide X_val and y_val in the constructor'
            assert hasattr(self, 'y_val'), 'y_validation does not exist. Please provide X_val and y_val in the constructor'
            y_pred = self.model.predict(self.X_val)
            y_true =  self.y_val
            if isinstance(remove_vars,list):
                columns_var = self.X_val.columns.to_list()
                for var in remove_vars:
                    columns_var.remove(var)
                df[columns_var] = self.X_val.drop(columns=remove_vars)
            else:
                df[self.X_test.columns] = self.X_val
        df['y_true'] = y_true
        df['y_pred'] = y_pred
        df['residuals'] = df['y_true'] - df['y_pred']
        out_num = np.where(df.columns.values == 'residuals')[0]
        nplots = df.shape[1]
        # Create subplots
        fig, axs = plt.subplots(int(np.floor(np.sqrt(nplots))+1), int(np.ceil(np.sqrt(nplots))), figsize=figsize)
        fig.tight_layout(pad=4.0)

        input_num = 0
        for ax in axs.ravel():
            if input_num < nplots:
                # Create plots
                if input_num == out_num:
                    df['residuals'].plot.hist(bins=bins, ax=ax)
                    ax.set_title('Histogram of residuals')
                else:
                    if df.iloc[:,input_num].dtype.name == 'category':
                        sns.boxplot(x=df.columns.values.tolist()[input_num], y='residuals', data=df, ax=ax)
                        ax.set_title(df.columns.values.tolist()[input_num] + ' vs ' + 'residuals')
                    else:
                        sns.regplot(x=df.columns.values.tolist()[input_num], y='residuals', data=df, ax=ax, order=smooth_order, ci=None, line_kws={'color':'navy'})
                        ax.set_title(df.columns.values.tolist()[input_num] + ' vs ' + 'residuals')

                input_num += 1
            else:
                ax.axis('off')
        plt.suptitle(self.model_name + train_or_test_or_val.capitalize() + ' Residual Analysis', fontsize=18)
        plt.show()
        self.fig_residual_analysis = fig
        if save:
            if not os.path.exists(f'./models/{self.model_name}'):
                os.makedirs(f'./models/{self.model_name}')
            fig.savefig(f'./models/{self.model_name}/residual_analysis_{train_or_test_or_val.lower()}.png')



    def summaryLinReg(self, use_old:bool= True):
        """
        Summary of scikit 'LinearRegression' models.
        
        Provide feature information of linear regression models,
        such as coefficient, standard error and p-value. It is adapted
        to stand-alone and Pipeline scikit models.
        
        Important restriction of the function is that LinearRegression 
        must be the last step of the Pipeline.

        Parameters
        ----------
        use_old (bool)
            Use previous version of summary of linear regression, useful when multicollinearity breaks new method. Default to True.
        """
        #assert that the model is linear regression or is a Linear Regression inside a pipeline
        assert type(self.model) is LinearRegression , "model must be a LinearRegression or a Pipeline with a LinearRegression as last step. Try model.best_estimator_ if you are using GridSearchCV or RandomizedSearchCV"
    
        if use_old:
            # Obtain coefficients of the model
            if type(self.model) is LinearRegression:
                coefs = self.model.coef_
                intercept = self.model.intercept_
            else:
                coefs = self.model[len(self.model) - 1].coef_ #We suppose last position of pipeline is the linear regression model
                intercept = self.model[len(self.model) - 1].intercept_
            
            if type(self.model) is Pipeline:
                X_design = self.model[0].transform(X)
                coefnames = list()
                if hasattr(self.model[0],"transformers_"):
                    for tt in range(len(self.model[0].transformers_)):
                        try:
                            if hasattr(self.model[0].transformers_[tt][1].steps[-1][1],"get_feature_names"):
                                aux = self.model[0].transformers_[tt][1].steps[-1][1].get_feature_names_out(self.model[0].transformers_[tt][2])
                                if type(aux)==list:
                                    coefnames = coefnames + aux
                                else:
                                    coefnames = coefnames + aux.tolist()
                            else:
                                coefnames = coefnames + self.model[0].transformers_[tt][2]
                        except:
                            continue
                else:
                    coefnames = self.X_train.columns.values.tolist()
            
                
            ## include constant ------------- 
            if self.model[len(self.model) - 1].intercept_ != 0:
                coefnames.insert(0,'Intercept')
                if type(X_design).__module__ == np.__name__:
                    X_design = np.hstack([np.ones((X_design.shape[0], 1)), X_design])
                    X_design = pd.DataFrame(X_design, columns=coefnames)
                elif type(X_design).__module__ == 'pandas.core.frame':
                    pass
                else:
                    X_design = np.hstack([np.ones((X_design.shape[0], 1)), X_design.toarray()])
                    X_design = pd.DataFrame(X_design, columns=coefnames)    
            else:
                try:
                    X_design = X_design.toarray()
                    X_design = pd.DataFrame(X_design, columns=coefnames)
                except:
                    pass
            

            ols = sm.OLS(y.values, X_design)
            ols_result = ols.fit()
            return ols_result.summary()
        else:
            # Obtain coefficients of the model
            if type(self.model) is LinearRegression:
                coefs = self.model.coef_
                intercept = self.model.intercept_
                input_names = self.X_train.columns
                X_t = self.X_train
            else:
                coefs = self.model[len(self.model) - 1].coef_ #We suppose last position of pipeline is the linear regression model
                intercept = self.model[len(self.model) - 1].intercept_
                X_t = self.model[len(self.model) - 2].transform(self.X_train)
                input_names = self.model[len(self.model) - 2].get_feature_names_out().tolist()

            intercept_included = True
            params = coefs
            if not intercept == 0 and not 'Intercept' in input_names:
                params = np.append(intercept,coefs)
                input_names = ['Intercept'] + input_names
                intercept_included = False
            elif 'Intercept' in input_names:
                coefs[input_names.index('Intercept')] = intercept
                params = coefs
            predictions = self.model.predict(self.X_train)
            residuals = self.y_train - predictions

            print('Residuals:')
            quantiles = np.quantile(residuals, [0,0.25,0.5,0.75,1], axis=0)
            quantiles = pd.DataFrame(quantiles, index=['Min','1Q','Median','3Q','Max'])
            print(quantiles.transpose())
            # Note if you don't want to use a DataFrame replace the two lines above with
            if not intercept_included:
                if not type(X_t) == pd.core.frame.DataFrame and not type(X_t) == np.ndarray:
                    newX = np.append(np.ones((len(X_t.toarray()),1)), X_t.toarray(), axis=1)
                else:
                    newX = np.append(np.ones((len(X_t),1)), X_t, axis=1)
            else:
                if not type(X_t) == pd.core.frame.DataFrame:
                    newX = X_t.toarray()
                else:
                    newX = X_t.values
                
            MSE = (sum((residuals)**2))/(len(newX)-len(newX[0]))

            var_b = MSE * (np.linalg.inv(np.dot(newX.T,newX)).diagonal())
            sd_b = np.sqrt(var_b)
            ts_b = params / sd_b

            p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX[0])))) for i in ts_b]

            sd_b = np.round(sd_b,3)
            ts_b = np.round(ts_b,3)
            p_values = np.round(p_values,3)
            params = np.round(params,4)

            myDF3 = pd.DataFrame()
            myDF3["Input"], myDF3["Coefficients"], myDF3["Standard Errors"], myDF3["t values"], myDF3["Pr(>|t|)"], myDF3["Signif"] = [input_names, params, sd_b, ts_b, p_values, np.vectorize(lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else ('.' if x < 0.1 else ' '))))(p_values)]
            myDF3.set_index("Input", inplace=True)
            myDF3.index.name = None
            print(myDF3)
            print('---\nSignif. codes:  0 `***` 0.001 `**` 0.01 `*` 0.05 `.` 0.1 ` ` 1\n')
            print(f'Residual Standard Error: {round(np.std(residuals), 3)} on {residuals.shape[0]} degrees of freedom')
            # error metrics
            r2 = mtrs.r2_score(y, predictions)
            n = len(self.y_train)
            k = self.X_train.shape[1]
            adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
            RMSE = np.sqrt(mtrs.mean_squared_error(self.y_train, predictions))
            MAE = mtrs.mean_absolute_error(self.y_train, predictions)
            print(f'R-squared: {round(r2, 3)}, Adjusted R-squared: {round(adjusted_r2, 3)}, RMSE: {round(RMSE, 3)}, MAE: {round(MAE, 3)}')
            # F test
            TSS = np.sum(y - predictions) ** 2
            RSS = (1 - r2) * TSS
            num_f = (TSS - RSS) / k
            den_f = RSS / (n - k - 1)
            f = num_f / den_f
            p_f = 1 - stats.f.cdf(f, k, (n - k - 1)) 
            print(f'F-statistic: {round(f, 3)} on {k} and {n - k - 1} DOF, P(F-statistic): {round(p_f, 3)}')
            return 
        

    def permutation_importance(self,n_repeats:int=10,random_state=None,figsize=(12, 4),title='Permutation Importance',rotation:int=90, save:bool = True):
        """
        Generate a permutation importance plot. Is used
        to determine the importance of each feature in the model.

        Parameters
        ----------
        n_repeats : int, optional
            Number of times to permute a feature. The default is 10.

        random_state : int, optional
            Random state for the permutation. The default is None.

        figsize : tuple, optional
            Size of the figure. The default is (12, 4).

        Returns
        -------
        None.
            Plot is generated.
        """
        assert not isinstance(self.model, list), 'model must be a single model, not a list. Comparison of models is only supported for plot_roc_curve(), plot_calibration_curve() and plot_accuracy_across_thresholds()'
        assert n_repeats > 0, "n_repeats must be greater than 0 for permutation importance"
        assert random_state is None or isinstance(random_state, int), "random_state must be an integer or None"
        assert isinstance(figsize, tuple) and len(figsize) == 2, "figsize must be a tuple and figsize must be a tuple of length 2"
        importances = permutation_importance(self.model, 
                                    self.X_train, self.y_train,
                                    n_repeats=n_repeats,
                                    random_state=random_state)
        
        fig = plt.figure(2, figsize=figsize) 
        plt.bar(self.X_train.columns, importances.importances_mean, yerr=importances.importances_std,color='black', alpha=0.5)
        plt.xlabel('Feature')
        plt.ylabel('Permutation Importance')
        plt.title(self.model_name + " " + title)
        plt.xticks(rotation=rotation)
        plt.grid()
        plt.show()
        self.fig_permutation_importance = fig
        if save:
            if not os.path.exists(f'./models/{self.model_name}'):
                os.makedirs(f'./models/{self.model_name}')

            fig.savefig(f'./models/{self.model_name}/permutation_importance.png')


    def get_metrics_summary(self, sample_weight:str=None, multioutput='uniform_average', save:bool = True)-> pd.DataFrame:
        """
        Prints a summary of the metrics of a model for a given threshold
        and returns them in a DataFrame

        Parameters
        ------------
        model_name : str
            The name of the model to use
        sample_weight : dict, optional
            A dictionary with the keys being the set names and the values being the weights
        multioutput : str, optional
            The type of averaging to use for the metrics. The default is 'uniform_average'.
            Options are 'raw_values', 'uniform_average' or 'variance_weighted' for R2 is not supported yet

        Returns
        -----------
        pd.DataFrame
            A DataFrame with the metrics (accuracy, balanced accuracy, precision, recall, f1-score, roc-auc)

        Limitations
        -----------
        The data_dict dictionary should have the following structure, with the keys being the set names
        and the values being dictionaries with the keys 'data' and 'target' containing the data and target.

        data_dict = {
            'train': {
                'data': X_train,
                'target': y_train
            },
            'test': {
                'data': X_test,
                'target': y_test
            },
            'validation': {
                'data': X_val,
                'target': y_val
            }
        }

        sample_weight should be a dictionary with the keys being the set names and the values being the weights

        sample_weight = {
            'train': train_weights,
            'test': test_weights,
            'validation': val_weights

        """
        assert not isinstance(self.model, list), 'model must be a single model, not a list. Comparison of models is only supported for plot_roc_curve(), plot_calibration_curve() and plot_accuracy_across_thresholds()'
        assert multioutput in ['uniform_average','raw_values']
        assert sample_weight is None or isinstance(sample_weight, dict), "sample_weight must be None or a dictionary"
        
        data_dict={'Train': {'data': self.X_train,'target': self.y_train}}
        #add test and validation  if it exists
        if hasattr(self,'X_test') and hasattr(self,'y_test'):
            data_dict['Test']={'data': self.X_test, 'target': self.y_test}
        if hasattr(self, 'X_val') and hasattr(self, 'y_val'):
            data_dict['Val']={'data': self.X_val, 'target': self.y_val}
            
        # Get the predicted probabilities and predictions
        predictions_dict = {}
        for dataset_type in data_dict.keys():
            predictions_dict[dataset_type] = self.model.predict(data_dict[dataset_type]['data'])
        # Calculate and print the metrics for each set
        metrics_dict = {
            'Model': self.model_name,
            'Weights': sample_weight,
        }
        # Iterate over the metrics
        for metric in REG_METRIC_FUNCS_SUMMARY.keys():
            # Print a separator
            #if multi_class print ("multiclass")
            # Iterate over the sets
            for dataset_type, predictions in predictions_dict.items():
                # Calculate the metric for the set
                if metric == '% BIAS': #For Forecast Bias there is not sample_weights its a global measure
                    metric_score = REG_METRIC_FUNCS_SUMMARY[metric](
                        data_dict[dataset_type]['target'], predictions)
                else:
                    if sample_weight is None:
                        metric_score = REG_METRIC_FUNCS_SUMMARY[metric](
                            data_dict[dataset_type]['target'], predictions, sample_weight=None, multioutput=multioutput)

                    else:
                        assert dataset_type in [key for key in sample_weight.keys()], f"sample_weight must have a key for {dataset_type}"
                        metric_score = REG_METRIC_FUNCS_SUMMARY[metric](
                            data_dict[dataset_type]['target'], predictions, 
                            sample_weight=sample_weight[dataset_type], multioutput=multioutput)    

                metrics_dict[f'{metric} {dataset_type}'] = metric_score

        metrics_dict["N_Vars"] = len(self.model.feature_names_in_)
        metrics_dict["Vars"] = str(self.model.feature_names_in_.tolist())
        metrics_dict["Samples_Train"] = self.X_train.shape[0]
        if hasattr(self,'X_test'):
            metrics_dict["Samples_Test"] = self.X_test.shape[0]
        if hasattr(self,'X_val'):
            metrics_dict["Samples_Val"] = self.X_val.shape[0]
        metrics_dict["CV"] = self.model.cv
        try:
            metrics_dict["best_params"] = str(self.model.best_params_)
            if "GridSearchCV" in str(self.model.__getattribute__):
                metrics_dict["Search"] = 'Grid' + str(self.model.param_grid)
            elif "RandomizedSearchCV" in str(self.model.__getattribute__):
                metrics_dict["Search"] = 'Random' + str(self.model.param_distributions)
            else:
                metrics_dict["Search"] = None

        except:
            metrics_dict["best_params"] = None
            metrics_dict["Search"] = None
        
        # Return the metrics as a DataFrame
        summary=pd.DataFrame(metrics_dict,index=[0])

        self.metrics_summary = summary
        if save:
            if not os.path.exists('./models'):
                os.makedirs('./models')

            if not os.path.isfile('./models/summary_models_analysis.xlsx'):
                df=pd.DataFrame(columns=summary.columns)
                #save the summary data to the excel
                df.to_excel('./models/summary_models_analysis.xlsx',index=False,sheet_name='Sheet1')
            else:
                df=pd.read_excel('./models/summary_models_analysis.xlsx',sheet_name='Sheet1')
                #concat the summary data to the excel
                df=pd.concat([df,summary],axis=0,ignore_index=True)
                df.to_excel('./models/summary_models_analysis.xlsx',index=False,sheet_name='Sheet1')
    
        return  self.metrics_summary
        



        

                        

        

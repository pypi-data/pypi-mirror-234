import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Xai:
    def __init__(self):
        pass


    #SHAP

    #FEATURE IMPORTANCE
    def shap_feature_importance(self, model, X_train, y_train, figsize=(20, 10), kernel_nsamples=100, max_display=15):

        assert isinstance(X_train, pd.DataFrame), "X_train must be a pandas DataFrame"
        assert isinstance(y_train, pd.Series) or isinstance(y_train,pd.DataFrame), "y_train must be a pandas Series or DataFrame"
        assert isinstance(figsize, tuple), "figsize must be a tuple"
        assert isinstance(max_display, int), "max_display must be an integer"
        assert isinstance(kernel_nsamples, int), "nsamples must be an integer" 

        model_name=[step for step in model.best_estimator_.named_steps.keys()][-1]

        if model_name in ["XGB","RF","DT","LGBM"]: #For tree based models
            explainer = shap.TreeExplainer(model.best_estimator_[model_name])
            shap_values = explainer.shap_values(X_train)
        else: #For not tree based models
            explainer = shap.KernelExplainer(model.best_estimator_.predict_proba, X_train)
            shap_values = explainer.shap_values(X_train, nsamples=kernel_nsamples)
        
        if y_train.value_counts().size > 2 and y_train.value_counts().size < 8: #For multiclass classification

            plt.figure()

            for i , class_names in enumerate(y_train.cat.categories):
                plt.subplot(2, 2, i+1)

                shap.summary_plot(shap_values[i], X_train, show=False, plot_size=figsize, max_display=max_display)
                plt.title(f'Importance for the {class_names} class', fontsize=14)
                #if the last i
                if i == y_train.value_counts().size-1:
                    plt.subplot(2, 2, i+2)
                    shap.summary_plot(shap_values, X_train, plot_type="bar",class_names=y_train.cat.categories, show=False, plot_size=figsize, max_display=max_display)
                    plt.title(f'Generalized Feature Importance', fontsize=14)


            plt.suptitle('SHAP Feature Importances', fontsize=20)
            plt.tight_layout()
            

        elif y_train.value_counts().size == 2: #For binary classification
            plt.subplot(2,2,1)
            shap.summary_plot(shap_values, X_train, show=False, plot_size=figsize)
            plt.title('Importance for the positive class', fontsize=14)
            plt.subplot(2,2,2)
            shap.summary_plot(shap_values, X_train, plot_type="bar",class_names=y_train.cat.categories, show=False, plot_size=figsize)
            plt.suptitle('SHAP Feature Importances', fontsize=20)
            plt.tight_layout()

        # FOR REGRESSION NEED TO BE IMPLEMENTED
            

        #For regression
        plt.show()

    #WATERFALL
    def shap_waterfall(self, model, X_train, y_train, index, figsize=(25,10), max_display=15, kernel_nsamples=100):


        assert isinstance(X_train, pd.DataFrame), "X_train must be a pandas DataFrame"
        assert isinstance(y_train, pd.Series) or isinstance(y_train,pd.DataFrame), "y_train must be a pandas Series or DataFrame"
        assert isinstance(index, int), "index must be an integer"
        assert isinstance(figsize, tuple), "figsize must be a tuple"
        assert isinstance(max_display, int), "max_display must be an integer"
        assert isinstance(kernel_nsamples, int), "nsamples must be an integer"
        
        model_name=[step for step in model.best_estimator_.named_steps.keys()][-1]
        if model_name in ["XGB", "LGBM", "DT", "RFC"]: #For tree based models
            explainer = shap.TreeExplainer(model.best_estimator_[model_name])
            shap_values = explainer.shap_values(X_train)
        else: 
            explainer = shap.KernelExplainer(model.best_estimator_.named_steps[model_name].predict_proba, X_train)
            shap_values = explainer.shap_values(X_train.iloc[index,:], nsamples=kernel_nsamples)

        if y_train.value_counts().size > 2 and y_train.value_counts().size < 8: #For multiclass classification
            for i , class_names in enumerate(y_train.cat.categories):
                plt.subplot(2, 2, i+1)
                shap.plots._waterfall.waterfall_legacy(explainer.expected_value[i], shap_values[i][index], X_train.iloc[index],show=False,max_display=max_display) #For each class
                plt.title(f" class {class_names}", fontsize=14)
                if i == y_train.value_counts().size-1: #In the last iteration the Generalized waterfall is added
                    plt.subplot(2, 2, i+2)
                    shap.plots._waterfall.waterfall_legacy(np.mean(explainer.expected_value), np.sum(np.array(shap_values), axis=0)[index], X_train.iloc[index],show=False, max_display=max_display) #Generalized
                    plt.title(f" Generalized ", fontsize=14)

            plt.gcf().set_size_inches(figsize[0],figsize[1])
            plt.suptitle(f'Waterfall Explanation for {index}', fontsize=20)
            plt.tight_layout()

        elif y_train.value_counts().size == 2 : #for binary classification
            shap.plots._waterfall.waterfall_legacy(explainer.expected_value, shap_values[index], X_train.iloc[index],show=False,max_display=max_display) #For each 
            plt.gcf().set_size_inches(figsize[0],figsize[1])
            plt.suptitle(f'Waterfall Explanation for register number {index}', fontsize=20)

        #FOR REGRESSION NEED TO BE IMPLEMENTED
        
        plt.show()

    
            
        
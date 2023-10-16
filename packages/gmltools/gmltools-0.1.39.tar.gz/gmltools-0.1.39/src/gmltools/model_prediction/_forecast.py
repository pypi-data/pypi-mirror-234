import numpy as np
import pandas as pd
from typing import List
import shap
import matplotlib.pyplot as plt
from datetime import datetime
import os
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error




class RecursivePredictor:

    def __init__(self, X_train, y_train, X_test, model, lags:List[int], columns_lags:List[int], column_rolled_lags:List[int], column_rolled_lags_initial:int, rolled_metrics:List[str], rolled_lags:List[int], save_shaps:bool=False, save_data:bool=False, save_preds_and_errors:bool=False, save_path:str='//ficheros2/Interdepartamental/Itrading/mercados/pred_day_ahead'):

        """
        Esta clase sirve para hacer predicciones recursivas. Es decir, para hacer predicciones de un modelo que tiene como input variables lagged y rolled.

        Parameters
        ----------
        X_train : pd.DataFrame
            Dataframe de pandas con los datos de entrenamiento del modelo.

        y_train : pd.Series
            Serie de pandas con los datos de entrenamiento del modelo.

        X_test : pd.DataFrame
            Dataframe de pandas con los datos de test del modelo.

        model : sklearn model
            Modelo de sklearn que se quiere utilizar para hacer las predicciones.

        lags : list
            Lista con los lags de las variables lagged.

        columns_lags : list
            Lista con las columnas de las variables lagged.
            Indica la posición de la columna, sin tener en cuenta la columna 'id' en caso de que exista.

        column_rolled_lags : list
            Lista con las columnas de las variables rolled.
            Indica la posición de la columna, sin tener en cuenta la columna 'id' en caso de que exista.

        column_rolled_lags_initial : int
            Valor inicial de la columna de las variables rolled.

        rolled_metrics : list
            Lista con las métricas de las variables rolled.
            ["mean","std","max","min"]

        rolled_lags : list
            Lista con los lags de las variables rolled.
        
        """

        self.model = model
        self.lags = lags
        self.columns_lags = columns_lags
        self.column_rolled_lags = column_rolled_lags
        self.column_rolled_lags_initial = column_rolled_lags_initial
        self.rolled_metrics = rolled_metrics
        self.rolled_lags = rolled_lags
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.save_shaps = save_shaps
        self.save_data = save_data
        self.save_preds_and_errors=save_preds_and_errors
        self.save_path = save_path
        

        if 'id' in X_train.columns:
            self.X_train.drop(columns=['id'],inplace=True)

        elif 'id' in X_test.columns:
            self.X_test.drop(columns=['id'],inplace=True)
        assert all(X_train.columns == X_test.columns), "X_train and X_test must have the same column names"

        
    def predict_rec(self):
        """
        This method makes the recursive prediction of the model.
        
        """

        y_pred= [] #here is where the predictions will be stored for each split of the validation set/test set
        X=self.X_test.copy() #convert the validation/test set to numpy array
        self.shaps_values_list=[]
        self.features_list=[]
        self.X_test_shap_all_hours=[]

        for i in range(len(X)): #for each register of the validation/test set
            for k,column in enumerate(self.columns_lags): #for each column of the lag type
                if self.lags[k]>len(y_pred) : #if the lag is bigger than the register number the operation is done on the train set
                    X.iloc[i,column] = self.y_train.iloc[-self.lags[k]+i]
                else: #if the lag is smaller than the register number the operation is previous predictions
                    X.iloc[i,column]=y_pred[-self.lags[k]]

            
            for k, column in enumerate(self.column_rolled_lags): #for each column of the roll type. This is more complex because it requires a rolling window
                #3 condiciones
                #1. cuando se hace roll sobre el train 
                if self.column_rolled_lags_initial >  i: #if the init start of the rolling window is bigger than the register number the operation is done on the train set
                    if self.rolled_metrics[k] == 'mean':
                        if self.column_rolled_lags_initial - i == 1:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]):].mean() #No se pone -1 porque el iloc no incluye el último valor y haciendo : se incluye el último valor
                        else:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]+self.column_rolled_lags_initial-1):-(self.column_rolled_lags_initial-1)].mean() # Se resta 1 porque el iloc no incluye el último valor
                    elif self.rolled_metrics[k] == 'std':
                        if self.column_rolled_lags_initial - i == 1:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]):].std() #No se pone -1 porque el iloc no incluye el último valor y haciendo : se incluye el último valor
                        else:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]+self.column_rolled_lags_initial-1):-(self.column_rolled_lags_initial-1)].std() #Se resta 1 porque el iloc no incluye el último valor
                    elif self.rolled_metrics[k] == 'min':
                        if self.column_rolled_lags_initial - i == 1:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]):].min() #No se pone -1 porque el iloc no incluye el último valor y haciendo : se incluye el último valor
                        else:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]+self.column_rolled_lags_initial-1):-(self.column_rolled_lags_initial-1)].min() #Se resta 1 porque el iloc no incluye el último valor
                    elif self.rolled_metrics[k] == 'max':
                        if self.column_rolled_lags_initial - i == 1:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]):].max() #No se pone -1 porque el iloc no incluye el último valor y haciendo : se incluye el último valor
                        else:
                            X.iloc[i,column] = self.y_train.iloc[-(self.rolled_lags[k]+self.column_rolled_lags_initial-1):-(self.column_rolled_lags_initial-1)].max() #Se resta 1 porque el iloc no incluye el último valor
                    else:
                        raise ValueError("rolled_metrics arguements provided not correct. Position must be ['mean','std','max','min']")
                    
                #2. cuando se hace  roll sobre el train y las nuevas preds del X_test
                elif self.column_rolled_lags_initial <= i and (self.rolled_lags[k] + self.column_rolled_lags_initial -1) > i:
                  
                    if self.column_rolled_lags_initial == 1:
                        y_train_part=self.y_train.iloc[-(self.rolled_lags[k]-i):].values
                        y_pred_part= np.array(y_pred[:i])
                    else:
                        y_train_part=self.y_train.iloc[-(self.rolled_lags[k]+(self.column_rolled_lags_initial-1)-i):].values #Este esta bien
                        y_pred_part= np.array(y_pred[:i+1-self.column_rolled_lags_initial]) 
                    #
                    #Est parte funcionaba antes solo con el try al hacer el ahead-4 dio fallo
                    #
                    try:
                        y_rolled_pred=np.concatenate((y_train_part,y_pred_part),axis=0)
                    # A veces tiene dimensiones distintas 
                    except:
                        
                        if isinstance(y_train_part, pd.DataFrame):

                            y_rolled_pred=np.concatenate((y_train_part.values.flatten(),y_pred_part),axis=0)
                        else:
                            y_rolled_pred=np.concatenate((y_train_part.flatten(),y_pred_part),axis=0)
                    #
                    #
                    #


                    if self.rolled_metrics[k] == 'mean':
                        X.iloc[i,column] = np.mean(y_rolled_pred)

                    elif self.rolled_metrics[k] == 'std':
                        X.iloc[i,column] = np.std(y_rolled_pred)

                    elif self.rolled_metrics[k] == 'min':

                        X.iloc[i,column] = np.min(y_rolled_pred)
                    
                    elif self.rolled_metrics[k] == 'max':
                        X.iloc[i,column] = np.max(y_rolled_pred)

                    else:
                        raise ValueError("rolled_metrics arguements provided not correct. Position must be ['mean','std','max','min']")
                #3. cuando solo se hace rolls sobre las nuevas preds
                elif self.column_rolled_lags_initial <= i and (self.rolled_lags[k] + self.column_rolled_lags_initial -1) <= i:
       
                    if self.rolled_metrics[k] == 'mean':
                        if self.column_rolled_lags_initial == 1:
                            X.iloc[i,column] = np.mean(y_pred[-self.rolled_lags[k]:])
                        else:
                            X.iloc[i,column] = np.mean(y_pred[-(self.rolled_lags[k]+self.column_rolled_lags_initial):-(self.column_rolled_lags_initial-1)])
                    elif self.rolled_metrics[k] == 'std':
                        if self.column_rolled_lags_initial == 1:
                            X.iloc[i,column] = np.std(y_pred[-self.rolled_lags[k]:])
                        else:
                            X.iloc[i,column] = np.std(y_pred[-(self.rolled_lags[k]+self.column_rolled_lags_initial):-(self.column_rolled_lags_initial-1)])

                    elif self.rolled_metrics[k] == 'min':
                        if self.column_rolled_lags_initial == 1:
                            X.iloc[i,column] = np.min(y_pred[-self.rolled_lags[k]:])
                        else:
                            X.iloc[i,column] = np.min(y_pred[-(self.rolled_lags[k]+self.column_rolled_lags_initial):-(self.column_rolled_lags_initial-1)])
                    
                    elif self.rolled_metrics[k] == 'max':
                        if self.column_rolled_lags_initial == 1:
                            X.iloc[i,column] = np.max(y_pred[-self.rolled_lags[k]:])
                        else:
                            X.iloc[i,column] = np.max(y_pred[-(self.rolled_lags[k]+self.column_rolled_lags_initial):-(self.column_rolled_lags_initial-1)])

                    else:
                        raise ValueError("rolled_metrics arguements provided not correct. Position must be ['mean','std','max','min']")
                    
                else :
                    raise ValueError("Some Error Ocurred when column_las[k] condition to i from X_test avaible")

            self.i=i
            self.X_test_shap=X.iloc[i].to_frame().T
            #lets make dtypes of self.X_test_shap the same as self.X_train
            self.X_test_shap=self.X_test_shap.astype(self.X_train.dtypes.to_dict())
            self.y_pred_rec=self.model.predict(X.iloc[i].to_frame().T)
            self.X_test_shap_all_hours.append(self.X_test_shap)
            if self.save_shaps:
                shaps,features=self._calculate_shap_values()
                self.shaps_values_list.append(shaps)
                self.features_list.append(features)

            #concat teh X_test_shap_all_hours
            #self.features_list.append(features)
            y_pred.append(self.y_pred_rec[0])

        

        self.X_test_shap_all_hours=pd.concat(self.X_test_shap_all_hours,axis=0)
        self.y_pred = np.array(y_pred)
        if self.save_data:
            self._save_data()
            self._save_model()
        if self.save_preds_and_errors:
            self._save_y_preds_and_errors()

        return self.y_pred
    
    def _calculate_shap_values(self):
        """
        This method calculates the shap values for the model in each step of the recursive prediction.
        
        """
        self.X_train_sample=self.X_train.copy()
        self.X_train_sample=self.model.named_steps['Prep'].fit_transform(self.X_train_sample)
        self.X_test_shap_= self.model.named_steps['Prep'].transform(self.X_test_shap)

        explainer = shap.Explainer(self.model.named_steps['SVR'].predict, self.X_train_sample)

        # Calcular los valores SHAP
        shap_values = explainer(self.X_test_shap_)

        fig = plt.figure()
        ax0 = fig.add_subplot(111)
        shap.waterfall_plot(shap.Explanation(values=shap_values[0], feature_names=self.model.named_steps["Prep"].get_feature_names_out()),max_display=58,show=False)
        w, h = plt.gcf().get_size_inches()
        # plt.gcf().set_size_inches(w*4, _)
        plt.gcf().set_size_inches(w*1.5, h*1.1)
        plt.title(f"SHAP Hora {self.i}",fontsize=24)
        #increase siz of y labels and x labels
        ax0.tick_params(axis='both', which='major', labelsize=24)
        plt.tight_layout() 

        if not os.path.exists(fr"{self.save_path}/{datetime.now().strftime('%Y-%m-%d')}/shaps"):
            os.makedirs(fr"{self.save_path}/{datetime.now().strftime('%Y-%m-%d')}/shaps")

        plt.savefig(rf"{self.save_path}/{datetime.now().strftime('%Y-%m-%d')}/shaps/waterfall_{(datetime.now().date()+pd.Timedelta(days=1)).strftime('%Y-%m-%d')}_{self.i}.png")

        return [shap_values, self.model.named_steps["Prep"].get_feature_names_out()]
    

    #SAVE THE DATA TRAIN AND TEST FOR EACH DAY IN A FOLDER
    def _save_data(self):
        """
        This method saves the data used for the recursive prediction in each step of the recursive prediction.
        """

        path=rf"{self.save_path}/{datetime.now().strftime('%Y-%m-%d')}/data/"

        if not os.path.exists(path):
            os.makedirs(path)

        print(os.path.join(path + "X_test.csv"))

        self.X_test_shap_all_hours.to_csv(os.path.join(path + "X_test.csv"))
        self.X_train.to_csv(os.path.join(path + "X_train.csv"))
        self.y_train.to_csv(os.path.join(path + "y_train.csv"))
        np.save(os.path.join(path, "y_pred.npy"), self.y_pred)


    #SAVE THE MODEL FOR EACH DAY IN A FOLDER
    def _save_model(self):
        """This method saves the model used for the recursive prediction in each step of the recursive prediction."""
        path=rf"{self.save_path}/{datetime.now().strftime('%Y-%m-%d')}/model/"

        if not os.path.exists(path):
            os.makedirs(path)

        #save self.model with joblib
        joblib.dump(self.model, os.path.join(path + "model.joblib"))

        np.save(os.path.join(path, "features.npy"), self.features_list)
        np.save(os.path.join(path, "shaps.npy"), self.shaps_values_list)


    #SAVE TEH PREDICTED VALUES OF TODAY AND THE ERRORS OF THE PREVIOUS DAY
    def _save_y_preds_and_errors(self):

        path=self.save_path+"/"


        df2=pd.read_excel(path + "y_preds.xlsx",index_col="datetime")
        df=pd.read_excel(path + "errors.xlsx",index_col="datetime")
        
        spot_yesterday=self.y_train.iloc[-24:].values
        pred_yesterday=df2.y_pred.iloc[-24:].values
        #calcaute the mse, rmse and mae of spot_yesterday and pred_yesterday
        epsilon=1e-5
        #try to calculate the errors
        try:
            mse=mean_squared_error(spot_yesterday,pred_yesterday)
            rmse=np.sqrt(mean_squared_error(spot_yesterday,pred_yesterday))
            mae=mean_absolute_error(spot_yesterday,pred_yesterday)
            mape=np.mean(np.abs((spot_yesterday - pred_yesterday) / spot_yesterday+epsilon)) 
            mdape=np.median(np.abs((spot_yesterday - pred_yesterday) / spot_yesterday+epsilon))
            smape=np.mean(np.abs((spot_yesterday - pred_yesterday) / (spot_yesterday + pred_yesterday)+epsilon))
        #if errors cant be because of nan values
        except:
            mse=np.nan
            rmse=np.nan
            mae=np.nan
            mape=np.nan
            mdape=np.nan
            smape=np.nan
        
        errors_yesterday=pd.DataFrame(index=[(datetime.now().date()).strftime("%Y-%m-%d")],columns=["mse","rmse","mae","mape","mdape","smape"],data=[[mse,rmse,mae,mape,mdape,smape]])
        errors_yesterday.index.name="datetime"
        #concat
        errors=pd.concat([df,errors_yesterday],axis=0)
        #save
        errors.to_excel(path + "errors.xlsx")

        #in the columns datetime append the new hours of the prediction and in the columns y_pred append the new predictions
        y_preds_today=pd.DataFrame(index=self.X_test.index.strftime("%Y-%m-%d %H:%M:%S").values,columns=["y_pred"],data=self.y_pred)
        y_preds_today.index.name="datetime"
        preds=pd.concat([df2,y_preds_today],axis=0)
        #save
        preds.to_excel(path + "y_preds.xlsx")
        
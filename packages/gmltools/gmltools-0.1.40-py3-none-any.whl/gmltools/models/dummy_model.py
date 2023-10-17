
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class NaiveModel():
    """
    This is the Naive Dummy Model that predicts the new vlues nbased on previous values given by the parameter shifts.
    Always a tscv muust be passed to the model. Actually a TimeSeriesInitialSplit object.
    """
    def __init__(self,tscv,shifts:int=24):
        """
        Parameters
        ----------
        tscv : TimeSeriesInitialSplit object
            This is the time series cross validation object that will be used to split the data.

        shifts : int, optional
            This is the number of hours that the model will shift to predict the next value. The default is 24.
        """

        self.shifts=shifts
        self.tscv=tscv
    def fit(self,X,y):
        """
        This function fits the model to the data.

        Parameters
        ----------
        X : pandas dataframe
            This is the dataframe with the features.
        y : pandas dataframe
        """
        self.X=X
        self.y=y

    def predict(self):
        """
        This function returns a list with the predictions and true values of the model for each test split.

        """

        assert hasattr(self,"X"), "You must fit the model first"
        assert hasattr(self,"y"), "You must fit the model first"
        self.predictions=[]
        index_train,index_test=self.tscv.get_index_splits(self.X)
        for index_test_ in index_test:
            y_real=self.y.loc[index_test_].values
            
            y_pred=self.y.loc[index_test_[0]-pd.Timedelta(hours=self.shifts):index_test_[0]-pd.Timedelta(hours=1)].values

            df=pd.DataFrame(index=index_test_)
            df["pred"]=y_pred
            df["true"]=y_real
            
            self.predictions.append(df)
        return self.predictions
    
    def get_scores(self):
        """
        This function returns a dataframe with the scores of the model for each test split.
        Currently only the MSE is calculated.
        """
        assert hasattr(self,"X"), "You must fit the model first"
        assert hasattr(self,"y"), "You must fit the model first"
        df_list=self.predict()
        #for each split calculate the RMSE
        mse_list=[]
        for df in df_list:
            mse_list.append(mean_squared_error(df["true"],df["pred"]))

        #create a dataframe with the results where teh columns are the days
        index=self.tscv.get_test_days(self.X)
        mse=np.mean(mse_list)
        std_mse=np.std(mse_list)
        index.extend(["mean","std"])
        mse_list.extend([mse,std_mse])

        self.df_scores=pd.DataFrame(mse_list,columns=[f"Naive Model shifts {self.shifts}"],index=index)
        return self.df_scores
    def get_plot(self,figsize:tuple=(5000,2800), title_font=25, ytitle="y", xtitle="x",xtickfont=18, ytickfont=18, ytitlefont=18, xtitlefont=18, legendfont=20, continious:bool=False):
        """
        This function returns a plotly figure with the predictions of the model for each test split.
        Making continious=True will plot all the predictions in one plot. Otherwise each test split will be plotted in a subplot.

        Parameters
        ----------
        figsize : tuple, optional
            This is the size of the figure. The default is (5000,2800).

        continious : bool, optional
            This is a boolean that indicates if the predictions of the model will be plotted in one plot or in a subplot for each test split. The default is False.

        Returns
        -------
        fig : plotly figure
            This is the figure with the predictions of the model for each test split.
        """
        assert hasattr(self,"X"), "You must fit the model first"
        assert hasattr(self,"y"), "You must fit the model first"
        pred_list=self.predict()
        #for each dataframe of the list with columns "true" and "pred" plot it in a subplot
        if continious:
            continious_preds=pd.concat(pred_list)
            #plot the true and pred col of the dataframe in one plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=continious_preds.index, y=continious_preds["true"], mode="lines", name="True",line=dict(color='gray')))
            fig.add_trace(go.Scatter(x=continious_preds.index, y=continious_preds["pred"], mode="lines", name="Predicted",line=dict(color='blue')))

            fig.update_layout(title="Naive, True vs Predicted Values",height=figsize[1], width=figsize[0],title_font=dict(size=title_font))
            fig.update_layout(xaxis=dict(title=xtitle, tickfont=dict(size=xtickfont), title_font=dict(size=xtitlefont)),
                              yaxis=dict(title=ytitle, tickfont=dict(size=ytickfont), title_font=dict(size=ytitlefont)),
                              legend=dict(font=dict(size=legendfont)))
            fig.show()


        else:
            fig=make_subplots(rows=len(pred_list),cols=1,subplot_titles=self.tscv.get_test_days(self.X),)
            for i,df in enumerate(pred_list):
                fig.add_trace(go.Scatter(x=df.index, y=df["true"], mode="lines", name="True"), row=i+1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df["pred"], mode="lines", name="Predicted"), row=i+1, col=1)

            fig.update_layout(height=figsize[1], width=figsize[0], title=f"Naive Model Predictions with {self.shifts} hour shifts")
            fig.show()



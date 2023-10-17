# from typing import Union
import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
from plotly.subplots import make_subplots
import itertools
from scipy.stats import pearsonr
import math
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
# from src.decomposition.seasonal import BaseDecomposition
import stumpy
import os
import plotly.io as pio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import Rectanmgle
from matplotlib.patches import Rectangle
import plotly.graph_objects as go
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.spatial import distance
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import coint
from scipy.stats import pearsonr, spearmanr

# OUTLIERMANAGER
# EXPLOREMANAGER


# -------------------------------------------------------------------------------------------------OUTLIERS------------------------------------------------------------------------------------------------------------------------------
class OutlierManager:
    """
    This class contains methods to detect outliers in time series.
    The dataframe  is used in the methods and not in the constructor 
    """
    def __init__(self):

        pass

    def detect_outlier_sd(self, df, sd_multiple=2,print_=True):
        """
        Detect outliers using standard deviation for each numerical column in a pandas DataFrame.
        A key assumption is the normality of the data. However, in reality, data is rarely normally distributed.
        Hence, this method is not recommended for most cases. Loses the theorethical guarantees quickly.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to detect outliers in.
        sd_multiple : int, optional
            Number of standard deviations to use as the threshold, by default 2
            1 corresponds to 68% confidence interval.
            2 corresponds to 95% confidence interval.
            3 corresponds to 99.7% confidence interval.
        
        print_ : bool, optional
            Whether to print the number of outliers and the percentage of outliers for each column, by default True
        Returns
        -------
        pd.DataFrame
            Boolean mask of outliers for each numerical column.
        """

        # select only the numeric columns
        numeric_cols = df.select_dtypes(include=np.number).columns

        # create an empty DataFrame to store the mask for each column
        outlier_masks = pd.DataFrame(columns=numeric_cols, index=df.index)

        # iterate over each numeric column and calculate the outlier mask
        for col in numeric_cols:
            ts = df[col].values
            mean = ts.mean()
            std = ts.std()
            higher_bound = mean + sd_multiple * std
            lower_bound = mean - sd_multiple * std
            outlier_mask = (ts > higher_bound) | (ts < lower_bound)
            if print_:
                print(f"Column: {col}, Nº of Outliers: {outlier_mask.sum()}, % of Outliers: {outlier_mask.mean()*100}%")
            outlier_masks[col] = outlier_mask

        return outlier_masks

    def detect_outlier_iqr(self, df, iqr_multiple=1.5,print_=True):
        """
        Detect outliers using interquartile range.

        Parameters
        ----------
        ts : pd.Series
            Time series to detect outliers in.
        iqr_multiple : int, optional
            Number of interquartile ranges to use as the threshold, by default 1.
            1.5 times the interquartile range is commonly used and corresponds to 2.7 STD almosr 3 STD.
        print_ : bool, optional
            Whether to print the number of outliers and the percentage of outliers for each column, by default True
        Returns
        -------
        pd.DataFrame
            Boolean mask of outliers.
        """
        # select only the numeric columns
        numeric_cols = df.select_dtypes(include=np.number).columns

        # create an empty DataFrame to store the mask for each column
        outlier_masks = pd.DataFrame(columns=numeric_cols, index=df.index)
        for col in numeric_cols:
            ts = df[col].values
            q1, q2, q3 = np.quantile(ts, 0.25), np.quantile(ts, 0.5), np.quantile(ts, 0.75)
            iqr = q3 - q1
            higher_bound = q3 + iqr_multiple * iqr
            lower_bound = q1 - iqr_multiple * iqr
            outlier_mask = (ts > higher_bound) | (ts < lower_bound)
            outlier_mask = (ts > higher_bound) | (ts < lower_bound)
            if print_:
                print("Nº de Outliers: ",outlier_mask.sum(), "% de Outliers: ", outlier_mask.mean(), "%")
            outlier_masks[col] = outlier_mask
        return outlier_masks

    def detect_outlier_isolation_forest(self, df, outlier_fraction, print_=True, **kwargs):
        """
        Detect outliers using isolation forest. Is an unsupervised learning algorithm that detects anomalies by isolating outliers.
        Based on Decision Trees. It models the oulliers directly: Assumes that the outlier points fall in the outer periphery and are
        easier to fall in the leaf node of a tree. Therefore, you can find ouliers in the short branches of the tree., whereas normal
        points are more likely to fall in the deeper branches of the tree.

        By default it uses 100 trees, but you can change this by passing the n_estimators parameter to kwargs.

        Parameters
        ----------
        ts : pd.Series
            Time series to detect outliers in.
        outlier_fraction : float, 'auto' or [0, 0.5]
            Fraction of outliers in the time series. Specifies the contamination parameter in IsolationForest.
            Is the same as the contamination parameter in IsolationForest.
        **kwargs
            Keyword arguments to pass to IsolationForest.
        
        Returns
        -------
        pd.Series
            Boolean mask of outliers.
        """
        if isinstance(outlier_fraction, str):
            assert outlier_fraction == "auto", "outlier_fraction must be between 0 and 0.5 or 'auto'"
        else:
            assert outlier_fraction >= 0 and outlier_fraction <= 0.5, "outlier_fraction must be between 0 and 0.5"
        # select only the numeric columns
        numeric_cols = df.select_dtypes(include=np.number).columns
        # create an empty DataFrame to store the mask for each column
        outlier_masks = pd.DataFrame(columns=numeric_cols, index=df.index)

        for col in numeric_cols:
            ts = df[col].values
            min_max_scaler = StandardScaler()
            scaled_time_series = min_max_scaler.fit_transform(ts.reshape(-1, 1))
            kwargs["contamination"] = outlier_fraction
            kwargs["random_state"] = 42
            model = IsolationForest(**kwargs)
            pred = model.fit_predict(scaled_time_series)
            pred = 1 - np.clip(pred, a_min=0, a_max=None)
            outlier_mask = pred.astype(bool)
            if print_:
                print("Nº de Outliers: ",outlier_mask.sum(), "% de Outliers: ", outlier_mask.mean(), "%")
            outlier_masks[col] = outlier_mask       
        return outlier_masks

    # Adapted from https://github.com/nachonavarro/seasonal-esd-anomaly-detection
    def calculate_test_statistic(self, ts, hybrid=False):
        """
        Calculate the test statistic for ESD.
        Calculate the test statistic defined by being the top z-score

        Parameters
        ----------
        ts : np.array
            Time series to calculate the test statistic for.
        hybrid : bool, optional
            Whether to use the hybrid ESD test statistic, by default False

        Returns
        -------
        int
            Index of the test statistic.
        float
            Value of the test statistic.
        """
        if hybrid:
            median = np.ma.median(ts)
            mad = np.ma.median(np.abs(ts - median))
            scores = np.abs((ts - median) / mad)
        else:
            scores = np.abs((ts - ts.mean()) / ts.std())
        max_idx = np.argmax(scores)
        return max_idx, scores[max_idx]

    def calculate_critical_value(self, size, alpha):
        """
        Calculate the critical value for ESD.
        https://en.wikipedia.org/wiki/Grubbs%27_test_for_outliers#Definition

        Parameters
        ----------
        size : int
            Size of the time series.
        alpha : float
            Significance level.
        
        Returns
        -------
        float
            Critical value.
        """

        t_dist = stats.t.ppf(1 - alpha / (2 * size), size - 2)
        numerator = (size - 1) * t_dist
        denominator = np.sqrt(size ** 2 - size * 2 + size * t_dist ** 2)
        return numerator / denominator

    # def seasonal_esd(
    #     self,
    #     ts: Union[pd.DataFrame, pd.Series],
    #     seasonal_decomposer: BaseDecomposition,
    #     hybrid: bool = False,
    #     max_anomalies: int = 10,
    #     alpha: float = 0.05,
    # ):
    #     """
    #     Seasonal ESD for detecting outliers in time series.

    #     Parameters
    #     ----------
    #     ts : Union[pd.DataFrame, pd.Series]
    #         Time series to detect outliers in.
    #     seasonal_decomposer : BaseDecomposition
    #         Seasonal decomposition model.
    #     hybrid : bool, optional
    #         Whether to use the hybrid ESD test statistic, by default False
    #     max_anomalies : int, optional
    #         Maximum number of anomalies to detect, by default 10
    #     alpha : float, optional
    #         Significance level, by default 0.05
        
    #     Returns
    #     -------
    #     pd.Series
    #         Boolean mask of outliers.
    #     """

    #     if max_anomalies >= len(ts) / 2:
    #         raise ValueError(
    #             "The maximum number of anomalies must be less than half the size of the time series."
    #         )

    #     decomposition = seasonal_decomposer.fit(ts)
    #     # Checking if MultiSeasonalDecomposition
    #     # if hasattr(seasonal_decomposer, "seasonal_model"):
    #     #     seasonal = np.sum(list(decomposition.seasonal.values()), axis=0)
    #     # else:
    #     seasonal = decomposition.total_seasonality
    #     residual = ts - seasonal - np.median(ts)
    #     outliers = self.generalized_esd(
    #         residual, max_anomalies=max_anomalies, alpha=alpha, hybrid=hybrid)
    #     return outliers
    
    def detect_outlier_generalized_esd(self, df, max_anomalies=10, alpha=0.05, hybrid=False, print_=True):
        """
        Generalized ESD (Extreme Studentized Deviate) for detecting outliers in time series. More sophisticated than the STD but still uses 
        the same assumptions of normality. Its based om Grubbs statistical test, which is used to find a single
        outlier in normally distributed data. ESD iteratively removes the most extreme value and recalculates
        the critical value based on the remaining data.

        https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm

        Parameters
        ----------
        ts : Union[pd.DataFrame, pd.Series]
            Time series to detect outliers in.
        max_anomalies : int, optional
            Maximum number of anomalies to detect, by default 10.
            The number of times the Grubbs' Test will be applied to the ts.
        alpha : float, optional
            Significance level, by default 0.05
        hybrid : bool, optional
            Whether to use the hybrid ESD test statistic, by default False
            A flag that determines the type of z-score.
        
        Returns
        -------
        pd.Series
            Boolean mask of outliers.
        """
        # select only the numeric columns
        numeric_cols = df.select_dtypes(include=np.number).columns

        # create an empty DataFrame to store the mask for each column
        outlier_masks = pd.DataFrame(columns=numeric_cols, index=df.index)

        for col in numeric_cols:
            ts = df[col].values
            ts = np.ma.array(
                ts
            )
            test_statistics = []
            num_outliers = 0
            for curr in range(max_anomalies):
                test_idx, test_val = self.calculate_test_statistic(ts, hybrid=hybrid)
                critical_val = self.calculate_critical_value(len(ts) - curr, alpha)
                if test_val > critical_val:
                    num_outliers = curr
                test_statistics.append(test_idx)
                ts[
                    test_idx
                ] = (
                    np.ma.masked
                )
            anomalous_indices = test_statistics[: num_outliers + 1] if num_outliers > 0 else []
            outlier_mask = np.zeros_like(ts)
            outlier_mask[anomalous_indices] = 1
            outlier_mask = outlier_mask.astype(bool)
            if print_:
                print("Nº de Outliers: ",outlier_mask.sum(), "% de Outliers: ", outlier_mask.mean(), "%")
            outlier_masks[col] = outlier_mask   
        return outlier_masks
    

    
    def detect_outlier_multivariable_isolation_forest(self,df,contaminacion=0.01,n_estimators=500,plot=True,random_state=2023):
        """
        Isolation Forest for detecting outliers in multivariate time series. It is based on the idea of isolating outliers in a dataset by randomly
        selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
        https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to detect outliers in.
        contaminacion : float, optional
            The amount of contamination of the data set, i.e. the proportion of outliers in the data set.
            Used when fitting to define the threshold on the decision function. by default 0.01
        n_estimators : int, optional
            The number of base estimators in the ensemble. by default 100
        plot : bool, optional
            Whether to plot the results, by default True
        
        Returns
        -------
        pd.DataFrame
            Dataframe with the outliers detected.
        """
        #obatain the numeric columns of the dataframe
        numeric_cols = df.select_dtypes(include=np.number).columns
        #Isolation Forest
        ISO_FOREST=IsolationForest(n_estimators=n_estimators,
                    max_samples=0.4, 
                    contamination=contaminacion, 
                    max_features=1.0, 
                    bootstrap=True, 
                    n_jobs=-1, 
                    random_state=random_state, 
                    verbose=0, 
                    warm_start=False)
        #fit the model
        ISO_FOREST.fit(df[numeric_cols])
        outliers=ISO_FOREST.predict(df[numeric_cols])
        df_anomaly=df[numeric_cols].copy()
        df_anomaly[f'MULTIVARIABLE_ISO_FOREST_{contaminacion}']=outliers
        #print the percentage of outliers
        print("Nº de Outliers: ",df_anomaly[f'MULTIVARIABLE_ISO_FOREST_{contaminacion}'].value_counts()[-1], ",  % de Outliers: ",
               df_anomaly[f'MULTIVARIABLE_ISO_FOREST_{contaminacion}'].value_counts(normalize=True)[-1]*100, "%")
        if plot: #plot the results
            print(f"The PCA is only for plotting purposes, the model is not trained with it. The model is trained with the original data. Model arguments are: contamination={contaminacion}, n_estimators=500, max_samples=0.4, max_features=1.0, bootstrap=True, n_jobs=-1, random_state={random_state}, verbose=0, warm_start=False")
            scaler = StandardScaler()
            X_transformed = scaler.fit_transform(X=df[numeric_cols])
            pca = PCA(n_components=3,) #Tanatas compoentes como variables tienen los datos y ya posteriormente elegimos las optimas
            X_pca = pca.fit_transform(X_transformed)
            exp_variance = pd.DataFrame(data=pca.explained_variance_ratio_, index = ['PC' + str(n_pca + 1) for n_pca in range(pca.n_components)], columns=['Exp_variance'])
            exp_variance['cum_Exp_variance'] = exp_variance['Exp_variance'].cumsum()
            fig = go.Figure(data=[go.Scatter3d(x=X_pca[:,0], y=X_pca[:,1], z=X_pca[:,2], mode='markers', marker=dict(color=outliers, size=3, opacity=0.8, colorscale='viridis'))])
            fig.update_layout(title='Isolation Forest', scene = dict(
                            xaxis_title='PC1',
                            yaxis_title='PC2',
                            zaxis_title='PC3'),
                            width=1400,
                            margin=dict(r=1, l=5, b=5, t=40))
            #add title to the plot and legend of anomaly
            fig.update_layout(title_text="Isolation Forest", title_x=0.5)
            #annotate the % of variance explained by each PC3 out of the 3D
            fig.add_annotation(x=0.5, y=1, text=f"Three principal components represents a variance of %"+ str(round(exp_variance.cum_Exp_variance["PC3"]*100,4))
                            +" of original data",
                                showarrow=False,
                                font=dict(size=16, color="black"))

            #add legend of anomaly color
            fig.show()

        #return an outlier mask
        return (df_anomaly[f'MULTIVARIABLE_ISO_FOREST_{contaminacion}'].apply(lambda x: True if x==-1 else False)).to_frame()

     
    
    def summary(self, df,iqr_multiple=1.5,sd_multiple=3,isolation_outlier_fraction=0.01,generalized_esd={"max_anomalies":10, "alpha":0.05, "hybrid":False}):
        #IQR
        outliers_iqr=self.detect_outlier_iqr(df,iqr_multiple=iqr_multiple,print_=False)
        percentage_outliers_iqr=outliers_iqr.mean()*100
        #SD
        outliers_sd=self.detect_outlier_sd(df,sd_multiple=sd_multiple,print_=False)
        percentage_outliers_sd=outliers_sd.mean()*100
        #Isolation Forest
        outliers_isolation_forest=self.detect_outlier_isolation_forest(df,outlier_fraction=isolation_outlier_fraction,print_=False)
        percentage_outliers_isolation_forest=outliers_isolation_forest.mean()*100
        #Generalized ESD
        outliers_generalized_esd=self.detect_outlier_generalized_esd(df,max_anomalies=generalized_esd["max_anomalies"],
                                                                       alpha=generalized_esd["alpha"],hybrid=generalized_esd["hybrid"],print_=False)
        percentage_outliers_generalized_esd=outliers_generalized_esd.mean()*100

        #obatain the numeric columns of the dataframe
        numeric_cols = df.select_dtypes(include=np.number).columns

        #make a mutiindex dataframe of the methods and the columns variables of the df
        index = pd.MultiIndex.from_product([numeric_cols,['% Percentage Outliers','INDEX']])
        columns=[f'IQR_{iqr_multiple}', f'STD_{sd_multiple}', f'ISO FOREST_{isolation_outlier_fraction}', f'GEN ESD_{generalized_esd["max_anomalies"]}_{generalized_esd["alpha"]}']
        summary_ = pd.DataFrame(index=index, columns=columns)
        for col in numeric_cols:
            #fill the dataframe with the values of the previous methods 
            #IQR
            summary_.loc[(col, '% Percentage Outliers'),f'IQR_{iqr_multiple}'] = percentage_outliers_iqr[col]
            summary_.loc[(col, 'INDEX'),f'IQR_{iqr_multiple}'] = outliers_iqr[col][outliers_iqr[col]==True].index
            #SD
            summary_.loc[(col, '% Percentage Outliers'),f'STD_{sd_multiple}'] = percentage_outliers_sd[col]
            summary_.loc[(col, 'INDEX'),f'STD_{sd_multiple}'] = outliers_sd[col][outliers_sd[col]==True].index
            #Isolation Forest
            summary_.loc[(col, '% Percentage Outliers'),f'ISO FOREST_{isolation_outlier_fraction}'] = percentage_outliers_isolation_forest[col]
            summary_.loc[(col, 'INDEX'),f'ISO FOREST_{isolation_outlier_fraction}'] = outliers_isolation_forest[col][outliers_isolation_forest[col]==True].index
            #Generalized ESD
            summary_.loc[(col, '% Percentage Outliers'),f'GEN ESD_{generalized_esd["max_anomalies"]}_{generalized_esd["alpha"]}'] = percentage_outliers_generalized_esd[col]
            summary_.loc[(col, 'INDEX'),f'GEN ESD_{generalized_esd["max_anomalies"]}_{generalized_esd["alpha"]}'] = outliers_generalized_esd[col][outliers_generalized_esd[col]==True].index
        #summary_.style.apply(lambda x: ['background: red' if x.name[1]=='% Percentage Outliers' and v > 5 else '' for v in x], axis=1)
       
        
        return summary_
    

#--------------------------------------------------------PLOT DATA--------------------------------------------------------#
class ExploreManager:
    def __init__(self,df):
        self.df=df



    def plot_correlations(self, method='pearson', figsize=(1000,1000), colorscale='agsunset', title=None, title_size=24, label_size=14, annotation_font_size=10, save=False, save_path="./imgs/correlations/",show=True,autosize=True,
                      margin=dict(t=150)):
        """
        Plotly heatmap of the correlation matrix of a dataframe

        Parameters
        ----------
        df : pd.DataFrame

        figsize : tuple, optional
            figsize adjusts the size of the plot. The default is (1000,1000).
        
        colorscale : str, optional
            The color scale used in the plot. The default is 'agsunset'.
            For more colorscales visit https://plotly.com/python/builtin-colorscales/
        
        title : str, optional
            The title of the plot. The default is None.
        
        title_size : int, optional
            The size of the plot's title. The default is 24.

        label_size : int, optional
            The size of the plot's labels. The default is 14.

        annotation_font_size : int, optional
            The size of the annotation's font inside the heatmap's cells. The default is 10.

        save : bool, optional
            Whether to save the plot as a file. The default is False.

        save_path : str, optional
            The path where to save the plot. The default is "./imgs/correlations/".

        Returns
        -------
        None.
        """
        assert isinstance(self.df, pd.DataFrame), "df must be a pd.DataFrame"
        assert isinstance(figsize, tuple), "figsize must be a tuple"
        assert isinstance(colorscale,str), "colorscale must be a str"
        
        fig = ff.create_annotated_heatmap(z=self.df.corr().values, 
                                        x=self.df.corr().columns.tolist(), 
                                        y=self.df.corr().columns.tolist(), 
                                        annotation_text=self.df.corr().round(2).values, 
                                        font_colors=['black'], 
                                        showscale=True)
        fig.update_layout(title=title, 
                        title_font=dict(size=title_size),
                        xaxis=dict(tickfont=dict(size=label_size)),
                        yaxis=dict(tickfont=dict(size=label_size)),autosize=autosize, margin=margin)
        fig.update_traces(colorscale='agsunset')

        # Increase annotation font size
        for i in range(len(fig.layout.annotations)):
            fig.layout.annotations[i].font.size = annotation_font_size

        fig.update_layout(width=figsize[0], height=figsize[1], autosize=autosize, margin=margin)
        if show:
            fig.show()

        # Check if save is set to True
        if save:
            # Check if the directory exists
            if not os.path.exists(save_path):
                # If the directory does not exist, create it
                os.makedirs(save_path)

            # Save the figure
            
            pio.write_image(fig, save_path + f'{title}_correlation_heatmap.png')

        self.fig=fig   

        return fig





    def plot_distribution(self, bins:int=50, figsize:tuple=(600, 400), save_name="", category_column=None, x_range=None, shared_yaxes:bool=False, shared_xaxes:bool=False, histnorm=None, label_size:int=14, tick_size:int=12, title_size:int=16):
        """
        Plot the distribution of the numeric columns in the dataset. When category_column is provided, the distribution of each category is plotted 
        with the boxplot. Otherwise, the distribution of the entire dataset is plotted with the histogram. You can select the number of bins for the histogram,
        the range of the x-axis and the type of normalization for the histogram. histnorm="probability density" or None.

        Parameters
        ----------
        bins : int, optional
            Number of bins for the histogram, by default 50
        figsize : tuple, optional
            Size of the figure, by default (1000, 600)
        category_column : str, optional
            Column to use for the category, by default None
        x_range : tuple, optional
            Range of the x-axis, by default None
        shared_yaxes : bool, optional
            Whether to share the y-axis, by default False
        shared_xaxes : bool, optional
            Whether to share the x-axis, by default False
        histnorm : str, optional
            Type of normalization for the histogram, by default None
            "probability density" or None
        label_size : int, optional
            Size of the axis labels, by default 14
        tick_size : int, optional
            Size of the axis ticks, by default 12
        title_size : int, optional
            Size of the plot's title, by default 16
        
        Returns
        -------
        plotly.graph_objects.Figure
            Distribution plot
        """
        assert category_column is None or isinstance(category_column, str), "category_column must be a str or None"
        numeric_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        assert isinstance(bins, int) and bins>0 , "bins must be an int"
        for i, col_ in enumerate(numeric_columns):

            if category_column is not None: #For categorical selection
                hist = px.histogram(
                    self.df, 
                    x=col_, 
                    nbins=bins, 
                    color=category_column,
                    histnorm=histnorm,
                    pattern_shape=category_column,
                    marginal="box",
                    barmode="overlay")

            else: #For no categorical selection
                
                hist = px.histogram(self.df, x=col_, nbins=bins,histnorm=histnorm,marginal="box",barmode="overlay")
            hist.update_xaxes(title_text=str(col_), title_font=dict(size=label_size), tickfont=dict(size=tick_size))
            #add the subplot title
            hist.update_yaxes(title_text="Count", title_font=dict(size=label_size), tickfont=dict(size=tick_size))

            hist.update_layout(height=figsize[1], width=figsize[0], title_text=f"Distribution of {col_}", title_font=dict(size=title_size), title_x=0.5)
            hist.show()

                    # Check if save is set to True


                #pio.write_image(hist, save_path + f'{col_}_dist_{save_name}.png')



    def correlation_sum_combinations(self , target_var:str,remove_vars:list=None):
        """
        Funcion que devuelve la combinacion de variables sumadas que maximiza la correlacion con la variable objetivo

        Parameters
        ----------
        df : pandas dataframe
            dataframe con las variables a analizar
        target_var : str
            nombre de la variable objetivo con la que se quiere calcular la correlacion
        remove_vars : list, optional
            lista de variables a eliminar del analisis. The default is None.
        Returns
        -------
        correlations_df : pandas dataframe
            dataframe con las correlaciones de cada combinacion de variables sumadas, ordenadas de mayor a menor
        """
        assert isinstance(target_var,str), "target_var debe ser un string"
        assert target_var in self.df.columns, "target_var debe ser una columna del dataframe"
        assert remove_vars is None or isinstance(remove_vars,list), "remove_vars debe ser una lista"
        #all remove vars must be in df
        if remove_vars is not None:
            assert all([remove_var in self.df.columns for remove_var in remove_vars]), "remove_vars debe ser una lista de variables del dataframe"

        var_list=self.df.select_dtypes(include=np.number).columns.tolist() #lista con todas las variables numericas
        var_list.remove(target_var)

        if remove_vars is not None and isinstance(remove_vars,list):
            for remove_var in remove_vars:
                var_list.remove(remove_var) 
        combinaciones=[] #lista con todas las combinaciones posibles de variables
        for L in range(len(var_list) + 1):
            for subset in itertools.combinations(var_list, L):
                #subset to list
                subset=list(subset)
                combinaciones.append(subset)
        correlations = {} #diccionario con las correlaciones de cada combinacion
        for comb in combinaciones:
            try:
                corr, _ = pearsonr(self.df[list(comb)].mean(axis=1), self.df[target_var]) #si la combinacion es de mas de una variable, se hace la media
            except:
                corr, _ = pearsonr(self.df[list(comb)], self.df[target_var]) #si la combinacion es de una sola variable, no se puede hacer la media

            key = " & ".join(list(comb)) #se crea la key para el diccionario
            correlations[key] = corr #se añade la correlacion al diccionario
        correlations_df=pd.DataFrame.from_dict(correlations,orient="index",columns=["corr"]) #se crea un dataframe con el diccionario
        correlations_df.sort_values(by="corr",ascending=False,inplace=True) #se ordena el dataframe por correlacion
        return correlations_df
    

    def detect_values(self,objective_value,selected_columns:list) -> tuple:
        """
        This function detects the rows where the objective value is present in the selected columns.
        It also detects the rows where the objective value is not present in the selected columns.

        Parameters
        ----------
        selected_columns : list
            Lista de columnas donde se van a buscar los valores que deben de pertencer a df.
        objective_value : int,float,str
            El valor que se va a buscar en las columnas seleccionadas.
        
        Returns
        -------
        tuple
            1. pandas.DataFrame
                El dataframe con las filas donde el valor objetivo está presente en las columnas seleccionadas.
            2. pandas.DataFrame
                El dataframe con las filas donde el valor objetivo no está presente en las columnas seleccionadas.
            3. pandas.DataFrame
                El dataframe con las filas donde el valor objetivo no está presente en las columnas seleccionadas.
            4. int
                Número de filas donde el valor objetivo no está presente en las columnas seleccionadas.
        """
        assert isinstance(selected_columns,list), "selected_columns debe ser una lista de las columnas donde se van a buscar los valores"
        assert isinstance(objective_value,(int,float,str)), "objective_value debe ser un int, float o str"
        assert all([column in self.df.columns for column in selected_columns]), "selected_columns debe ser una lista de columnas del dataframe"
        print("Detecting values... the are 4 outputs for this funcion so a,b,c,d=funcion()")
        s1=pd.Series(dtype=float) #dtype float para que no salga warning por actualización
        s2=pd.Series(dtype=float)
        s3=pd.Series(dtype=float)   
        idxs_list=[]           
        for column in selected_columns:
            if objective_value in [np.nan,"Nan",None]:
                idxs=self.df[column][self.df[column].isnull()].index.values
                idxs_list.extend(idxs.tolist())
                sum_=self.df[column].isna().sum()
            else:
                idxs=self.df[column][self.df[column]==objective_value].index.values
                idxs_list.extend(idxs.tolist())
                sum_=(self.df[column]==objective_value).sum()
            s1[column]=idxs
            s2[column]=np.array(sum_)              
        s3_=pd.Series(idxs_list)
        s4=pd.Series(dtype=float)
        repeats=sorted(s3_.value_counts().unique())
        for n in repeats:  
            idx=(s3_.value_counts()==n)[(s3_.value_counts()==n)==True].index.values
            s3[str(n)]=idx
            s4[str(n)]=idx.size
                
        df4=self.df[self.df[selected_columns].all(axis=1)==False] 
        #renaming the output columns
        s1.name=str(objective_value)
        s2.name="sum"+str(objective_value)
        s3.name=str(objective_value)
        s3.name="sum"+str(objective_value)
        return pd.concat([s1.to_frame(),s2.to_frame()],axis=1),pd.concat([s3.to_frame(),s4.to_frame()],axis=1),df4, len(np.unique(idxs_list))


    def plot_pairplot(self, y_var:list, x_var:list=None, hues:list=None,split_vars:int=None,alpha=0.4,size=6,aspect=8/10):
        print("NOTE: Make sure you encode to category the variables you want to plot as hue")
        """
        This function plots a pairplot with the selected variables and the selected hue for categorical variables.

        Parameters
        ----------
        y_var : list
            Lista de variables que se van a plotear.

        x_var : list, optional
            Lista de variables que se van a plotear. The default is None.
            Por defecto se plotearan todas las variables numericas.
        hues : list, optional
            Lista de variables categoricas que se van a plotear. The default is None.

        split_vars : int, optional
            Number of variables to plot in each pairplot. The default is None.

        alpha : float, optional
            Alpha is the transparency of the dots. The default is 0.4.
        
        size
            Size of the plot. The default is 10.
        
        aspect
            Aspect of the plot. The default is 8/10.

        Returns
        -------
        None.
            Plots a pairplot with the selected variables and the selected hue for categorical variables.
        """
        assert hues is None or isinstance(hues, list), "hues must be None or a list"
        assert x_var is None or isinstance(x_var, list), "x_vars must be None or a list"
        df2=self.df.copy()
        if y_var is str:
            y_var=[y_var]

        if hues is None:
            hues=df2.select_dtypes(include=['category']).columns.tolist()
        hues_drop=df2.select_dtypes(include=['category']).columns.tolist()
        hues_drop.extend(y_var)

        if len(hues_drop)!=0:

            if isinstance(split_vars,int):
                print("NOTE: Because you selected split_vars, the pairplot is going to be splited due to  size of the variables")
                #split the vars of df in the  equally in the number of split_vars
                split_vars=split_vars
                var_list=df2.drop(columns=hues_drop).columns.tolist()
                var_list_split=np.array_split(var_list,split_vars)
                var_list_split=[var.tolist() for var in var_list_split]
                #every list in var_list_split needs to have the y_var one time
                for var in var_list_split:
                    for y in y_var:
                        var.append(y)
                    #all the categories of the hue need to be in all the lists
                    if isinstance(hues,list):
                        for hue in hues:
                            if hue not in var:
                                var.append(hue)
                    else:
                        hues=[]
                        for hue in df2.select_dtypes(include=['category']).columns.tolist():
                            if hue not in var:
                                for var in var_list_split:
                                    var.append(hue)
                            
                                hues.append(hue)

                for hue in hues:
                    for split in var_list_split:
                        
                        sns.pairplot(data=df2[split], y_vars=y_var, hue=hue,diag_kws=dict(alpha=alpha), plot_kws=dict(alpha=alpha),size=size,aspect=aspect)
                    plt.show()
            else:
                for hue in hues:
                    sns.pairplot(data=df2, y_vars=y_var, x_vars=x_var, hue=hue,diag_kws=dict(alpha=alpha), plot_kws=dict(alpha=alpha),size=size,aspect=aspect)

        else:
             sns.pairplot(data=df2, y_vars=y_var, x_vars=x_var,diag_kws=dict(alpha=alpha), plot_kws=dict(alpha=alpha),size=size,aspect=aspect)

        plt.show()


    def plot_cointegration(self, var1, var2,sequence=1,x_title='Número de registros anteriores calculados', show=True, figsize=(1500,900), x_tickfont=14, y_tickfont=14):
        # Subplots con dos filas y una columna
        fig = make_subplots(rows=2, cols=1)

        # Listas para guardar los resultados
        cointegrations = []
        p_values = []
        if sequence==1:
            div=1
        else:
            div=2
        x=list(range(int(2*sequence/div), len(self.df) + 1,sequence))
        x_2=list(range(1,len(x)+1))
        x_3=[1, (len(self.df)/sequence)]

        for i in range(int(2*sequence/div), len(self.df) + 1,sequence):  # comenzar desde 5 porque necesitamos al menos 5 puntos para calcular la cointegración
            df_tmp = self.df.iloc[-i:][[var1, var2]]
            coint_t, p_value, _ = coint(df_tmp[var1], df_tmp[var2])
            cointegrations.append(coint_t)  # estadístico de cointegración de la prueba Engle-Granger
            p_values.append(p_value)  # valor p de la prueba

        # Agregar los resultados al primer subplot
        fig.add_trace(go.Scatter(
            x=x_2,  # número de observaciones
            y=cointegrations,  # cointegración
            mode='lines',
            name='Estadístico de cointegración a lo largo del tiempo',
        ), row=1, col=1)

        # Colores apagados para las líneas de los valores críticos
        colors = ['#D2B48C', '#FF7F50', '#B22222']

        # Agregar líneas horizontales para los valores críticos al primer subplot
        _, _, crit_value = coint(self.df[var1], self.df[var2])
        for i, key in enumerate(['1%', '5%', '10%']):
            fig.add_trace(
                go.Scatter(
                    x=x_3,
                    y=[crit_value[i], crit_value[i]],
                    mode='lines',
                    name=f'Valor crítico al {key}',
                    line=dict(color=colors[i], dash="dash"),
                ), 
                row=1, col=1
            )

        # Agregar los resultados al segundo subplot
        fig.add_trace(go.Scatter(
            x=x_2,  # número de observaciones
            y=p_values,  # valor p
            mode='lines',
            name='Valor p a lo largo del tiempo',
        ), row=2, col=1)

        # Agregar una línea horizontal al segundo subplot para indicar el umbral de significancia de 0.05
        fig.add_trace(
            go.Scatter(
                x=x_3,
                y=[0.05, 0.05],
                mode='lines',
                name='Umbral de significancia del 0.05',
                line=dict(color="Grey", dash="dash"),
            ),
            row=2, col=1
        )

        # Configurar los ejes
        fig.update_xaxes(title_text=x_title, row=1, col=1)
        fig.update_yaxes(title_text='Estadístico de cointegración', row=1, col=1)
        fig.update_xaxes(title_text=x_title, row=2, col=1)
        fig.update_yaxes(title_text='Valor p', row=2, col=1)

        # Configurar el título del gráfico
        fig.update_layout(height=figsize[1], width=figsize[0], title_text=f"Análisis Cointegración y valor p de {var1} vs {var2}")

        # Mostrar la figura
        if show:
            fig.show()

        self.fig_cointegration=fig

    def plot_correlation(self, var1, var2, sequence=1, x_title='Número de registros anteriores calculados', x_tickfont=14, y_tickfont=14, figsize=(1500,900),show=True):
        fig = go.Figure()

        pearson_corrs = []
        spearman_corrs = []
        if sequence==1:
            div=1
        else:
            div=2

        x=list(range(int(2*sequence/div), len(self.df) + 1,sequence))
        x_2=list(range(1,len(x)+1))
        for i in range(int(2*sequence/div), len(self.df) + 1, sequence):  # comenzar desde 5 porque necesitamos al menos 5 puntos para calcular la correlación
            df_tmp = self.df.iloc[-i:][[var1, var2]]
            pearson_corr, _ = pearsonr(df_tmp[var1], df_tmp[var2])  # calcular la correlación de Pearson (lineal)
            spearman_corr, _ = spearmanr(df_tmp[var1], df_tmp[var2])  # calcular la correlación de Spearman (monotónica)
            pearson_corrs.append(pearson_corr)
            spearman_corrs.append(spearman_corr)

        fig.add_trace(go.Scatter(
            x=x_2,  # número de observaciones
            y=pearson_corrs,  # correlación de Pearson
            mode='lines',
            name='Pearson Linear Correlation',
        ))
        fig.add_trace(go.Scatter(
            x=x_2,  # número de observaciones
            y=spearman_corrs,  # correlación de Spearman
            mode='lines',
            name='Spearman Monotonic Correlation ',
            line=dict(color='grey')

        ))
        # Establecer los nombres de los ejes
        fig.update_layout(
            xaxis_title=x_title,
            yaxis_title='Correlación',
            autosize=False,
            width=figsize[0],   # Cambia el tamaño en función de tus necesidades
            height=figsize[1],
            title=f"Evolución Correlación {var1} vs {var2}",
            )

        fig.update_xaxes(tickfont=dict(size=x_tickfont))  # Incrementar tamaño de los ticks del eje X
        fig.update_yaxes(tickfont=dict(size=y_tickfont))  # Incrementar tamaño de los ticks del eje Y

        # Mostrar la figura
        if show:
            fig.show()

        self.fig_correlation=fig





class SimilarPattern:
    """
    Class to obtain the similar pattern of a given sequence. The sequence could be 2D or 1D.
    For 2D the columns are stacked to obtain a 1D sequence, ready to be used by stumpy.
    """
    def __init__(self,df, subsequence):
        if not isinstance(df, pd.DataFrame):
            df=df.to_frame()
            
        self.df = df
        self.subsequence = subsequence
        self.y = df.stack().reset_index(drop=True)
        self.x = df.stack().reset_index(drop=True).index
        self.m = subsequence*df.columns.size
        
    def get_matrix_profile(self):

        matrix_profile = stumpy.stump(self.y, self.m)
        self.matrix_profile_df = pd.DataFrame(matrix_profile, columns=['profile', 'profile index', 'left profile index', 'right profile index'])
        return self.matrix_profile_df
    
    def _get_values(self,df,columns,remove_):
        """
        Obtains the different values of a dataframe selecting the columns to seek
        
        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe to obtain the values
        columns: list
            Columns to obtain the values
        Returns
        -------
        values: list
            List of the values of the columns
        """
        values=[]
        for col in columns:
            values.extend(df[col].unique())
        values=np.unique(values).tolist()
        values.remove(remove_)
        #make an array of int
        return np.array(values)

    def get_similar_pattern(self,date):
        """
        Obtains the similar date pattern to the given date
        
        Parameters
        ----------
        date: str
            Date to obtain the similar pattern
        Returns
        -------
        patron: str or tuple
            Date of the similar pattern
        """
        slice_index=self.df.index.get_loc(date)
        start_index=slice_index.start
        self.stumpy_index=start_index*self.df.columns.size
        patron=0 #initialize the patron variable
        matrix_profile_df=self.get_matrix_profile()
        matrix_profile_df_=matrix_profile_df[(matrix_profile_df['right profile index'] != -1) & (matrix_profile_df['left profile index'] != -1)]
        try:
            self.seek_motif=matrix_profile_df[matrix_profile_df['profile index'] == self.stumpy_index]
            #order the values of the seek motif smallest to biggest on column profile
            self.seek_motif=self.seek_motif.sort_values(by="profile")

        
            close_values=self._get_values(self.seek_motif,['left profile index','right profile index'],self.stumpy_index.item())
        except:
            try:
                self.seek_motif=matrix_profile_df[matrix_profile_df['right profile index'] == self.stumpy_index]
                self.seek_motif=self.seek_motif.sort_values(by="profile")
                close_values=self._get_values(self.seek_motif,['left profile index','right profile index'],self.stumpy_index.item())

            except:
                try:
                    self.seek_motif=matrix_profile_df[matrix_profile_df['left profile index'] == self.stumpy_index]
                    self.seek_motif=self.seek_motif.sort_values(by="profile")
                    close_values=self._get_values(self.seek_motif,['left profile index','right profile index'],self.stumpy_index.item())
                except:
                    patron= ["No se ha podido encontrar el día más parecido"]

        if patron != ["No se ha podido encontrar el día más parecido"]:            

            self.stumpy_close_values=close_values
            #if in the self.stumpy close values ther is -1 value, and tehres also a 0 quit the -1 and if there irs only a -1 alone convert it to 0
            if -1 in self.stumpy_close_values:

                if 0 in close_values:
                    self.stumpy_close_values=self.stumpy_close_values[self.stumpy_close_values!=-1]
                else:
                    self.stumpy_close_values[self.stumpy_close_values==-1]=0
            self.close_values=close_values/self.df.columns.size
            self.close_values=self.close_values.astype(int)
                

            patron= [self.df.iloc[int(i)].to_frame().T.index[0].strftime('%Y-%m-%d') for i in self.close_values]
        else:
            pass

        return patron
    
    def plot_similar_pattern(self,date,figsize=(1200,3950),title_font_size=45,legend_size=35,annotation_font_size=40,x_tickfont=20,y_tickfont=20,show=True,vertical_spacing=0.1):
        """
        Plot similar pattern of a given date
        Parameters
        ----------
        date : str
            Date to plot similar pattern
        """
        patron=self.get_similar_pattern(date)
        #drop on eif its duplicated
        patron=list(set(patron))
        self.patron=patron
        height_adjuts= len(patron)
        if patron != ["No se ha podido encontrar el día más parecido"]:
            try:
                patron_profile=[pat + ", " + str(round(self.seek_motif.reset_index().profile.iloc[i],3)) for i, pat in enumerate(patron)]
            except:
                
                patron_profile=patron

            fig = make_subplots(rows=len(patron), cols=1, vertical_spacing=vertical_spacing, subplot_titles= patron_profile , )

            for i,idx in enumerate(self.stumpy_close_values):
                plot_y = self.y.iloc[idx:idx.item()+self.m].to_list()
                plot_base = self.y.iloc[self.stumpy_index:self.stumpy_index+self.m].to_list()
            
                fig.add_trace(go.Scatter(x=np.linspace(0,self.subsequence-1,len(list(range(len(plot_y))))), y=plot_y, name=patron[i] ), row=i+1, col=1)
                fig.add_trace(go.Scatter(x=np.linspace(0,self.subsequence-1,len(list(range(len(plot_base))))), y=plot_base, name=date, line={'color': '#000000'}), row=i+1, col=1)
                fig.update_yaxes(title_text="Serie {}".format(i+1), row=i+1, col=1)

            #indicate all int x values in the x axis
                fig.update_xaxes(tickmode = 'array', tickvals = np.linspace(0,self.subsequence-1,self.subsequence), row=i+1, col=1)
            fig.update_layout(title_text=f"Patrones similares para {date} {self.df.columns.values}", title_x=0.5, height=800+height_adjuts*100)
            #x name as Hour
            fig.update_xaxes(title_text="Hour", tickfont=dict(size=x_tickfont))
            fig.update_yaxes(title_text="Valor", tickfont=dict(size=y_tickfont))

            if len(patron) ==1:
                height=figsize[0]/1.4
                width=figsize[1]

            #tight layout automatically adjusts subplot params so that the subplot(s) fits in to the figure area
            fig.update_layout(showlegend=True, title_x=0.5, title_y=0.999, title_font_size=title_font_size, title_font_color="black", title_font_family="Arial", title_xanchor="center", title_yanchor="top",
                            margin=dict(t=100, b=50, l=50, r=50),legend=dict(font=dict(size=legend_size)), height=figsize[0], width=figsize[1]) 
            fig.update_annotations(font_size=annotation_font_size)
            #increase size of xticks values
            
            
        else:
            fig = go.Figure()

            fig.add_annotation(
                dict(
                    x=0.5, # posición en x
                    y=0.5, # posición en y
                    showarrow=False,
                    text="No se ha podido encontrar el día más parecido", # mensaje de texto
                    xref="paper",
                    yref="paper",
                    font=dict(size=annotation_font_size+5, color='black'), # tamaño y color del texto
                )
            )
            fig.update_layout(title_text=f"Patrones similares para {date} {self.df.columns.values}", title_x=0.5, height=800+height_adjuts*100, title_font_size=title_font_size)
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), # esconde el eje x
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), # esconde el eje y
                height=figsize[0],

                width=figsize[1])
            
        if show:
            fig.show()

        self.fig=fig


#------------------------------------------------------------------------------------------------------EUCLIDIAN DISTANACE--------------------------------------------#



class EuclidianSequence:

    def __init__(self, df, sequence):
        self.df = df
        self.sequence = sequence
        self.y = df.stack().reset_index(drop=True)
        self.m = sequence * df.columns.size

    def get_similar_pattern(self, date):

        df_compute = self.df.loc[date]
        self.y_seek = df_compute.stack().reset_index(drop=True)

        euclidian_distances = []
        indices = []
        for count, i in enumerate(range(0, self.y.shape[0], self.m)):
            moving_df = self.y.iloc[i:i+self.m]
            
            # Ensure the moving_df and df_compute has the same length, otherwise skip
            if len(moving_df) != len(self.y_seek):
                continue
            distancia = distance.euclidean(self.y_seek.values, moving_df.values)
            euclidian_distances.append(distancia)
            seek_index = i // self.df.columns.size

            indices.append(self.df.index[seek_index])

        # Create a DataFrame with the euclidean distances and the index
        euclidian_distances_df = pd.DataFrame({"index": indices, "euclidian_distances": euclidian_distances})
        # Sort the DataFrame by euclidean distances
        euclidian_distances_df = euclidian_distances_df.sort_values(by="euclidian_distances")
        euclidian_distances_df.reset_index(drop=True, inplace=True)

        return euclidian_distances_df.iloc[1:]
    


    def plot_similar_pattern(self,date,figsize=(1200,3950),title_font_size=45,legend_size=35,annotation_font_size=40,x_tickfont=20,y_tickfont=20,show=True,vertical_spacing=0.1):
            """
            Plot similar pattern of a given date
            Parameters
            ----------
            date : str
                Date to plot similar pattern
            """
            patrons=self.get_similar_pattern(date)
            patrons=patrons.iloc[:5]
            patrons_date=patrons.iloc[:,0].apply(lambda x: x.strftime('%Y-%m-%d')).values

  
            #drop on eif its duplicated
            
            self.patron=patrons
            self.patron_date=patrons_date
            height_adjuts= len(patrons)
    
            patron_profile= [str(row[0].date()) + " , Euclidian Distance Value: " + str(round(row[1],2)) for index, row in patrons.iterrows()]



            fig = make_subplots(rows=len(patrons), cols=1, vertical_spacing=vertical_spacing, subplot_titles = patron_profile , )

            for i,p_date in enumerate(patrons_date):
                plot_y=self.df.loc[p_date].stack().reset_index(drop=True).to_list()
                plot_base = self.y_seek
            
                fig.add_trace(go.Scatter(x=np.linspace(0,self.sequence-1,len(list(range(len(plot_y))))), y=plot_y, name=patrons_date[i] ), row=i+1, col=1)
                fig.add_trace(go.Scatter(x=np.linspace(0,self.sequence-1,len(list(range(len(plot_base))))), y=plot_base, name=date, line={'color': '#000000'}), row=i+1, col=1)
                fig.update_yaxes(title_text="Serie {}".format(i+1), row=i+1, col=1)

            #indicate all int x values in the x axis
                fig.update_xaxes(tickmode = 'array', tickvals = np.linspace(0,self.sequence-1,self.sequence), row=i+1, col=1)
            fig.update_layout(title_text=f"Patrones similares para {date} {self.df.columns.values}", title_x=0.5, height=800+height_adjuts*100)
            #x name as Hour
            fig.update_xaxes(title_text="Hour", tickfont=dict(size=x_tickfont))
            fig.update_yaxes(title_text="Valor", tickfont=dict(size=y_tickfont))

            if len(patrons) ==1:
                height=figsize[0]/1.4
                width=figsize[1]

            #tight layout automatically adjusts subplot params so that the subplot(s) fits in to the figure area
            fig.update_layout(showlegend=True, title_x=0.5, title_y=0.999, title_font_size=title_font_size, title_font_color="black", title_font_family="Arial", title_xanchor="center", title_yanchor="top",
                            margin=dict(t=100, b=50, l=50, r=50),legend=dict(font=dict(size=legend_size)), height=figsize[0], width=figsize[1]) 
            fig.update_annotations(font_size=annotation_font_size)
            #increase size of xticks values
                
        
                
            if show:
                fig.show()

            self.fig=fig



class RecentSimilarPattern:


    def __init__(self, df, subsequence, select_columns=None):
        self.df_orig=df.copy()
        if isinstance(select_columns, list):
            self.df = df[select_columns]
        else:
            self.df = df

        self.subsequence = subsequence
        self.m = subsequence * self.df.columns.size
        self.df_stack=self.df.stack().reset_index(drop=True)
        self.query=self.df_stack.iloc[-self.m:]
        self.reference=self.df_stack.iloc[:-self.m]

    def matrix_profile(self):
        """
        Returns
        -------
        matrix_profile_df : pandas dataframe
            Dataframe with the matrix profile
        
        """
        results=[]
        query_=(self.query-self.query.min())/(self.query.max()-self.query.min())

        for i in range(0,self.df_stack.shape[0]+1):
            
            serie=self.reference.iloc[i:i+self.m].values

            if len(serie) == len(self.query.values):
                #normalize the serie and the query bewteen 0-1
                serie=(serie-serie.min())/(serie.max()-serie.min())
                #calculate the ecuclidean distance between the query and the serie
                distancia = distance.euclidean(serie , query_)
                result=[i,i+self.m,distancia]
                results.append(result)


        matrix_profile_=pd.DataFrame(results,columns=["index0","index1","distance"]).sort_values(by="distance",ascending=True)

        condition1a = (matrix_profile_["index0"] % self.df.columns.size == 0)
        # condition1b = (matrix_profile_["index0"] % 4 == 3)
        condition2a = (matrix_profile_["index1"] % self.df.columns.size == 0)
        # condition2b = (matrix_profile_["index1"] % 4 == 3)
        condition1 = condition1a #| condition1b
        condition2 = condition2a #| condition2b


        matrix_profile_df_4 = matrix_profile_[condition1 & condition2]

        self.matrix_profile_df=matrix_profile_df_4


        return matrix_profile_df_4
    
    def _iloc_translator(self,index):
        """
        Translates the index of the matrix profile to the index of the dataframe
        Parameters
        ----------
        index : int
            Index of the matrix profile
        Returns
        -------
        index : int
            Index of the dataframe
        """
        columns=self.df.columns.size
        return index//columns
    
    def plot_candles(self,n_plots:int=6, ahead:int=7):

        """
        Parameters
        ----------
        n_plots : int, optional
            Number of plots to show, by default 6

        ahead : int, optional
            Number of candles to show ahead of the most similar pattern, by default 7   

        Returns
        -------
        Plotly graph
            Plotly graph with the candles of the most similar patterns and the query
        
        """



        #if matrix profile has been executed
        if not hasattr(self, 'matrix_profile_df'):
            self.matrix_profile_df=self.matrix_profile()

        for k,row in enumerate(self.matrix_profile_df.iterrows()):
            if k>=n_plots:
                break

            index1=self._iloc_translator(row[0])

            df1_=self.df_orig.iloc[:-self.subsequence]
            df1 = df1_.iloc[index1:index1+self.subsequence]
            df1_ahead=df1_.iloc[index1+self.subsequence:index1+self.subsequence+ahead]
            df2 = self.df_orig.iloc[-self.subsequence:]

                
            fig = make_subplots(rows=1, cols=3, subplot_titles=(f'Más Parecido {df1.index[0]} : {df1.index[-1]}', f'Ahead {df1_ahead.index[0]} : {df1_ahead.index[-1]}', 'Query '+df2.index[0].strftime('%Y-%m-%d')+' : '+df2.index[-1].strftime('%Y-%m-%d')))

            #df1.index = df1.index.astype(str)
            df1_plot=df1.reset_index()
            fig.add_trace(go.Candlestick(x=df1_plot.index,
                                        open=df1_plot['precio_apertura'],
                                        high=df1_plot['precio_maximo'],
                                        low=df1_plot['precio_minimo'],
                                        close=df1_plot['precio_acordado']), row=1, col=1)


            
            df1_ahead_plot=df1_ahead.reset_index()
            fig.add_trace(go.Candlestick(x=df1_ahead_plot.index,
                                        open=df1_ahead_plot['precio_apertura'],
                                        high=df1_ahead_plot['precio_maximo'],
                                        low=df1_ahead_plot['precio_minimo'],
                                        close=df1_ahead_plot['precio_acordado']), row=1, col=2)


            


            # Crear datos para el segundo subplot

            df2_plot=df2.reset_index()
            fig.add_trace(go.Candlestick(x=df2_plot.index,
                                        open=df2_plot['precio_apertura'],
                                        high=df2_plot['precio_maximo'],
                                        low=df2_plot['precio_minimo'],
                                        close=df2_plot['precio_acordado']), row=1, col=3)

            # Actualizar la configuración del gráfico para que sea más alto
            fig.update_layout(height=1000, width=1900)
            #update title of the graph
            fig.update_layout(title=f"{k+1}_Distance Value: {round(row[1]['distance'],3)}  Subsequence: {self.subsequence}",title_x=0.5)
            fig.show()









  


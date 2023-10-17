import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import matplotlib.pyplot as plt

class MontecarloInterval:

    def __init__(self,y_preds:pd.DataFrame,spot:pd.DataFrame):

        """
        Se inicializa la clase con los datos de y_preds y spot

        Parameters
        ----------
        y_preds : pd.DataFrame
            DataFrame con las predicciones de y

        spot : pd.DataFrame

            DataFrame con los datos de spot

        Returns
        -------
        None.

        """

        assert isinstance(y_preds.index,pd.DatetimeIndex) and isinstance(spot.index,pd.DatetimeIndex), "Both index must be datetime"

        self.y_preds=y_preds
        self.spot=spot
        self.residuals=self.spot[spot.columns[0]]-self.y_preds[y_preds.columns[0]]

    def hist_residuals(self,bins:int=50):
        """
        compute the histogram of residuals

        Parameters
        ----------
        bins : int, optional
            DESCRIPTION. The default is 50.

        Returns
        -------
        None.
        
        """
        plt.hist(self.residuals,bins=bins)  

    def compute_hourly_montecarlo(self,n_iterations:int):
        """
        
        Esta función calcula el montecarlo por hora de la serie temporal de residuos

        Parameters
        ----------
        n_iterations : int
            Número de simulaciones a realizar.

        Returns
        -------
        None.
        self.simulated_paths: np.array
        
        """

        #assert data must be hourly in index
        hourly_std_devs = [np.std(self.residuals[self.residuals.index.hour == i]) for i in range(24)]

        # Simulación de Monte Carlo con restricciones y desviación estándar por hora
        num_simulations = n_iterations
        simulated_paths = []


        while len(simulated_paths) < num_simulations:
            simulated_demand = np.zeros(24)
            for t in range(24):
                forecast = self.y_preds.iloc[-24:].values.flatten()[t]  # Asumo que y es tu serie temporal
                perturbation = np.random.normal(0, hourly_std_devs[t])
                simulated_demand[t] = forecast + perturbation
            # Restricciones adicionales
            conditions = [
                simulated_demand[4] <= simulated_demand[21],
                simulated_demand[5] <= simulated_demand[21],
                simulated_demand[11] <= simulated_demand[20],
                simulated_demand[12] <= simulated_demand[20],
                simulated_demand[16] <= simulated_demand[21],
                simulated_demand[13] <= simulated_demand[21],
                simulated_demand[14] <= simulated_demand[21],
                simulated_demand[15] <= simulated_demand[21],
                simulated_demand[16] <= simulated_demand[18],
                simulated_demand[14] <= simulated_demand[19],
                simulated_demand[15] <= simulated_demand[19],
                simulated_demand[16] <= simulated_demand[19],
                simulated_demand[13] <= simulated_demand[20],
                simulated_demand[15] <= simulated_demand[20],
                simulated_demand[16] <= simulated_demand[20],
                simulated_demand[17] <= simulated_demand[19],
                simulated_demand[14] <= simulated_demand[20],
                simulated_demand[21] > simulated_demand[23],
                simulated_demand[22] > simulated_demand[23],
                simulated_demand[0] > simulated_demand[4],
                simulated_demand[0] > simulated_demand[3],
                simulated_demand[9] > simulated_demand[11],
                simulated_demand[0] > simulated_demand[2],
                simulated_demand[8] > simulated_demand[13],
                simulated_demand[9] > simulated_demand[12],
                simulated_demand[8] > simulated_demand[11],
                simulated_demand[8] > simulated_demand[12],
                simulated_demand[8] > simulated_demand[15],
                simulated_demand[9] > simulated_demand[13],
                simulated_demand[9] > simulated_demand[15],
                simulated_demand[8] > simulated_demand[14],
                simulated_demand[9] > simulated_demand[14],
                simulated_demand[3] <= simulated_demand[20],
                simulated_demand[12] <= simulated_demand[22],
                simulated_demand[11] <= simulated_demand[19],
                simulated_demand[18] <= simulated_demand[19],
                simulated_demand[5] <= simulated_demand[22],
                simulated_demand[6] <= simulated_demand[21],
                simulated_demand[17] <= simulated_demand[18],
                simulated_demand[1] <= simulated_demand[21],
                simulated_demand[4] <= simulated_demand[20],
                simulated_demand[5] <= simulated_demand[20],
                simulated_demand[13] <= simulated_demand[22],
                simulated_demand[4] <= simulated_demand[22],
                simulated_demand[12] <= simulated_demand[19],
                simulated_demand[15] <= simulated_demand[18],
                simulated_demand[16] <= simulated_demand[17],
                simulated_demand[2] <= simulated_demand[21],
                simulated_demand[3] <= simulated_demand[22],
                simulated_demand[15] <= simulated_demand[22],
                simulated_demand[10] <= simulated_demand[20],
                simulated_demand[17] <= simulated_demand[20],
                simulated_demand[3] <= simulated_demand[21],
                simulated_demand[11] <= simulated_demand[21],
                simulated_demand[13] <= simulated_demand[19],
                simulated_demand[14] <= simulated_demand[22],
                simulated_demand[12] <= simulated_demand[21]
            ]

            # Verificar todas las condiciones
            if all( conditions):
                simulated_paths.append(simulated_demand)

        self.simulated_paths = np.array(simulated_paths)


    def plot_montecarlo_hourly(self,n_iterations:int=1000,percentiles:list=[10,90],figsize=(2200,600)):

        """
        Esta función calcula el montecarlo por hora de la serie temporal de residuos

        Parameters
        ----------

        n_iterations : int
            Número de simulaciones a realizar.

        
        percentiles : list

            Lista con los percentiles a calcular
            El percentil bajo es el primer elemento de la lista


        Returns
        -------

        fig : plotly.graph_objects.Figure
        Tambien genera los atributos self.percentile_bajo y self.percentile_alto y self.prediction
        
        """

        if not hasattr(self,"simulated_paths"):
            self.compute_hourly_montecarlo(n_iterations=n_iterations)

        # Para las horas futuras
        future_time = self.y_preds.index[-24:].values

        # Crear un objeto de trazado
        fig = go.Figure()



        # Pronóstico promedio
        mean_forecast = self.y_preds.iloc[-24:].values.flatten()

        # Calcular percentiles 20 y 80 para cada hora
        percentile_bajo = [np.percentile(self.simulated_paths[:, i], percentiles[0]) for i in range(24)]
        percentile_alto = [np.percentile(self.simulated_paths[:, i], percentiles[1]) for i in range(24)]

        fig.add_trace(go.Scatter(x=future_time, y=mean_forecast, mode='lines', name='y_pred', line=dict(color='royalblue', width=2)))
        fig.add_trace(go.Scatter(x=future_time, y=percentile_alto, fill=None, mode='lines', line_color='royalblue', name=f'P{percentiles[1]}'))
        fig.add_trace(go.Scatter(x=future_time, y=percentile_bajo, fill='tonexty', mode='lines', line_color='royalblue', name=f'P{percentiles[0]}', ))

        
        tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        # Comprobar si el día de mañana está en el índice de 'spot' y su valor no es nulo
        # if tomorrow_date in self.spot.index and not pd.isnull(self.spot[tomorrow_date]):
        #     fig.add_trace(go.Scatter(x=future_time, y=self.spot.values.flatten(), mode='lines', fill=None, line=dict(color='gray'), name='Real'))

        fig.update_layout(title='Intervalos Montecarlo Predicción',width=figsize[0],height=figsize[1])

        self.percentile_bajo=percentile_bajo
        self.percentile_alto=percentile_alto
        self.prediction=mean_forecast



        return fig

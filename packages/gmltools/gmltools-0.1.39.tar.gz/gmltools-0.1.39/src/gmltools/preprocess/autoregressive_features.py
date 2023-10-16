import warnings
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from window_ops.rolling import (
    seasonal_rolling_max,
    seasonal_rolling_min,
    seasonal_rolling_mean,
    seasonal_rolling_std,
)


ALLOWED_AGG_FUNCS = ["mean", "max", "min", "std"]
SEASONAL_ROLLING_MAP = {
    "mean": seasonal_rolling_mean,
    "min": seasonal_rolling_min,
    "max": seasonal_rolling_max,
    "std": seasonal_rolling_std,

}

def _get_32_bit_dtype(x):
    """
    Get the 32 bit dtype for the provided column
    Parameters
    ----------
    x: pd.Series
        The column for which the 32 bit dtype is to be found
    Returns
    -------
    redn_dtype: str
        The 32 bit dtype for the provided column
    """
    dtype = x.dtype
    if dtype.name.startswith("float"):
        redn_dtype = "float32"
    elif dtype.name.startswith("int"):
        redn_dtype = "int32"
    else:
        redn_dtype = None
    return redn_dtype


class Lags:
    """
    Class to create lags for a column in a dataframe

    Parameters
    ----------
    None

    Methods
    -------
    add_lags(df: pd.DataFrame,lags: List[int],column: str,ts_id: str = None, use_32_bit: bool = False) -> Tuple[pd.DataFrame, List]:
        Create Lags for the column provided and adds them as other columns in the provided dataframe
    
    add_rolling_features(self, df: pd.DataFrame,rolls: List[int],column: str,agg_funcs: List[str] = ["mean", "std"],ts_id: str = None, n_shift: int = 1, use_32_bit: bool = False,) -> Tuple[pd.DataFrame, List]:
        Add rolling statistics from the column provided and adds them as other columns in the provided dataframe
    
    add_seasonal_rolling_features(self, df: pd.DataFrame,rolls: List[int],column: str,agg_funcs: List[str] = ["mean", "std"],ts_id: str = None, n_shift: int = 1, use_32_bit: bool = False,) -> Tuple[pd.DataFrame, List]:
        Add seasonal rolling statistics from the column provided and adds them as other columns in the provided dataframe
    
    add_ewm_features(self, df: pd.DataFrame,span: int,column: str,agg_funcs: List[str] = ["mean", "std"],ts_id: str = None, n_shift: int = 1, use_32_bit: bool = False,) -> Tuple[pd.DataFrame, List]:
        Add exponential weighted moving average statistics from the column provided and adds them as other columns in the provided dataframe
    
    """


    def __init__(self):
        pass
    
    def add_lags(self,df: pd.DataFrame,lags: List[int],column: str,ts_id: str = None, use_32_bit: bool = False) -> Tuple[pd.DataFrame, List]:
        """
        Create Lags for the column provided and adds them as other columns in the provided dataframe

       Parameters
        ----------
        df: pd.DataFrame
            The dataframe to add lags to
        lags: List[int]
            A list of all required lags
        column: str
            The column for which lags are to be created
        ts_id: str, optional
            The column which contains the time series id. If not provided, it is assumed that there is just one time series
            in the dataset
        use_32_bit: bool, optional
            Whether to use 32 bit dtypes for the newly created columns. This is useful when the dataset is large and
            memory is a constraint. Defaults to False
        
        Returns:
        -------
        df: pd.DataFrame
            The dataframe with the newly created lags
        added_features: List
            A list of all the newly created columns

        """
        assert is_list_like(lags), "`lags` should be a list of all required lags"
        assert (column in df.columns), "`column` should be a valid column in the provided dataframe"
        _32_bit_dtype = _get_32_bit_dtype(df[column])
        if ts_id is None:
            warnings.warn("Assuming just one unique time series in dataset. If there are multiple, provide `ts_id` argument")
            # Assuming just one unique time series in dataset
            if use_32_bit and _32_bit_dtype is not None:
                col_dict = { f"{column}_lag_{l}": df[column].shift(l).astype(_32_bit_dtype) for l in lags}
            else:
                col_dict = {f"{column}_lag_{l}": df[column].shift(l) for l in lags}
        else:
            assert (
                ts_id in df.columns
            ), "`ts_id` should be a valid column in the provided dataframe"
            if use_32_bit and _32_bit_dtype is not None:
                col_dict = {f"{column}_lag_{l}": df.groupby([ts_id])[column].shift(l).astype(_32_bit_dtype) for l in lags}
            else:
                col_dict = {f"{column}_lag_{l}": df.groupby([ts_id])[column].shift(l) for l in lags}
        df = df.assign(**col_dict)
        added_features = list(col_dict.keys())
        return df, added_features
    

    def add_rolling_features(self, df: pd.DataFrame,rolls: List[int],column: str,agg_funcs: List[str] = ["mean", "std"],ts_id: str = None, n_shift: int = 1, use_32_bit: bool = False,) -> Tuple[pd.DataFrame, List]:
        """
        Add rolling statistics from the column provided and adds them as other columns in the provided dataframe

        Parameters
        ----------
        df: pd.DataFrame
            The dataframe to add rolling statistics to
        rolls: List[int]
            A list of all required rolling windows
        column: str
            The column for which rolling statistics are to be created
        agg_funcs: List[str], optional
            A list of all the aggregation functions to be used. Defaults to ["mean", "std"]
        ts_id: str, optional
            The column which contains the time series id. If not provided, it is assumed that there is just one time series
            in the dataset
        n_shift: int, optional
            The number of rows to shift the data by before calculating rolling statistics. Defaults to 1
        use_32_bit: bool, optional
            Whether to use 32 bit dtypes for the newly created columns. This is useful when the dataset is large and
            memory is a constraint. Defaults to False
        
        Returns:
        -------
        df: pd.DataFrame
            The dataframe with the newly created rolling statistics
        added_features: List
            A list of all the newly created columns
        """
        assert is_list_like(rolls), "`rolls` should be a list of all required rolling windows"
        assert (column in df.columns), "`column` should be a valid column in the provided dataframe"
        assert (len(set(agg_funcs) - set(ALLOWED_AGG_FUNCS)) == 0), f"`agg_funcs` should be one of {ALLOWED_AGG_FUNCS}"

        _32_bit_dtype = _get_32_bit_dtype(df[column])

        if ts_id is None:
            warnings.warn("Assuming just one unique time series in dataset. If there are multiple, provide `ts_id` argument")
            # Assuming just one unique time series in dataset
            rolling_df = pd.concat(
                [
                    df[column]
                    .shift(n_shift)
                    .rolling(l)
                    .agg({f"{column}_rolling_{l}_{agg}": agg for agg in agg_funcs})
                    for l in rolls
                ],
                axis=1,
            )

        else:
            assert (
                ts_id in df.columns
            ), "`ts_id` should be a valid column in the provided dataframe"
            rolling_df = pd.concat(
                [
                    df.groupby(ts_id)[column]
                    .shift(n_shift)
                    .rolling(l)
                    .agg({f"{column}_rolling_{l}_{agg}": agg for agg in agg_funcs})
                    for l in rolls
                ],
                axis=1,
            )

        df = df.assign(**rolling_df.to_dict("list"))
        added_features = rolling_df.columns.tolist()
        if use_32_bit and _32_bit_dtype is not None:
            df[added_features] = df[added_features].astype(_32_bit_dtype)
        return df, added_features
    
    def add_seasonal_rolling_features(self, df: pd.DataFrame, seasonal_periods: List[int], rolls: List[int], column: str, agg_funcs: List[str] = ["mean", "std"], ts_id: str = None, n_shift: int = 1, use_32_bit: bool = False,) -> Tuple[pd.DataFrame, List]:
        """
        Add seasonal rolling statistics from the column provided and adds them as other columns in the provided dataframe

        Parameters
        ----------
        df: pd.DataFrame
            The dataframe to add seasonal rolling statistics to
        seasonal_periods: List[int]
            A list of all required seasonal cycles over which rolling statistics to be created
        rolls: List[int]
            A list of all required rolling windows
        column: str
            The column for which seasonal rolling statistics are to be created
        agg_funcs: List[str], optional
            A list of all the aggregation functions to be used. Defaults to ["mean", "std"]
        ts_id: str, optional
            The column which contains the time series id. If not provided, it is assumed that there is just one time series
            in the dataset
        n_shift: int, optional
            The number of rows to shift the data by before calculating rolling statistics. Defaults to 1
        use_32_bit: bool, optional
            Whether to use 32 bit dtypes for the newly created columns. This is useful when the dataset is large and
            memory is a constraint. Defaults to False
        
        Returns:
        -------
        df: pd.DataFrame
            The dataframe with the newly created seasonal rolling statistics
        added_features: List
            A list of all the newly created columns
            
        """
        assert is_list_like(rolls), "`rolls` should be a list of all required rolling windows"
        assert isinstance(seasonal_periods, list), "`seasonal_periods` should be a list of all required seasonal cycles over which rolling statistics to be created"
        assert (column in df.columns), "`column` should be a valid column in the provided dataframe"
        assert (len(set(agg_funcs) - set(ALLOWED_AGG_FUNCS)) == 0), f"`agg_funcs` should be one of {ALLOWED_AGG_FUNCS}"

        _32_bit_dtype = _get_32_bit_dtype(df[column])

        agg_funcs = {agg: SEASONAL_ROLLING_MAP[agg] for agg in agg_funcs}
        added_features = []
        for sp in seasonal_periods:
            if ts_id is None:
                warnings.warn("Assuming just one unique time series in dataset. If there are multiple, provide `ts_id` argument")
                # Assuming just one unique time series in dataset
                if use_32_bit and _32_bit_dtype is not None:
                    col_dict = {
                        f"{column}_{sp}_seasonal_rolling_{l}_{name}": df[column]
                        .transform(
                            lambda x: agg(
                                x.shift(n_shift * sp).values,
                                season_length=sp,
                                window_size=l,
                            )
                        )
                        .astype(_32_bit_dtype)
                        for (name, agg) in agg_funcs.items()
                        for l in rolls
                    }
                else:
                    col_dict = {
                        f"{column}_{sp}_seasonal_rolling_{l}_{name}": df[column].transform(
                            lambda x: agg(
                                x.shift(n_shift * sp).values,
                                season_length=sp,
                                window_size=l,
                            )
                        )
                        for (name, agg) in agg_funcs.items()
                        for l in rolls
                    }

            else:
                assert (ts_id in df.columns), "`ts_id` should be a valid column in the provided dataframe"
                if use_32_bit and _32_bit_dtype is not None:
                    col_dict = {
                        f"{column}_{sp}_seasonal_rolling_{l}_{name}": df.groupby(ts_id)[
                            column
                        ]
                        .transform(
                            lambda x: agg(
                                x.shift(n_shift * sp).values,
                                season_length=sp,
                                window_size=l,
                            )
                        )
                        .astype(_32_bit_dtype)
                        for (name, agg) in agg_funcs.items()
                        for l in rolls
                    }
                else:
                    col_dict = {
                        f"{column}_{sp}_seasonal_rolling_{l}_{name}": df.groupby(ts_id)[
                            column
                        ].transform(
                            lambda x: agg(
                                x.shift(n_shift * sp).values,
                                season_length=sp,
                                window_size=l,
                            )
                        )
                        for (name, agg) in agg_funcs.items()
                        for l in rolls
                    }
            df = df.assign(**col_dict)
            added_features += list(col_dict.keys())
        return df, added_features
    

    def add_ewma(self, df: pd.DataFrame, column: str, alphas: List[float] = [0.5], spans: List[float] = None, ts_id: str = None, n_shift: int = 1, use_32_bit: bool = False,) -> Tuple[pd.DataFrame, List]:
        """
        
        Create Exponentially Weighted Average for the column provided and adds them as other columns in the provided dataframe


        Parameters
        ----------
        df: pd.DataFrame
            The dataframe to add Exponentially Weighted Average to
        column: str
            The column for which Exponentially Weighted Average is to be created
        alphas: List[float], optional
            A list of all required smoothing parameters. Defaults to [0.5]
        spans: List[float], optional
            A list of all required period spans. Defaults to None
        ts_id: str, optional
            The column which contains the time series id. If not provided, it is assumed that there is just one time series
            in the dataset
        n_shift: int, optional
            The number of rows to shift the data by before calculating Exponentially Weighted Average. Defaults to 1
        use_32_bit: bool, optional
            Whether to use 32 bit dtypes for the newly created columns. This is useful when the dataset is large and
            memory is a constraint. Defaults to False

        Returns
        -------
        df: pd.DataFrame
            The dataframe with the newly created Exponentially Weighted Average
        added_features: List
            A list of all the newly created columns
        
        

        """
        if spans is not None:
            assert isinstance(spans, list), "`spans` should be a list of all required period spans"
            use_spans = True
        if alphas is not None:
            assert isinstance(alphas, list), "`alphas` should be a list of all required smoothing parameters"
        if spans is None and alphas is None:
            raise ValueError("Either `alpha` or `spans` should be provided for the function to")
        assert (column in df.columns), "`column` should be a valid column in the provided dataframe"

        _32_bit_dtype = _get_32_bit_dtype(df[column])

        if ts_id is None:
            warnings.warn("Assuming just one unique time series in dataset. If there are multiple, provide `ts_id` argument")
            # Assuming just one unique time series in dataset
            if use_32_bit and _32_bit_dtype is not None:
                col_dict = {
                    f"{column}_ewma_{'span' if use_spans else 'alpha'}_{param}": df[column]
                    .shift(n_shift)
                    .ewm(
                        alpha=None if use_spans else param,
                        span=param if use_spans else None,
                        adjust=False,
                    )
                    .mean()
                    .astype(_32_bit_dtype)
                    for param in (spans if use_spans else alphas)
                }

            else:
                col_dict = {
                    f"{column}_ewma_{'span' if use_spans else 'alpha'}_{param}": df[column]
                    .shift(n_shift)
                    .ewm(
                        alpha=None if use_spans else param,
                        span=param if use_spans else None,
                        adjust=False,
                    )
                    .mean()
                    for param in (spans if use_spans else alphas)
                }
        else:
            assert (ts_id in df.columns), "`ts_id` should be a valid column in the provided dataframe"
            if use_32_bit and _32_bit_dtype is not None:
                col_dict = {
                    f"{column}_ewma_{'span' if use_spans else 'alpha'}_{param}": df.groupby(
                        [ts_id]
                    )[
                        column
                    ]
                    .shift(n_shift)
                    .ewm(
                        alpha=None if use_spans else param,
                        span=param if use_spans else None,
                        adjust=False,
                    )
                    .mean()
                    .astype(_32_bit_dtype)
                    for param in (spans if use_spans else alphas)
                }
            else:
                col_dict = {
                    f"{column}_ewma_{'span' if use_spans else 'alpha'}_{param}": df.groupby(
                        [ts_id]
                    )[
                        column
                    ]
                    .shift(n_shift)
                    .ewm(
                        alpha=None if use_spans else param,
                        span=param if use_spans else None,
                        adjust=False,
                    )
                    .mean()
                    for param in (spans if use_spans else alphas)
                }
        df = df.assign(**col_dict)
        return df, list(col_dict.keys())
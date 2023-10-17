import warnings
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from pandas.api.types import is_list_like






def make_multistep_target(df, var,steps):
    """
    Given a dataframe and a variable, it creates a multistep target. It creates
    a new column for each step, with the value of the variable shifted by the
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the variable.
    var : str
        The name of the variable.
    steps : int
        The number of steps to shift the variable.

    Returns
    -------
    df : pd.DataFrame
        The dataframe with the new columns.
    
    """

    ts=df[var]
    ts=pd.concat(
        {f'{var}_step_{i + 1}': ts.shift(-i)
         for i in range(steps)},
        axis=1)
    df=pd.concat([df,ts],axis=1)
    df=df.drop(var,axis=1)
    df.dropna(inplace=True,axis=0)
    return df


def reduce_mem_usage(df:pd.DataFrame, verbose:bool=True, select_categorical:list=None,agressive = False) -> pd.DataFrame:
    """
    Iterate through all the columns of a dataframe and modify the data type to
    reduce memory usage. Only applies to columns with numeric data types.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to reduce memory usage.
    
    verbose : bool, optional
        Whether to print the reduction in memory usage. The default is True.
    
    select_categorical : list, optional
        List of columns to be converted to categorical. The default is None.

    aggressive : bool, optional
        Whether to use aggressive memory reduction. The default is False.
        Defaults False reduces int to 32 bits and float to 32 bits.
    
    Returns
    -------
    df : pd.DataFrame
        The dataframe with reduced memory usage.
    """
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2

        
    for col in df.columns:
        col_type = df[col].dtype

        if select_categorical is not None and col in select_categorical:
            df[col] = df[col].astype('category')
        elif col_type in numerics:
            if agressive:
                c_min = df[col].min()
                c_max = df[col].max()

                if str(col_type)[:3] == 'int':
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)
                else:
                    if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                        df[col] = df[col].astype(np.float16)
                    elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
                    else:
                        df[col] = df[col].astype(np.float64)
            else:
                #every numeric to 32 bits if float and if int
                if str(col_type)[:3] == 'int':
                    df[col] = df[col].astype(np.int32)
                else:
                    df[col] = df[col].astype(np.float32)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2

    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem), "from ", start_mem, "Mb")
    return df
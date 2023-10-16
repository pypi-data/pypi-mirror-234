import numpy as np
import matplotlib.pyplot as plt
import re
import pandas as pd

class BlockingTimeSeriesSplit():

    """
    BlockingTimeSeriesSplit is a variation of TimeSeriesSplit that splits the data into n_splits blocks of equal size.
    https://towardsdatascience.com/4-things-to-do-when-applying-cross-validation-with-time-series-c6a5674ebf3a
    https://neptune.ai/blog/cross-validation-mistakes
    """
    def __init__(self, n_splits:int):
        """
        Parameters
        ----------
        n_splits : int
            Number of splits.
        """
        self.n_splits = n_splits
    
    def get_n_splits(self, X, y, groups):
        """
        Returns the number of splitting iterations in the cross-validator.

        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        return self.n_splits
    
    def split(self, X, y=None, groups=None):
        """
        Generate indices to split data into training and test set.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape (n_samples,)
            The target variable for supervised learning problems.
        groups : array-like, with shape (n_samples,), optional
            Group labels for the samples used while splitting the dataset into
            train/test set.

        Returns
        -------
        yield indices[start: mid], indices[mid + margin: stop] : generator
        """
        n_samples = len(X)
        k_fold_size = n_samples // self.n_splits
        indices = np.arange(n_samples)

        margin = 0
        for i in range(self.n_splits):
            start = i * k_fold_size
            stop = start + k_fold_size
            mid = int(0.5 * (stop - start)) + start
            yield indices[start: mid], indices[mid + margin: stop]


class TimeSeriesInitialSplit():
    """Time Series cross-validator with initial period
    Provides time series splits for rolling origin type 
    cross validation. This means users may set an initial
    time period. gap size, and increment_size and intra gap.
    Parameters:
        initial : int, default=21
            Number of splits.
        increment_size : int, default=7
            Sets the size of the test set to be added at each iteration
        gap : int, default=0
            Number of samples to exclude from the end of each train set before
            the test set.
        intra_gap : int, default=0
            Number of samples of train to add constantly to the end of each train split.
            Its apply after the fisrt split
    Examples:
    ```py

    X = np.arange(0,50)
    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0, intra_gap=0)
    for train_index, test_index in tscv.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20] TEST: [21 22 23 24 25 26 27]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27] TEST: [28 29 30 31 32 33 34]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34] TEST: [35 36 37 38 39 40 41]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41] TEST: [42 43 44 45 46 47 48]
    ```

    ```py
    X = np.arange(0,50)

    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0,intra_gap=3)
    for train_index, test_index in tscv.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
    
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19] TEST: [20 21 22 23 24 25 26]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 ] TEST: [30 31 32 33 34 35 36]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 32 33 34 35 36 37 38 39] TEST: [40 41 42 43 44 45 46]
    """

    def __init__(self, initial=7 * 3, increment_size=7, gap=0,intra_gap=0):
        self.initial = initial
        self.increment_size = increment_size
        self.gap = gap
        self.intra_gap=intra_gap
        self.is_timeseriesinitialsplit = True


    def split(self, X, y=None, groups=None):
        """Generate indices to split data into training and test set.
        Parameters:
            X : array-like of shape (n_samples, n_features)
                Training data, where `n_samples` is the number of samples
                and `n_features` is the number of features.
        Yields: 
            train : ndarray
                The training set indices for that split.
            test : ndarray
                The testing set indices for that split.
        """
        if isinstance(self.initial, str):
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", self.initial) or re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", self.initial), "date format should be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, the same index as dataframe"
            #obatin the iloc index of self.initial date
            self.initial = X.index.get_loc(self.initial)
        n_samples = len(X)
        initial = self.initial
        gap = self.gap
        intra_gap=self.intra_gap
        increment_size = self.increment_size

        # Make sure we have enough samples for the given split parameters
        if initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - initial - increment_size - gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={initial} increment_size={increment_size} and gap={gap}."
            )

        indices = np.arange(n_samples)
        test_starts = range(initial, n_samples, increment_size)
        for i,test_start in enumerate(test_starts):
            if i == 0 :
                test = indices[test_start + gap : test_start + increment_size + gap]
                if len(test) < increment_size:
                    # break if the test set is smaller than a complete increment_size
                    break
                else:
                    yield (
                        indices[:test_start],
                        indices[test_start + gap : test_start  + increment_size + gap],
                    )
            else:
                test = indices[test_start + gap + intra_gap: test_start + increment_size + intra_gap + gap]
                if len(test) < increment_size:
                    # break if the test set is smaller than a complete increment_size
                    break
                else:
                    yield (
                        indices[:test_start+ intra_gap],
                        indices[test_start + gap + intra_gap: test_start + intra_gap + increment_size + gap],
                    )

    def get_n_splits(self, X, y=None, groups=None)->int:
        """
        Returns the number of splitting iterations in the cross-validator

        Parameters
        ----------
        
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.
        
        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        n_splits : int
        """

        n_samples = len(X)

        # Make sure we have enough samples for the given split parameters
        if self.initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={self.initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - self.initial - self.increment_size - self.gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={self.initial} increment_size={self.increment_size} and gap={self.gap}."
            )
        n_splits=0
        for train_index, test_index in self.split(X):
            n_splits +=1
        return n_splits
    
    def get_index_splits(self,X,y=None,groups=None):
        """
        Returns the index of the train and test sets for each split

        Parameters
        ----------

        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        X_train_date : list
            List of the index of the train set for each split
        X_test_date : list
            List of the index of the test set for each split
        """
        train_real_index=[]
        test_real_index=[]
        for train_index, test_index in self.split(X):
            train_real_index.append(X.index[train_index])
            test_real_index.append(X.index[test_index])

        return train_real_index,test_real_index
    
    def get_test_days(self,X,y=None,groups=None):
        """
        Returns the days of the test sets for each split

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        test_days : list
            List of the days of the test set for each split
        """
        test_days=[]
        train_real_index,test_real_index=self.get_index_splits(X)
        for day in test_real_index:
            day_=np.unique(day.date)
            test_days.append(day_[0].strftime("%Y-%m-%d"))
        return test_days
    def __repr__(self):
        return "TimeSeriesInitialSplit(initial={}, increment_size={}, gap={}, intra_gap={})".format(
            self.initial, self.increment_size, self.gap, self.intra_gap
        )

def plot_timesplit(n_splits, n_samples,test_size=None , min_train_size=None, text=False,figsize=(20,10)):

    """
    Plot the train and test size depending on the number of splits for TimeSeriesSplit

    Parameters
    ----------
    n_splits : int
        Number of splits.

    n_samples : int
        Number of samples.
    
    test_size : int, optional
        Size of the test set, by default None
    
    text : bool, optional
        Add the percentage of the train and test size to the side of the bar, by default False

    Returns
    -------
    None
        Plot the train and test size depending on the number of splits for TimeSeriesSplit
    """

    n_splits=n_splits
    n_samples=n_samples
    if test_size is None:
        test_size= n_samples // (n_splits+1)
    train_size=[]
    test_size_=[]
    plt.figure(figsize=figsize)
    for i in reversed(range(1,n_splits+1)):
        train_set=i * n_samples // (n_splits + 1) + n_samples % (n_splits + 1)
        train_size.append(train_set)
        test_size_.append(test_size)
    plt.barh(np.arange(1,n_splits+1),train_size)
    plt.barh(np.arange(1,n_splits+1),test_size_, left=train_size)
    plt.legend(["Train Size", "Test Size"])
    plt.xlabel("Number of Splits")
    plt.ylabel("Size")
    plt.title("Train and Test Size depending on the number of splits")
    #add the percentage of the train and test size to the side of the bar
    if text == True:
        for i in range(n_splits):
            plt.text(train_size[i]+test_size_[i]+1000, i+1, f"Train: {train_size[i]*100/n_samples:.2f}%  Test: {test_size_[i]*100/n_samples:.2f}%", fontsize=7)

        #extend the frame to the right to make room for the text
        plt.xlim(0, n_samples+n_samples*0.43)

    plt.show()






class TimeSeriesWindowSplit():
    """Time Series cross-validator with initial period
    Provides time series splits for rolling origin type 
    cross validation. This means users may set an initial
    time period. gap size, and increment_size and intra gap.
    Parameters:
        initial : int, default=21
            Number of splits.
        increment_size : int, default=7
            Sets the size of the test set to be added at each iteration
        gap : int, default=0
            Number of samples to exclude from the end of each train set before
            the test set.
        intra_gap : int, default=0
            Number of samples of train to add constantly to the end of each train split.
            Its apply after the fisrt split
    Examples:
    ```py

    X = np.arange(0,50)
    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0, intra_gap=0)
    for train_index, test_index in tscv.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20] TEST: [21 22 23 24 25 26 27]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27] TEST: [28 29 30 31 32 33 34]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34] TEST: [35 36 37 38 39 40 41]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41] TEST: [42 43 44 45 46 47 48]
    ```

    ```py
    X = np.arange(0,50)

    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0,intra_gap=3)
    for train_index, test_index in tscv.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
    
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19] TEST: [20 21 22 23 24 25 26]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 ] TEST: [30 31 32 33 34 35 36]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 32 33 34 35 36 37 38 39] TEST: [40 41 42 43 44 45 46]
    """

    def __init__(self, initial=7 * 3, increment_size=7, gap=0,intra_gap=0):
        self.initial = initial
        self.increment_size = increment_size
        self.gap = gap
        self.intra_gap=intra_gap
        self.is_timeseriesinitialsplit = True


    def split(self, X, y=None, groups=None):
        """Generate indices to split data into training and test set.
        Parameters:
            X : array-like of shape (n_samples, n_features)
                Training data, where `n_samples` is the number of samples
                and `n_features` is the number of features.
        Yields: 
            train : ndarray
                The training set indices for that split.
            test : ndarray
                The testing set indices for that split.
        """
        if isinstance(self.initial, str):
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", self.initial) or re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", self.initial), "date format should be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, the same index as dataframe"
            #obatin the iloc index of self.initial date
            self.initial = X.index.get_loc(self.initial)
        n_samples = len(X)
        initial = self.initial
        gap = self.gap
        intra_gap=self.intra_gap
        increment_size = self.increment_size

        # Make sure we have enough samples for the given split parameters
        if initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - initial - increment_size - gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={initial} increment_size={increment_size} and gap={gap}."
            )

        indices = np.arange(n_samples)
        test_starts = range(initial, n_samples, increment_size)
        for i,test_start in enumerate(test_starts):
            if i == 0 :
                test = indices[test_start + gap : test_start + increment_size + gap]
                if len(test) < increment_size:
                    # break if the test set is smaller than a complete increment_size
                    break
                else:
                    yield (
                        indices[:test_start],
                        indices[test_start + gap : test_start  + increment_size + gap],
                    )
            else:
                test = indices[test_start + gap + intra_gap: test_start + increment_size + intra_gap + gap]
                if len(test) < increment_size:
                    # break if the test set is smaller than a complete increment_size
                    break
                else:
                    yield (
                        indices[i*increment_size:test_start+ intra_gap], #train
                        indices[test_start + gap + intra_gap: test_start + intra_gap + increment_size + gap], #test
                    )

    def get_n_splits(self, X, y=None, groups=None)->int:
        """
        Returns the number of splitting iterations in the cross-validator

        Parameters
        ----------
        
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.
        
        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        n_splits : int
        """

        n_samples = len(X)

        # Make sure we have enough samples for the given split parameters
        if self.initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={self.initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - self.initial - self.increment_size - self.gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={self.initial} increment_size={self.increment_size} and gap={self.gap}."
            )
        n_splits=0
        for train_index, test_index in self.split(X):
            n_splits +=1
        return n_splits
    
    def get_index_splits(self,X,y=None,groups=None):
        """
        Returns the index of the train and test sets for each split

        Parameters
        ----------

        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        X_train_date : list
            List of the index of the train set for each split
        X_test_date : list
            List of the index of the test set for each split
        """
        train_real_index=[]
        test_real_index=[]
        for train_index, test_index in self.split(X):
            train_real_index.append(X.index[train_index])
            test_real_index.append(X.index[test_index])

        return train_real_index,test_real_index
    
    def get_test_days(self,X,y=None,groups=None):
        """
        Returns the days of the test sets for each split

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        test_days : list
            List of the days of the test set for each split
        """
        test_days=[]
        train_real_index,test_real_index=self.get_index_splits(X)
        for day in test_real_index:
            day_=np.unique(day.date)
            test_days.append(day_[0].strftime("%Y-%m-%d"))
        return test_days
    def __repr__(self):
        return "TimeSeriesWindowSplit(initial={}, increment_size={}, gap={}, intra_gap={})".format(
            self.initial, self.increment_size, self.gap, self.intra_gap
        )

def plot_timesplit(n_splits, n_samples,test_size=None , min_train_size=None, text=False,figsize=(20,10)):

    """
    Plot the train and test size depending on the number of splits for TimeSeriesSplit

    Parameters
    ----------
    n_splits : int
        Number of splits.

    n_samples : int
        Number of samples.
    
    test_size : int, optional
        Size of the test set, by default None
    
    text : bool, optional
        Add the percentage of the train and test size to the side of the bar, by default False

    Returns
    -------
    None
        Plot the train and test size depending on the number of splits for TimeSeriesSplit
    """

    n_splits=n_splits
    n_samples=n_samples
    if test_size is None:
        test_size= n_samples // (n_splits+1)
    train_size=[]
    test_size_=[]
    plt.figure(figsize=figsize)
    for i in reversed(range(1,n_splits+1)):
        train_set=i * n_samples // (n_splits + 1) + n_samples % (n_splits + 1)
        train_size.append(train_set)
        test_size_.append(test_size)
    plt.barh(np.arange(1,n_splits+1),train_size)
    plt.barh(np.arange(1,n_splits+1),test_size_, left=train_size)
    plt.legend(["Train Size", "Test Size"])
    plt.xlabel("Number of Splits")
    plt.ylabel("Size")
    plt.title("Train and Test Size depending on the number of splits")
    #add the percentage of the train and test size to the side of the bar
    if text == True:
        for i in range(n_splits):
            plt.text(train_size[i]+test_size_[i]+1000, i+1, f"Train: {train_size[i]*100/n_samples:.2f}%  Test: {test_size_[i]*100/n_samples:.2f}%", fontsize=7)

        #extend the frame to the right to make room for the text
        plt.xlim(0, n_samples+n_samples*0.43)

    plt.show()





class TimeSeriesWindowGapSplit():
    """Time Series cross-validator with initial period
    Provides time series splits for rolling origin type 
    cross validation. This means users may set an initial
    time period. gap size, and increment_size and intra gap.
    Parameters:
        initial : int, default=21
            Number of splits.
        increment_size : int, default=7
            Sets the size of the test set to be added at each iteration
        gap : int, default=0
            Number of samples to exclude from the end of each train set before
            the test set.
        intra_gap : int, default=0
            Number of samples of train to add constantly to the end of each train split.
            Its apply after the fisrt split
    Examples:
    ```py

    X = np.arange(0,50)
    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0, intra_gap=0)
    for train_index, test_index in tscv.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20] TEST: [21 22 23 24 25 26 27]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27] TEST: [28 29 30 31 32 33 34]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34] TEST: [35 36 37 38 39 40 41]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41] TEST: [42 43 44 45 46 47 48]
    ```

    ```py
    X = np.arange(0,50)

    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0,intra_gap=3)
    for train_index, test_index in tscv.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
    
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19] TEST: [20 21 22 23 24 25 26]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 ] TEST: [30 31 32 33 34 35 36]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 32 33 34 35 36 37 38 39] TEST: [40 41 42 43 44 45 46]
    """

    def __init__(self, initial=7 * 3, increment_size=7, gap=0,intra_gap=0):
        self.initial = initial
        self.increment_size = increment_size
        self.gap = gap
        self.intra_gap=intra_gap
        self.is_timeseriesinitialsplit = True


    def split(self, X, y=None, groups=None):
        """Generate indices to split data into training and test set.
        Parameters:
            X : array-like of shape (n_samples, n_features)
                Training data, where `n_samples` is the number of samples
                and `n_features` is the number of features.
        Yields: 
            train : ndarray
                The training set indices for that split.
            test : ndarray
                The testing set indices for that split.
        """
        if isinstance(self.initial, str):
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", self.initial) or re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", self.initial), "date format should be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, the same index as dataframe"
            #obatin the iloc index of self.initial date
            self.initial = X.index.get_loc(self.initial)
        n_samples = len(X)
        initial = self.initial
        gap = self.gap
        intra_gap=self.intra_gap
        increment_size = self.increment_size

        # Make sure we have enough samples for the given split parameters
        if initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - initial - increment_size - gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={initial} increment_size={increment_size} and gap={gap}."
            )

        indices = np.arange(n_samples)
        test_starts = range(initial, n_samples+increment_size*2, increment_size)
        for i,test_start in enumerate(test_starts):
            if i == 0 :
                test = indices[test_start  : test_start + increment_size ]
                if len(test) < increment_size:
                    # break if the test set is smaller than a complete increment_size
                    break
                else:
                    yield (
                        indices[:test_start],
                        indices[test_start : test_start  + gap],
                    )
            else:
                test = indices[test_start : test_start + increment_size]
                if len(test) < increment_size:
                    # break if the test set is smaller than a complete increment_size
                    break
                else:
                    yield (
                        indices[i*increment_size:test_start], #train
                        indices[test_start : test_start + gap], #test
                    )

    def get_n_splits(self, X, y=None, groups=None)->int:
        """
        Returns the number of splitting iterations in the cross-validator

        Parameters
        ----------
        
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.
        
        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        n_splits : int
        """

        n_samples = len(X)

        # Make sure we have enough samples for the given split parameters
        if self.initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={self.initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - self.initial - self.increment_size - self.gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={self.initial} increment_size={self.increment_size} and gap={self.gap}."
            )
        n_splits=0
        for train_index, test_index in self.split(X):
            n_splits +=1
        return n_splits
    
    def get_index_splits(self,X,y=None,groups=None):
        """
        Returns the index of the train and test sets for each split

        Parameters
        ----------

        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        X_train_date : list
            List of the index of the train set for each split
        X_test_date : list
            List of the index of the test set for each split
        """
        train_real_index=[]
        test_real_index=[]
        for train_index, test_index in self.split(X):
            train_real_index.append(X.index[train_index])
            test_real_index.append(X.index[test_index])

        return train_real_index,test_real_index
    
    def get_test_days(self,X,y=None,groups=None):
        """
        Returns the days of the test sets for each split

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        test_days : list
            List of the days of the test set for each split
        """
        test_days=[]
        train_real_index,test_real_index=self.get_index_splits(X)
        for day in test_real_index:
            day_=np.unique(day.date)
            test_days.append(day_[0].strftime("%Y-%m-%d"))
        return test_days
    def __repr__(self):
        return "TimeSeriesWindowGapSplit(initial={}, increment_size={}, gap={}, intra_gap={})".format(
            self.initial, self.increment_size, self.gap, self.intra_gap
        )




class TimeSeriesWindowAheadsSplit():
    """Time Series cross-validator with initial period
    Provides time series splits for rolling origin type 
    cross validation. This means users may set an initial
    time period. gap size, and increment_size and intra gap.
    Magaing two dataframes, one for train and another for test,
    due to the different struture of the aproach.
    Parameters:
        initial : int, default=21
            Number of splits.
        increment_size : int, default=7
            Sets the size of the test set to be added at each iteration
        gap : int, default=0
            Number of samples to exclude from the end of each train set before
            the test set.
    Examples:
    ```py

    X = np.arange(0,50)
    tscv = TimeSeriesInitialSplit(initial=20, increment_size=7, gap=0)
    for train_index, test_index in tscv.split(X,X_4_test):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X_4_test[test_index]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20] TEST: [21 22 23 24 25 26 27]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27] TEST: [28 29 30 31 32 33 34]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34] TEST: [35 36 37 38 39 40 41]
    > TRAIN: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41] TEST: [42 43 44 45 46 47 48]
    ```

    """

    def __init__(self, initial=7 * 3, increment_size=7, gap=0, intra_gap=0):
        self.initial = initial
        self.increment_size = increment_size
        self.intra_gap=intra_gap
        self.gap = gap
        self.is_timeseriesinitialsplit = True


    def split(self, X,X_test, y=None, groups=None):
        #assert X index is datetime
        assert isinstance(X.index,pd.DatetimeIndex), "X index should be datetime"
        assert isinstance(X_test.index,pd.DatetimeIndex), "X index should be datetime"
        assert "id" in X_test.columns, "X_test should have a column named id with the same index as X"

        """Generate indices to split data into training and test set.
        Parameters:
            X : array-like of shape (n_samples, n_features)
                Training data, where `n_samples` is the number of samples
                and `n_features` is the number of features.

            X_test : array-like of shape (n_samples_test, n_features)
                Test data
        Yields: 
            train : ndarray
                The training set indices for that split.
            test : ndarray
                The testing set indices for that split.
        """
        if isinstance(self.initial, str):
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", self.initial) or re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", self.initial), "date format should be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, the same index as dataframe"
            #obatin the iloc index of self.initial date
            self.initial = X.index.get_loc(self.initial)


        is_hourly = (X_test.index[1] - X_test.index[0]) == pd.Timedelta(hours=1)

        if is_hourly == True:

            registers=int((X_test.loc[X_test.id==X_test.id[0]]).shape[0]/24)
            n_samples = len(X)-registers*24

        else:

            registers=int((X_test.loc[X_test.id==X_test.id[0]]).shape[0])
            n_samples = len(X)-registers
        X_test_split=X_test.copy()
        X_test_split.reset_index(inplace=True)
        initial = self.initial
        gap = self.gap
        intra_gap=self.intra_gap

        increment_size = self.increment_size




        # Make sure we have enough samples for the given split parameters
        if initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - initial - increment_size - gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={initial} increment_size={increment_size} and gap={gap}."
            )

        indices = np.arange(n_samples)
        test_starts = range(initial, n_samples, increment_size)

        for i,test_start in enumerate(test_starts):
            test_start_datetime=X.index[test_start]
            test_start_datetime=test_start_datetime-pd.Timedelta(days=1)
            test_indexes=X_test_split[X_test_split.id==test_start_datetime].index.to_list()            

            if i == 0 :



                yield (
                    indices[:test_start],
                    test_indexes,
                )
            else:

                yield (
                    indices[i*increment_size:test_start], #train
                    test_indexes, #test
                )
    def get_n_splits(self, X, X_test, y=None, groups=None)->int:
        """
        Returns the number of splitting iterations in the cross-validator

        Parameters
        ----------
        
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.
        
        X_test : array-like of shape (n_samples, n_features)
            Test data

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.
        
        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        n_splits : int
        """

        n_samples = len(X)

        # Make sure we have enough samples for the given split parameters
        if self.initial > n_samples:
            raise ValueError(
                f"Cannot have number of initial_size={self.initial} greater"
                f" than the number of samples={n_samples}."
            )
        if n_samples - self.initial - self.increment_size - self.gap < 0:
            raise ValueError(
                f"Size of initial + increment_size + gap too large given sample"
                f"={n_samples} with initial={self.initial} increment_size={self.increment_size} and gap={self.gap}."
            )
        n_splits=0
        for train_index, test_index in self.split(X, X_test):
            n_splits +=1
        return n_splits
    
    def get_index_splits(self,X, X_test,y=None,groups=None):
        """
        Returns the index of the train and test sets for each split

        Parameters
        ----------

        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        X_train_date : list
            List of the index of the train set for each split
        X_test_date : list
            List of the index of the test set for each split
        """
        train_real_index=[]
        test_real_index=[]
        for train_index, test_index in self.split(X,X_test):
            train_real_index.append(X.index[train_index])
            test_real_index.append(X_test.index[test_index])

        return train_real_index,test_real_index
    
    def get_test_days(self,X,X_test,y=None,groups=None):
        """
        Returns the days of the test sets for each split

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the dataset into

        Returns
        -------
        test_days : list
            List of the days of the test set for each split
        """
        test_days=[]
        train_real_index,test_real_index=self.get_index_splits(X,X_test)
        for day in test_real_index:
            day_=np.unique(day.date)
            test_days.append(day_[0].strftime("%Y-%m-%d"))
        return test_days
    
    def __repr__(self):
        return "TimeSeriesWindowAheadsSplit(initial={}, increment_size={}, gap={}, intra_gap={})".format(
            self.initial, self.increment_size, self.gap, self.intra_gap
        )

def plot_timesplit(n_splits, n_samples,test_size=None , min_train_size=None, text=False,figsize=(20,10)):

    """
    Plot the train and test size depending on the number of splits for TimeSeriesSplit

    Parameters
    ----------
    n_splits : int
        Number of splits.

    n_samples : int
        Number of samples.
    
    test_size : int, optional
        Size of the test set, by default None
    
    text : bool, optional
        Add the percentage of the train and test size to the side of the bar, by default False

    Returns
    -------
    None
        Plot the train and test size depending on the number of splits for TimeSeriesSplit
    """

    n_splits=n_splits
    n_samples=n_samples
    if test_size is None:
        test_size= n_samples // (n_splits+1)
    train_size=[]
    test_size_=[]
    plt.figure(figsize=figsize)
    for i in reversed(range(1,n_splits+1)):
        train_set=i * n_samples // (n_splits + 1) + n_samples % (n_splits + 1)
        train_size.append(train_set)
        test_size_.append(test_size)
    plt.barh(np.arange(1,n_splits+1),train_size)
    plt.barh(np.arange(1,n_splits+1),test_size_, left=train_size)
    plt.legend(["Train Size", "Test Size"])
    plt.xlabel("Number of Splits")
    plt.ylabel("Size")
    plt.title("Train and Test Size depending on the number of splits")
    #add the percentage of the train and test size to the side of the bar
    if text == True:
        for i in range(n_splits):
            plt.text(train_size[i]+test_size_[i]+1000, i+1, f"Train: {train_size[i]*100/n_samples:.2f}%  Test: {test_size_[i]*100/n_samples:.2f}%", fontsize=7)

        #extend the frame to the right to make room for the text
        plt.xlim(0, n_samples+n_samples*0.43)

    plt.show()

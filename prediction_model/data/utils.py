import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def load_data():
    """
    Reads the training dataset from the specified path.

    Returns:
        pd.DataFrame: Training dataset.
    """
    data = pd.read_csv("../prediction_model/data/data.csv", encoding="ISO-8859-1", sep=";")
    return data

def check_df(dataframe):
    """
    Checks the overall structure and key metrics of a DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame to inspect.

    Returns:
        None: Prints shape, data types, head, tail, missing values, and quantiles.
    """
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(3))
    print("##################### Tail #####################")
    print(dataframe.tail(3))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print('##################### Unique Values #####################')
    print(dataframe.nunique())
    print("##################### Quantiles #####################")
    # Uncomment below to include quantile information
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
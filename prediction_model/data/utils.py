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
    print(dataframe[[col for col in dataframe.columns if dataframe[col].dtypes != "O"]].quantile([0, 0.05, 0.50, 0.75, 0.95, 0.99, 1]).T)
    #print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


def plot_importance(model, features, num=50, save=False):
    """
    Bu fonksiyon, bir modelin özelliklerinin önem derecelerini görselleştirir.
    
    Parametreler:
    model : Trained model
        Özelliklerin önem derecelerini çıkarmak için kullanılan eğitimli model.
    features : pandas.DataFrame
        Modelin eğitiminde kullanılan özelliklerin veri çerçevesi.
    num : int, optional, default=len(X) => ***num=10 olarak degistirildi***
        Görselleştirilecek en yüksek `num` özelliği sayısı. 
    save : bool, optional, default=False
        Eğer True ise, görselleştirilen grafiği kaydeder.
    
    Görselleştirme:
    - Özelliklerin önem derecelerine göre sıralanmış bir bar plot.
    """
    # Modelin özellik önem derecelerini al
    feature_imp = pd.DataFrame({'Value': model.feature_importances_, 'Feature': features.columns})
    
    # Görselleştirme
    plt.figure(figsize=(25, 25))
    sns.set(font_scale=1)
    sns.barplot(x="Value", y="Feature", data=feature_imp.sort_values(by="Value", ascending=False)[0:num])
    plt.title('Features')
    plt.tight_layout()
    plt.show()
    
    # Eğer save=True ise, görselleştirmeyi kaydet
    if save:
        plt.savefig('importances.png')
    
    return feature_imp

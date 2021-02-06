import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import PATH_TO_DATA


def load_data(path):
    """
        Takes path of data, loads dataset, preprocesses by adding frequency category and fault rate feature
        and return dataset
    """
    data = pd.read_csv(path)
    data['freq_category'] = pd.cut(data['count'], bins=[0, 1000, 3000, 5000, 7000, 10000, 20000], labels=False)
    data['rate'] = data['sum'] / data['count'] * 100
    assert data.freq_category.dtype == 'int', 'Must be integer type'
    assert data.rate.dtype == 'float', 'Must be float type'
    return data


def plot_side_graph(data, plot_type='hist'):
    """
        This function plots two different graphs (plot_type)
        Plot_type = 'hist' - histogram of frequency category
        Plot_type = 'scatter' - scatter plot with x = frequency and y = fault rate
    """
    if plot_type == 'hist':
        plt.figure(figsize=(8, 5))
        data.freq_category.plot.hist()
        plt.title('Frequency histogram ', fontsize=16)
        plt.ylabel('Amount', fontsize=16)
        plt.xlabel('Bin', fontsize=16)
        plt.tick_params(axis='both', which='major', labelsize=12)
    elif plot_type == 'scatter':
        plt.figure(figsize=(12, 8))
        sns.scatterplot(x=data['count'], y=data.rate)
        plt.title('Faults rate / frequency', fontsize=20)
        plt.ylabel('Faults rate', fontsize=20)
        plt.xlabel('Frequency', fontsize=20)
        plt.tick_params(axis='both', which='major', labelsize=16)


def plot_bar_save(data):
    """
        This function plots bar plot with target value = fault rate depending on frequency category
        And saves graph with name 'bar_plot_(date of the first timestamp value in the dataset)'
    """
    plt.figure(figsize=(10, 6))
    hist = sns.barplot(x=data.freq_category, y=data.rate)
    plt.title('Fault rate in different categories ', fontsize=16)
    plt.ylabel('Fault rate(%)', fontsize=16)
    plt.xlabel('Frequency category', fontsize=16)
    plt.text(0, round(data.groupby('freq_category')['rate'].mean().max()),
             'Frequency category:\n0:(0,1000)\n1:(1000,3000)\n2:(3000,5000)'
             '\n3:(5000,7000):\n4:(7000,10000)\n5:(10000,20000)')
    plt.tick_params(axis='both', which='major', labelsize=12)

    with open(os.path.join(PATH_TO_DATA, 'sample.csv'), 'r') as f:
        f.readline()
        start_time = f.readline()
    picture_path = f"pics/Bar_plot_{start_time.split('|')[1][:10]}.png"
    hist.figure.savefig(picture_path)
    return picture_path

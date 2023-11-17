"""
This script fits the model to the data to obtain an equation
"""
import matplotlib.pyplot as plt

import pandas as pd
from scipy.stats import *

import numpy as np
from functions import eliminate_outliers


if __name__ == '__main__':
    pd_values = pd.read_csv('../csv/sensitivity_specificity.csv')
    pd_values['sensitivity'] = pd.to_numeric(pd_values['sensitivity'].str.replace(',', '.', regex=True))
    pd_values['specificity'] = pd.to_numeric(pd_values['specificity'].str.replace(',', '.', regex=True))

    pd_values['sensitivity_no_outliers'] = eliminate_outliers(pd_values['sensitivity'])
    pd_values['specificity_no_outliers'] = eliminate_outliers(pd_values['specificity'])

    pd_values.dropna(inplace=True, axis=0)

    x = np.ones(len(pd_values['specificity_no_outliers'])) - np.array(pd_values['specificity_no_outliers'])
    y = np.array(pd_values['sensitivity_no_outliers'])

    s = pd.DataFrame()
    s['specificity_no_outliers'] = pd_values['specificity_no_outliers']
    s['false_positive_rate'] = x
    s['sensitivity_no_outliers'] = y

    s.to_csv('binary_files/new_csv.csv')

    degree = 2

    z = np.polyfit(x, y, degree)

    # Create a polynomial object using np.poly1d
    poly = np.poly1d(z)

    # Generate y values for the fitted curve
    y_fit = poly(x)

    # Plot the original data and the fitted curve
    plt.scatter(x, y, label='Original data')
    plt.plot(x, y_fit, 'r-', label=f'Polynomial Fit (Degree {degree})')
    plt.xlabel('1 - Specificity')
    plt.ylabel('Sensitivity')
    plt.legend()
    plt.show()

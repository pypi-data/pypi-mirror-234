import pkg_resources
import json

import numpy as np
from sklearn.linear_model import LinearRegression
from pygamecentering.generate_offset_data import generate_offset_data



def generate_linear_regression(params = None):
    if not params:
        file_path = pkg_resources.resource_filename('pygamecentering', 'offset_data_unadjusted.json')
        try:
            with open(file_path, "r") as file:
                dict = json.load(file)
        except:
            dict = generate_offset_data()
            with open(file_path, "w") as file:
                json.dump(dict, file, indent=4)

    else:
        file_path = pkg_resources.resource_filename('pygamecentering', 'offset_data_adjusted.json')
        try:
            with open(file_path, "r") as file:
                dict = json.load(file)
        except:
            dict = generate_offset_data(params)
            with open(file_path, "w") as file:
                json.dump(dict, file, indent=4)


    x_data = dict['font_size_list']
    y_data = dict['offset_list']

    x_data = np.array(x_data)  
    y_data = np.array(y_data)

    #{a, b} -> {[a], [b]}
    x_data = x_data.reshape(-1, 1)
    y_data = y_data.reshape(-1, 1)

    model = LinearRegression()
    model.fit(x_data, y_data)

    # Percent error = offset / font size
    percent_error = np.abs(y_data / x_data) * 100

    # Mean percent error
    mape = np.mean(percent_error)
    coef = float(model.coef_[0][0])
    intercept = float(model.intercept_[0])
    params = {'coef': round(coef, 4), 'intercept': round(intercept, 4), 'MAPE': round(mape, 4)}
    return params


data = {'x': 'font size', 'y': 'offset'}
params = generate_linear_regression()
data['unadjusted_data'] = params
data['adjusted_data'] = generate_linear_regression(data['unadjusted_data'])

offset_reduction = (data['unadjusted_data']['MAPE'] - data['adjusted_data']['MAPE']) / data['unadjusted_data']['MAPE']
data['offset_reduction'] = f"{round(offset_reduction, 2)*100}%"

file_path = pkg_resources.resource_filename('pygamecentering', 'offset_data_results.json')
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)
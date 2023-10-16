import math
import numpy as np
import random as rd
import matplotlib.pyplot as plt

import time
from matplotlib.pyplot import figure


figure(figsize=(8, 6), dpi=80)

# Import necessary libraries
import pandas as pd
import numpy as np
import json
import zipfile
from datetime import datetime

import copy

import matplotlib.colors as mcolors



"""# 3. Process data"""

# Function to convert date string to Julian Date
def convert_date_stringtojd(s):
    """
    Convert a date string in ISO format to Julian Date.

    Args:
    s (str): Date string in ISO format.

    Returns:
    int: Julian Date.
    """
    return round(datetime.fromisoformat(s).timestamp() / (24 * 3600))

# Function to get start and end dates from data
def get_start_end_date(data):
    """
    Get the start and end dates from a DataFrame containing date information.

    Args:
    data (DataFrame): DataFrame with a 'actualshipdate' column.

    Returns:
    int: Start date as Julian Date.
    int: End date as Julian Date.
    """
    dates = pd.DataFrame()
    dates = copy.copy(pd.to_datetime(data['actualshipdate'], format='%Y-%m-%d'))
    start_date, end_date = dates.min(), dates.max()
    return convert_date_stringtojd(start_date.isoformat()), convert_date_stringtojd(end_date.isoformat())

# Function to create a matrix and data dictionary for supply or demand
def create_matrix_and_data(data, is_supply=True):
    """
    Create a matrix and data dictionary for supply or demand data.

    Args:
    data (DataFrame): DataFrame containing the data.
    is_supply (bool): True for supply data, False for demand data.

    Returns:
    ndarray: Supply or demand matrix.
    dict: Data dictionary.
    """
    start_date, end_date = get_start_end_date(data)
    list_code_column = ['whseid', 'sku'] if is_supply else ['customercode', 'sku']
    matrix_name = 'supply_matrix' if is_supply else 'demand_matrix'
    data_encode_name = 'data_encode_supply' if is_supply else 'data_encode_demand'

    unique_codes_sku = data[list_code_column[1]].unique()
    code_dict_sku = {code: sku_id for sku_id, code in enumerate(unique_codes_sku)}

    unique_codes = data[list_code_column[0]].unique()
    code_dict = {code: i for i, code in enumerate(unique_codes)}

    number_days = end_date - start_date + 1
    matrix = np.zeros((number_days, len(unique_codes), len(data['sku'].unique())), np.int_)

    for item in data.values:
        date_id = convert_date_stringtojd(item[0]) - start_date
        code_id = code_dict[item[1]]
        sku_id = code_dict_sku[item[2]]
        matrix[date_id, code_id, sku_id] = item[3]


    data_encode = {
        f'list_{list_code_column[0]}_code': list(unique_codes),
        f'dict_{list_code_column[0]}_code': code_dict,
        f'list_{list_code_column[1]}_code': list(unique_codes_sku),
        f'dict_{list_code_column[1]}_code': code_dict_sku,
        'start_date': start_date,
        'end_date': end_date
    }

    return matrix, data_encode

# Create and save matrices and data for supply

"""# Main"""

def transform_main(past_data):

    data_NM_TCO = past_data['data_NM_TCO']
    data_TCO_NPP = past_data['data_TCO_NPP']

    # Preprocess the data
    data_NM_TCO = data_NM_TCO.sort_values(by='actualshipdate')
    data_TCO_NPP = data_TCO_NPP.sort_values(by='actualshipdate')

    # Tổng hợp dữ liệu theo ngày, mã kho (NM hoặc NPP), và mã sản phẩm
    data_NM_TCO = data_NM_TCO.groupby(['actualshipdate', 'whseid', 'sku'])['qty'].sum().reset_index()
    data_TCO_NPP = data_TCO_NPP.groupby(['actualshipdate', 'customercode', 'sku'])['qty'].sum().reset_index()

    supply_matrix, data_encode_supply = create_matrix_and_data(data_NM_TCO, is_supply=True)
    demand_matrix, data_encode_demand = create_matrix_and_data(data_TCO_NPP, is_supply=False)

    distribution_data = {}
    distribution_data['supply_matrix'] = np.copy(supply_matrix)
    distribution_data['data_encode_supply'] = copy.copy(data_encode_supply)

    distribution_data['demand_matrix'] = np.copy(demand_matrix)
    distribution_data['data_encode_demand'] = copy.copy(data_encode_demand)

    return distribution_data

"""# 4. Ghi file"""

# Function to convert a NumPy array to a list
def ndarray_to_list(arr):
    """
    Convert a NumPy array to a Python list.

    Args:
    arr (ndarray): NumPy array.

    Returns:
    list: Python list.
    """
    return arr.tolist()

def write_file():
    # Save supply data to a compressed ZIP file
    supply_matrix, data_encode_supply = create_matrix_and_data(data_NM_TCO, is_supply=True)
    with zipfile.ZipFile("compressed_data_NM.zip", mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        dumped_JSON = json.dumps({"supply_matrix": ndarray_to_list(supply_matrix), "data_encode_supply": data_encode_supply},
                                ensure_ascii=False, indent=4)
        zip_file.writestr("data_NM.json", data=dumped_JSON)

    # Create and save matrices and data for demand
    demand_matrix, data_encode_demand = create_matrix_and_data(data_TCO_NPP, is_supply=False)
    with zipfile.ZipFile("compressed_data_NPP.zip", mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        dumped_JSON = json.dumps({"demand_matrix": ndarray_to_list(demand_matrix), "data_encode_demand": data_encode_demand},
                                ensure_ascii=False, indent=4)
        zip_file.writestr("data_NPP.json", data=dumped_JSON)

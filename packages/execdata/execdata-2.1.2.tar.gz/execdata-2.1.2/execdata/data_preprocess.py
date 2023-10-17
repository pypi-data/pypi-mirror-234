'''
Date         : 2023-10-11 13:39:36
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-10-11 16:55:32
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\data_preprocess.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''

import numpy as np
import pandas as pd


def filtered_value_list(df, column, limit_number):
    value_counts_series = df[column].value_counts()
    filtered_value_counts = value_counts_series[value_counts_series < limit_number]
    filtered_value_counts_list = filtered_value_counts.index.values.tolist()
    return filtered_value_counts_list, filtered_value_counts


def drop_columns(df, del_columns_list):
    if isinstance(del_columns_list, str):
        del_columns_list = [del_columns_list]
    elif isinstance(del_columns_list, list):
        del_columns_list = del_columns_list
    else:
        return print("input is not list or str! please redo the function with correct parameter.")
    for column in del_columns_list:
        df = df.drop(column, axis=1)
    return df

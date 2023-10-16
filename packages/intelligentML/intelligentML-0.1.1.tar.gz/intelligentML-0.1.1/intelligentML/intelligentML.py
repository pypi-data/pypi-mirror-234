"""Main module."""
import numpy as np
import pandas as pd


def hd_and_dp(dataPath):
    handle_duplication(dataPath)
    return dataPreprocessing(dataPath)


def handle_duplication(dataPath):
    dataSet = pd.read_csv(dataPath)
    # # Identify duplicate columns
    # duplicate_columns = data.columns[data.columns.duplicated()]
    # # Print duplicate column names
    # print("Duplicate Columns:", duplicate_columns)
    # # Drop duplicate columns
    # df = data.drop(columns=duplicate_columns)

    # Identify duplicate rows
    duplicates = dataSet.duplicated()
    # Print the duplicate rows
    print(f"Duplicate Rows Founded: \n{dataSet[duplicates]}")
    # Remove duplicate rows
    new_dataset = dataSet.drop_duplicates(keep='first')
    print("-----------------------------------------------------")
    print(f"After Removing Duplications: \n{new_dataset.head()}")
    print("-----------------------------------------------------")
    # data.to_csv('dataset.csv', index=False)
    # return dataPreprocessing(new_dataset)
    return new_dataset


def dataPreprocessing(dataPath):
    data = pd.read_csv(dataPath)
    # print(data)
    # print(data.describe())
    # print(data.info())
    # numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    print(f"Dataset null counter:\n{data.isnull().sum()}")
    print("-----------------------------------------------------")
    columns_with_nulls = data.columns[data.isnull().any()].tolist()
    column_data_types = data[columns_with_nulls].dtypes

    for column_name, data_type in column_data_types.items():
        if data_type == 'int64' or data_type == 'float64':
            # print(f"INT/FLOAT => {column_name}")
            # data[column_name] = data[column_name].fillna(data[column_name].mean())
            data.loc[:, column_name] = data[column_name].fillna(data[column_name].mean())
            # print(data.isnull().sum())
        if data_type == 'object':
            # print(f"OBJ ==> {column_name}")
            # data[column_name] = data[column_name].fillna(data[column_name].mode()[0])
            data.loc[:, column_name] = data[column_name].fillna(data[column_name].mode()[0])
            # print(data.isnull().sum())

    print(f"Dataset Without Nulls:\n{data.isnull().sum()}")
    print("-----------------------------------------------------")
    print(f"Preprocessed Data: \n{data.head()}")
    print("-----------------------------------------------------")

    # preprocessed_dataSet = data
    print(f"Preprocessed Data: \n{data.head()}")
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    print(f"{len(numerical_columns)} numerical_columns Data: \n{numerical_columns}")
    print(data.dtypes)
    return data

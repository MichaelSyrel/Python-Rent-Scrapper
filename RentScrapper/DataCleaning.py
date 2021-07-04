import pandas as pd
import numpy as np

# Loads a csv with name file_name
def load_csv(file_name):
    df = pd.read_csv(file_name)
    return df

# Checks whether a given value is a float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Changes a given column by name to numeric type
def set_column_to_numeric(df, col_name):
    df1 = df[df[col_name].apply(lambda x: (str(x).isnumeric() or isfloat(x)))].copy()  # Remove non numeric values
    df1[col_name] = df1[col_name].astype('float')  # Change the column type to float
    return df1



def outlier_detection_zscore_dist(df, cols):
    df2 = df.copy()
    for col in cols:
        z_score = (df2[col] - df2[col].mean()) / df2[col].std()
        outliers = abs(z_score) > 3
        df2.loc[outliers, col] = np.nan

    return df2


# Main start function for data cleaning and csv writing
def start():
    df = load_csv('./main.csv') # Load main csv table

    df1 = set_column_to_numeric(df, "price")  # Changes the price column to numeric

    df2 = set_column_to_numeric(df1, "rooms")  # Changes the rooms column to numeric

    df3 = set_column_to_numeric(df2, "furniture")  # Changes the furniture column to numeric

    df3.loc[(df3["price"] <= 1000) | (df3["price"] >= 25000), "price"] = np.nan  # Changes invalid price values to nan

    df3.loc[(df3["rooms"] <= 1) | (df3["rooms"] >= 7), "rooms"] = np.nan  # Changes invalid rooms values to nan

    df4 = outlier_detection_zscore_dist(df3, ["price", "rooms"])

    df5 = df4.copy().dropna(axis=0)

    df6 = set_column_to_numeric(df5, "size_in_meters") # Changes the size_in_meters column to numeric

    df6.loc[(df6["size_in_meters"] <= 1) | (df6["size_in_meters"] >= 2500), "size_in_meters"] = np.nan # Changes invalid size_in_meters values to nan

    df7 = df6.copy().dropna(axis=0)

    df8 = set_column_to_numeric(df7, "floor")  # Changes the floor column to numeric

    df9 = set_column_to_numeric(df8, "max_floor")  # Changes the max_floor column to numeric

    df10 = df9.copy().dropna(axis=0)

    df10.to_csv('FinalData.csv')  # Write the final table to a csv representation


if __name__ == '__main__':
    start()
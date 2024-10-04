import pandas as pd

def read_csv_to_dataframe(path):
    df = pd.read_csv(path)
    acc_df = df[["Acc_X", "Acc_Y", "Acc_Z"]]
    return acc_df

def read_csv_to_data_frame(path):
    df= pd.read_csv(path)
    return df
    
import pandas as pd
import glob
import os

def read_csv_to_dataframe(path):
    df = pd.read_csv(path)
    acc_df = df[["Acc_X", "Acc_Y", "Acc_Z"]]
    return acc_df

def read_csv_to_data_frame(path):
    df= pd.read_csv(path)
    return df

def read_all_patient_data_paths(patient_data_path):
    patient_file_paths = []
    excluded_dirs = {'.ipynb_checkpoints'}  # Use a set for faster lookups

    # List subdirectories, excluding the specified directories
    subdirs = [d for d in os.listdir(patient_data_path)
               if os.path.isdir(os.path.join(patient_data_path, d)) and d not in excluded_dirs]
    print(subdirs)
    
    # Loop through each subdirectory
    for subdir in subdirs:
        subdir_path = os.path.join(patient_data_path, subdir)    
        # Use glob to find all files in the current subdirectory
        files = glob.glob(os.path.join(subdir_path, '*.csv'))  # Get all files
        patient_file_paths.append((subdir, files[len(files)-2 : len(files)]))
    return patient_file_paths
    
def read_patient(p, patient_file_paths):
    left_path = ""
    right_path=""
    for p_num, files in patient_file_paths:
        if(int(p_num) == p):
            left_path = files[0]
            right_path = files[1]
    return left_path, right_path
    
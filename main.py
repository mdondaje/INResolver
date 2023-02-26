# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import os

# VALUES
# Target INR (international normalized ratio) values for patients receiving anti-clotting medicine
target_inr_min = 2.0
target_inr_mid = 2.5
target_inr_max = 3.0

# Referential body weight [kg]
referential_body_weight_men = 80
referential_body_weight_women = 60

# Dataset
patients_data_directory = 'patients_data'
results_directory = 'results'
delimiter = ','
number_of_fields_in_patients_data = 7

def solve(file):
    print(f'Hi, {file}')
    arr = np.loadtxt(file, delimiter=delimiter, dtype=str)
    print(arr)
    # np.datetime64


if __name__ == '__main__':
    # Run solver for each file in patient's data directory
    for filename in os.listdir(patients_data_directory):
        file = os.path.join(patients_data_directory, filename)
        # checking if it is a file
        if os.path.isfile(file):
            solve(file)

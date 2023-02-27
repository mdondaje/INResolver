# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
from datetime import datetime
import os

# MEDICAL VALUES
# Target INR (international normalized ratio) values for patients receiving anti-clotting medicine
target_inr_min = 2.0
target_inr_mid = 2.5
target_inr_max = 3.0

# Referential body weight [kg]
referential_body_weight_men = 80
referential_body_weight_women = 60

# DATASET
patients_data_directory = 'patients_data'
results_directory = 'results'
delimiter = ','
number_of_fields_in_patients_data = 8


def solve(file):
    patient_data_array = np.loadtxt(file, delimiter=delimiter, dtype=str)
    number_of_rows = len(patient_data_array)

    # COLUMNS WITH PATIENT'S DATA
    dates_column = patient_data_array[:, 0]
    inr_test_results_column = patient_data_array[:, 1].astype('float64')
    weights_column = patient_data_array[:, 2].astype('float64')
    diet_circumstances_column = patient_data_array[:, 3]
    other_medicines_taken_column = patient_data_array[:, 4]
    age_column = patient_data_array[:, 5].astype('float64')
    sex_column = patient_data_array[:, 6]
    prescribed_medicine_dose_column = patient_data_array[:, 7].astype('float64')

    # RESULT'S COLUMNS
    results = np.zeros([number_of_rows], dtype='float64')

    for row in range(number_of_rows):
        # RECORD DATA
        date = dates_column[row]
        inr_test_result = inr_test_results_column[row]
        weight = weights_column[row]
        diet_circumstances = diet_circumstances_column[row]
        other_medicines_taken = other_medicines_taken_column[row]
        age = age_column[row]
        sex = sex_column[row]
        prescribed_medicine_dose = prescribed_medicine_dose_column[row]

        if sex == 'M':
            referential_body_weight = referential_body_weight_men
        else:
            referential_body_weight = referential_body_weight_women

        # PROPER ALGORITHM
        # !!! for example !!!
        weight_ratio = weight / referential_body_weight
        results[row] = 4 + 2 * (target_inr_mid - inr_test_result) * weight_ratio
        # END OF PROPER ALGORITHM

    results_array = np.column_stack((dates_column, results))
    print(results_array)
    # PLOTS
    x_axis = [datetime.strptime(date, "%Y-%m-%d").date() for date in dates_column]
    fig, axs = plt.subplots(2, 1)
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title(f'{filename}')
    axs[0].plot(x_axis, inr_test_results_column, color='red', label='INR test result', marker='.')
    axs[0].set_title(f'{filename}')
    axs[0].set_ylabel('INR test result')
    axs[0].grid(True)
    for index in range(len(x_axis)):
        axs[0].text(x_axis[index], inr_test_results_column[index], inr_test_results_column[index])
    axs[0].legend()
    axs[0].margins(0.08)

    axs[1].plot(x_axis, results, label='Calculated', marker='.')
    axs[1].plot(x_axis,prescribed_medicine_dose_column, label='Prescribed', marker='.')
    axs[1].set_ylabel('Medicine dose [mg]')
    axs[1].grid(True)
    for index in range(len(x_axis)):
        axs[1].text(x_axis[index], results[index], f'{results[index]:.2f}')
        axs[1].text(x_axis[index], prescribed_medicine_dose_column[index], f'{prescribed_medicine_dose_column[index]:.2f}')
    axs[1].legend()
    axs[1].margins(0.08)
    fig.tight_layout()
    plt.savefig(f'{results_directory}/{filename}.png')
    plt.show()


if __name__ == '__main__':
    # Run solver for each file in patient's data directory
    for filename in os.listdir(patients_data_directory):
        file = os.path.join(patients_data_directory, filename)
        # checking if it is a file
        if os.path.isfile(file):
            solve(file)

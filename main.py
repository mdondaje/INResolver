# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import pylab
from datetime import datetime
import os

# MEDICAL VALUES
# Target INR (international normalized ratio) values for patients receiving anti-clotting medicine
target_inr_min = 2.0
target_inr_mid = 2.5
target_inr_max = 3.0
very_high_inr = 4.5

# DATASET
patients_data_directory = 'patients_data'
results_directory = 'results'
delimiter = ';'


def solve(data_file):
    print(f'{filename}')
    patient_data_array = np.loadtxt(data_file, delimiter=delimiter, dtype=str)
    # Delete row zero with columns' names
    patient_data_array = np.delete(patient_data_array, 0, axis=0)
    number_of_rows = len(patient_data_array)

    # COLUMNS WITH PATIENT'S DATA
    dates_column = patient_data_array[:, 0]
    dates_column = [datetime.strptime(date, "%d.%m.%Y").date() for date in dates_column]
    inr_test_results_column = patient_data_array[:, 1].astype('float64')
    other_medicines_taken_column = patient_data_array[:, 2]
    # diet_circumstances_column = patient_data_array[:, 3]
    # alt_test_result_column = patient_data_array[:, 4]
    # ast_test_result_column = patient_data_array[:, 5]
    # ggtp_test_result_column = patient_data_array[:, 6]
    prescribed_medicine_dose_column = patient_data_array[:, 7].astype('float64')

    medicine_type_column = patient_data_array[:, 8]

    # CONSTANT PATIENT'S DATA taken from first row
    birthdate = datetime.strptime(patient_data_array[0, 9], "%d.%m.%Y").date()
    sex = patient_data_array[0, 10]

    # RESULT'S COLUMNS
    results = np.zeros([number_of_rows], dtype='float64')

    for row in range(number_of_rows):
        # RECORD DATA
        date = dates_column[row]
        inr_test_result = inr_test_results_column[row]
        other_medicines_taken = other_medicines_taken_column[row]
        # diet_circumstances = diet_circumstances_column[row]
        # alt_test_result = alt_test_result_column[row]
        # ast_test_result = alt_test_result_column[row]
        # ggtp_test_result = ggtp_test_result_column[row]
        prescribed_medicine_dose = prescribed_medicine_dose_column[row]
        medicine_type = medicine_type_column[row]
        age = date - birthdate

        # PROPER ALGORITHM
        # results[row] = 3 + 2 * (target_inr_mid - inr_test_result)
        if medicine_type == 'A':
            if row == 0:
                results[row] = prescribed_medicine_dose
                print(f'{date}: brak wcześniejszego wyniku - set {prescribed_medicine_dose}')
            else:
                previous_prescribed_medicine_dose=prescribed_medicine_dose_column[row-1]
                if inr_test_result >= very_high_inr: # większe niż 4.5
                    results[row] = 0
                    print(f'{date}: INR {inr_test_result} bardzo za wysokie - set 0 mg')
                    # TODO male odchylenie przy wcześniejszych wynikach w normie
                    # TODO dodatkowy wspolczynnik dla danego pacjenta
                elif inr_test_result >= target_inr_max:  # większe niż 3.0
                    # wspolczynnik = odchylenie / zakres
                    factor = (inr_test_result - target_inr_mid) / (very_high_inr - target_inr_max)
                    results[row] = previous_prescribed_medicine_dose * (1 - 0.5*factor)
                    print(f'{date}: INR {inr_test_result} za wysokie - zmniejsz do {results[row]} mg')
                elif inr_test_result >= target_inr_min:  # 2.0-3.0
                    results[row] = previous_prescribed_medicine_dose
                    print(f'{date}: INR {inr_test_result} w normie - zostaw {results[row]} mg')
                else:  # INR test result below target_inr_min
                    factor = (target_inr_mid - inr_test_result) / target_inr_min
                    if previous_prescribed_medicine_dose == 0:
                        results[row] = 2 * factor
                        print(f'a {date}: INR {inr_test_result} za niskie - zwiększ do {results[row]} mg')
                    else:
                        results[row] = previous_prescribed_medicine_dose * (1 + 0.5*factor)
                        print(f'{date}: INR {inr_test_result} za niskie - zwiększ do {results[row]} mg')
        else:
            print('ERROR!!!')

        # ROUNDING off floating digits to the nearest 0.5
        # results[row] = round((results[row] * 2) / 2)
        results[row] = round(results[row])

        # END OF PROPER ALGORITHM

    results_array = np.column_stack((dates_column, results))
    #print(results_array)

    # PLOTS
    fig, axs = plt.subplots(2, 1)
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title(f'{filename}')
    axs[0].plot(dates_column, inr_test_results_column, color='C3', label='INR test result', marker='.')
    axs[0].set_title(f'{filename}')
    axs[0].set_ylabel('INR test result')
    axs[0].xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(axs[0].xaxis.get_major_locator()))
    axs[0].grid(True)
    for index in range(len(dates_column)):
        axs[0].text(dates_column[index], inr_test_results_column[index], inr_test_results_column[index])
    axs[0].legend()
    axs[0].margins(0.08)

    axs[1].plot(dates_column, prescribed_medicine_dose_column, color='C1', label='Prescribed', marker='.')
    axs[1].plot(dates_column, results, color='C0', label='Calculated', marker='.')
    axs[1].set_ylabel('Medicine dose [mg]')
    axs[1].xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(axs[1].xaxis.get_major_locator()))
    axs[1].xaxis_date()
    axs[1].grid(True)
    for index in range(len(dates_column)):
        axs[1].text(dates_column[index], results[index], f'{results[index]:.1f}')
        try:
            axs[1].text(dates_column[index], prescribed_medicine_dose_column[index],
                        f'{prescribed_medicine_dose_column[index]:.1f}')
        except ValueError:
            pass
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

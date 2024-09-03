import pandas as pd
import numpy as np
from statsmodels.stats.diagnostic import lilliefors
import os

# upload the CSV file
# define the CSV file path
script_dir = os.path.dirname(os.path.abspath(__file__))  # obtain the current script directory
file_path = os.path.join(script_dir, '..', 'simulation_results.csv')  # CSV file path

# takes data using the pandas library
data = pd.read_csv(file_path)

# list of metrics to test
metrics = ['elapsed_time', 'min_distance', 'crash_count', 'missed_silver_tokens']

# DIvide the data for different implementations (the lilliefors test will be done for each implementation)
data_russo = data[data['script_name'] == 'AssignmentRussoGabriele.py']
data_assignment1 = data[data['script_name'] == 'assignment1.py']

# function for execute the Lilliefors test
def lilliefors_test(data, metric):
    if np.std(data[metric]) == 0:  # check if standard deviation is zero
        return 'N/A', 'N/A'
    stat, p_value = lilliefors(data[metric])
    return stat, p_value

# execute the Lilliefors test for each metrics of each implementation
results = {}
for metric in metrics:
    russo_stat, russo_p = lilliefors_test(data_russo, metric)
    assignment1_stat, assignment1_p = lilliefors_test(data_assignment1, metric)
    
    results[metric] = {
        'Russo': {'statistic': russo_stat, 'p-value': russo_p},
        'Assignment1': {'statistic': assignment1_stat, 'p-value': assignment1_p}
    }

# print the result
for metric, result in results.items():
    print(f"\nMetric: {metric}")
    print(f"  AssignmentRussoGabriele.py -> Statistic: {result['Russo']['statistic']}, p-value: {result['Russo']['p-value']}")
    print(f"  assignment1.py -> Statistic: {result['Assignment1']['statistic']}, p-value: {result['Assignment1']['p-value']}")


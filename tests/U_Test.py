import pandas as pd
from scipy.stats import mannwhitneyu
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Construct the path to the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
csv_path = os.path.join(script_dir, '..', 'simulation_results.csv')  # Path to your CSV file

# Load the CSV file
data = pd.read_csv(csv_path)

# Split the data by implementation
data_russo = data[data['script_name'] == 'AssignmentRussoGabriele.py']
data_assignment1 = data[data['script_name'] == 'assignment1.py']

# List of metrics to test
metrics = ['elapsed_time', 'min_distance']

# Perform the Mann-Whitney U test for each metric
results = {}
for metric in metrics:
    # Perform the test (two-sided by default, change to 'greater' or 'less' for one-sided)
    stat, p_value = mannwhitneyu(data_russo[metric], data_assignment1[metric], alternative='two-sided')
    results[metric] = {'statistic': stat, 'p-value': p_value}

# Print the results
for metric, result in results.items():
    print(f"\nMetric: {metric}")
    print(f"  Statistic: {result['statistic']}, p-value: {result['p-value']}")

# Calculate medians
median_russo = data_russo['min_distance'].median()
median_assignment1 = data_assignment1['min_distance'].median()

# Calculate means
mean_russo = data_russo['min_distance'].mean()
mean_assignment1 = data_assignment1['min_distance'].mean()

print("")
print(f"Median min_distance for AssignmentRussoGabriele.py: {median_russo}")
print(f"Median min_distance for assignment1.py: {median_assignment1}")
print("")
print(f"Mean min_distance for AssignmentRussoGabriele.py: {mean_russo}")
print(f"Mean min_distance for assignment1.py: {mean_assignment1}")

# HIstogram
plt.figure(figsize=(10, 6))
plt.hist(data_russo['min_distance'], bins=10, alpha=0.5, label='AssignmentRussoGabriele.py')
plt.hist(data_assignment1['min_distance'], bins=10, alpha=0.5, label='assignment1.py')
plt.xlabel('min_distance')
plt.ylabel('Frequency')
plt.title('Histogram of min_distance for Two Implementations')
plt.legend(loc='upper right')
plt.show()



import pandas as pd
import os

# Construct the path to the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
csv_path = os.path.join(script_dir, '..', 'simulation_results.csv')  # Path to your CSV file

# Load the CSV file
data = pd.read_csv(csv_path)

# Create the contingency table by counting occurrences
contingency_table = pd.crosstab(data['script_name'], data['completed_circuit'])
print("")
print("")
# Display the contingency table
print("Contingency Table:")
print("")
print(contingency_table)

# Extract the individual counts needed for the Chi-Square test
observed_success_russo = contingency_table.loc['AssignmentRussoGabriele.py', True]
observed_failure_russo = contingency_table.loc['AssignmentRussoGabriele.py', False]

observed_success_assignment1 = contingency_table.loc['assignment1.py', True]
observed_failure_assignment1 = contingency_table.loc['assignment1.py', False]

print("\nObserved Frequencies:")
print(f"AssignmentRussoGabriele.py - Success: {observed_success_russo}, Failure: {observed_failure_russo}")
print(f"assignment1.py - Success: {observed_success_assignment1}, Failure: {observed_failure_assignment1}")
print("")
print("")

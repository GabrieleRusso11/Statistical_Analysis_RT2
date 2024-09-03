import subprocess
import time

# Define the number of iterations
num_iterations = 30
config_path = "games/sunny_side_up.yaml"  # Use the correct path and file name

# Loop to run the scripts multiple times
for i in range(num_iterations):
    print("Iteration {} of {}".format(i + 1, num_iterations))

    # Generate a random seed based on the current time
    seed = int(time.time())  # Current time as an integer seed

    # Run the first script (AssignmentRussoGabriele.py) with the seed
    print("Running AssignmentRussoGabriele.py with seed {}...".format(seed))
    subprocess.call(["python2", "run.py", "-c", config_path, "AssignmentRussoGabriele.py", "--seed", str(seed)])

    # Wait a brief moment to ensure the first script has fully finished
    time.sleep(2)

    # Run the second script (assignment1.py) with the same seed
    print("Running assignment1.py with seed {}...".format(seed))
    subprocess.call(["python2", "run.py", "-c", config_path, "assignment1.py", "--seed", str(seed)])

    # Optionally wait before the next iteration
    print("Completed iteration {}. Waiting before the next iteration...".format(i + 1))
    time.sleep(5)  # Adjust the sleep time as needed

print("All iterations completed.")


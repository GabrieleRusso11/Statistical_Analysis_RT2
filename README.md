# Gabriele Russo's Statistical Analysis of the first assignment for the Research Track 1 course (Mat. 5180813)

## Installation and how to run
If you want to install the application you can follow the indications in the [first assignment repository](https://github.com/GabrieleRusso11/RT_Assignment1)

## Overview
In this repository you will find all the necessary files that I have implemented and used to perform a statistical analysis in order to compare my implementation of the Research Track 1 first assignment (AssignmentRussoGabriele.py) with Professor Recchiuto’s implementation (assignment1.py).

### Some changes
Some files are the same of the [first assignment repository](https://github.com/GabrieleRusso11/RT_Assignment1) but there are some changes in order to collect all the needed performance metrics for the statistical analysis. All the files in this repository are specifically designed to perform simulations and collect data. Additionally, the repository includes a new folder named 'tests,' which contains all the Python scripts used for the analysis.

### How to Run the simulations
To run the simulations autonomously, execute the following command from the folder created after cloning this repository:

```
 python2 run_multiple_times.py
 ```

With this command line, will be executed both implementations (AssignmentRussoGabriele.py and assignment1.py) for 30 times. Each i-th simulation (or execution) has the same condition for both implementations, therefore the same number of tokens and the same displacement in the circuit, but the number and the displacement of the silver token is randomly changed when it pass from the i-th simulation to the i+1 simulation. In this way, each simulation has a scenario that differs from the other simulation.

### Conclusion
In the file 'simulation_results.csv' there are the data that I have collected during my simulations.
If you want to know How I have performed the Statistical Analysis using this data, read the report present in this repository. ([report](https://github.com/GabrieleRusso11/Statistical_Analysis_RT2/blob/main/Statistical_Analysis_Gabriele_Russo.pdf))
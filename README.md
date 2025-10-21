# Asphalt Back-End

## Flask App - `main.py`

The flask app, found in `main.py` simply provides an endpoint for the front end to get an optimized route from.

The POST endpoint, `/reorder_stops` takes a json object with a "stop" key and a corresponding value of a list of stops, and then returns
the stops dict with the correct order applied to the list.

Notably, the end point calls methods from the `ithaca_model` module, which is the entry point for the TSP/OR-Tools Solver

## Model

### Overview

First off, there is a lot of extraneous code kept for testing/legacy purposes, which will have to be cleaned later. The only three files you have to care about are

- `ithaca_model.py`
- `data_generation.py`
- `data_calculation.py`

These three modules contain the necessary methods to generate the data necessary to solve the TSP, solve the TSP, and then return the relevant solution data.
I will subsequently describe each of these in a bit more detail.

### Ithaca Model - `ithaca_model.py`

This module encompasses the main workflow for the solver. In fact, by tracing `find_solution()` you can generally get a good idea of how the entire solve works. Aside from this,
the other methods interact directly with the OR-Tools API.

- `format_tsp( ... )` : Formats the cost matrix for the TSP using work values as the cost and location_to_index for matrix index, also using high cost and zeroes to dissuade certain paths
- `solve_tsp( ... )` : Initialize the solver objects from the OR-Tools API and also segment dict callback using the work matrix. Finally, set the problem parameters and solve

### Data Calculations - `data_calculations.py`

This module contains all of the methods for creating matrices of data using physics-based calculations. Essentially, the model uses elevation, velocity, and distance to calculate the theoretical work between segments, then finds the external work constant (stuff like noise, energy loss), by subtracting the theoretical work of the original route from the total measured work of the original route (calculated through fuel * Joules per liter). This constant, w_ext (work external), can then be applied later when comparing our new optimized route with the baseline.

- `compute_work_theoretical_matrix( ... )` : takes various parameters containing elevation, distance, duration, etc. to compute a matrix with the information of the work theoretical between every possible two stop segment
- `determine_w_ext( ... )` : aforementioned method that subtracts the w_th of the original route from the measured total work, extracting a constant of external work.
- `compute_work_for_route( ... )` : Computes the work for a specific route, with or without w_ext provided

And various other util functions.

### Data Generation - `data_generation.py`

NOTE: A lot of the info is hard-coded in the absence of an API we can use cheaply and frequently to do location lookup + segment data.

Essentially, this module defines some utility methods to load the data from csv files, and also defines some hard coded constants for ithaca specific locations. This will be subject to change hopefully soon!

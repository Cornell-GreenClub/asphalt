"""

Calculations necessary to compute the costs between each node for the TSP problem


"""


# constants
g = 9.81  # gravitational acceleration [m/s^2]
fuel_consumption_liters = 246.052/5  # fuel consumption given by TST
diesel_to_J = 38290000  # conversion for diesel to J

"""
    Computes the work actual matrix for all segments in the route.

    Args:
        distance_data (list of dict): Distance and time data for segments.
        elevation_data (list of dict): Elevation data for locations.
        weight_data (list of dict): Weight data for locations.
        f (float): The constant f determined from route data.

    Returns:
        list of dict: Work data for each segment.
"""
def compute_work_theoretical_matrix(distance_data, elevation_data, weight_data, location_to_index, w_ext):
    
    work_matrix = []

    location_to_elevation = {row['name']: int(
        row['elevation_in_m']) for row in elevation_data}
    location_to_weight = {row['start']: float(
        row['weight average']) for row in weight_data}

    for row in distance_data:
        #NOTE: this below is a ithaca only jank solution
        #only add to the work matrix IF the start and end are part of the current problem
        if (location_to_index.get(row['end']) == None or location_to_index.get(row['start']) == None):
            continue

        start = row['start']
        end = row['end']
        dist_km = float(row['DIST_KM'])
        duration_h = float(row['DURATION_H'])

        # calculate v_avg (average velocity) in m/s
        v_avg = (dist_km * 1000) / (duration_h * 3600)

        # get mass (m) and elevation change (delta h)
        m = location_to_weight.get(start, 0) + 18325.1317
        #if start == 'tst boces tompkins':
        #    m = 18325.1317
        delta_h = location_to_elevation.get(
            end, 0) - location_to_elevation.get(start, 0)

        # calculate theoretical and actual work
        w_th = 0.5 * m * v_avg**2 + m * g * delta_h #if mgh < 0, make it 0

        if (w_th < 0):
            w_th = 0.5 * m * v_avg**2

        # append calculated values for each path segment
        work_matrix.append({
            'start': start,
            'end': end,
            'mass (m)': m,
            'v_avg': v_avg,
            'delta_h': delta_h,
            'W_ThA->B': w_th,
        })

    return work_matrix

"""
Determines an f value, or inefficiency coefficient, for work actual computation


"""
def determine_w_ext(work_data): #old: determine_f(work_data)
    """
    Determines the constant f from the model for the specified route.
    """
    total_wth = sum(segment['W_ThA->B'] for segment in work_data)

    #print("total w_th: ", total_wth)

    w_actual_total = fuel_consumption_liters * diesel_to_J
    return w_actual_total - total_wth #old: (w_actual_total / total_wth) - 1


"""
Computes total work done (theoretical and actual) for a specific route using cumulative mass.

Two possible outputs depending on whether f is provided:
    1. Dictionary including theoretical work for route (calculated if f is not provided or is 0)
    2. Dictionary including both theoretical and actual work for route (calculated if f provided is non-zero) 
    - used for finding cost of optimized route

route: a list with indices representing the route if the original route is 0, 1... n
distance_data: a list of dictionaries with the distance between every two stops
weight_data: a list of dicts with the weight added at each combination of two stops
index_to_location_name: a list where each index corresponds to a location name
work_actual_f: inefficiency coefficient TODO: update calcs

returns: a list of dicts represnting the work between all two stop combinations

"""
def compute_work_for_route(route, distance_data, elevation_data, weight_data, index_to_location_name, w_ext=0,): #last param old: work_actual_f=0
    # map location indices to elevation and weight data
    location_to_elevation = {row['name']: int(
        row['elevation_in_m']) for row in elevation_data}
    location_to_weight = {row['start']: float(
        row['weight average']) for row in weight_data}

    # build dictionary for quick segment lookup
    segment_data = {(row['start'], row['end']): row for row in distance_data}

    # initialize cumulative mass
    cumulative_mass = 0
    work_data = []

    # iterate through the route segments
    for i in range(len(route) - 1):
        start = route[i]
        end = route[i + 1]

        # get the segment data
        segment_key = (
            index_to_location_name[start], index_to_location_name[end])
        segment = segment_data.get(segment_key)

        dist_km = float(segment['DIST_KM'])
        duration_h = float(segment['DURATION_H'])

        # calculate v_avg (average velocity) in m/s
        v_avg = (dist_km * 1000) / (duration_h * 3600)

        # get segment mass and elevation change
        segment_mass = location_to_weight.get(index_to_location_name[start], 0)
        if index_to_location_name[start] == 'tst boces tompkins' or index_to_location_name[start] == '14. tompkins recycling':
            cumulative_mass = 0
            segment_mass = 18325.1317  # mass of empty truck

        cumulative_mass += segment_mass  # accumulate mass

        #print("mass for segment", i, ":", cumulative_mass)

        if index_to_location_name[start] == '14. tompkins recycling':
            cumulative_mass = 18325.1317  # mass of empty truck

        delta_h = location_to_elevation.get(index_to_location_name[end], 0) - \
            location_to_elevation.get(index_to_location_name[start], 0)

        # calculate theoretical work
        w_th = 0.5 * cumulative_mass * v_avg**2 + cumulative_mass * g * delta_h

        if (w_th < 0):
            w_th = 0.5 * cumulative_mass * v_avg**2

        # calculate actual work depending on if f is provided, if not add
        # other calculated values to the dictionary to return
        work_entry = {
            'start': index_to_location_name[start],
            'end': index_to_location_name[end],
            'segment_mass': segment_mass,
            'cumulative_mass': cumulative_mass,
            'v_avg': v_avg,
            'delta_h': delta_h,
            'W_ThA->B': w_th,
        }
        # add actual work if f is non-zero
        #print("Work Theoretical For ", index_to_location_name[start], " to ", index_to_location_name[end], " : ", w_th)
        #print("V_avg for ", index_to_location_name[start], " to ", index_to_location_name[end], " : ", v_avg)

        work_data.append(work_entry)
    return work_data

"""
    Calculates total work from given matrix by accumulating actual work
"""
def calculate_total_work_cost_in_J(work_matrix, w_ext):
    return sum(segment['W_ThA->B'] for segment in work_matrix) + w_ext #sum(segment['W_AA->B'] for segment in work_matrix)

def calculate_original_cost_in_J():
    return fuel_consumption_liters * diesel_to_J
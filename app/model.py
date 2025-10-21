import csv
import numpy as np
from ortools.constraint_solver import routing_enums_pb2, pywrapcp


# constants
g = 9.81  # gravitational acceleration [m/s^2]
fuel_consumption_liters = 246.052/5  # fuel consumption given by TST
diesel_to_J = 38290000  # conversion for diesel to J

# original route
original_route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# mapping of locations to indices (TODO: clean this up)
location_to_index = {
    'tst boces tompkins': 0,
    '1. dewitt middle school': 1,
    '2. northeast elementary': 2,
    '3. cayuga heights elementary': 3,
    '4. belle sherman': 4,
    '5. caroline elementary': 5,
    '6. south hill elementary': 6,
    '7. bjm elementary': 7,
    '8. fall creek elementary': 8,
    '9. boynton middle school': 9,
    '10. maint garage': 10,
    '11. bus garage': 11,
    '12. enfield elementary': 12,
    '13. lehman alternative': 13,
    '14. tompkins recycling': 14
}
index_to_location_name = [None] * (15)
for location, index in location_to_index.items():
    index_to_location_name[index] = location


def parse_matrix(file_path):
    """
    Reads a CSV file and returns as a list of dictionaries.
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def compute_work_for_route(route, distance_data, elevation_data, weight_data, work_actual_f):
    """
    Computes work values (either theoretical or actual) for a specific route using cumulative mass.

    Two possible outputs depending on whether f is provided:
    1. Dictionary including theoretical work for route (calculated if f provided is 0)
    2. Dictionary including both theoretical and actual work for route
    (calculated if f provided is non-zero)

    Args:
        route (list of int): List of location indices representing the route.
        distance_data (list of dict): Distance and time data for segments.
        elevation_data (list of dict): Elevation data for locations.
        is_work_actual (int): 0 if not calculating work_actual, f value in model if calculating work actual

    Returns:
        list of dict: Work data for the specified route.
    """
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
        if index_to_location_name[start] == 'tst boces tompkins':
            segment_mass = 18325.1317  # mass of empty truck

        cumulative_mass += segment_mass  # accumulate mass

        print("Route segment", i, "weight:" , cumulative_mass)

        delta_h = location_to_elevation.get(index_to_location_name[end], 0) - \
            location_to_elevation.get(index_to_location_name[start], 0)

        # calculate theoretical work
        w_th = 0.5 * cumulative_mass * v_avg**2 + cumulative_mass * g * delta_h

        # calculate actual work depending on if f is provided, if not add
        # other calculated values to the dictionary to return
        if (work_actual_f == 0):
            work_data.append({
                'start': index_to_location_name[start],
                'end': index_to_location_name[end],
                'segment_mass': segment_mass,
                'cumulative_mass': cumulative_mass,
                'v_avg': v_avg,
                'delta_h': delta_h,
                'W_ThA->B': w_th,
            })
        else:
            #w_actual = w_th * (1 + work_actual_f)
            # w_int = wth + w_ext
            w_actual = w_th + work_actual_f
            print("Work actual: ", work_actual_f)
            work_data.append({
                'start': index_to_location_name[start],
                'end': index_to_location_name[end],
                'segment_mass': segment_mass,
                'cumulative_mass': cumulative_mass,
                'v_avg': v_avg,
                'delta_h': delta_h,
                'W_ThA->B': w_th,
                'W_AA->B': w_actual
            })

    return work_data

# def determine w_ext
def determine_w_ext(work_data):
    """
    Determines the constant f from the model for the specified route.

    Args:
        work_data (list of dict): Work data for the specified route.
        fuel_consumption_liters (float): Total fuel consumption for the route.
        diesel_to_J (float): Conversion factor for diesel to joules.

    Returns:
        float: The constant f from the emissions optimization model
    """
    total_wth = sum(segment['W_ThA->B'] for segment in work_data)

    sum1 = 0

    print("Printing individual segments")
    for segment in work_data:
        sum1 += segment['W_ThA->B']
        print(segment["W_ThA->B"])

    print("computed sum:", sum1)


    print("Calculated total work in determine_w_ext: ", total_wth)
    #w_actual_total = fuel_consumption_liters * diesel_to_J
    w_internal_total = fuel_consumption_liters * diesel_to_J

    print("Calculated total internal work in determine_w_ext: ", w_internal_total)
    return w_internal_total - total_wth
    #return (w_actual_total / total_wth) - 1


def compute_work_actual_matrix(distance_data, elevation_data, weight_data, f):
    """
    Computes the work matrix for all segments in the route.

    Args:
        distance_data (list of dict): Distance and time data for segments.
        elevation_data (list of dict): Elevation data for locations.
        weight_data (list of dict): Weight data for locations.
        f (float): The constant f determined from route data.

    Returns:
        list of dict: Work data for each segment.
    """
    work_matrix = []

    location_to_elevation = {row['name']: int(
        row['elevation_in_m']) for row in elevation_data}
    location_to_weight = {row['start']: float(
        row['weight average']) for row in weight_data}

    for row in distance_data:
        start = row['start']
        end = row['end']
        dist_km = float(row['DIST_KM'])
        duration_h = float(row['DURATION_H'])

        # calculate v_avg (average velocity) in m/s
        v_avg = (dist_km * 1000) / (duration_h * 3600)

        # get mass (m) and elevation change (delta h)
        m = location_to_weight.get(start, 0) + 18325.1317
        delta_h = location_to_elevation.get(
            end, 0) - location_to_elevation.get(start, 0)

        # calculate theoretical and actual work
        w_th = 0.5 * m * v_avg**2 + m * g * delta_h
        #w_actual = w_th * (1 + f) TODO
        w_actual = w_th + f #new model, work actual is external plus theoretical

        # append calculated values for each path segment
        work_matrix.append({
            'start': start,
            'end': end,
            'mass (m)': m,
            'v_avg': v_avg,
            'delta_h': delta_h,
            'W_ThA->B': w_th,
            'W_AA->B': w_actual
        })

    return work_matrix


def format_tsp(work_matrix):
    """
    Converts the work matrix into a ORTools TSP-compatible distance matrix.

    Args:
        work_matrix (list of dict): Work data between all pairs of locations.

    Returns:
        dict: Data model containing the TSP distance matrix and problem details for ORTools
    """

    # create an empty cost matrix
    num_locations = len(location_to_index)
    cost_matrix = np.zeros((num_locations, num_locations))

    # populate the distance matrix with actual work values
    for row in work_matrix:
        start = row['start']
        end = row['end']
        w_actual = row['W_AA->B']
        start_idx = location_to_index[start]
        end_idx = location_to_index[end]
        cost_matrix[start_idx][end_idx] = abs(w_actual)

    num_nodes = len(cost_matrix)

    # add an edge from the end node to the start node with 0 cost (for tsp)
    cost_matrix[num_nodes - 1][0] = 0

    # add edges from every other node to the start node with very high cost (for tsp)
    high_cost = float('inf')
    for i in range(1, num_nodes - 1):
        cost_matrix[i][0] = high_cost

    # convert matrix to int for compatibility with OR-Tools
    cost_matrix = cost_matrix.astype(int)

    # create data dictionary to feed into TSP model
    data = {
        "cost_matrix": cost_matrix.tolist(),
        "num_vehicles": 1,  # single vehicle for TSP (OR-tools argument)
        "depot": 0  # fixed starting point (OR-tools argument)
    }
    return data


def save_matrix_to_csv(matrix, output_file_name):
    """
    Saves list of dictionaries representing the matrix to a CSV file.
    """
    if not matrix:
        print("Matrix is empty. Nothing to save.")
        return

    # extract field names from the first dictionary in the matrix
    fieldnames = matrix[0].keys()

    # write data to the CSV file
    with open(output_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matrix)


def print_and_return_solution(manager, routing, solution):
    """
    Prints solution on console. (ORTools provided function)

    Returns:
        list: Optimized route in form of indices
    """
    print(f"Total work: {solution.ObjectiveValue()}")
    index = routing.Start(0)
    plan_output = "Route:\n"
    route_distance = 0
    route_indices = []
    while not routing.IsEnd(index):
        plan_output += f" {
            index_to_location_name[manager.IndexToNode(index)]} ->"
        route_indices.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, 0)
    plan_output += f" {index_to_location_name[manager.IndexToNode(index)]}\n"
    route_indices.append(manager.IndexToNode(index))
    print(plan_output)
    return route_indices


def calculate_total_work_cost_in_J(work_matrix, f):
    """
    Calculates total work from given matrix by accumulating actual work
    """
    return sum(segment['W_ThA->B'] for segment in work_matrix)


def solve_tsp(data):
    """
    Finds the optimized route using ORTools

    Args:
        data: data dictionary to feed into TSP model

    Returns:
        list: Optimized route in form of indices
    """

    # Create the routing index manager for ORTools
    manager = pywrapcp.RoutingIndexManager(
        len(data["cost_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create routing model for ORTools
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes. (ORTools provided)"""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["cost_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print and return solution
    opt_indices = print_and_return_solution(manager, routing, solution)
    return opt_indices


def main():
    # Load csv data files
    distance_data = parse_matrix('distance_time_matrix.csv')
    elevation_data = parse_matrix('elevation_matrix.csv')
    weight_data = parse_matrix('weight_matrix.csv')

    # Determine f
    work_for_original_route = compute_work_for_route(
        original_route, distance_data, elevation_data, weight_data, 0)
    
    f_value = abs(determine_w_ext(work_for_original_route))
    print(f"Determined value of f: {f_value:.4f}")

    # Compute the work matrix using f
    work_matrix = compute_work_actual_matrix(
        distance_data, elevation_data, weight_data, f_value)

    # Save work matrices
    save_matrix_to_csv(work_matrix, 'work_matrix.csv')
    save_matrix_to_csv(work_for_original_route, 'work_for_original_route.csv')

    # Format work matrix into a ORTools TSP-compatible distance matrix
    tsp_data = format_tsp(work_matrix)

    # Find optimized route using ORTools
    opt_route = solve_tsp(tsp_data)
    work_for_opt_route = compute_work_for_route(
        opt_route, distance_data, elevation_data, weight_data, f_value)
    total_cost_for_opt_route = calculate_total_work_cost_in_J(
        work_for_opt_route, f_value)
    save_matrix_to_csv(work_for_opt_route, 'work_for_opt_route.csv')

    # Display route and cost
    print("Optimized Route Indices:", opt_route)
    print("Route Cost:", total_cost_for_opt_route)

    work_for_bad_route = compute_work_for_route(original_route, distance_data, elevation_data, weight_data, f_value)
    total_cost_for_bad_route = calculate_total_work_cost_in_J(work_for_bad_route, f_value)

    print("Bad Route: ", original_route)
    print("Bad Route Cost: ", total_cost_for_bad_route)


if __name__ == "__main__":
    main()

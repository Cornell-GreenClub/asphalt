import numpy as np
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from data_generation import parse_matrix, get_original_route,save_matrix_to_csv, create_index_to_location, addresses_to_location_to_index
from data_calculations import compute_work_for_route, determine_w_ext, compute_work_theoretical_matrix, calculate_total_work_cost_in_J, calculate_original_cost_in_J

"""
high level function that summarizes the entire calculation model of the process

stops: a list of dictionaries of stops

returns: a stops reordered to match the solution of the TSP problem
"""
def find_solution(stops):
    #create mappings for name and index
    location_to_index = addresses_to_location_to_index(stops)
    index_to_location_name = create_index_to_location(location_to_index)

    # load csv data files
    distance_data = parse_matrix('distance_time_matrix.csv')
    elevation_data = parse_matrix('elevation_matrix.csv')
    weight_data = parse_matrix('weight_matrix.csv')

    # determine f
    original_route = get_original_route(stops)
    work_for_original_route = compute_work_for_route(
        original_route, distance_data, elevation_data, weight_data, index_to_location_name, 0)
    w_ext_value = abs(determine_w_ext(work_for_original_route)) #was abs
    print(f"Determined value of w_ext: {w_ext_value:.4f}")

    # compute the work matrix using f
    work_matrix = compute_work_theoretical_matrix(
        distance_data, elevation_data, weight_data, location_to_index, w_ext_value)
    
    # save work matrices
    save_matrix_to_csv(work_matrix, 'work_matrix.csv')
    save_matrix_to_csv(work_for_original_route, 'work_for_original_route.csv')

    # format work matrix into a ORTools TSP-compatible distance matrix
    tsp_data = format_tsp(work_matrix, location_to_index)

    # find optimized route using ORTools
    opt_route = solve_tsp(tsp_data, work_matrix, w_ext_value, index_to_location_name)
    work_for_opt_route = compute_work_for_route(
        opt_route, distance_data, elevation_data, weight_data, index_to_location_name, w_ext_value)
    total_cost_for_opt_route = calculate_total_work_cost_in_J(
        work_for_opt_route, w_ext_value)
    save_matrix_to_csv(work_for_opt_route, 'work_for_opt_route.csv')

    # display route and cost
    #print("Optimized Route Indices:", opt_route)
    print("Route Cost:", total_cost_for_opt_route)

    #work1 = compute_work_for_route(
    #    original_route, distance_data, elevation_data, weight_data, index_to_location_name, w_ext_value)
    #total = calculate_total_work_cost_in_J(work1, w_ext_value)
    print("original cost:", calculate_original_cost_in_J())

    print("recalulated original cost:", calculate_total_work_cost_in_J(work_for_original_route, w_ext_value))

    return opt_route

"""
Finds the optimized route using ORTools to solve TSP
"""
def solve_tsp(data, work_matrix, w_ext_value, index_to_location_name):


    # create the routing index manager for ORTools
    manager = pywrapcp.RoutingIndexManager(
        len(data["cost_matrix"]), data["num_vehicles"], data["depot"]
    )

    # create routing model for ORTools
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes. (ORTools provided)"""
        # convert from routing variable Index to distance matrix NodeIndex
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["cost_matrix"][from_node][to_node]

    segment_dict = {(row['start'], row['end']): row for row in work_matrix}

    #distance_callback.cumulative_mass = [0] * len(data["cost_matrix"])
    #distance_callback.cumulative_mass[0] = 0  # default starting mass

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # print and return solution
    opt_indices = print_and_return_solution(manager, routing, solution, index_to_location_name)
    return opt_indices


"""
    Converts the work matrix into a ORTools TSP-compatible distance matrix.

    Args:
        work_matrix (list of dict): Work data between all pairs of locations.

    Returns:
        dict: Data model containing the TSP distance matrix and problem details for ORTools
"""
def format_tsp(work_matrix, location_to_index):
    # create an empty cost matrix
    num_locations = len(location_to_index)
    cost_matrix = np.zeros((num_locations, num_locations))

    # populate the distance matrix with actual work values
    for row in work_matrix:
        start = row['start']
        end = row['end']
        w_th = row['W_ThA->B']
        start_idx = location_to_index[start]
        end_idx = location_to_index[end]
        cost_matrix[start_idx][end_idx] = w_th #was abs

    high_cost = float('inf')

    num_nodes = len(cost_matrix + 1)

    # add an edge from the end node to the start node with 0 cost (for tsp)
    cost_matrix[num_nodes - 1][0] = 0

    # add edges from every other node to the start node with very high cost (for tsp)
    high_cost = 10**11
    for i in range(1, num_nodes - 1):
        cost_matrix[i][0] = high_cost

    print(cost_matrix)

    # shift the matrix to make all values non-negative
    min_value = np.min(cost_matrix)
    print("min_value:", min_value)
    if min_value < 0:
        cost_matrix += abs(min_value) 

    # convert matrix to int for compatibility with OR-Tools
    cost_matrix = cost_matrix.astype(int)

    # create data dictionary to feed into TSP model
    data = {
        "cost_matrix": cost_matrix.tolist(),
        "num_vehicles": 1,  # single vehicle for TSP (OR-tools argument)
        "depot": 0  # fixed starting point (OR-tools argument)
    }

    print(cost_matrix)

    return data


"""
    Prints solution on console. (ORTools provided function)

    Returns:
        list: Optimized route in form of indices
"""
def print_and_return_solution(manager, routing, solution, index_to_location_name):

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
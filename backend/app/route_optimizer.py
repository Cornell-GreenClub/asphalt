"""
Main route optimization class.
1. Optimizes route based on API-provided 'distances' (assumed to be in METERS).
2. Compares fuel cost (distance / mpg) of original vs. optimized route.
"""
import numpy as np
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

# --- Constants for conversion ---
METERS_PER_KM = 1000.0
MILES_PER_KM = 0.621371

class RouteOptimizer:
    
    def __init__(self, config):
        """
        Initializes the optimizer. This is a stateless class.
        """
        print("Initializing RouteOptimizer (API-Only, Distance/MPG)...")
        self.config = config
        
        # Make the solver time limit configurable, default to 10 seconds
        self.solver_time_limit_seconds = int(config.get("SOLVER_TIME_LIMIT", 10))
        print(f"--- Optimizer is ready (Search Strategy: GUIDED_LOCAL_SEARCH, Time Limit: {self.solver_time_limit_seconds}s) ---")

    def optimize_route(self, api_response):
        """
        High-level function to find the optimal route.
        """
        try:
            # 1. Extract all data from the API response
            stops_list = api_response['sources']
            location_names = [loc['name'] for loc in stops_list]
            distance_matrix_meters = api_response['distances'] 
            mpg = float(api_response['mpg'])
            index_to_location_name = location_names

        except KeyError as e:
            print(f"Error: API response missing required key: {e}")
            return None
        except (ValueError, TypeError):
            print(f"Error: Invalid 'mpg' value. Must be a number.")
            return None
        
        if len(index_to_location_name) <= 2:
            print("Route has 2 or fewer stops. No optimization needed.")
            return stops_list

        # 2. Format the matrix for the OR-Tools solver (using METERS as cost)
        tsp_data = self._format_tsp_for_distance(distance_matrix_meters)
        
        # 3. Solve the TSP (based on METERS)
        opt_route_indices = self._solve_tsp(tsp_data, index_to_location_name)
        
        if not opt_route_indices:
            print("Solver failed to find a solution.")
            return None

        # 4. Calculate and print all cost comparisons
        print("\n--- Cost Analysis (Distance & Fuel) ---")
        self._calculate_and_print_costs(opt_route_indices, index_to_location_name, distance_matrix_meters, mpg)
        
        # 5. Re-order the original stops list and return it
        reordered_stops_list = self._apply_order(stops_list, opt_route_indices)
        
        return reordered_stops_list

    def _format_tsp_for_distance(self, distance_matrix_meters):
        """
        Converts the distance matrix (in meters) into an integer
        cost matrix for the OR-Tools solver.
        """
        num_locations = len(distance_matrix_meters)
        cost_matrix = np.zeros((num_locations, num_locations), dtype=int)

        for i in range(num_locations):
            for j in range(num_locations):
                if i == j:
                    continue
                # Use the raw meter value, rounded to the nearest integer
                cost = distance_matrix_meters[i][j]
                cost_matrix[i, j] = int(round(cost))
                    
        return {
            "cost_matrix": cost_matrix.tolist(),
            "num_vehicles": 1,
            "depot": 0  # Assumes the depot is always the first stop in the list
        }

    def _solve_tsp(self, data, index_to_location_name):
        """
        Runs the Google OR-Tools TSP solver.
        Returns the optimized route indices.
        """
        manager = pywrapcp.RoutingIndexManager(
            len(data["cost_matrix"]), data["num_vehicles"], data["depot"]
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance (cost) between two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["cost_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        
        # Set a good first solution strategy to give the local search a good starting point
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        
        # --- Set the Guided Local Search strategy ---
        # This is a more advanced metaheuristic that allows the solver
        # to escape local minima and find a better global solution.
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        
        # --- Set the time limit ---
        # This strategy *requires* a time limit to know when to stop.
        # We use the value set in the __init__ method.
        search_parameters.time_limit.seconds = self.solver_time_limit_seconds
        
        # Uncomment this to see the solver's log
        # search_parameters.log_search = True
        
        print(f"\nSolving TSP with GUIDED_LOCAL_SEARCH (Time limit: {self.solver_time_limit_seconds}s)...")
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("\n--- Distance Optimization Results ---")
            obj_meters = solution.ObjectiveValue()
            obj_km = obj_meters / METERS_PER_KM
            print(f"Solver objective value (Total Distance): {obj_km:.2f} km")
            
            return self._get_route_from_solution(manager, routing, solution, index_to_location_name)
        else:
            print("No solution found!")
            return []

    def _get_route_from_solution(self, manager, routing, solution, index_to_location_name):
        """ Extracts the route indices from the solver. """
        index = routing.Start(0)
        plan_output = "Optimized Route (by distance):\n"
        route_indices = []
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_indices.append(node_index)
            plan_output += f" {index_to_location_name[node_index]} ->"
            index = solution.Value(routing.NextVar(index))
            
        node_index = manager.IndexToNode(index) # Add final depot
        route_indices.append(node_index)
        plan_output += f" {index_to_location_name[node_index]}\n"
        
        print(plan_output)
        return route_indices

    def _get_route_cost_km(self, route_indices, distance_matrix_meters):
        """ Calculates the total distance (in km) for a given route. """
        total_meters = 0
        for i in range(len(route_indices) - 1):
            start_idx = route_indices[i]
            end_idx = route_indices[i+1]
            total_meters += distance_matrix_meters[start_idx][end_idx]
        # Convert total meters to kilometers
        return total_meters / METERS_PER_KM
    
    def _get_original_route_indices(self, num_locations):
        """ Generates a simple sequential route (0, 1, ..., n-1, 0). """
        if num_locations == 0: 
            return []
        og_route = list(range(num_locations))
        og_route.append(0)  # Return to depot
        return og_route

    def _calculate_and_print_costs(self, opt_route_indices, index_to_location_name, distance_matrix_meters, mpg):
        """
        Calculates and compares the distance (km) and fuel cost (gallons)
        of the original vs. optimized routes.
        """
        num_locations = len(index_to_location_name)
        original_route_indices = self._get_original_route_indices(num_locations)

        # --- Get Distances ---
        original_distance_km = self._get_route_cost_km(original_route_indices, distance_matrix_meters)
        optimized_distance_km = self._get_route_cost_km(opt_route_indices, distance_matrix_meters)

        # --- Print Distance Analysis ---
        print(f"Original Route Distance (Sequential): {original_distance_km:.2f} km")
        print(f"Optimized Route Distance: {optimized_distance_km:.2f} km")
        
        if optimized_distance_km < original_distance_km:
            savings_km = original_distance_km - optimized_distance_km
            percent_saved_km = (savings_km / original_distance_km) * 100
            print(f"Optimization SAVED {savings_km:.2f} km ({percent_saved_km:.2f}%)")

        print("\n--- Fuel Cost Analysis (Distance / MPG) ---")
        if mpg <= 0:
            print("MPG value is zero or negative. Skipping fuel cost analysis.")
            return
        
        try:
            # --- Original Route Fuel Cost ---
            original_distance_miles = original_distance_km * MILES_PER_KM
            original_gallons = original_distance_miles / mpg
            print(f"Original Route Fuel Cost: {original_gallons:.2f} gallons ({original_distance_miles:.2f} miles / {mpg} mpg)")

            # --- Optimized Route Fuel Cost ---
            optimized_distance_miles = optimized_distance_km * MILES_PER_KM
            optimized_gallons = optimized_distance_miles / mpg
            print(f"OptimZized Route Fuel Cost: {optimized_gallons:.2f} gallons ({optimized_distance_miles:.2f} miles / {mpg} mpg)")
            
            if optimized_gallons < original_gallons:
                savings_gal = original_gallons - optimized_gallons
                percent_saved_gal = (savings_gal / original_gallons) * 100
                print(f"Optimization SAVED {savings_gal:.2f} gallons ({percent_saved_gal:.2f}%)")
            
        except Exception as e:
            print(f"Error during fuel cost comparison: {e}")

    def _apply_order(self, original_list, solution_indices):
        """
        Reorders the original list of stops based on the solver's index list.
        """
        original_stops_map = {i: stop for i, stop in enumerate(original_list)}
        reordered_list = []
        for idx in solution_indices:
            if idx in original_stops_map:
                reordered_list.append(original_stops_map[idx])
        return reordered_list
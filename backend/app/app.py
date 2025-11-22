"""
Flask Web Server
Receives an API-style JSON object, optimizes the route based on
'distances', and returns the re-ordered list of 'sources'.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import config  
from route_optimizer import RouteOptimizer 
import requests

# --- Initialize the Application ---
app = Flask(__name__)
CORS(app)

# --- Create a Single Optimizer Instance ---
try:
    optimizer = RouteOptimizer(app.config)
except Exception as e:
    print(f"FATAL ERROR: Could not initialize RouteOptimizer. {e}")
    optimizer = None

def format_osrm_url(stops):
    """
    Takes in a list of ordered stops and returns a formatted OSRM url
    """

    # schema: {"location" : "name", "coords" : {"lat" : float, "lng" : float}}
    coords_list = [stop["coords"] for stop in stops]

    # OSRM api schema:
    # http://127.0.0.1:5000/table/v1/driving/{{lon1}},{{lat1}};{{lon2}},{{lat2}};...;{{lonN}},{{latN}}?annotations=distance
    
    # Format coordinates as "lng,lat;lng,lat;..."
    coordinates_str = ";".join([f"{coord['lng']},{coord['lat']}" for coord in coords_list])
    
    # Construct the full URL
    url = f"http://127.0.0.1:5000/table/v1/driving/{coordinates_str}?annotations=distance"
    
    return url


@app.route('/reorder_stops', methods=['POST'])
def reorder_stops():
    """
    API endpoint to receive stops and return an optimized route.
    """

    if optimizer is None:
        return jsonify({"error": "Optimizer is not initialized. Check server logs."}), 500
        
    front_end_request = request.json
    print(f"[DEBUG]: {front_end_request}")

    if not front_end_request:
        return jsonify({"error": "No JSON payload provided."}), 400
    
    required_keys = ["stops"]
    missing_keys = [key for key in required_keys if key not in front_end_request]
    if missing_keys:
       return jsonify({"error": f"JSON payload missing required keys: {', '.join(missing_keys)}"}), 400

    # calculate mpg from given stats
    # TODO: fix this
    mpg = 20.0

    # send a request to the OSRM server
    osrm_url = format_osrm_url(stops = front_end_request["stops"])
    api_response = requests.get(url = osrm_url).json()

    print(f"api_response: {api_response}")

    print(f"\nReceived request to optimize {len(api_response['sources'])} stops.")
    
    try:
        reordered_stops_list = optimizer.optimize_route(api_response, mpg)
        
        if reordered_stops_list is None:
            return jsonify({"error": "Solver could not find a solution or input was invalid."}), 500

        print("Successfully reordered stops. Returning solution.")
        print(f"Solutions: {reordered_stops_list}")
        # Return the reordered stops in the same structure as the frontend expects
        return jsonify({"stops": reordered_stops_list})

    except Exception as e:
        print(f"An error occurred during optimization: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == '__main__':
    print(f"Starting Flask server on {config.FLASK_HOST}:{config.FLASK_PORT}")
    app.run(debug=True, host=config.FLASK_HOST, port=config.FLASK_PORT)
"""
Flask Web Server
Receives an API-style JSON object, optimizes the route based on
'distances', and returns the re-ordered list of 'sources'.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import config  
from route_optimizer import RouteOptimizer 

# --- Initialize the Application ---
app = Flask(__name__)
CORS(app)

# --- Create a Single Optimizer Instance ---
try:
    optimizer = RouteOptimizer(config)
except Exception as e:
    print(f"FATAL ERROR: Could not initialize RouteOptimizer. {e}")
    optimizer = None

@app.route('/reorder_stops', methods=['POST'])
def reorder_stops():
    """
    API endpoint to receive stops and return an optimized route.
    """
    if optimizer is None:
        return jsonify({"error": "Optimizer is not initialized. Check server logs."}), 500
        
    api_response = request.json

    if not api_response:
        return jsonify({"error": "No JSON payload provided."}), 400
    
    # Check for all required keys
    required_keys = ["distances", "sources", "mpg"]
    missing_keys = [key for key in required_keys if key not in api_response]
    if missing_keys:
        return jsonify({"error": f"JSON payload missing required keys: {', '.join(missing_keys)}"}), 400

    print(f"\nReceived request to optimize {len(api_response['sources'])} stops.")
    
    try:
        reordered_stops_list = optimizer.optimize_route(api_response)
        
        if reordered_stops_list is None:
            return jsonify({"error": "Solver could not find a solution or input was invalid."}), 500

        print("Successfully reordered stops. Returning solution.")
        # Return the reordered stops in the same structure as the frontend expects
        return jsonify({"stops": reordered_stops_list})

    except Exception as e:
        print(f"An error occurred during optimization: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == '__main__':
    print(f"Starting Flask server on {config.FLASK_HOST}:{config.FLASK_PORT}")
    app.run(debug=True, host=config.FLASK_HOST, port=config.FLASK_PORT)
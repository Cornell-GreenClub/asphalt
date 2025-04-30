from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows frontend to communicate with backend
import ithaca_model

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/reorder_stops', methods=['POST'])
def reorder_stops():
    data = request.json  # Get the incoming data (JSON)
    stops = data.get('stops', [])

    print("WE GOT DATA!!!!")
    print(stops)
    
    solution = ithaca_model.find_solution(stops)

    # Example reorder logic (sort by 'location')
    reordered_stops = apply_order(stops, solution)

    print("REORDERED:", reordered_stops)
    
    return jsonify({"stops": reordered_stops})  # Return reordered stops as JSON

"""
applies the order of a solution list to stops
"""
def apply_order(stops, solution):
    reordered = [0] * len(solution)

    for i in range(0, len(solution)):
        reordered[i] = stops[solution[i]]
    
    return reordered



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


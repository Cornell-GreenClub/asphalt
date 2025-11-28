"""
Flask Web Server
Receives an API-style JSON object, optionally optimizes the route via your RouteOptimizer
(using an OSRM distance matrix), then returns the reordered stops and route geometry.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests
import config
from route_optimizer import RouteOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)
CORS(app)

try:
    optimizer = RouteOptimizer(app.config)
except Exception as e:
    logging.critical(f"Could not initialize RouteOptimizer: {e}")
    optimizer = None



def print_stops(label, stops):
    """Nicely print a list of stops with coordinates."""
    logging.info("=" * 60)
    logging.info(f"{label}")
    logging.info("=" * 60)
    for i, s in enumerate(stops):
        loc = s.get("location", "No Name")
        coords = s.get("coords", {})
        lat = coords.get("lat")
        lng = coords.get("lng")
        logging.info(f"{i+1}. {loc}  |  lat: {lat}, lng: {lng}")
    logging.info("=" * 60)


def normalize_stops_for_printing(stops):
    """Ensure every stop has a string 'location' for printing."""
    normalized = []
    for s in stops:
        stop_copy = s.copy()
        loc = s.get("location")
        if isinstance(loc, list) and len(loc) == 2:
            stop_copy["location"] = f"Lat {loc[1]:.6f}, Lng {loc[0]:.6f}"
        elif not isinstance(loc, str):
            stop_copy["location"] = "Unknown Location"
        normalized.append(stop_copy)
    return normalized


def format_table_url(stops):
    """Build OSRM table API URL for a list of stops."""
    coords_list = []
    for s in stops:
        c = s.get("coords")
        if c is None or "lat" not in c or "lng" not in c:
            raise ValueError("All stops must include coords with lat and lng.")
        coords_list.append(f"{c['lng']},{c['lat']}")
    return f"{config.OSRM_HOST}/table/v1/driving/{';'.join(coords_list)}?annotations=distance,duration"


def format_route_url(stops):
    """Build OSRM route API URL for ordered stops with GeoJSON overview."""
    coords_list = [f"{s['coords']['lng']},{s['coords']['lat']}" for s in stops]
    return f"{config.OSRM_HOST}/route/v1/driving/{';'.join(coords_list)}?overview=full&geometries=geojson&steps=false"


@app.route("/optimize_route", methods=["POST"])
def optimize_route():
    if optimizer is None:
        return jsonify({"error": "Optimizer is not initialized. Check server logs."}), 500

    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No JSON payload provided."}), 400

    stops = payload.get("stops")
    if not isinstance(stops, list) or len(stops) < 2:
        return jsonify({"error": "Payload must include a 'stops' list with at least 2 stops."}), 400

    maintain_order = bool(payload.get("maintainOrder", False))

    # Validate coords
    for i, s in enumerate(stops):
        c = s.get("coords")
        if not c or "lat" not in c or "lng" not in c:
            return jsonify({"error": f"Stop at index {i} is missing coords.lat/coords.lng."}), 400

    try:
        # --- PRINT ORIGINAL STOPS ---
        print_stops("ORIGINAL STOP ORDER", normalize_stops_for_printing(stops))

        if maintain_order:
            ordered_stops = stops
        else:
            # --- Call OSRM Table API ---
            table_url = format_table_url(stops)
            table_resp = requests.get(table_url, timeout=10)
            table_data = table_resp.json()

            # --- Call RouteOptimizer ---
            mpg_val = float(payload.get("currentFuel", 20.0))
            reordered = optimizer.optimize_route(table_data, mpg_val)

            # --- PRINT RAW OPTIMIZER OUTPUT ---
            logging.info("=== OPTIMIZER RAW OUTPUT ===")
            logging.info(reordered)
            logging.info("============================")

            # --- Map optimizer output ---
            ordered_stops = []
            if isinstance(reordered, list):
                # If elements are dicts with coords, use them directly
                if len(reordered) > 0 and isinstance(reordered[0], dict) and "coords" in reordered[0]:
                    ordered_stops = reordered
                # If elements are ints, treat as indices
                elif all(isinstance(x, int) for x in reordered):
                    ordered_stops = [stops[i] for i in reordered]
                # If elements are strings representing indices
                else:
                    try:
                        idxs = [int(x) for x in reordered]
                        ordered_stops = [stops[i] for i in idxs]
                    except Exception:
                        logging.warning("Could not parse optimizer output. Printing original stops as fallback.")
                        ordered_stops = stops
            else:
                logging.warning("Optimizer output not a list. Printing original stops as fallback.")
                ordered_stops = stops



        # --- PRINT OPTIMIZED STOPS ---
        print_stops("OPTIMIZED STOP ORDER", normalize_stops_for_printing(ordered_stops))

        # --- Call OSRM Route API ---
        route_url = format_route_url(ordered_stops)
        route_resp = requests.get(route_url, timeout=10)
        route_data = route_resp.json()

        geometry_coords = route_data["routes"][0]["geometry"]["coordinates"]
        route_geometry_latlng = [[coord[1], coord[0]] for coord in geometry_coords]

        distance = route_data["routes"][0].get("distance")
        duration = route_data["routes"][0].get("duration")

        return jsonify({
            "optimizedStops": ordered_stops,
            "routeGeometry": route_geometry_latlng,
            "distance": distance,
            "duration": duration
        })

    except Exception as e:
        logging.error(f"Exception in /optimize_route: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    logging.info(f"Starting Flask server on {config.FLASK_HOST}:{config.FLASK_PORT}")
    app.run(debug=True, host=config.FLASK_HOST, port=config.FLASK_PORT)

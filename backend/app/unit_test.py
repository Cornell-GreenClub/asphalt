"""
Test script to call the local optimizer service.
"""
import requests
import json

fake_api_response = {
    "mpg": 10.0,
    "code": "Ok",
    "distances": [
        [0, 1888, 3800.9],
        [1903.4, 0, 2845.2],
        [3278.4, 2292.2, 0]
    ],
    "sources": [
        {
            "hint": "HINT_1",
            "location": [13.38882, 52.517034],
            "name": "Friedrichstraße (Depot)"
        },
        {
            "hint": "HINT_2",
            "location": [13.39763, 52.529433],
            "name": "Torstraße (Stop 1)"
        },
        {
            "hint": "HINT_3",
            "location": [13.428554, 52.523239],
            "name": "Platz der Vereinten (Stop 2)"
        }
    ]
}

def test_optimizer():
    """
    Sends the fake data to the running Flask server and prints the response.
    """
    url = "http://127.0.0.1:5001/reorder_stops"
    
    try:
        response = requests.post(url, json=fake_api_response)
        
        if response.status_code == 200:
            print("Success! Server returned optimized route:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {url}.")
        print("Please make sure your 'app.py' server is running in another terminal.")

if __name__ == "__main__":
    test_optimizer()
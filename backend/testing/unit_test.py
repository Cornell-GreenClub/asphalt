"""
Test script to call the local optimizer service.
"""
import requests
import json


sample_stops = {"stops" : [
    {
      "location": 'TST BOCES, 555 Warren Road, Northeast Ithaca, NY 14850',
      "coords": { "lat": 42.4808, "lng": -76.457 },
    },
    {
      "location": 'Dewitt Middle School, 560 Warren Road, Ithaca, NY 14850',
      "coords": { "lat": 42.4803, "lng": -76.4566 },
    },
    {
      "location":
        'Northeast Elementary School, 425 Winthrop Dr, Ithaca, NY 14850',
      "coords": { "lat": 42.4775, "lng": -76.4647 },
    },
    {
      "location":
        'Cayuga Heights Elementary School, 110 E Upland Rd, Ithaca, NY 14850',
      "coords": { "lat": 42.4697, "lng": -76.4791 },
    },
    {
      "location":
        'Belle Sherman Elementary School, Valley Road, Ithaca, NY 14853',
      "coords": { "lat": 42.4478, "lng": -76.4766 },
    },
    {
      "location":
        'Caroline Elementary School, Slaterville Road, Besemer, NY 14881',
      "coords": { "lat": 42.3839, "lng": -76.4165 },
    },
    {
      "location":
        'South Hill Elementary School, 520 Hudson Street, Ithaca, NY 14850',
      "coords": { "lat": 42.4336, "lng": -76.495 },
    },
    {
      "location":
        'Beverly J. Martin Elementary School, 302 West Buffalo Street, Ithaca, NY',
      "coords": { "lat": 42.4422, "lng": -76.4976 },
    },
    {
      "location": 'Fall Creek School, Linn Street, Ithaca, NY 14850',
      "coords": { "lat": 42.4527, "lng": -76.4869 },
    },
    {
      "location":
        'Boynton Middle School, 1601 North Cayuga Street, Ithaca, NY 14850',
      "coords": { "lat": 42.4624, "lng": -76.4921 },
    },
    {
      "location": '602 Hancock Street, Ithaca, NY 14850',
      "coords": { "lat": 42.4808, "lng": -76.457 },
    },
    {
      "location": '737 Willow Ave, Ithaca, NY 14850',
      "coords": { "lat": 42.4445, "lng": -76.5097 },
    },
    {
      "location": 'Enfield School, 20 Enfield Main Road, Ithaca, NY 14850',
      "coords": { "lat": 42.4436, "lng": -76.5491 },
    },
    {
      "location":
        'Lehmann Alternative Community School, 111 Chestnut Street, Ithaca, NY',
      "coords": { "lat": 42.4506, "lng": -76.515 },
    },
    {
      "location":
        'Recycling and Solid Waste Center, 160 Commercial Avenue, Ithaca, NY',
      "coords": { "lat": 42.4461, "lng": -76.5138 },
    },
  ],
  "currentFuel" : 40.0,
  "time" : 80.0,
  "vehicleNumber" : 'BUS-001',
}

def test_optimizer():
    """
    Sends the fake data to the running Flask server and prints the response.
    """
    url = "http://127.0.0.1:8000/optimize_route"
    
    try:
        response = requests.post(url, json=sample_stops)
        
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
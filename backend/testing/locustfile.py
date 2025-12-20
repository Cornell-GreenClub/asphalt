from locust import HttpUser, task, between

class RouteOptimizerUser(HttpUser):
    wait_time = between(1, 5)  # Simulate a user waiting 1-5 seconds between requests

    @task
    def optimize_route(self):
        # Sample payload matching the "Sample School Route"
        payload = {
            "stops": [
                { "location": 'TST BOCES, 555 Warren Road, Northeast Ithaca, NY 14850', "coords": { "lat": 42.476169, "lng": -76.465092 } },
                { "location": 'Dewitt Middle School, 560 Warren Road, Ithaca, NY 14850', "coords": { "lat": 42.475434, "lng": -76.468026 } },
                { "location": 'Northeast Elementary School, 425 Winthrop Dr, Ithaca, NY 14850', "coords": { "lat": 42.472932, "lng": -76.468742 } },
                { "location": 'Cayuga Heights Elementary School, 110 E Upland Rd, Ithaca, NY 14850', "coords": { "lat": 42.465637, "lng": -76.488499 } },
                { "location": 'Belle Sherman Elementary School, Valley Road, Ithaca, NY 14853', "coords": { "lat": 42.435757, "lng": -76.481317 } },
                { "location": 'Caroline Elementary School, Slaterville Road, Besemer, NY 14881', "coords": { "lat": 42.392593, "lng": -76.3715585 } },
                { "location": 'South Hill Elementary School, 520 Hudson Street, Ithaca, NY 14850', "coords": { "lat": 42.4338533, "lng": -76.4931807 } },
                { "location": 'Beverly J. Martin Elementary School, 302 West Buffalo Street, Ithaca, NY', "coords": { "lat": 42.4422, "lng": -76.4976 } },
                { "location": 'Fall Creek School, Linn Street, Ithaca, NY 14850', "coords": { "lat": 42.4415514, "lng": -76.5021644 } },
                { "location": 'Boynton Middle School, 1601 North Cayuga Street, Ithaca, NY 14850', "coords": { "lat": 42.4606674, "lng": -76.500035 } },
                { "location": '602 Hancock Street, Ithaca, NY 14850', "coords": { "lat": 42.4460873, "lng": -76.5065422 } },
                { "location": '737 Willow Ave, Ithaca, NY 14850', "coords": { "lat": 42.453183, "lng": -76.5053133 } },
                { "location": 'Enfield School, 20 Enfield Main Road, Ithaca, NY 14850', "coords": { "lat": 42.449517, "lng": -76.6316132 } },
                { "location": 'Lehmann Alternative Community School, 111 Chestnut Street, Ithaca, NY', "coords": { "lat": 42.440077, "lng": -76.5177744 } },
                { "location": 'Recycling and Solid Waste Center, 160 Commercial Avenue, Ithaca, NY', "coords": { "lat": 42.4242689, "lng": -76.5159428 } },
            ],
            "maintainOrder": False,
            "currentFuel": "40.0",
            "time": "80.0",
            "vehicleNumber": "BUS-001"
        }
        
        self.client.post("/optimize_route", json=payload)

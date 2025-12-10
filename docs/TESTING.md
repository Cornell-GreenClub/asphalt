# Testing Documentation

This document outlines the testing procedures for the Asphalt backend, including unit tests and load testing.

## Unit Testing

The backend includes a suite of unit tests to verify the functionality of the API and route optimization logic.

### Running Unit Tests

1.  Navigate to the backend application directory:
    ```bash
    cd backend/app
    ```

2.  Ensure your virtual environment is activated and dependencies are installed.

3.  Run the tests using Python:
    ```bash
    python unit_test.py
    ```

### Test Coverage

The `unit_test.py` file typically covers:
-   **API Endpoints**: Checks if `/health` and `/optimize_route` return correct status codes and responses.
-   **Input Validation**: Verifies that the API correctly handles missing or invalid data (e.g., missing stops, invalid coordinates).
-   **Optimizer Logic**: Tests the integration with the `RouteOptimizer` class.

## Load Testing

We use [Locust](https://locust.io/) to perform load testing and ensure the system can handle concurrent users.

### Running Load Tests

1.  Navigate to the backend application directory:
    ```bash
    cd backend/app
    ```

2.  Start the Locust server:
    ```bash
    locust -f locustfile.py
    ```

3.  Open your browser and go to `http://localhost:8089`.

4.  **Configure the Test**:
    -   **Number of users**: Enter the peak number of concurrent users you want to simulate.
    -   **Spawn rate**: Enter how many users to add per second.
    -   **Host**: Enter the URL of your running backend (e.g., `http://localhost:8000`).

5.  **Start Swarming**: Click the button to begin the load test. Locust will simulate users hitting the `/optimize_route` endpoint with sample data.

### Locustfile Details

The `locustfile.py` defines the behavior of the simulated users:
-   It generates random or fixed sets of stops.
-   It sends `POST` requests to `/optimize_route`.
-   It waits for a random time between requests to simulate realistic user behavior.

# Asphalt API Documentation

The Asphalt backend provides a RESTful API for route optimization and data analysis.

## Base URL

- **Local**: `http://localhost:8000`
- **Production**: https://asphalt-backend.onrender.com

## Endpoints

### 1. Optimize Route

Calculates the most efficient route visiting a set of stops. It uses OSRM for distance matrices and Google OR-Tools for solving the Traveling Salesperson Problem (TSP).

- **URL**: `/optimize_route`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

| Field | Type | Description |
| :--- | :--- | :--- |
| `stops` | `Array` | **Required**. A list of stop objects to visit. |
| `currentFuel` | `Number` | Optional. Current fuel efficiency in MPG. Default: `20.0`. |
| `maintainOrder` | `Boolean` | Optional. If `true`, returns the route without reordering stops. Default: `false`. |

**Stop Object Structure:**

```json
{
  "location": "Stop Name or Address",
  "coords": {
    "lat": 42.443961,
    "lng": -76.501881
  }
}
```

#### Example Request

```json
{
  "currentFuel": 25.5,
  "maintainOrder": false,
  "stops": [
    {
      "location": "Start Point",
      "coords": { "lat": 42.4406, "lng": -76.4966 }
    },
    {
      "location": "Destination A",
      "coords": { "lat": 42.4534, "lng": -76.4735 }
    },
    {
      "location": "Destination B",
      "coords": { "lat": 42.4430, "lng": -76.5010 }
    }
  ]
}
```

#### Response

- **Status**: `200 OK`

```json
{
  "optimizedStops": [
    {
      "location": "Start Point",
      "coords": { "lat": 42.4406, "lng": -76.4966 }
    },
    {
      "location": "Destination B",
      "coords": { "lat": 42.4430, "lng": -76.5010 }
    },
    {
      "location": "Destination A",
      "coords": { "lat": 42.4534, "lng": -76.4735 }
    }
  ],
  "routeGeometry": [
    [42.4406, -76.4966],
    [42.4410, -76.4970],
    ...
  ],
  "distance": 15430.5,  // in meters
  "duration": 1200.2    // in seconds
}
```

### 2. Health Check

Simple endpoint to verify the server is running and responsive.

- **URL**: `/health`
- **Method**: `GET`

#### Response

- **Status**: `200 OK`

```json
{
  "status": "ok"
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (e.g., missing coordinates, invalid JSON)
- `500`: Internal Server Error (e.g., optimizer failure)

Error responses typically include an `error` message:

```json
{
  "error": "Payload must include a 'stops' list with at least 2 stops."
}
```

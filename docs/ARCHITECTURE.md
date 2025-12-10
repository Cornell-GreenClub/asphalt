# System Architecture

This document provides a high-level overview of the Asphalt system architecture, explaining how the different components interact to provide route optimization services.

## High-Level Overview

Asphalt is a web-based application composed of a modern frontend interface and a robust backend service. It leverages external mapping and routing services to solve the Traveling Salesperson Problem (TSP) for user-defined stops.

```mermaid
graph TD
    User[User] -->|Interacts with| Frontend[Frontend (Next.js)]
    Frontend -->|API Requests| Backend[Backend (Flask)]
    Backend -->|Distance Matrix| OSRM[OSRM Service]
    Backend -->|Optimization| ORTools[Google OR-Tools]
    Frontend -->|Map Tiles| GoogleMaps[Google Maps API]
    Frontend -->|Map Tiles| Leaflet[Leaflet / OSM]
```

## Components

### 1. Frontend (Client-Side)
-   **Technology**: Next.js 15 (React 19), TypeScript, Tailwind CSS.
-   **Responsibility**:
    -   Renders the user interface (Landing page, Map view, Dashboard).
    -   Manages application state (list of stops, user preferences).
    -   Visualizes maps and routes using `react-leaflet` and `@react-google-maps/api`.
    -   Communicates with the backend via REST API calls.

### 2. Backend (Server-Side)
-   **Technology**: Python, Flask, Gunicorn.
-   **Responsibility**:
    -   Exposes REST endpoints (e.g., `/optimize_route`).
    -   Validates input data.
    -   Orchestrates the optimization process.
    -   Calculates fuel savings and emissions metrics.

### 3. Optimization Engine
-   **Technology**: Google OR-Tools.
-   **Responsibility**:
    -   Solves the routing problem (TSP).
    -   Takes a distance matrix as input and returns the optimal order of stops to minimize total distance or duration.

### 4. Routing Service
-   **Technology**: OSRM (Open Source Routing Machine).
-   **Responsibility**:
    -   Provides the distance/duration matrix between all pairs of stops.
    -   Generates the detailed route geometry (polylines) for the optimized path.
    -   Hosted as a separate service (or external API) that the backend queries.

## Data Flow: Route Optimization

1.  **Input**: The user selects a set of locations on the frontend map.
2.  **Request**: The frontend sends a `POST /optimize_route` request to the backend with the list of stops and vehicle parameters (e.g., MPG).
3.  **Matrix Calculation**: The backend forwards the coordinates to the OSRM `table` service to get a distance matrix.
4.  **Optimization**: The backend passes this matrix to the `RouteOptimizer` (OR-Tools), which computes the most efficient sequence of stops.
5.  **Route Generation**: The backend requests the full route geometry for the *ordered* stops from the OSRM `route` service.
6.  **Response**: The backend returns the optimized order, route geometry, total distance, and duration to the frontend.
7.  **Visualization**: The frontend updates the map to show the new route and displays statistics (fuel saved, distance reduced).

## Deployment

The system is designed to be deployed on cloud platforms like **Render**.

-   **Frontend**: Deployed as a static site or Node.js service.
-   **Backend**: Deployed as a Python web service.
-   **Configuration**: Managed via `render.yaml` for Infrastructure as Code (IaC).

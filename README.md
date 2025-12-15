# Asphalt - Smarter Routes, Greener Future

**Asphalt** is a comprehensive route optimization platform designed to make transportation smarter and more eco-friendly. By leveraging spatial data and advanced algorithms, Asphalt helps users visualize infrastructure, analyze bottlenecks, and plan the most efficient paths to minimize fuel consumption and emissions.

## Features

- **Interactive Map Visualization**: Explore transportation networks with detailed map views using Leaflet and Google Maps.
- **Route Optimization**: Intelligent routing algorithms (TSP) to reorder stops for maximum efficiency.
- **Eco-Friendly Analysis**: Calculate potential fuel savings and emission reductions.
- **Data-Driven Insights**: Identify traffic bottlenecks and alternative routes.
- **Responsive Design**: A modern, responsive user interface built with Next.js and Tailwind CSS.

## System Overview

Asphalt is a web application for route optimization, focusing on reducing fuel consumption and emissions. It consists of:
- **Frontend**: A Next.js application (React) using Tailwind CSS for styling and Leaflet for maps.
- **Backend**: A Flask (Python) server that handles route optimization logic.
- **Routing Engine**: Integrates with OSRM (Open Source Routing Machine) for distance matrices and route geometry.

## High-Level Data Flow

1.  **User Input**: User enters stops in the Frontend (`ExplorePage`).
2.  **Optimization Request**: Frontend sends stops to Backend (`/optimize_route`).
3.  **Distance Matrix**: Backend requests a distance matrix from OSRM.
4.  **Optimization**: Backend uses Google OR-Tools to solve the Traveling Salesperson Problem (TSP) based on the distance matrix.
5.  **Route Geometry**: Backend requests the final route geometry from OSRM for the optimized order.
6.  **Visualization**: Backend returns optimized stops and geometry to Frontend, which renders them on a map (`MapView`).

## Backend Architecture

The backend is a lightweight Flask wrapper around an optimization engine.

### Key Files

#### `app/app.py`
The entry point for the Flask server.

**Endpoints:**
-   `GET /health`: Simple health check.
    -   Called immediately when the application is opened.
    -   **Purpose**: Starts the render wake-up process to reduce wait time when "Optimize Route" is actually called.
-   `POST /optimize_route`: The main endpoint.
    -   **Input**: JSON with `stops` (list of locations/coords), `currentFuel`, `maintainOrder` flag.
    -   **Process**:
        1.  Validates input.
        2.  If `maintainOrder` is `false`, calls `RouteOptimizer` to reorder stops.
        3.  Fetches route geometry from OSRM for the final actual driving route.
        4.  Calculates total distance and duration.
    -   **Output**: JSON with `optimizedStops`, `routeGeometry` (lat/lng array), `distance`, and `duration`.

#### `app/route_optimizer.py`
Contains the core logic for solving the routing problem.

**Class `RouteOptimizer`:**
-   `optimize_route(api_response, mpg)`:
    -   Takes OSRM distance matrix (`api_response`).
    -   Uses `ortools.constraint_solver` to solve the TSP.
    -   Optimizes for **shortest distance**.
-   `_solve_tsp`:
    -   Configures and runs the OR-Tools solver with `GUIDED_LOCAL_SEARCH` strategy.
-   `_calculate_and_print_costs`:
    -   Compares the original vs. optimized route in terms of distance (km) and fuel usage (gallons), logging the savings.

## Frontend Architecture

The frontend is a modern Next.js 15 application using the App Router.

### Key Files

#### `src/app/layout.tsx`
The root layout file.
-   Sets up global fonts (Poppins).
-   Includes `BackendWakeup` component to ensure the backend is ready.
-   Includes Vercel Analytics.

#### `src/app/page.tsx`
The Landing Page.
-   Features a "Hero" section with a call to action ("Explore Routes").
-   Explains the value proposition: Visualize, Analyze, Optimize.
-   Showcases sustainability and data-driven benefits.

#### `src/app/explore/page.tsx` (`ExplorePage`)
The main functional page for route planning.
-   **State Management**: Handles `formData` (stops, fuel info), `route` data, and view state (`isMapView`).
-   **`optimizeRoute`**:
    -   Sends a POST request to the backend.
    -   Updates state with the optimized route and geometry.
    -   Switches view to `MapView`.

#### `src/app/explore/MapView.tsx`
The interactive map component.
-   **MapView**: Main container. Renders `MapContainer`, `TileLayer`, `Marker`s, and `Polyline` (route path).
-   **MapController**: Automatically fits map bounds to show the route.
-   **Legend**: Explains marker colors (Blue=Start/End, Orange=Intermediate).

## Tech Stack

### Frontend
- **Framework**: [Next.js 15](https://nextjs.org/) (React 19)
- **Language**: TypeScript
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Maps**: [Leaflet](https://leafletjs.com/), [React Leaflet](https://react-leaflet.js.org/), Google Maps API
- **Icons**: Lucide React, React Icons
- **Charts**: Recharts

### Backend
- **Framework**: [Flask](https://flask.palletsprojects.com/) (Python)
- **Optimization**: [Google OR-Tools](https://developers.google.com/optimization)
- **Routing Engine**: [OSRM](http://project-osrm.org/) (Open Source Routing Machine)
- **Server**: Gunicorn

### Deployment
- **Platform**: [Render](https://render.com/)
- **Configuration**: Infrastructure as Code via `render.yaml`

## Prerequisites

Before you begin, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://www.python.org/) (v3.8 or higher)
- [pip](https://pip.pypa.io/en/stable/)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/asphalt.git
cd asphalt
```

### 2. Backend Setup

The backend handles route optimization logic.

```bash
cd backend/app

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```
The backend will start on `http://localhost:8000` (or the port defined in `config.py`).

### 3. Frontend Setup

The frontend provides the user interface.

```bash
# Open a new terminal window
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

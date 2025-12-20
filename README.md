# pathOS

pathOS is a web application designed for **route optimization**, specifically engineered to reduce fuel consumption and environmental emissions. By leveraging advanced optimization and real-time map data, PathOS provides users with the most efficient paths for their journeys.

---

## 1. System Overview

The platform is built on a modern, three-tier architecture:

* **Frontend**: A responsive **Next.js 15** application (React) styled with **Tailwind CSS** and featuring interactive mapping via **Leaflet**.
* **Backend**: A **Flask** (Python) REST API that houses the core optimization logic.
* **Routing Engine**: An **OSRM (Open Source Routing Machine)** instance that provides high-performance distance matrices and precise route geometry.

---

## 2. High-Level Data Flow

The following sequence describes how data moves through the system to generate an optimized route:

1.  **User Input**: User enters destinations via the `ExplorePage` in the Frontend.
2.  **Request**: Frontend sends coordinates to the Backend `/optimize_route` endpoint.
3.  **Matrix Calculation**: Backend requests a distance matrix from the OSRM server.
4.  **Optimization**: The Backend uses **Google OR-Tools** to solve the Traveling Salesperson Problem (TSP).
5.  **Geometry Fetching**: After reordering stops, the Backend requests the specific driving path (geometry) from OSRM.
6.  **Visualization**: The Frontend receives the optimized order and polyline data, rendering it on the `MapView`.



---

## 3. Backend Architecture

The backend is a lightweight Flask wrapper around a powerful optimization engine.

### Key Files & Endpoints
* **`app/app.py`**: The primary entry point.
    * `GET /health`: Used as a "warm-up" signal to wake up the Render instance when a user first lands on the site.
    * `POST /optimize_route`: The main processing hub. Validates input, triggers the optimizer, and returns distance, duration, and geometry.
* **`app/route_optimizer.py`**: Contains the `RouteOptimizer` class.
    * **Logic**: Uses `ortools.constraint_solver` with a `GUIDED_LOCAL_SEARCH` strategy.
    * **Savings Analysis**: Automatically calculates and logs the distance and fuel saved compared to the original input order.

---

## 4. Frontend Architecture

Built using the **Next.js App Router**, the frontend focuses on performance and user experience.

### Core Components
* **`layout.tsx`**: Sets the global theme (Poppins font) and includes the `BackendWakeup` component to trigger early server spin-up.
* **`explore/page.tsx`**: The mission control for route planning. Manages form state, fuel parameters, and view toggling.
* **`explore/MapView.tsx`**: An interactive Leaflet-based map.
    * **MapController**: Logic to auto-zoom/pan to the generated route.
    * **Legend**: Distinguishes between start/end points (Blue) and waypoints (Orange).

> [!NOTE]
> The contact page (`/contact/page.tsx`) currently requires integration with a Google Sheets/AppScript backend to be fully functional.

---

## 5. Hosting & Infrastructure

| Component | Provider | Notes |
| :--- | :--- | :--- |
| **Frontend** | Vercel | Next.js deployment with built-in analytics. |
| **Backend** | Render | Free tier hosting. Subject to "cold starts" (mitigated by health-check). |
| **Routing (OSRM)** | AWS EC2 | Hosted on a `t3.large` instance (New York State dataset). |

### Cost & Optimization Strategy
* **Resource Management**: OSRM requires significant RAM; a `t3.medium` was insufficient for the NYS dataset.
* **Scaling**: Current AWS resources are paused/deleted during inactive periods (like winter break) to eliminate the ~$1/day idle cost.
* **Future Roadmap**: Transition OSRM management to **API Gateway + AWS Lambda** to programmatically trigger the EC2 instance only when active users are detected.

---

## 6. Testing & Validation

PathOS includes three distinct testing layers to ensure reliability and proof of value:

1.  **Integration Testing** (`unit_test.py`): Validates the full API handshake using real-world Ithaca, NY coordinates.
2.  **Load Testing** (`locustfile.py`): Uses **Locust** to simulate concurrent users and measure system stability under pressure.
3.  **Savings Verification** (`calculate_sample_savings.py`): A specialized script that compares baseline routes against optimized versions to quantify actual fuel and distance reduction.

---

## 7. OSRM Setup

To set up your local OSRM server (downloading and processing map data), please follow the [official OSRM Backend Guide](https://github.com/Project-OSRM/osrm-backend).

**Crucial Configuration for pathOS:**
When running the final `osrm-routed` command, you **must expose port 5000** to allow the Flask backend to connect.

```bash
# Ensure -p 5000:5000 is included
docker run -d -t -i -p 5000:5000 -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/your-map-data.osrm
```

**Verify Connection:**
Run the integration test to confirm the backend can reach your local OSRM instance:

```bash
cd backend/testing
python3 unit_test.py
```

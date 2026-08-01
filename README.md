# FedRoute — Ambulance Route Optimization

FedRoute is a real-time ambulance route recommendation system that uses reports from multiple ambulances to determine the route with the lowest average delay.

Reporter ambulances simulate traffic conditions and send their route experiences to a Flask server. The server aggregates the reported delays and recommends the best route to newcomer ambulances. A live web dashboard displays the current reports, average delays, and recommended route.

---

## Important Setup Step

Before running the project, create a folder named:

```text
templates
```

Move `index.html` inside the `templates` folder.

Your project structure must look like this:

```text
FedRoute/
│
├── client.py
├── server.py
│
└── templates/
    └── index.html
```

This is required because Flask loads the dashboard HTML file from the `templates` directory.

---

## Features

* Multiple simulated ambulance clients
* Real-time traffic condition reporting
* Three available routes
* Dynamic traffic simulation
* Aggregation of reports from multiple ambulances
* Automatic selection of the route with the lowest average delay
* Newcomer ambulance route recommendation
* Flask-based REST API
* Real-time web dashboard
* Dashboard refreshes automatically every 2 seconds

---

## How the System Works

The system contains two types of ambulance clients:

### 1. Reporter Ambulance

A reporter represents an ambulance that has already experienced the available routes.

Each reporter:

1. Generates traffic conditions for Routes A, B, and C.
2. Calculates the estimated delay for each route.
3. Sends the information to the Flask server.
4. Continues sending updated conditions periodically.

The available routes are:

| Route | Distance | Description         |
| ----- | -------: | ------------------- |
| A     |     5 km | Short — City Centre |
| B     |    10 km | Medium — Ring Road  |
| C     |    15 km | Long — Highway      |

Traffic can be:

* Low
* Medium
* High

The simulated delay is calculated using the route distance and corresponding traffic value.

### 2. Newcomer Ambulance

A newcomer represents an ambulance that needs to decide which route to take.

Instead of generating traffic information, it queries the server and receives:

* Recommended route
* Average delay of each route

The server recommends the route with the lowest aggregated average delay.

---

## System Architecture

```text
Reporter Ambulance 1 ----\
                          \
Reporter Ambulance 2 ------> Flask Server ----> Global Average
                          /                         |
Reporter Ambulance 3 ----/                         |
                                                    v
                                             Best Route
                                                 /   \
                                                /     \
                                               v       v
                                         Newcomer   Dashboard
                                         Ambulance
```

Reporter ambulances send their observations to the server through the `/report` endpoint.

The server stores the latest report from each ambulance and calculates the average delay for each route.

The route with the minimum average delay becomes the recommended route.

---

## Requirements

Make sure Python is installed on your system.

Install the required Python packages:

```bash
pip install flask requests
```

---

## Running the Project

### Step 1 — Start the Server

Open a terminal inside the project directory and run:

```bash
python server.py
```

The Flask server starts on:

```text
http://localhost:5000
```

Open this address in your browser to access the dashboard.

---

### Step 2 — Start Reporter Ambulances

Open another terminal and run:

```bash
python client.py reporter Ambulance-1
```

You can simulate multiple ambulances by opening additional terminals:

```bash
python client.py reporter Ambulance-2
```

```bash
python client.py reporter Ambulance-3
```

Each reporter continuously generates traffic conditions and sends its latest route delays to the server.

---

### Step 3 — Start a Newcomer Ambulance

Open another terminal and run:

```bash
python client.py newcomer MyAmbulance
```

The newcomer asks the server for the currently recommended route.

Example output:

```text
[MyAmbulance] Server says → Take ROUTE B | Avg delays: {'A': 15.3, 'B': 12.0, 'C': 17.0}
```

---

## API Endpoints

### POST `/report`

Used by reporter ambulances to send traffic and delay information.

Example data:

```json
{
    "name": "Ambulance-1",
    "traffic": {
        "A": "High",
        "B": "Medium",
        "C": "Low"
    },
    "delays": {
        "A": 19,
        "B": 17,
        "C": 17
    }
}
```

---

### GET `/query`

Used by newcomer ambulances to request the recommended route.

Example response:

```json
{
    "global_avg": {
        "A": 16.5,
        "B": 13.0,
        "C": 17.0
    },
    "recommended": "B"
}
```

---

### GET `/state`

Used by the web dashboard to retrieve the complete current state of the system.

It provides:

* Reporter data
* Global average delays
* Recommended route
* Number of active reporter entries

---

## Dashboard

The web dashboard displays:

* Current recommended route
* Average delay for Routes A, B, and C
* Number of reporter ambulances
* Traffic condition reported by each ambulance
* Individual route delays
* Lowest-delay route reported by each ambulance

The dashboard automatically requests the latest state from the Flask server every 2 seconds.

---

## Traffic Simulation

Traffic conditions are generated with different probabilities depending on the route.

Route A represents a city-centre route and therefore has a higher probability of heavy traffic.

Route B represents a ring road with more balanced traffic conditions.

Route C represents a highway and therefore has a higher probability of low traffic.

This means that the shortest route is not necessarily always the fastest route.

---

## Project Files

```text
client.py
```

Simulates reporter and newcomer ambulances.

```text
server.py
```

Runs the Flask server, stores reports, calculates average route delays, and determines the recommended route.

```text
templates/index.html
```

Provides the live web dashboard used to visualize ambulance reports and route recommendations.

---

## Current Limitations

This project currently uses simulated traffic information rather than real GPS or traffic data.

The aggregation mechanism calculates the arithmetic mean of the latest delay reported by each ambulance. Although the project demonstrates a federated-style collaborative routing concept, it does not currently train or aggregate machine-learning model parameters.

---

## Future Improvements

The system can be extended with:

* Real GPS coordinates
* Live traffic APIs
* Actual ambulance tracking
* Map-based route visualization
* Historical traffic storage
* Authentication for ambulance clients
* Database integration
* Mobile application support
* Machine-learning-based traffic prediction
* True federated learning with local model training and model aggregation

---

## Technologies Used

* Python
* Flask
* Requests
* HTML
* CSS
* JavaScript

---

## Purpose

The project demonstrates how multiple ambulances can collaboratively report road conditions to help another ambulance choose a route with a lower expected delay.

It provides a prototype for distributed emergency vehicle route optimization and can be extended with real-world traffic, GPS, and machine-learning systems.

## Author  
**Metla Srinath**

B.Tech Computer Science and Engineering (Internet of Things)

## License

This project is developed for **academic and educational purposes**.


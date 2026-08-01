"""
Two roles:
  reporter  → simulates an ambulance that HAS travelled the routes and reports conditions
  newcomer  → simulates a NEW ambulance asking which route to take
"""
import random
import time
import requests
import sys

SERVER_URL = "http://localhost:5000"

ROUTES = {
    "A": {"distance": 5,  "label": "Short (City Centre)"},
    "B": {"distance": 10, "label": "Medium (Ring Road)"},
    "C": {"distance": 15, "label": "Long (Highway)"},
}

TRAFFIC_LEVELS = ["Low", "Medium", "High"]
TRAFFIC_VALUES = {"Low": 2, "Medium": 7, "High": 14}

# Realistic traffic biases per route
TRAFFIC_BIAS = {
    "A": [0.15, 0.35, 0.50],   # city centre — often heavy
    "B": [0.35, 0.40, 0.25],   # ring road   — balanced
    "C": [0.60, 0.30, 0.10],   # highway     — usually clear
}

def pick_traffic(route):
    return random.choices(TRAFFIC_LEVELS, weights=TRAFFIC_BIAS[route], k=1)[0]

# ── REPORTER: ambulance that has already travelled all routes ──────────────
def run_reporter(name):
    print(f"[{name}] MODE: REPORTER — sending route experience to server")
    while True:
        traffic = {r: pick_traffic(r) for r in ROUTES}
        delays  = {r: ROUTES[r]["distance"] + TRAFFIC_VALUES[traffic[r]] for r in ROUTES}

        payload = {"name": name, "traffic": traffic, "delays": delays}
        try:
            resp = requests.post(f"{SERVER_URL}/report", json=payload, timeout=3)
            rec  = resp.json().get("recommended", "?")
            avg  = resp.json().get("global_avg",  {})
            print(f"[{name}] Reported → Traffic:{traffic} | Delays:{delays} | Server recommends: Route {rec} | FedAvg:{avg}")
        except Exception as e:
            print(f"[{name}] Server unreachable: {e}")

        time.sleep(random.uniform(3, 6))

# ── NEWCOMER: ambulance deciding which route to take ─────────────────────
def run_newcomer(name):
    print(f"[{name}] MODE: NEWCOMER — asking server for best route")
    while True:
        try:
            resp = requests.get(f"{SERVER_URL}/query", timeout=3)
            data = resp.json()
            rec  = data.get("recommended", "No data yet")
            avg  = data.get("global_avg",  {})
            if rec and rec != "No data yet":
                print(f"[{name}] Server says → Take ROUTE {rec} | Avg delays: {avg}")
            else:
                print(f"[{name}] No recommendation yet — waiting for reporters...")
        except Exception as e:
            print(f"[{name}] Server unreachable: {e}")

        time.sleep(4)

if __name__ == "__main__":
    # Usage:
    #   python client.py reporter Ambulance-1
    #   python client.py reporter Ambulance-2
    #   python client.py newcomer MyAmbulance
    if len(sys.argv) < 3:
        print("Usage: python client.py [reporter|newcomer] <name>")
        print("  reporter → ambulance that has travelled routes and reports conditions")
        print("  newcomer → ambulance asking which route to take")
        sys.exit(1)

    role = sys.argv[1].lower()
    name = sys.argv[2]

    if role == "reporter":
        run_reporter(name)
    elif role == "newcomer":
        run_newcomer(name)
    else:
        print("Role must be 'reporter' or 'newcomer'")
        sys.exit(1)
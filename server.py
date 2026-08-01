from flask import Flask, request, jsonify, render_template
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# Stores latest report from each past ambulance
route_reports = {}   # { amb_name: { A: delay, B: delay, C: delay, traffic: {...} } }
global_avg    = {}   # { "A": avg_delay, "B": avg_delay, "C": avg_delay }
recommended   = None # best route based on federated average
lock          = threading.Lock()

def compute_fedavg():
    global global_avg, recommended
    if not route_reports:
        return
    totals = {"A": 0, "B": 0, "C": 0}
    for report in route_reports.values():
        for r in ["A", "B", "C"]:
            totals[r] += report["delays"][r]
    n = len(route_reports)
    global_avg  = {r: round(totals[r] / n, 2) for r in ["A", "B", "C"]}
    recommended = min(global_avg, key=global_avg.get)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/report", methods=["POST"])
def report():
    """Past ambulances POST their experienced delays on each route."""
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Invalid payload"}), 400
    with lock:
        route_reports[data["name"]] = {
            "delays":  data["delays"],
            "traffic": data["traffic"],
        }
        compute_fedavg()
    return jsonify({
        "status":      "ok",
        "global_avg":  global_avg,
        "recommended": recommended,
    })

@app.route("/query", methods=["GET"])
def query():
    """New ambulance asks: which route should I take?"""
    with lock:
        return jsonify({
            "global_avg":  global_avg,
            "recommended": recommended,
        })

@app.route("/state", methods=["GET"])
def state():
    """Dashboard polls this for full state."""
    with lock:
        return jsonify({
            "reporters":   route_reports,
            "global_avg":  global_avg,
            "recommended": recommended,
            "count":       len(route_reports),
        })

if __name__ == "__main__":
    print(f"[server] Dashboard → http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
# File: app.py
# Purpose: Flask API to optimize inventory items using Octave
# Updates:
# - Accepts JSON payload with job_id, horizon_days, service_level, and items[]
# - Loops through items and calculates EOQ, ROP, SS for each
# - Returns {"results": [...]} for PHP service consumption

from flask import Flask, request, jsonify
import subprocess
import math

app = Flask(__name__)

def run_octave_function(func_name, params):
    """
    Call Octave with the given function and parameters.
    Returns the stdout string result or raises an Exception.
    """
    if isinstance(params, list):
        param_str = ",".join(str(p) for p in params)
    else:
        param_str = str(params)

    octave_cmd = f"disp({func_name}({param_str}));"
    result = subprocess.check_output(
        ["octave", "--quiet", "--eval", octave_cmd]
    ).decode("utf-8").strip()
    return result


@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json or {}

    items = data.get("items", [])
    horizon_days = data.get("horizon_days", 90)
    service_level = data.get("service_level", 0.95)

    results = []

    # If no items passed, return error
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "No items provided"}), 400

    try:
        for item in items:
            item_id = item.get("item_id")

            demand = float(item.get("avg_daily_demand", 0))
            lead_time = float(item.get("lead_time_days", 0))
            unit_cost = float(item.get("unit_cost", 0))
            order_cost = float(item.get("order_cost", 50))
            safety_stock = float(item.get("safety_stock", 0))

            # Calculate EOQ, ROP, SS
            try:
                # Example: EOQ = sqrt((2 * D * S) / H)
                # where H = holding cost = 0.2 * unit_cost (20% carrying cost assumption)
                annual_demand = demand * 365
                holding_cost = 0.2 * unit_cost if unit_cost > 0 else 1
                eoq = math.sqrt((2 * annual_demand * order_cost) / holding_cost)

                # Reorder point = demand * lead_time + safety_stock
                reorder_point = demand * lead_time + safety_stock

                # Safety stock left as provided or a basic z-score approach
                ss = safety_stock
            except Exception as calc_err:
                eoq = None
                reorder_point = None
                ss = None

            results.append({
                "item_id": item_id,
                "eoq": round(eoq, 2) if eoq is not None else None,
                "reorder_point": round(reorder_point, 2) if reorder_point is not None else None,
                "safety_stock": round(ss, 2) if ss is not None else None
            })

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

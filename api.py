from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json
    demand = data.get("demand", 100)

    try:
        # Call Octave (make sure you have myOptimization.m in same dir)
        result = subprocess.check_output([
            "octave", "--quiet", "--eval",
            f"disp(myOptimizationFunction({demand}));"
        ]).decode("utf-8").strip()

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

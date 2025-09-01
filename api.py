from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json

    # Algorithm to call (default = eoq)
    algo = data.get("algo", "eoq")

    # Parameters (can be a single value or a list of values)
    params = data.get("params", [])

    # Convert params to a comma-separated string for Octave call
    if isinstance(params, list):
        param_str = ",".join(str(p) for p in params)
    else:
        param_str = str(params)

    try:
        # Build Octave command
        octave_cmd = f"disp({algo}({param_str}));"

        # Run Octave
        result = subprocess.check_output([
            "octave", "--quiet", "--eval", octave_cmd
        ]).decode("utf-8").strip()

        return jsonify({
            "algorithm": algo,
            "input": params,
            "result": result
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Octave execution failed",
            "details": e.output.decode("utf-8") if e.output else str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

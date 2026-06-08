import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from blueprint_generator import generate_blueprint, validate_requirements

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "BlueprintAI backend is running."
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Blueprint API is available."
    })


@app.route("/api/routes", methods=["GET"])
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "path": str(rule),
            "methods": sorted(list(rule.methods))
        })
    return jsonify(routes)


@app.route("/api/generate-blueprint", methods=["GET", "POST"])
def generate_blueprint_api():
    if request.method == "GET":
        return jsonify({
            "status": "success",
            "message": "Generate blueprint API is available. Use POST request."
        })

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "error",
                "message": "No requirements received."
            }), 400

        is_valid, validation_message = validate_requirements(data)

        if not is_valid:
            return jsonify({
                "status": "error",
                "message": validation_message
            }), 400

        blueprint = generate_blueprint(data)

        return jsonify({
            "status": "success",
            "message": "Blueprint generated successfully.",
            "blueprint": blueprint
        }), 200

    except Exception as error:
        print("Backend error:", error)
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

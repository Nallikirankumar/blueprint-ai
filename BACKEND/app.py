from flask import Flask, jsonify, request
from flask_cors import CORS

from blueprint_generator import (
    generate_blueprint,
    validate_requirements
)

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "BlueprintAI backend is running.",
        "status": "success"
    })


@app.route(
    "/api/generate-blueprint",
    methods=["POST"]
)
def generate_blueprint_route():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No requirements received."
            }), 400

        is_valid, validation_message = (
            validate_requirements(data)
        )

        if not is_valid:
            return jsonify({
                "status": "error",
                "message": validation_message
            }), 400

        blueprint = generate_blueprint(data)

        return jsonify({
            "status": "success",
            "message":
                "Blueprint generated successfully.",
            "blueprint": blueprint
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception as error:
        print("Server error:", error)

        return jsonify({
            "status": "error",
            "message":
                "An unexpected server error occurred."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
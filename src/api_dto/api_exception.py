from flask import jsonify

def error_handler(e):
    if isinstance(e, ValueError):
        return jsonify({"error": "Invalid input!"}), 400
    return jsonify({"error": "Server error!"}), 500
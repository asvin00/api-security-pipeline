from flask import Flask, jsonify

# Create a Flask application instance
# __name__ tells Flask where to find resources relative to this file
app = Flask(__name__)


# @app.route("/") means: "when someone visits the root URL (/), run this function"
@app.route("/")
def home():
    # jsonify converts a Python dictionary into a proper JSON HTTP response
    return jsonify({
        "message": "Hello from my CI/CD pipeline!",
        "status":  "ok"
    })


# Health check endpoint — used by monitoring tools to verify the app is alive
@app.route("/health")
def health():
    # The second argument to jsonify is the HTTP status code (200 = OK)
    return jsonify({"status": "healthy"}), 200


# Dynamic URL: <int:a> and <int:b> capture integers from the URL
# e.g., visiting /add/3/5 calls add(a=3, b=5)
@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify({"result": a + b})


# This block only runs when you execute this file directly (not when imported)
# Used for local development. Jenkins won't use this — it imports the app.
if __name__ == "__main__":
    # host="0.0.0.0" means "listen on all network interfaces"
    # port=5000 is the standard Flask development port
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Blueprint, jsonify, request
from app.models import ItemStore

main = Blueprint("main", __name__)
store = ItemStore()

@main.route("/")
def home():
    return jsonify({"message": "🚀 DevSecOps Python App Running"})

@main.route("/health")
def health():
    return jsonify({"status": "OK"})

# Create item
@main.route("/items", methods=["POST"])
def create_item():
    data = request.json
    item = store.add_item(data["name"])
    return jsonify(item), 201

# Get all items
@main.route("/items", methods=["GET"])
def get_items():
    return jsonify(store.get_all())

# Delete item
@main.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    result = store.delete(item_id)
    if result:
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404

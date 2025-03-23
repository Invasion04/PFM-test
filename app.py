from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
try:
    cred = credentials.Certificate("firebase_credentials.json")  # Ensure this file exists
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print("Error initializing Firebase:", e)
    db = None  # Avoid crashes if Firebase fails

# Homepage route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Personal Finance Manager API!"})

# Get expenses route
@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    if db is None:
        return jsonify({"error": "Firebase not initialized"}), 500

    expenses = []
    try:
        docs = db.collection("expenses").stream()
        for doc in docs:
            expense = doc.to_dict()
            expense["id"] = doc.id  # Include document ID in the response
            expenses.append(expense)
        return jsonify(expenses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add expense route
@app.route("/add_expense", methods=["POST"])
def add_expense():
    if db is None:
        return jsonify({"error": "Firebase not initialized"}), 500

    try:
        data = request.json  # Get JSON data from the request
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Add the expense to Firestore
        doc_ref = db.collection("expenses").add(data)
        return jsonify({"message": "Expense added successfully!", "id": doc_ref[1].id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update expense route
@app.route("/update_expense/<expense_id>", methods=["PUT"])
def update_expense(expense_id):
    if db is None:
        return jsonify({"error": "Firebase not initialized"}), 500

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        doc_ref = db.collection("expenses").document(expense_id)

        if not doc_ref.get().exists:
            return jsonify({"error": "Expense not found"}), 404

        doc_ref.update(data)
        return jsonify({"message": "Expense updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete expense route
@app.route("/delete_expense/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    if db is None:
        return jsonify({"error": "Firebase not initialized"}), 500

    try:
        doc_ref = db.collection("expenses").document(expense_id)

        if not doc_ref.get().exists:
            return jsonify({"error": "Expense not found"}), 404

        doc_ref.delete()
        return jsonify({"message": "Expense deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
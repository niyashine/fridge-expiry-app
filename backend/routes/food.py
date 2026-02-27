from flask import Blueprint, request, jsonify
from config import db

food = Blueprint("food", __name__)

# Add food
@food.route("/foods", methods=["POST"])
def add_food():
    data = request.get_json()

    name = data["name"]
    quantity = data["quantity"]
    expiry_date = data["expiry_date"]
    barcode = data.get("barcode", None)   # <-- THIS IS THE NEW LINE

    cursor = db.cursor()

    query = """
        INSERT INTO foods (name, quantity, expiry_date, barcode, status)
        VALUES (%s, %s, %s, %s, 'active')
    """

    cursor.execute(query, (name, quantity, expiry_date, barcode))
    db.commit()

    return jsonify({"message": "Food added successfully"}), 201

# Get all food
@food.route("/foods", methods=["GET"])
def get_foods():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM foods")
    foods = cursor.fetchall()

    return jsonify(foods), 200

#delete food
@food.route("/foods/use/<int:id>", methods=["PUT"])
def use_food(id):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE foods SET status='used' WHERE id=%s",
        (id,)
    )
    db.commit()

    return jsonify({"message": "Food marked as used"})

# Update food
@food.route("/foods/<int:id>", methods=["PUT"])
def update_food(id):
    data = request.get_json()

    name = data["name"]
    quantity = data["quantity"]
    expiry_date = data["expiry_date"]

    cursor = db.cursor()
    query = """
        UPDATE foods 
        SET name=%s, quantity=%s, expiry_date=%s 
        WHERE id=%s
    """
    cursor.execute(query, (name, quantity, expiry_date, id))
    db.commit()

    return jsonify({"message": "Food updated successfully"}), 200

from datetime import date

@food.route("/foods/shelf", methods=["GET"])
def get_shelf():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM foods WHERE status='active'")
    foods = cursor.fetchall()

    today = date.today()

    expiring_soon = []
    fresh_stock = []
    expired = []

    for item in foods:
        days_left = (item["expiry_date"] - today).days

        if days_left < 0:
            expired.append(item)
        elif days_left <= 3:
            expiring_soon.append(item)
        else:
            fresh_stock.append(item)

    return jsonify({
        "expiring_soon": expiring_soon,
        "fresh_stock": fresh_stock,
        "expired": expired
    })
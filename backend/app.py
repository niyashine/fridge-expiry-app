from flask import Flask
from flask_cors import CORS
import mysql.connector

# --------------------
# Flask setup
# --------------------
app = Flask(__name__)
CORS(app)

# --------------------
# MySQL setup
# --------------------
db = mysql.connector.connect(
    host="localhost",       # your MySQL host
    user="root",            # your MySQL username
    password="niya99",
    database="fridge_db"    # your MySQL database
)

# --------------------
# Register blueprint
# --------------------
from routes.food import food_bp
app.register_blueprint(food_bp)

# --------------------
# Run server
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
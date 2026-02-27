from flask import Flask
from flask_cors import CORS
from routes.food import food

app = Flask(__name__)
CORS(app)

app.register_blueprint(food)

@app.route("/")
def home():
    return "Fridge API Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
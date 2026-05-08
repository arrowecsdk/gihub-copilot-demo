from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory store
cars = [
    {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020},
    {"id": 2, "make": "Ford", "model": "Mustang", "year": 2021},
]
next_id = 3


def find_car(car_id):
    return next((c for c in cars if c["id"] == car_id), None)


@app.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(cars), 200


@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = find_car(car_id)
    if car is None:
        abort(404, description="Car not found")
    return jsonify(car), 200


@app.route("/cars", methods=["POST"])
def create_car():
    global next_id
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("make", "model", "year")):
        abort(400, description="'make', 'model', and 'year' are required")
    car = {"id": next_id, "make": data["make"], "model": data["model"], "year": data["year"]}
    next_id += 1
    cars.append(car)
    return jsonify(car), 201


@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    car = find_car(car_id)
    if car is None:
        abort(404, description="Car not found")
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Request body must be JSON")
    car.update({k: data[k] for k in ("make", "model", "year") if k in data})
    return jsonify(car), 200


@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    car = find_car(car_id)
    if car is None:
        abort(404, description="Car not found")
    cars.remove(car)
    return "", 204


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify(error=str(e.description)), e.code


if __name__ == "__main__":
    app.run(debug=True)

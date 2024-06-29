#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    formatted_response = []
    for restaurant in restaurants:
        formatted_response.append({
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name
        })
    return formatted_response
            
@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id = id).first()

    if restaurant:
        if request.method == 'GET':
            response = restaurant.to_dict()
            status = 200

        elif request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()
            
            response = {}
            status = 204

    else:
        response = {
            "error": "Restaurant not found"
        }
        status = 404

    return make_response(response, status)

@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []
    for pizza in pizzas:
        pizza_list.append({
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        })
    return pizza_list

@app.route('/restaurant_pizzas', methods=["POST"])
def restaurant_pizzas():
    data = request.json
    try:
        new_restaurant_pizza = RestaurantPizza(
            price = data.get("price"),
            pizza_id = data.get("pizza_id"),
            restaurant_id = data.get("restaurant_id")
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()
        
        response  = new_restaurant_pizza.to_dict()
        status = 201
        return make_response(response, status)
    
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 400)
    
    
    
if __name__ == "__main__":
    app.run(port=5555, debug=True)

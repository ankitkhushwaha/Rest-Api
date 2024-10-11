from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random  
import json

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
API_KEY = 'TopSecretAPIKey'

db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __init__(self, id, name, map_url, img_url, location, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price):
        self.id = id
        self.name = name
        self.map_url = map_url
        self.img_url = img_url
        self.location = location
        self.seats = seats
        self.has_toilet = has_toilet
        self.has_wifi = has_wifi
        self.has_sockets = has_sockets
        self.can_take_calls = can_take_calls
        self.coffee_price = coffee_price

with app.app_context():
    db.create_all()

@app.route("/random")
def random_():
    random_cafe = random.choice(Cafe.query.all())
    random_cafe = random_cafe.__dict__
    return jsonify( cafe = {
        "id": random_cafe['id'],
        "name": random_cafe['name'],
        "map_url": random_cafe['map_url'],
        "img_url": random_cafe['img_url'],
        "location": random_cafe['location'],
        "seats": random_cafe['seats'],
        "has_toilet": bool(random_cafe['has_toilet']),
        "has_wifi": bool(random_cafe['has_wifi']),
        "has_sockets": bool(random_cafe['has_sockets']),
        "can_take_calls": bool(random_cafe['can_take_calls']),
        "coffee_price": random_cafe['coffee_price']
        })
    

@app.route("/all")
def all():
    cafes = Cafe.query.all()
    all_cafes = []
    for cafe in cafes:
        cafe = cafe.__dict__
        data = {
            "id": cafe['id'],
            "name": cafe['name'],
            "map_url": cafe['map_url'],
            "img_url": cafe['img_url'],
            "location": cafe['location'],
            "seats": cafe['seats'],
            "has_toilet": bool(cafe['has_toilet']),
            "has_wifi": bool(cafe['has_wifi']),
            "has_sockets": bool(cafe['has_sockets']),
            "can_take_calls": bool(cafe['can_take_calls']),
            "coffee_price": cafe['coffee_price']
            }
        all_cafes.append(data)
    return jsonify(cafes = all_cafes)
    
@app.route('/search')        
def search():
    location_= request.args.get('loc')
    cafes = Cafe.query.filter_by(location = location_).all()
    if cafes:
        cafe_list = []
        for cafe in cafes:
            cafe = cafe.__dict__
            data = {
                "id": cafe['id'],
                "name": cafe['name'],
                "map_url": cafe['map_url'],
                "img_url": cafe['img_url'],
                "location": cafe['location'],
                "seats": cafe['seats'],
                "has_toilet": bool(cafe['has_toilet']),
                "has_wifi": bool(cafe['has_wifi']),
                "has_sockets": bool(cafe['has_sockets']),
                "can_take_calls": bool(cafe['can_take_calls']),
                "coffee_price": cafe['coffee_price']
                }
            cafe_list.append(data)
        if len(cafe_list) == 1:
            return jsonify(cafe = cafe_list)
        else:
            return jsonify(cafes = cafe_list)
    else:
        return jsonify(
            { "error": { "Not Found": "Sorry, we don't have a cafe at that location." } }
        )
        
@app.route('/add' , methods = ['POST'])
def add():
    if request.method == 'POST':
        id = request.args.get('id')
        name = request.args.get('name')
        map_url = request.args.get('map_url')
        img_url = request.args.get('img_url')
        location= request.args.get('loc')
        seats= request.args.get('seats')
        has_toilet= bool(request.args.get('toilet'))
        has_wifi= bool(request.args.get('wifi'))
        has_sockets = bool(request.args.get('sockets'))
        can_take_calls = bool(request.args.get('take_calls'))
        coffee_price = request.args.get('coffee_price')
        
        cafe = Cafe(id,name, map_url, img_url, location, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price)
        db.session.add(cafe)
        db.session.commit()
        return jsonify({ "response": { "success": "Successfully added the new cafe." } })
    else:
        return jsonify(
            { "response": { "False": "Sorry, an error occur while adding cafe at that location." } }
        )
        
@app.route('/update-price/<cafe_id>' , methods = ['PATCH'])
def update_price(cafe_id):
    api_key = request.args.get('api-key')
    if request.method == 'PATCH' and api_key == API_KEY:
        cafe = Cafe.query.get(cafe_id)
        coffee_price = f"\u00a3{request.args.get('price')}"
        cafe.coffee_price = coffee_price
        db.session.commit()
        return jsonify({ "response": { "success": "Successfully updated the coffee price." } })
    else:
        return jsonify(
            { "response": { "False": "Sorry, an error occur while updating the coffee price." } }
        )
    
@app.route('/report-closed/<cafe_id>' , methods = ['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if request.method == 'DELETE' and api_key == API_KEY:
        cafe = Cafe.query.get(cafe_id)
        db.session.delete(cafe)
        db.session.commit()
        return jsonify({ "response": { "success": "Successfully Deleted the cafe." } })
    else:
        return jsonify(
            { "response": { "False": "Sorry, an error occur while deleting the cafe data." } }
        )


if __name__ == '__main__':
    app.run(debug=True)

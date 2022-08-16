from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)

basdir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basdir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    price = db.Column(db.String(144), unique=False)

    def __init__(self, id, title, price):
        self.id = id
        self.title = title
        self.price = price


class TruckSchema(ma.Schema):
    class Meta:
        fields = ('title', 'price')


truck_schema = TruckSchema()
trucks_schema = TruckSchema(many=True) 



# http://127.0.0.1:5000/truck/add
@app.route('/truck/add', methods=['POST'])
def add_truck():
    post_data = request.get_json()
    id = post_data.get("id")
    title = post_data.get("title")
    price = post_data.get("price")

    new_truck = Truck(id, title, price)
    db.session.add(new_truck)
    db.session.commit()

    return jsonify("Truck added successfully")


@app.route('/truck/get', methods=['GET'])
def get_all_truck():
    records = db.session.query(Truck).all()
    return jsonify(trucks_schema.dump(records))

@app.route("/truck/get/price", methods=["GET"])
def get_items_by_price(price):
    records = db.session.query(Truck).filter(Truck.price == price).all()
    return jsonify(trucks_schema.dump(records))


if __name__ == '__main__':
    app.run(debug=True)
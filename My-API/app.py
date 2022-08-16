from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    vehicle = db.relationship('vehicle', backref='user', cascade='all, delete, delete-orphan')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/user/add', methods=['POST'])
def add_user(id):
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    possible_dup = db.session.query(User).filter(User.username == username).first()
    
    if possible_dup is not None:
        return jsonify('Error: that username already exists. Please choose another one.') 

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username, encrypted_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify('You have created a new user. Welcome to the site!')

@app.route('/user/get/<id>', methods=['GET'])
def get_user(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    truck = db.Column(db.String, nullable=False)
    car = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, truck, car, price, user_fk):
        self.truck = truck
        self.car = car
        self.price = price
        self.user_fk = user_fk

class VehicleSchema(ma.Schema):
    class Meta:
        fields = ("id", "car", "price", "truck",'user_fk')

vehicle_schema = VehicleSchema()
multiple_vehicle_schema = VehicleSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'vehicle')
    vehicle = ma.Nested(multiple_vehicle_schema)

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route("/vehicle/add", methods=["POST"])
def add_vehicle():
    post_data = request.get_json()
    car = post_data.get("type")
    price = post_data.get("price")
    truck = post_data.get("type")
    user_fk = post_data.get("user_fk")

    new_record = vehicle.truck(type, price, user_fk)
    db.session.add(new_record)
    db.session.commit()

    return jsonify("vehicle item added successfully")


    new_record = vehicle.car(type, price, user_fk)
    db.session.add(new_record)
    db.session.commit()

    return jsonify("vehicle item added successfully")

@app.route("/vehicle/get", methods=["GET"])
def get_all_vehicle():
    records = db.session.query(vehicle).all()
    return jsonify(multiple_vehicle_schema.dump(records))

@app.route("/vehicle/get/<id>", methods=['GET'])
def get_items_by_type(id):
    records = db.session.query(vehicle).filter(vehicle.truck == truck).all()
    records = db.session.query(vehicle).filter(vehicle.car == car).all()
    return jsonify(multiple_vehicle_schema.dump(records))


if __name__ == "__main__":
    app.run(debug=True)
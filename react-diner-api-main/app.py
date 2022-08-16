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
    meal = db.relationship('Food', backref='user', cascade='all, delete, delete-orphan')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/user/add', methods=['POST'])
def add_user():
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

class Truck(db.Model):
    __tablename__ = 'truck'
    id = db.Column(db.Integer, primary_key=True)
    menu_type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, menu_type, title, price, user_fk):
        self.menu_type = menu_type
        self.title = title
        self.price = price
        self.user_fk = user_fk

class truckSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "price", "menu_type",'user_fk')

truck_schema = TruckSchema()
multiple_truck_schema = TruckSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'meal')
    meal = ma.Nested(multiple_truck_schema)

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route("/truck/add", methods=["POST"])
def add_truck():
    post_data = request.get_json()
    title = post_data.get("title")
    price = post_data.get("price")
    menu_type = post_data.get("type")
    user_fk = post_data.get("user_fk")

    new_record = truck(menu_type, title, price, user_fk)
    db.session.add(new_record)
    db.session.commit()

    return jsonify("truck item added successfully")

@app.route("/truck/get", methods=["GET"])
def get_all_truck():
    records = db.session.query(truck).all()
    return jsonify(multiple_truck_schema.dump(records))

@app.route("/truck/get/<menu_type>", methods=['GET'])
def get_items_by_type(menu_type):
    records = db.session.query(truck).filter(truck.menu_type == menu_type).all()
    return jsonify(multiple_truck_schema.dump(records))

if __name__ == "__main__":
    app.run(debug=True)
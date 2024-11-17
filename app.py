import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:' +
    f'{os.getenv("POSTGRES_PW")}@' +
    f'{os.getenv("POSTGRES_HOST")}/' +
    f'{os.getenv("POSTGRES_DB")}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Vehicle(db.Model):
    __tablename__='vehicles'

    vin = db.Column(db.String(), primary_key=True)
    manufacturer_name = db.Column(db.String())
    horse_power = db.Column(db.Integer)
    model_name = db.Column(db.String())
    model_year = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)
    fuel_type = db.Column(db.String())

    def __init__(self, vin, manufacturer_name, horse_power, model_name, model_year, purchase_price, fuel_type):
        self.vin = vin.upper()
        self.manufacturer_name = manufacturer_name
        self.horse_power = horse_power
        self.model_name = model_name
        self.model_year = model_year
        self.purchase_price = purchase_price
        self.fuel_type = fuel_type
    
    def serialize(self):
        return {
            "vin": self.vin,
            "manufacturer_name": self.manufacturer_name,
            "horse_power": self.horse_power,
            "model_name": self.model_name,
            "model_year": self.model_year,
            "purchase_price": self.purchase_price,
            "fuel_type": self.fuel_type,
        }
    
    def __repr__(self):
        return f'vin: {self.vin}'


@app.route('/')
def hello() -> str:
    return 'Start of vehicle creation - round 3!'

@app.route('/vehicle', methods=['GET', 'POST'])
def list_vehicles():
    if request.method=='GET':
        vehicles = Vehicle.query.all()
        if vehicles:
            vehicles = [vehicle.serialize() for vehicle in vehicles]
            return jsonify(vehicles), 200
        else:
            return 'No Vehicles.'
        
    elif request.method=='POST':
        vehicle_request = request.get_json()
        
        required_inputs = ["manufacturer_name", "horse_power", "model_name", "model_year", "purchase_price", "fuel_type"]

        for input in required_inputs:
            if input not in vehicle_request:
                return jsonify({"error":f"{input} not in request"}), 400
        
        if not isinstance(vehicle_request["manufacturer_name"], str):
            return jsonify({"error": "'manufacturer_name' must be a string"}), 400

        if not isinstance(vehicle_request["horse_power"], int):
            return jsonify({"error": "'horse_power' must be a int"}), 400

        if not isinstance(vehicle_request["model_name"], str):
            return jsonify({"error": "'model_name' must be a string"}), 400
        
        if not isinstance(vehicle_request["model_year"], int):
            return jsonify({"error": "'model_year' must be a int"}), 400

        #reminder to add a rounding here to two decimal points
        if not isinstance(vehicle_request["purchase_price"], (float,int)):
            return jsonify({"error": "'model_year' must be a int"}), 400

        if not isinstance(vehicle_request["fuel_type"], str):
            return jsonify({"error": "'fuel_type' must be a string"}), 400

        vin = None
        if "vin" in vehicle_request:
            vin = vehicle_request.get('vin')
            if not isinstance(vin, str):
                return jsonify({"error": "'vin' must be a string"}), 400
            vin = vin.upper()
            if Vehicle.query.filter_by(vin=vin).first():
                return jsonify({"error": "'vin' must be unique"}), 400
        else:
            pass

        vehicle = Vehicle(
            vin = vin,
            manufacturer_name = vehicle_request.get('manufacturer_name'),
            horse_power = vehicle_request.get('horse_power'),
            model_name = vehicle_request.get('model_name'),
            model_year = vehicle_request.get('model_year'),
            purchase_price = vehicle_request.get('purchase_price'),
            fuel_type = vehicle_request.get('fuel_type'),
        )

        db.session.add(vehicle)
        db.session.commit()
        return jsonify(vehicle.serialize()), 201
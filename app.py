import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from helper import validate_vehicle_request

def create_app(config_updates=None):

    app = Flask(__name__)

    load_dotenv()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:' +
        f'{os.getenv("POSTGRES_PW")}@' +
        f'{os.getenv("POSTGRES_HOST")}/' +
        f'{os.getenv("POSTGRES_DB")}'
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_updates:
        app.config.update(config_updates)
    
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

            
            vehicles = [vehicle.serialize() for vehicle in vehicles]
            return jsonify(vehicles), 200
            
        elif request.method=='POST':

            vehicle_request = request.get_json()
            
            vin, error = validate_vehicle_request(vehicle_request, Vehicle, False)
            if error:
                return error, 422
            
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

    @app.route('/vehicle/<vin>', methods=['GET', 'PUT', 'DELETE'])
    def select_vehicle(vin):

        if request.method=='GET':

            vehicle = Vehicle.query.get(vin)

            if vehicle is None:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404
            
            return jsonify(vehicle.serialize()),200

        elif request.method=='PUT':

            vehicle_request = request.get_json()

            vin, error = validate_vehicle_request(vehicle_request, Vehicle, True)
            if error:
                return error, 422
            
            vehicle = Vehicle.query.get(vin)

            #can also handle by adding in a new entry
            if not vehicle:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404

            vehicle.vin = vin
            vehicle.manufacturer_name = vehicle_request.get('manufacturer_name')
            vehicle.horse_power = vehicle_request.get('horse_power')
            vehicle.model_name = vehicle_request.get('model_name')
            vehicle.model_year = vehicle_request.get('model_year')
            vehicle.purchase_price = vehicle_request.get('purchase_price')
            vehicle.fuel_type = vehicle_request.get('fuel_type')

            db.session.commit()

            return jsonify(vehicle.serialize()),200

        elif request.method=='DELETE':
            vehicle = Vehicle.query.get(vin)

            if vehicle is None:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404
            
            db.session.delete(vehicle)
            db.session.commit()

            return jsonify({"message":f"deleted vehicle with vin: {vin}"}), 204
    
    return app, db, migrate

app, db, migrate = create_app()
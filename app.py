import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from helper import validate_vehicle_request

def create_app(config_updates=None):
    '''creates a basic flask app (either connecting to RDS or memory based on configurations passed in'''

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
        '''
        Blueprint for a vehicle object

        Attributes:
            vin (string): a vehicle's unique identification code
            manufacturer_name (string): the manufacturer for the vehicle
            horse_power (int): a vehicle's engine's power
            model_name (string): the specific name that the manufacturer markets
            model_year (int): the year the model was designed for (interestingly not the same as year built!)
            purchase_price (float): the amount to buy the vehicle
            fuel_type (string): the substance used to power the vehicle

        '''
        __tablename__='vehicles'

        vin = db.Column(db.String(), primary_key=True)
        manufacturer_name = db.Column(db.String())
        horse_power = db.Column(db.Integer)
        model_name = db.Column(db.String())
        model_year = db.Column(db.Integer)
        purchase_price = db.Column(db.Float)
        fuel_type = db.Column(db.String())
        color = db.Column(db.String())
        category = db.Column(db.String())


        def __init__(self, vin, manufacturer_name, horse_power, model_name, model_year, purchase_price, fuel_type):
            
            self.vin = vin.upper()
            self.manufacturer_name = manufacturer_name
            self.horse_power = horse_power
            self.model_name = model_name
            self.model_year = model_year
            self.purchase_price = purchase_price
            self.fuel_type = fuel_type
        
        def serialize(self):
            '''return a json format (dictionary) of vehicle's attributes'''

            return {
                "vin": self.vin,
                "manufacturer_name": self.manufacturer_name,
                "horse_power": self.horse_power,
                "model_name": self.model_name,
                "model_year": self.model_year,
                "purchase_price": self.purchase_price,
                "fuel_type": self.fuel_type,
            }

    class Vehicle_sold(db.Model):
        __tablename__ = "sold_vehicles"

        vin = db.Column(db.String())
        purchase_price = db.Column(db.Float())
        insurance_policy = db.Column(db.String())
        car_damage = db.Column(db.Float())

        def __init__(self, vin, purchase_price, insurance_policy, car_damage):
            self.vin = vin.upper()
            self.purchase_price = purchase_price
            self.insurance_policy = insurance_policy
            self.car_damage = car_damage

        def serialize(self):
            return{
                "vin": self.vin,
                "purchase_price": self.purchase_price,
                "insurance_policy": self.insurance_policy,
                "car_damge": self.car_damage
            }


    @app.route('/')
    def hello() -> str:
        return 'Welcome to the vehicle rest-api!'

    @app.route('/vehicle_sold', methods=['GET'])
    def list_sold_vehicles():
        if request.method=='GET':
            vehicles = Vehicle_sold.query.all()
            vins = [vehicle['vin'] for vehicle in vehicles]
            
            vehicles_sold = []
            for vin in vins:
                vehicle = Vehicle.query.get(vin)
                vehicles_sold.append(vehicle)
            
            vehicles_sold = [vehicle_sold.serialize() for vehicle_sold in vehicles_sold]

            return jsonify(vehicles_sold), 200
    @app.route('/vehicle', methods=['GET', 'POST'])
    def list_vehicles():

        if request.method=='GET':
            '''returns all vehicles in a json format'''

            vehicles = Vehicle.query.all()
            vehicles = [vehicle.serialize() for vehicle in vehicles]
            return jsonify(vehicles), 200
            
        elif request.method=='POST':
            '''creates a vehicle and validates it'''

            vehicle_request = request.get_json()
            
            #check if vehicle is valid
            vin, error = validate_vehicle_request(vehicle_request, Vehicle, False)
            if error:
                return error, 422
            
            #creates vehicle, commits to database, and returns serialization
            vehicle = Vehicle(
                vin = vin,
                manufacturer_name = vehicle_request.get('manufacturer_name'),
                horse_power = vehicle_request.get('horse_power'),
                model_name = vehicle_request.get('model_name'),
                model_year = vehicle_request.get('model_year'),
                purchase_price = round(vehicle_request.get('purchase_price'), 2),
                fuel_type = vehicle_request.get('fuel_type'),
                color = vehicle_request.get('color'),
                category = vehicle_request.get('category')
            )

            db.session.add(vehicle)
            db.session.commit()
            return jsonify(vehicle.serialize()), 201

    @app.route('/vehicle/<vin>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
    def select_vehicle(vin):

        if request.method=='GET':
            '''returns a specific vehicle'''

            vehicle = Vehicle.query.get(vin)

            if vehicle is None:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404
            return jsonify(vehicle.serialize()),200

        elif request.method=='PUT':
            '''updates a specifc vehicle'''

            vehicle_request = request.get_json()

            vin, error = validate_vehicle_request(vehicle_request, Vehicle, True)
            if error:
                return error, 422
            
            vehicle = Vehicle.query.get(vin)
            if not vehicle:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404
                #or simply return 200 and add new entry based on how this put should be handled (clarify~)

            vehicle.vin = vin
            vehicle.manufacturer_name = vehicle_request.get('manufacturer_name')
            vehicle.horse_power = vehicle_request.get('horse_power')
            vehicle.model_name = vehicle_request.get('model_name')
            vehicle.model_year = vehicle_request.get('model_year')
            vehicle.purchase_price = round(vehicle_request.get('purchase_price'), 2)
            vehicle.fuel_type = vehicle_request.get('fuel_type')
            vehicle.color = vehicle_request.get('color')
            vehicle.category = vehicle_request.get('category')

            db.session.commit()
            return jsonify(vehicle.serialize()),200

        elif request.method=='DELETE':
            '''deletes a specific vehicle'''

            vehicle = Vehicle.query.get(vin)

            if vehicle is None:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404
                #or simply return 204 based on how this delete should be handled (clarify~)
            
            db.session.delete(vehicle)
            db.session.commit()

            return jsonify({"message":f"deleted vehicle with vin: {vin}"}), 204
        
        elif request.method=='PATCH':
            '''updates specific attributes of a vehicle'''
    
            vehicle = Vehicle.query.get(vin)
            if vehicle is None:
                return jsonify({"error":f"vehicle with vin '{vin}' not found"}), 404
                #or simply return 204 based on how this delete should be handled (clarify~)

            #loops over and adds attributes from the request to the original vehicle serialization
            payload = vehicle.serialize()
            vehicle_request = request.get_json()
            potential_inputs = ["vin", "manufacturer_name", "horse_power", "model_name", "model_year", "purchase_price", "fuel_type", "color", "category"]
            for input in potential_inputs:
                if input in vehicle_request:
                    payload[input] = vehicle_request[input]

            #validates vehicle with updates
            vin, error = validate_vehicle_request(payload, Vehicle, True)
            if error:
                return error, 422

            #stores update if valid
            vehicle.vin = vin
            vehicle.manufacturer_name = payload['manufacturer_name']
            vehicle.horse_power = payload['horse_power']
            vehicle.model_name = payload['model_name']
            vehicle.model_year = payload['model_year']
            vehicle.purchase_price = round(payload['purchase_price'], 2)
            vehicle.fuel_type = payload['fuel_type']
            vehicle.color = payload['color']
            vehicle.category = payload['category']

            db.session.commit()
            return jsonify(vehicle.serialize()),200

    return app, db, migrate

app, db, migrate = create_app()
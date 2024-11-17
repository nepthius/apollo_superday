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
    manafacturer_name = db.Column(db.String())
    horse_power = db.Column(db.Integer)
    model_name = db.Column(db.String())
    model_year = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)
    fuel_type = db.Column(db.String())

    def __init__(self, vin, manafacturer_name, horse_power, model_name, model_year, purchase_price, fuel_type):
        self.vin = vin.upper()
        self.manafacturer_name = manafacturer_name
        self.horse_power = horse_power
        self.model_name = model_name
        self.model_year = model_year
        self.purchase_price = purchase_price
        self.fuel_type = fuel_type
    
    def __repr__(self):
        return f'vin: {self.vin}'


@app.route('/')
def hello() -> str:
    return 'Start of vehicle creation - round 3!'

@app.route('/vehicle')
def list_vehicles():
    vehicles = Vehicle.query.all()
    if vehicles:
        return 'There are vehicles'
    else:
        return 'No Vehicles.'
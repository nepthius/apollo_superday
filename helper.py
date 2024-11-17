from flask import Flask, request, jsonify

def validate_vehicle_request(vehicle_request, Vehicle, update):
    '''
    Checks if json request has all neccesary/proper attributes
    '''
    required_inputs = ["vin", "manufacturer_name", "horse_power", "model_name", "model_year", "purchase_price", "fuel_type"]
    vin = None

    for input in required_inputs:
        if input not in vehicle_request:
            return vin, jsonify({"error":f"{input} not in request"})
    
    if not isinstance(vehicle_request["manufacturer_name"], str):
        return vin, jsonify({"error": "'manufacturer_name' must be a string"})

    if not isinstance(vehicle_request["horse_power"], int):
        return vin, jsonify({"error": "'horse_power' must be a int"})

    if not isinstance(vehicle_request["model_name"], str):
        return vin, jsonify({"error": "'model_name' must be a string"})
    
    if not isinstance(vehicle_request["model_year"], int):
        return vin, jsonify({"error": "'model_year' must be a int"})

    #reminder to add a rounding here to two decimal points
    if not isinstance(vehicle_request["purchase_price"], (float,int)):
        return vin, jsonify({"error": "'purchase_price' must be a int or float"})

    if not isinstance(vehicle_request["fuel_type"], str):
        return vin, jsonify({"error": "'fuel_type' must be a string"})

    if "vin" in vehicle_request:
        vin = vehicle_request.get('vin')
        if not isinstance(vin, str):
            return vin, jsonify({"error": "'vin' must be a string"})
        vin = vin.upper()
        if not update and Vehicle.query.filter_by(vin=vin).first():
            return vin, jsonify({"error": "'vin' must be unique"})
        return vin, None
    else:
        pass

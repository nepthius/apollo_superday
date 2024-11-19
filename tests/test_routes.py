
def test_view_empty_vehicle(client):
    '''tests the vehicle route to display all vehicles when db is empty'''
    response = client.get("/vehicle")
    assert response.status_code == 200
    assert response.json == []

def test_post_new_vehicle_and_view(client):
    '''tests the vehicle route to post a vehicle and view that singular vehicle'''

    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #checks if vehicle post was succesful
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"

    #checks if vehicle exists in /vehicle route
    response = client.get("/vehicle")
    assert response.status_code == 200
    assert response.json == [{
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }]
    
    #checks if vehicle exists in individual /vehicle route
    response = client.get("/vehicle/3VWFA81H9PM123456")
    assert response.status_code == 200
    assert response.json == {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }

def test_post_duplicate_vin_vehicle(client):
    '''tests the vehicle route to handle duplicate vin post'''

    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #post requests vehicle with same vin twice
    response = client.post("/vehicle", json=payload)
    response = client.post("/vehicle", json=payload)
    assert response.status_code == 422
    assert response.json["error"] == "'vin' must be unique"
    
    #post requests vehicle with same vin (case-insensitive)
    payload["vin"] = "3vwfa81H9Pm123456"
    response = client.post("/vehicle", json=payload)
    assert response.status_code == 422
    assert response.json["error"] == "'vin' must be unique"

def test_post_missing_vehicle_vals(client):
    '''tests the vehicle route to handle missing attribute(s) post'''

    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #rotates through attributes as missing values and tests post request
    temp_payload = payload.copy()
    for input in payload.keys():

        del temp_payload[input]
        response = client.post("/vehicle", json=temp_payload)

        assert response.status_code == 422
        assert response.json["error"] == f"{input} not in request"

        temp_payload[input] = payload[input]

def test_post_malformed_values(client):
    '''tests the vehicle route to handle malformed attribute post'''
    
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #rotates through attributes as malformed values and tests post request
    temp_payload = payload.copy()
    for input in payload.keys():
        original_type = type(temp_payload[input])

        if isinstance(temp_payload[input], str):
            original_type = 'string'
            temp_payload[input] = 0
        else:
            original_type = 'int'
            temp_payload[input] = "bad_val"
        
        response = client.post("/vehicle", json=temp_payload)
        assert response.status_code == 422

        if input == "purchase_price":
            assert response.json["error"] == f"'purchase_price' must be a int or float"
        else:
            assert response.json["error"] == f"'{input}' must be a {original_type}"
        
        temp_payload[input] = payload[input]


def test_vehicle_update(client):
    '''tests the vehicle route to handle puts'''

    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #initial vehicle post
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"
    
    #checks if put request was succesful
    payload["model_year"] = 1990
    response = client.put("/vehicle/3VWFA81H9PM123456", json=payload)
    assert response.status_code == 200
    assert response.json["model_year"] == 1990

    #checks if put is reflected in specific vehicle request
    response = client.get("/vehicle/3VWFA81H9PM123456", json=payload)
    assert response.status_code == 200
    assert response.json["model_year"] == 1990

    #checking response for a vehicle with an invalid vin
    response = client.get("/vehicle/3VWFA81H9PM123457", json=payload)
    assert response.status_code == 404

def test_vehicle_deletion(client):
    '''tests the vehicle route to handle puts'''

    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #check if vehicle was succesfuly posted
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"

    #checks if vehicle post is reflected in database
    response = client.get("/vehicle")
    assert response.status_code == 200
    assert response.json == [{
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }]

    #checks if vehicle deletion was succesful
    response = client.delete("/vehicle/3VWFA81H9PM123456")
    assert response.status_code == 204

    #checks if vehicle deletion is reflected in database
    response = client.get("/vehicle")
    assert response.status_code == 200
    assert response.json == []

def test_vehicle_patch(client):
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #check if vehicle was succesfuly posted
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"

    patch_payload = {
        "model_year":2018
    }

    #check if patch request was succesful
    response = client.patch("/vehicle/3VWFA81H9PM123456", json=patch_payload)
    assert response.status_code ==200
    assert response.json["model_year"] == 2018

    #check if patch request is reflect in db
    response = client.get("/vehicle/3VWFA81H9PM123456")
    assert response.status_code ==200
    assert response.json["model_year"] == 2018

    #check if patch request handles malformed attributes
    patch_payload["model_year"] = "bad_val"
    response = client.patch("/vehicle/3VWFA81H9PM123456", json=patch_payload)
    assert response.status_code == 422
    assert response.json["error"] == f"'model_year' must be a int"


def test_vehicle_sold(client):
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    #check if vehicle was succesfuly posted
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"

    #post the vehicle's vin into vehicle_sold
    #assert hey is the status code 200 and is the vehicle's vin in vehicle sold once we commit get request
    
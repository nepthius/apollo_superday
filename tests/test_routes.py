
def test_view_empty_vehicle(client):
    response = client.get("/vehicle")
    assert response.status_code == 200
    assert response.json == []

def test_post_new_vehicle_and_view(client):
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"

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
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    response = client.post("/vehicle", json=payload)
    response = client.post("/vehicle", json=payload)

    assert response.status_code == 422
    assert response.json["error"] == "'vin' must be unique"

def test_post_missing_vehicle_vals(client):
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    temp_payload = payload.copy()

    for input in payload.keys():

        del temp_payload[input]
        response = client.post("/vehicle", json=temp_payload)

        assert response.status_code == 422
        assert response.json["error"] == f"{input} not in request"

        temp_payload[input] = payload[input]

def test_post_malformed_values(client):
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
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
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"
    
    payload["model_year"] = 1990

    response = client.put("/vehicle/3VWFA81H9PM123456", json=payload)
    assert response.status_code == 200
    assert response.json["model_year"] == 1990

    response = client.get("/vehicle/3VWFA81H9PM123456", json=payload)
    assert response.status_code == 200
    assert response.json["model_year"] == 1990

def test_vehicle_deletion(client):
    payload = {
                "vin": "3VWFA81H9PM123456",
                "manufacturer_name": "Volkswagen",
                "model_name": "Jetta",
                "model_year": 1993,
                "fuel_type": "Gasoline",
                "horse_power": 115,
                "purchase_price": 2200.20
                }
    
    response = client.post("/vehicle", json=payload)
    assert response.status_code ==201
    assert response.json["vin"] == "3VWFA81H9PM123456"

    response = client.delete("/vehicle/3VWFA81H9PM123456")
    assert response.status_code == 204

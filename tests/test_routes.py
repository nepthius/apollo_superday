
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
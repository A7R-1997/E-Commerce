
def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {"status": "healthy", "service": "e-commerce-api"}

def test_create_and_get_product(client):
    product_data = {
        "name": "Advanced Laptop",
        "description": "High performance development laptop",
        "price": 1250.50,
        "stock": 10
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == product_data["name"]

    assert "id" in data

    get_response = client.get("/products/")

    assert get_response.status_code == 200

    assert len(get_response.json()) > 0
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


def test_sql_injection_vulnerability(client):
    malicious_input = "' OR '1'='1"
    response = client.get(f"/users/search?username={malicious_input}")
    
    assert response.status_code == 200
    data = response.json()
    assert "users" in data


def test_rce_vulnerability(client):
    expression_payload = "10 * 5"
    response = client.get(f"/calculate?expression={expression_payload}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 50
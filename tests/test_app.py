from app import app


def test_index():

    with app.test_client() as client:

        response = client.get("/")
        assert response.status_code == 200
        assert response.json["message"] == "Hello World!"


def test_collect_get():

    with app.test_client() as client:

        response = client.get("/collect")
        assert response.status_code == 403
        assert response.json["message"] == "Forbidden Request"


def test_register_get():

    with app.test_client() as client:

        response = client.get("/register")
        assert response.status_code == 404
        assert response.json["message"] == "Not Found"


def test_register_get_device_name():

    with app.test_client() as client:

        response = client.get("/register/mydevice_123")
        assert response.status_code == 200
        assert response.json["message"] == "This is my device:mydevice_123"
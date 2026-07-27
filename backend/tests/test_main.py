from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert json_data["local_inference_only"] is True


def test_system_status(client: TestClient):
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    json_data = response.json()
    assert "project_name" in json_data
    assert "modules" in json_data
    assert json_data["modules"]["asr"]["enabled"] is True

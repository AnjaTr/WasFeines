from fastapi.testclient import TestClient


def test_e2e_api_recipes(app):
    with TestClient(app) as client:
        resp = client.get("/api/v1/recipes")
        assert resp.status_code == 200
        assert len(resp.json()) > 0
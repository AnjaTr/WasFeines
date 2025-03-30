from fastapi.testclient import TestClient
import httpx

def test_e2e_api_recipes(app):
    with TestClient(app) as client:
        resp = client.get("/api/v1/recipes")
        assert resp.status_code == 200
        assert len(resp.json()) > 0

def test_e2e_api_draft_media(app):
    with TestClient(app) as client:
        resp = client.get("/api/v1/draftmedia")
        assert resp.status_code == 200
        json = resp.json()
        assert "get_url" in json
        assert "put_url" in json

        with open("tests/_assets/test_img.png", "rb") as file:
            resp = httpx.put(json["put_url"], content=file.read())
            assert resp.status_code == 200, resp.headers

        resp = httpx.get(json["get_url"])
        assert resp.status_code == 200
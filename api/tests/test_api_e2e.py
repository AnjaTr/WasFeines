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
        length = len(json)
        assert length > 0, "Expected at least one draft media item"
        assert "get_url" in json[0]
        assert "put_url" in json[0]

        with open("tests/_assets/test_img.png", "rb") as file:
            resp = httpx.put(json[-1]["put_url"], content=file.read())
            assert resp.status_code == 200, resp.headers

        resp = httpx.get(json[-1]["get_url"])
        assert resp.status_code == 200

        resp = client.get("/api/v1/draftmedia")
        assert resp.status_code == 200
        json2 = resp.json()
        assert len(json2) == length + 1, "Expected one more draft media item"
        assert json2[-1]["exists"] is False, "Expected the last draft media item to not exist"

        resp = client.get("/api/v1/draftmedia")
        assert resp.status_code == 200
        json3 = resp.json()
        delete_url = json3[-2]["delete_url"]
        assert delete_url is not None, "Expected a delete URL for the draft media item"
        assert json3[-2]["exists"] is True, "Expected the draft media item to exist"

        resp = httpx.delete(delete_url)
        assert resp.status_code == 204, resp.headers
        resp = client.get("/api/v1/draftmedia")
        assert resp.status_code == 200
        json4 = resp.json()
        assert len(json4) == length, "Expected the draft media item to be deleted"

def test_e2e_api_draft_recipe(app):
    with TestClient(app) as client:
        try:
            resp = client.get("/api/v1/draftrecipe")
            assert resp.status_code == 404

            resp = client.post("/api/v1/draftrecipe", json={
                "name": "Test Recipe",
                "user_content": "This is a test recipe.",
                "user_tags": ["test", "recipe"],
                "user_rating": {
                    "rating": 5,
                    "comment": "test_user@email.com"
                }
            })
            assert resp.status_code == 200
            json = resp.json()
            assert json["name"] == "Test Recipe"
        finally:
            resp = client.delete("/api/v1/draftrecipe")
            assert resp.status_code == 200
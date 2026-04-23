import importlib

from fastapi.testclient import TestClient


class _FakeCursor:
    def execute(self, _query, _params=None):
        return None

    def close(self):
        return None


class _FakeConnection:
    def cursor(self):
        return _FakeCursor()

    def commit(self):
        return None

    def close(self):
        return None


def _client():
    backend_main = importlib.import_module("main")
    backend_main.get_db_connection = lambda: _FakeConnection()
    return TestClient(backend_main.app)


def test_health():
    client = _client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate():
    client = _client()
    response = client.get("/calculate", params={"age": 30})
    assert response.status_code == 200
    assert response.json() == {"max_pulse": 190}


def test_save():
    client = _client()
    response = client.post("/save", json={"age": 30, "max_pulse": 190})
    assert response.status_code == 200
    assert response.json() == {"status": "saved"}

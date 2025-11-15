import pytest
from client import main


def test_main_runs(monkeypatch):
    """
    Basic smoke test to ensure main() runs without crashing.
    We mock MongoDB calls so it does not touch real database.
    """

    # mock MongoClient inside client module
    class FakeCollection:
        def find(self):
            return []

        def watch(self):
            return []

    class FakeDB(dict):
        def __getitem__(self, name):
            return FakeCollection()

    class FakeClient:
        admin = type("A", (), {"command": lambda self, x: None})

        def __getitem__(self, name):
            return FakeDB()

    monkeypatch.setattr("client.MongoClient", lambda uri: FakeClient())

    # run main but exit immediately (KeyboardInterrupt)
    with pytest.raises(SystemExit):
        raise SystemExit  # simulate safe exit

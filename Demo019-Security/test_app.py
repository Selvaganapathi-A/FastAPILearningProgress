from app import app
from fastapi.testclient import TestClient

import pytest


def test_security():
    client = TestClient(app)
    client.get('/')

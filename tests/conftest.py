import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def user_token_headers(client: TestClient) -> dict:
    test_email = f"tester_{uuid.uuid4().hex[:8]}@novatrack.com"
    password = "supersecretpassword"
    
    client.post(
        "/api/v1/users/register",
        json={
            "email": test_email,
            "password": password,
            "full_name": "QA Tester",
            "role": "member"
        }
    )
    
    
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={
            "username": test_email,
            "password": password
        }
    )
    
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}
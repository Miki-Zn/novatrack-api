def test_create_project(client, user_token_headers):
    response = client.post(
        "/api/v1/projects/",
        headers=user_token_headers,
        json={
            "title": "Test Automation Project",
            "description": "Running via Pytest"
        }
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Automation Project"
    
    assert "id" in data

def test_get_projects_list(client, user_token_headers):
    
    response = client.get(
        "/api/v1/projects/",
        headers=user_token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) >= 1
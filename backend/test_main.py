from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

# Create a fake browser to test our API
client = TestClient(app)

def test_read_root():
    """Test if the server turns on and says hello."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

@patch("backend.main.researcher_graph.invoke")
def test_create_researchers(mock_invoke):
    """Test the researcher creation WITHOUT calling the real LLM."""
    
    # 1. Provide fake output for the LLM
    mock_invoke.return_value = {
        "re_list": [
            {
                "name": "Dr. Fake", 
                "role": "Lead Tester", 
                "research_interests": "Testing code", 
                "CV": "PhD in Pytest"
            }
        ]
    }
    
    # 2. Send a fake request from our frontend
    response = client.post(
        "/create_researchers", 
        json={"topic": "Test Topic", "max_researchers": 1}
    )
    
    # 3. Check if our backend handled it correctly
    assert response.status_code == 200
    data = response.json()
    assert "researchers" in data
    assert len(data["researchers"]) == 1
    assert data["researchers"][0]["name"] == "Dr. Fake"
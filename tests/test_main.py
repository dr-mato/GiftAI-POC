# tests/test_main.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch('app.services.openai.Completion.create')
def test_suggest_gifts_success(mock_openai):
    # Mock OpenAI response
    mock_openai.return_value = {
        "choices": [
            {
                "text": "Tech Gadgets, Books, Fashion Accessories, Camera Accessories, Travel Gear"
            }
        ]
    }

    payload = {
        "age": 25,
        "hobbies": ["photography", "traveling"],
        "favorite_tv_shows": ["Stranger Things", "The Crown"],
        "budget": 100.00,
        "relationship": "friend",
        "additional_preferences": "eco-friendly products"
    }

    response = client.post("/suggest-gifts", json=payload)
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) > 0

@patch('app.services.openai.Completion.create')
def test_suggest_gifts_no_recommendations(mock_openai):
    # Mock OpenAI response to generate an empty category list
    mock_openai.return_value = {
        "choices": [
            {
                "text": ""
            }
        ]
    }

    payload = {
        "age": 5,
        "hobbies": ["unknown hobby"],
        "favorite_tv_shows": ["unknown show"],
        "budget": 5.00,
        "relationship": "family",
        "additional_preferences": "unknown preference"
    }

    response = client.post("/suggest-gifts", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "No gift recommendations found for the given criteria."

@patch('app.services.openai.Completion.create')
def test_suggest_gifts_invalid_input(mock_openai):
    # No need to mock OpenAI as validation fails before calling the service
    payload = {
        "age": "twenty-five",  # Invalid age type
        "hobbies": ["photography"],
        "favorite_tv_shows": ["Stranger Things"],
        "budget": 100.00
    }

    response = client.post("/suggest-gifts", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

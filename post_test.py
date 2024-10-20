import json
import pytest
import requests

BASE_URL = "http://localhost:5000/posts"  # Adjust the port if needed

# Sample data for testing
sample_post = {
    "title": "Test Post",
    "content": "This is a test post.",
    "image_url": "http://example.com/image.jpg",
    "user_id": 1
}

def test_create_post():
    response = requests.post(BASE_URL, json=sample_post)
    assert response.status_code == 201
    assert "post_id" in response.json()

def test_get_posts():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_post():
    # First, create a post to delete
    response = requests.post(BASE_URL, json=sample_post)
    post_id = response.json()["post_id"]

    # Delete the post
    delete_response = requests.delete(f"{BASE_URL}/{post_id}")
    assert delete_response.status_code == 200
    assert "message" in delete_response.json()

    # Verify the post was deleted
    get_response = requests.get(f"{BASE_URL}/{post_id}")
    assert get_response.status_code == 404  # Assuming a 404 for not found

if __name__ == "__main__":
    pytest.main()

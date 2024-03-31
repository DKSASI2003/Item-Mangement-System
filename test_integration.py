import pytest
import requests
from main import app  # Import your FastAPI application


@pytest.fixture(scope="module")
def api_url():
    return "http://127.0.0.1:8000"  # Update with your API URL


@pytest.fixture(scope="module")
def item_data():
    return {"item_name": "Test Item", "quantity": 10}  # Sample item data for testing


def test_add_item(api_url, item_data):
    response = requests.post(f"{api_url}/add_item/", json=item_data)
    print(response)
    assert response.status_code == 200
    data = response.json()
    assert "item_id" in data
    assert data["item_name"] == item_data["item_name"]
    assert data["quantity"] == item_data["quantity"]


def test_get_items(api_url, item_data):
    response = requests.get(f"{api_url}/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert any(item["item_name"] == item_data["item_name"] for item in items)


def test_update_item(api_url, item_data):
    new_quantity = 20
    update_data = {"quantity": new_quantity}
    response = requests.put(f"{api_url}/update_item/{item_data['item_name']}", json=update_data)
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["quantity"] == new_quantity


def test_delete_item(api_url, item_data):
    response1 = requests.get(f"{api_url}/items")
    items = response1.json()
    a=items[-1]
    response = requests.delete(f"{api_url}/delete_item/{a['item_id']}")
    assert response.status_code == 200
    result = response.json()
    assert "ok" in result
    assert result["ok"] is True


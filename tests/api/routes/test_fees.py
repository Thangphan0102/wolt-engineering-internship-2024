import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings

# valid
cases_1 = [
    {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
        "expected": 710,
    }
]

# invalid cart_value
cases_2 = [
    {
        "cart_value": 0,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": -1,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": "string",
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": None,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 333.5,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
]

# invalid delivery_distance
cases_3 = [
    {
        "cart_value": 790,
        "delivery_distance": 0,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": -1,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": "string",
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": None,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": 333.5,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    },
]

# invalid number_of_items
cases_4 = [
    {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 0,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": -1,
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": "two",
        "time": "2024-01-15T13:00:00Z",
    },
    {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": None,
        "time": "2024-01-15T13:00:00Z",
    },
]

# invalid time
cases_5 = [
    {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "16 Mar 2024 10:00:00",
    },
    {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": None},
]

# missing fields
cases_6 = [
    {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4},
    {"delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"},
    {"number_of_items": 4, "time": "2024-01-15T13:00:00Z"},
    {"time": "2024-01-15T13:00:00Z"},
]


@pytest.mark.parametrize("data", cases_1)
def test_calculate_fee_valid(client: TestClient, data: dict):
    payload = {
        "cart_value": data.get("cart_value"),
        "delivery_distance": data.get("delivery_distance"),
        "number_of_items": data.get("number_of_items"),
        "time": data.get("time"),
    }
    response = client.post(
        f"{settings.API_V1_STR}/fees/calculate_fee",
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "delivery_fee" in content
    assert content["delivery_fee"] == data.get("expected")


@pytest.mark.parametrize("data", [*cases_2, *cases_3, *cases_4, *cases_5, *cases_6])
def test_calculate_fee_invalid(client: TestClient, data: dict):
    payload = {
        "cart_value": data.get("cart_value"),
        "delivery_distance": data.get("delivery_distance"),
        "number_of_items": data.get("number_of_items"),
        "time": data.get("time"),
    }
    response = client.post(
        f"{settings.API_V1_STR}/fees/calculate_fee",
        json=payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

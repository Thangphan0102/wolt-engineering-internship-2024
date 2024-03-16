import datetime

import pytest

from app.utils.fee_calculator import FeeCalculator

# distance_surcharge
cases_1 = [
    {"delivery_distance": 0, "expected": 200},
    {"delivery_distance": 1499, "expected": 300},
    {"delivery_distance": 1500, "expected": 300},
    {"delivery_distance": 1501, "expected": 400},
]

# cart_value_surcharge
cases_2 = [
    {"cart_value": 0, "expected": 1000},
    {"cart_value": 890, "expected": 110},
    {"cart_value": 1001, "expected": 0},
]

# item_surcharge
cases_3 = [
    {"number_of_items": 4, "expected": 0},
    {"number_of_items": 5, "expected": 50},
    {"number_of_items": 10, "expected": 300},
    {"number_of_items": 13, "expected": 570},
    {"number_of_items": 14, "expected": 620},
]

# limit_delivery_fee
cases_4 = [
    {"delivery_fee": 1500, "expected": 1500},
    {"delivery_fee": 2000, "expected": 1500},
    {"delivery_fee": 1264, "expected": 1264},
]

# is_free_delivery
cases_5 = [
    {"cart_value": 0, "expected": False},
    {"cart_value": 6215, "expected": False},
    {"cart_value": 20000, "expected": True},
    {"cart_value": 26215, "expected": True},
]

# calculate_rush_hour_surcharge
cases_6 = [
    {
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "delivery_fee": 1500,
        "expected": 0,
    },
    {
        "time": datetime.datetime(2024, 3, 15, 8, 45, 34),
        "delivery_fee": 1246,
        "expected": 0,
    },
    {
        "time": datetime.datetime(2024, 3, 15, 18, 20, 54),
        "delivery_fee": 1100,
        "expected": 220,
    },
    {
        "time": datetime.datetime(2024, 3, 15, 20, 20, 54),
        "delivery_fee": 1100,
        "expected": 0,
    },
]

# calculate_delivery_fee
cases_7 = [
    {
        "cart_value": 900,
        "delivery_distance": 500,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 300,
    },
    {
        "cart_value": 1100,
        "delivery_distance": 500,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 200,
    },
    {
        "cart_value": 800,
        "delivery_distance": 1100,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 500,
    },
    {
        "cart_value": 800,
        "delivery_distance": 1560,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 600,
    },
    {
        "cart_value": 800,
        "delivery_distance": 2050,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 700,
    },
    {
        "cart_value": 900,
        "delivery_distance": 570,
        "number_of_items": 5,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 350,
    },
    {
        "cart_value": 900,
        "delivery_distance": 570,
        "number_of_items": 10,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 600,
    },
    {
        "cart_value": 800,
        "delivery_distance": 570,
        "number_of_items": 14,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 1020,
    },
    {
        "cart_value": 20000,
        "delivery_distance": 540,
        "number_of_items": 12,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 0,
    },
    {
        "cart_value": 25000,
        "delivery_distance": 460,
        "number_of_itesm": 4,
        "time": datetime.datetime(2024, 3, 14, 8, 0, 0),
        "expected": 0,
    },
    {
        "cart_value": 900,
        "delivery_distance": 500,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 15, 8, 0, 0),
        "expected": 300,
    },
    {
        "cart_value": 900,
        "delivery_distance": 500,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 15, 15, 0, 0),
        "expected": 360,
    },
    {
        "cart_value": 900,
        "delivery_distance": 1560,
        "number_of_items": 2,
        "time": datetime.datetime(2024, 3, 15, 18, 39, 12),
        "expected": 600,
    },
    {
        "cart_value": 860,
        "delivery_distance": 3050,
        "number_of_items": 14,
        "time": datetime.datetime(2024, 3, 15, 18, 39, 12),
        "expected": 1500,
    },
]


@pytest.fixture(scope="module")
def fee_calculator():
    return FeeCalculator()


@pytest.mark.parametrize("distance_surcharge", cases_1)
def test_calculate_distance_surcharge(fee_calculator, distance_surcharge):
    delivery_distance = distance_surcharge.get("delivery_distance")
    expected_surcharge = distance_surcharge.get("expected")
    assert (
        fee_calculator._calculate_distance_surcharge(
            delivery_distance=delivery_distance
        )
        == expected_surcharge
    )


@pytest.mark.parametrize("cart_value_surcharge", cases_2)
def test_calculate_cart_value_surcharge(fee_calculator, cart_value_surcharge):
    cart_value = cart_value_surcharge.get("cart_value")
    expected_surcharge = cart_value_surcharge.get("expected")
    assert (
        fee_calculator._calculate_cart_value_surcharge(cart_value=cart_value)
        == expected_surcharge
    )


@pytest.mark.parametrize("item_surcharge", cases_3)
def test_calculate_number_of_items_surcharge(fee_calculator, item_surcharge):
    number_of_items = item_surcharge.get("number_of_items")
    expected_surcharge = item_surcharge.get("expected")
    assert (
        fee_calculator._calculate_item_surcharge(number_of_items=number_of_items)
        == expected_surcharge
    )


@pytest.mark.parametrize("limit_delivery_fee", cases_4)
def test_limit_delivery_fee(fee_calculator, limit_delivery_fee):
    delivery_fee = limit_delivery_fee.get("delivery_fee")
    expected_fee = limit_delivery_fee.get("expected")
    assert fee_calculator._limit_delivery_fee(delivery_fee=delivery_fee) == expected_fee


@pytest.mark.parametrize("is_free_delivery", cases_5)
def test_is_free_delivery(fee_calculator, is_free_delivery):
    cart_value = is_free_delivery.get("cart_value")
    expected_result = is_free_delivery.get("expected")
    assert fee_calculator._is_free_delivery(cart_value=cart_value) == expected_result


@pytest.mark.parametrize("calculate_rush_hour_surcharge", cases_6)
def test_calculate_rush_hour_surcharge(fee_calculator, calculate_rush_hour_surcharge):
    time = calculate_rush_hour_surcharge.get("time")
    delivery_fee = calculate_rush_hour_surcharge.get("delivery_fee")
    expected_surcharge = calculate_rush_hour_surcharge.get("expected")
    assert (
        fee_calculator._calculate_rush_hour_surcharge(
            time=time, delivery_fee=delivery_fee
        )
        == expected_surcharge
    )


@pytest.mark.parametrize("calculate_delivery_fee", cases_7)
def test_calculate_delivery_fee(fee_calculator, calculate_delivery_fee):
    delivery_distance = calculate_delivery_fee.get("delivery_distance")
    cart_value = calculate_delivery_fee.get("cart_value")
    number_of_items = calculate_delivery_fee.get("number_of_items")
    time = calculate_delivery_fee.get("time")
    inputs = {
        "delivery_distance": delivery_distance,
        "cart_value": cart_value,
        "number_of_items": number_of_items,
        "time": time,
    }
    expected_fee = calculate_delivery_fee.get("expected")
    assert fee_calculator.calculate_delivery_fee(**inputs) == expected_fee

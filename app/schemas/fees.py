import datetime

from pydantic import BaseModel, Field


class FeeCalculatorRequest(BaseModel):
    cart_value: int = Field(ge=0, description="Value of the shopping cart in cents")
    delivery_distance: int = Field(
        ge=0,
        description="The distance between the store and customer’s location in meters",
    )
    number_of_items: int = Field(
        ge=0, description="The number of items in the customer's shopping cart"
    )
    time: datetime.datetime = Field(description="Order time in UTC in ISO format")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cart_value": 790,
                    "delivery_distance": 2235,
                    "number_of_items": 4,
                    "time": "2024-01-15T13:00:00Z",
                }
            ]
        }
    }


class FeeCalculatorResponse(BaseModel):
    delivery_fee: int = Field(ge=0, description="Calculated delivery fee in cents")
    model_config = {"json_schema_extra": {"examples": [{"delivery_fee": 1500}]}}

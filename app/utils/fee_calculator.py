import math
import datetime


class Const:
    BASE_CART_VALUE = 1000

    BASE_SURCHARGE = 200
    BASE_DISTANCE = 1000
    ADDITIONAL_DISTANCE_SURCHARGE = 100
    ADDITIONAL_DISTANCE = 500

    ADDITIONAL_ITEM_LIMIT = 4
    ADDITIONAL_ITEM_SURCHARGE = 50
    BULK_ITEM_LIMIT = 12
    BULK_SURCHARGE = 120

    FEE_LIMIT = 1500

    CART_VALUE_FOR_FREE_DELIVERY = 20000

    RUSH_HOUR_ISOWEEKDAY = 5  # Friday
    RUSH_HOUR_START = datetime.time(15, 0, 0)
    RUSH_HOUR_END = datetime.time(19, 0, 0)
    RUSH_HOUR_MULTIPLIER = 1.2


class FeeCalculator:
    def __init__(self):
        pass

    def _calculate_cart_value_surcharge(self, cart_value: int) -> int:
        """Calculate cart value surcharge.

        If the cart value is less than 1000, the surcharge is the difference between the cart value and 1000. Otherwise, the surcharge is 0.
        For example, if the cart value is 890, the surcharge is 1000 - 890 = 110.

        Args:
            cart_value (int): Value of the shopping cart in cents

        Returns:
            int: The surcharge in cents
        """
        surcharge = 0
        if cart_value < Const.BASE_CART_VALUE:
            surcharge += Const.BASE_CART_VALUE - cart_value

        return surcharge

    def _calculate_distance_surcharge(self, delivery_distance: int) -> int:
        """Calculate distance surcharge.

        A delivery fee for the first 1000 meters (=1km) is 200. If the delivery distance is longer than that, 100 is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 100.
            - Example 1: If the delivery distance is 1499 meters, the delivery fee is: 200 base fee + 100 for the additional 500 m => 300
            - Example 2: If the delivery distance is 1500 meters, the delivery fee is: 200 base fee + 100 for the additional 500 m => 300
            - Example 3: If the delivery distance is 1501 meters, the delivery fee is: 200 base fee + 100 for the first 500 m + 100 for the second 500 m => 400

        Args:
            delivery_distance (int): The distance between the store and customer’s location in meters.

        Returns:
            int: The surcharge in cents
        """
        surcharge = Const.BASE_SURCHARGE
        if delivery_distance > Const.BASE_DISTANCE:
            surcharge += (
                math.ceil(
                    (delivery_distance - Const.BASE_DISTANCE)
                    / Const.ADDITIONAL_DISTANCE
                )
                * Const.ADDITIONAL_DISTANCE_SURCHARGE
            )

        return surcharge

    def _calculate_item_surcharge(self, number_of_items: int) -> int:
        """Calculate item surcharge.

        If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 120
            - Example 1: If the number of items is 4, no extra surcharge
            - Example 2: If the number of items is 5, 50 cents surcharge is added
            - Example 3: If the number of items is 10, 300 surcharge (6 x 50 cents) is added
            - Example 4: If the number of items is 13, 570 surcharge is added ((9 * 50 cents) + 120)
            - Example 5: If the number of items is 14, 620 surcharge is added ((10 * 50 cents) + 120)

        Args:
            number_of_items (int): The number of items in the customer's shopping cart

        Returns:
            int: The surcharge in cents
        """
        surcharge = 0

        if number_of_items > Const.ADDITIONAL_ITEM_LIMIT:
            surcharge += (
                number_of_items - Const.ADDITIONAL_ITEM_LIMIT
            ) * Const.ADDITIONAL_ITEM_SURCHARGE
            if number_of_items > Const.BULK_ITEM_LIMIT:
                surcharge += Const.BULK_SURCHARGE

        return surcharge

    def _limit_delivery_fee(self, delivery_fee: int) -> int:
        """Limit the delivery fee.

        If the delivery fee exceeds the limit, the function should return limit. Otherwise, the delivery fee should remain unchanged.

        Args:
            delivery_fee (int): The delivery fee in cents

        Returns:
            int: The delivery fee in cents
        """
        return min(delivery_fee, Const.FEE_LIMIT)

    def _is_free_delivery(self, cart_value: int) -> bool:
        """Check if the order is eligible for free delivery

        Args:
            cart_value (int): The value of the shopping cart in cents

        Returns:
            bool: True if the order is eligible for free delivery, False otherwise
        """
        if cart_value >= Const.CART_VALUE_FOR_FREE_DELIVERY:
            return True
        return False

    def _calculate_rush_hour_surcharge(
        self, time: datetime.date, delivery_fee: int
    ) -> int:
        """Calculate the rush hour surcharge to be added to the delivery fee.

        Args:
            time (_type_): Order time in UTC in ISO format

        Returns:
            int: The delivery fee in cents
        """
        surcharge = 0

        if time.isoweekday() == Const.RUSH_HOUR_ISOWEEKDAY:
            if Const.RUSH_HOUR_START <= time.time() < Const.RUSH_HOUR_END:
                surcharge = delivery_fee * Const.RUSH_HOUR_MULTIPLIER - delivery_fee

        return surcharge

    def calculate_delivery_fee(self, **inputs) -> int:
        """Calculate the delivery fee.

        Args:
            **inputs: Arbitrary keyword arguments

        Returns:
            int: The delivery fee in cents
        """
        cart_value = inputs.get("cart_value")
        delivery_distance = inputs.get("delivery_distance")
        number_of_items = inputs.get("number_of_items")
        time = inputs.get("time")

        delivery_fee = 0

        if self._is_free_delivery(cart_value):
            return 0

        delivery_fee += self._calculate_cart_value_surcharge(cart_value)
        delivery_fee += self._calculate_distance_surcharge(delivery_distance)
        delivery_fee += self._calculate_item_surcharge(number_of_items)
        delivery_fee += self._calculate_rush_hour_surcharge(time, delivery_fee)
        delivery_fee = self._limit_delivery_fee(delivery_fee)

        return delivery_fee

import json
from typing import List
from products import Product, get_product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict):
        """Load Cart object from a dictionary."""
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[
                get_product(product_id) for product_id in json.loads(data['contents'])
            ],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """Retrieve cart details for a user and return the list of products."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    products_list = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Replace eval with JSON for safety
            products_list.extend(get_product(product_id) for product_id in contents)
        except (json.JSONDecodeError, KeyError):
            # Handle cases where data is invalid
            continue
    return products_list


def add_to_cart(username: str, product_id: int):
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """Delete the user's cart."""
    dao.delete_cart(username)


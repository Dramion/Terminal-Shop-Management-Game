"""Module containing short object classes until they become larger."""


class Store:
    """Class for defining a store."""
    # Inv Dictionary format: {item_name: {"price": item_price, "quantity": item_quantity}, ...}
    inventory = {}

    def __init__(self, store_name, store_funds):
        self.name = store_name
        self.balance = store_funds

    def __repr__(self):
        return f"{self.name} has an inventory of {self.inventory}, and a total balance\
            of ${self.balance}."

    def add_inv(self, item):
        """Method for adding items to the store's inventory."""
        if isinstance(item) is Item and item.name in self.inventory:
            self.inventory[item.name]["quantity"] += item.dict[item.name]["quantity"]
        elif isinstance(item) is Item and item.name not in self.inventory:
            self.inventory.update(item.dict)
            self.inventory[item.name]["quantity"] = 1
        else:
            print(f"'{item}' is not a valid item.")


class Item:
    """Class for defining an item."""
    def __init__(self, item_name, item_price, item_quantity=1):
        self.name = item_name
        self.price = item_price
        self.dict = {self.name: {
            "price": self.price, "quantity": item_quantity}}

    def __repr__(self):
        return "f{self.name} costs ${self.price} per item."


class Customer:
    """Class for defining a customer."""
    cart = {}

    def __init__(self, customer_name, customer_balance, store):
        self.name = customer_name
        self.balance = customer_balance
        self.location = store

    def __repr__(self):
        return f"{self.name} has ${self.balance} in their wallet and {self.cart} in their cart."

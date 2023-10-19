"""Module containing object classes."""

class Store:
    """
    Class for defining a store.
    """
    # Inv Dictionary format: {item_name: {"price": item_price, "quantity": item_quantity}, ...}
    inventory = []
    customers = []

    def __init__(self, store_name, store_funds):
        self.name = store_name
        self.balance = store_funds

    def __repr__(self):
        return f"{self.name} has an inventory of {self.inventory}, and a total balance "\
            f"of ${self.balance}. \nCustomers are "

    def add_inv(self, item):
        """
        Method for adding items to the store's inventory.
        """
        if isinstance(item) is Item and item.name in self.inventory:
            self.inventory[item.name]["quantity"] += item.dict[item.name]["quantity"]
        elif isinstance(item) is Item and item.name not in self.inventory:
            self.inventory.append(item.dict)
            self.inventory[item.name]["quantity"] = 1
        else:
            print(f"'{item}' is not a valid item.")


class Item:
    """
    Class for defining an item.
    """
    def __init__(self, item_name, sell_price, purchase_price, item_quantity):
        self.name = item_name
        self.dict = {self.name: {"sell price": sell_price, "purchase price":
             purchase_price, "quantity": item_quantity}}

    def __repr__(self):
        return f'{self.dict[self.name]["quantity"]}-{self.name}: $\
{self.dict[self.name]["sell price"]}/item'


class Customer:
    """
    Class for defining a customer.
    """
    def __init__(self, customer_name, customer_balance):
        self.name = customer_name
        self.balance = customer_balance

    def __repr__(self):
        return f"{self.name} has ${self.balance} in their wallet."

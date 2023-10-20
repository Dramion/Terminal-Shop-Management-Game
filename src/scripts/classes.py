"""Module containing object classes."""
import json
import random

class Item:
    """
    Class for defining an item.
    
    Args:
    -----
        - item_name (str): string of the item's name.
        - sell_price (int): price for which the player can sell each item.
        - purchase_price (int): price for which the player can buy the item for their store.
        - item_quantity (int): how many of the item exists in the store. Might change or be 
        contained somewhere else.
    """
    def __init__(self, item_name=str, sell_price=int, purchase_price=int, item_quantity=int):
        self.name = item_name
        self.dict = {self.name: {"sell price": sell_price, "purchase price":
             purchase_price, "quantity": item_quantity}}

    def __repr__(self):
        return f'{self.dict[self.name]["quantity"]}-{self.name}: $\
{self.dict[self.name]["sell price"]}/item'

class Customer:
    """
    Class for defining a customer.
    
    Args:
    -----
        - customer_name (str): string of the customer's first and last name.
        - customer_balance (float): float of the customer's balance.
    """
    def __init__(self, customer_name=str, customer_balance=int):
        self.name = customer_name
        self.balance = customer_balance

    def __repr__(self):
        return f"{self.name} has ${self.balance} in their wallet."

class Store:
    """
    Class for defining a store.
    
    Args:
    -----
        - store_name (str): string of the store's name.
        - store_funds (int): amount of money the store has.
    """
    inventory = []
    """Inv List format: [{item_name: {"price": item_price, "quantity": item_quantity}}, {...}}"""
    customers = []

    def __init__(self, store_name=str, store_funds=int):
        self.name = store_name
        self.balance = store_funds

    def __repr__(self):
        return f"{self.name} has an inventory of {self.inventory}, and a total balance "\
            f"of ${self.balance}. \nCustomers are "

    def add_item(self, item=Item):
        """
        Method for adding items to the store's inventory.
        
        Args:
        -----
            - item (Item): class Item instance to be added to the store's inventory list.
        """
        if isinstance(item) is Item and item.name in self.inventory:
            self.inventory[item.name]["quantity"] += item.dict[item.name]["quantity"]
        elif isinstance(item) is Item and item.name not in self.inventory:
            self.inventory.append(item.dict)
            self.inventory[item.name]["quantity"] = 1
        else:
            print(f"'{item}' is not a valid item.")

    def new_customer(self) -> Customer:
        """
        Function to create a new customer using random numbers to pick random first and last names 
        from the names.json file and create a random balance between $3.50 and $9.00.
        
        Returns:
        --------
            Instance of the class Customer(customer_name = cust_name, customer_balance = random 
            int between 350 and 900 divided by 100 to make the balance between 3.50 and 9.00).
        """
        # Creates variable, names_dict(dict). containing the contents of the names.json file.
        with open('/workspaces/codecadproj/src/files/names.json', 'r', encoding='utf-8') as file:
            names_dict = json.load(file)
        # Creates variable, cust_name(str). Uses randint() to get a number between 0 and the
        # length of the "first names" & "last names" lists, subtracts one, and pulls the first/last
        # name from it's respective list.
        cust_name = (
            f'{names_dict["first names"][random.randint(0, len(names_dict["first names"])) - 1]} '\
            f'{names_dict["last names"][random.randint(0, len(names_dict["last names"])) - 1]}')

        return Customer(cust_name, random.randint(350, 900) / 100)

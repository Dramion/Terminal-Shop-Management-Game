"""
Module containing object classes.

This work falls under the GNU General Public License v3.0
See https://github.com/Dramion/Codecademy-Terminal-Py-Game/blob/Testing/LICENSE 
for more information.
"""
import json
import random
import curses


#TODO Remove dictionaries where possible and assign values to internal class vars.
class Item:
    """
    Class for defining an item.
    
    ### Args:
        - item_name (str): string of the item's name.
        - sell_price (int): price for which the player can sell each item.
        - purchase_price (int): price for which the player can buy the item for their store.
        - item_quantity (int): how many of the item exists in the store. Might change or be 
        contained somewhere else.
    """
    def __init__(self, item_name:str, sell_price:int, purchase_price:int, item_quantity:int):
        self.name = item_name
        self.dict = {self.name: {"sell price": sell_price, "purchase price": purchase_price,
                                 "quantity": item_quantity, "name": item_name}}

    def __repr__(self):
        return f'{self.dict["quantity"]}-{self.name}: $'\
            f'{self.dict["sell price"]}/item'

class Customer:
    """
    Class for defining a customer.
    
    ### Args:
        - customer_name (str): string of the customer's first and last name.
        - customer_balance (float): float of the customer's balance.
    """
    def __init__(self, customer_name:str, customer_balance:int):
        self.name = customer_name
        self.dict = {customer_name: {"bal": customer_balance, "inv": ""}}

    def __repr__(self):
        return f"{self.dict[self.name]} has ${self.dict[self.name]['bal']} in their wallet."

class Store:
    """
    Class for defining a store.
    
    ### Args:
        - store_name (str): string of the store's name.
        - store_funds (int): amount of money the store has.
    """
    inventory = {}
    """
    Inv Dict format: 
        {item_name: {"sell price": sell_price, "purchase price": purchase_price, "quantity":
        item_quantity}}, {...}}
    """
    customers = {}

    def __init__(self, store_name:str, store_funds:int):
        self.name = store_name
        self.balance = store_funds

    def __repr__(self):
        return f"{self.name} has an inventory of {self.inventory}, and a total balance "\
            f"of ${self.balance}. \nCustomers are "

    def total_quantity(self) -> int:
        """
        Calculates the total number of all items contained in the store's inventory.

        Returns:
        -------
            - total (int): The total numerical stock of the store.
        """
        total = 0
        for item in self.inventory.items():
            total += item[1]["quantity"]
        return total

    def add_item(self, item:Item) -> None:
        """
        Method for adding items to the store's inventory.
        
        Currently has the functionality of adding new items that don't yet exist, maybe can
        implement player made items? In the menu?
        
        ### Args:
            - item (Item): class Item instance to be added to the store's inventory list.
        """
        # If item arg is of type Item and is in the inventory Dict, add the item arg's "quantity"
        # to the Inventory Dict item's "quantity".
        if isinstance(item) is Item and item.name in self.inventory:
            self.inventory[item.name]["quantity"] += item.dict[item.name]["quantity"]
        # If item arg is of type Item and is not in the inventory Dict, add the item arg to the
        # inventory Dict.
        elif isinstance(item) is Item and item.name not in self.inventory:
            self.inventory.update(item.dict)
        else:
            print(f"'{item}' is not a valid item.")

    def new_customer(self) -> None:
        """
        Function to create a new customer using random numbers to pick random first and last names 
        from the names.json file and create a random balance between $3.50 and $9.00. Appends 
        created customer to the customers list.
        """
        # Creates variable, names_dict(dict). containing the contents of the names.json file.
        with open('src/files/lists.json', 'r', encoding='utf-8') as file:
            lists_dict = json.load(file)
        # Creates variable, cust_name(str). Uses randint() to get a number between 0 and the
        # length of the "first names" & "last names" lists, subtracts one, and pulls the first/last
        # name from it's respective list.
        cust_name = (
            f'{lists_dict["first names"][random.randint(1, len(lists_dict["first names"])) - 1]} '\
            f'{lists_dict["last names"][random.randint(1, len(lists_dict["last names"])) - 1]}')

        self.customers.update(Customer(cust_name, random.randint(350, 900)).dict)
        item_num_dict = {}
        num = 1
        done = False
        for item in self.inventory:
            item_num_dict.update({num: item})
            num += 1
        while not done:
            random_item = self.inventory[item_num_dict[random.randint(1,4)]]
            if random_item["quantity"] > 0:
                self.customers[cust_name]["inv"] = random_item
                random_item["quantity"] -= 1
                done = True
        return cust_name

class SelScene:
    """
    Creates a selectable scene at the provided window's y position which is also an arguement.
    
    ### Args:
        - y (int): Y position on the provided window.
        - spacing (int): How many lines between each selection.
        - sel_dict (dict): The dictionary containing the parameters for the scene.
        - win (curses.window): Window for the scene to be written on.
    """
    def __init__(self, y:int, spacing:int, sel_dict:dict, win:curses.window):
        self.y = y
        self.spacing = spacing
        self.win = win
        self.dict = sel_dict

    def scene_builder(self, selected:str):
        """
        Updates the currently selected option based off of the only arguement provided.

        ### Args:
            - selected (str): The key from the scene's dictionary that determines which option this
                function displays as selected.
        """
        curr_y = self.y
        for sel in self.dict["selections"]:
            sel_txt = self.dict["selections"][sel]["text"]
            if self.dict["center"] is True:
                scene_x = self.win.getmaxyx()[1] // 2 - len(sel_txt) // 2
            else:
                scene_x = self.dict["x"]
            if selected == sel:
                self.win.addstr(curr_y, scene_x, sel_txt,
                                curses.A_REVERSE)
                curr_y = curr_y + self.spacing + 1
            elif not selected == sel:
                self.win.addstr(curr_y, scene_x, sel_txt)
                curr_y = curr_y + self.spacing + 1
        self.win.refresh()

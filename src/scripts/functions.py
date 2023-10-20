"""Module containing functions."""
import sys
import os
from .classes import Item, Store # pylint: disable=relative-beyond-top-level

def start() -> Store:
    """
    Function used to contain the user inputs for game setup.
    
    Returns:
    --------
        - store (Store): An instance of the class Store(store_name = result of user input, 
        store_funds = 30)
    """
    sponge = Item("Sponge", 3.50, 2.20, 0)
    soap = Item("Soap", 4.38, 3.08, 0)
    brush = Item("Brush", 6.20, 4.90, 0)
    milk = Item("Milk", 8.10, 6.80, 0)
    os.system('cls||clear')
    start_in = input("For this game, type what is prompted and press enter to proceed. Are you"\
        "ready to begin?\nPress Y/N: ")
    if start_in == "Y" or start_in == "y":
        pass
    elif start_in == "N" or start_in == "n":
        sys.exit()

    store = Store(
        input("What would you like the name of your store to be?\n").capitalize(), 30)
    for item in [sponge, soap, brush, milk]:
        store.inventory.append(item)

    return store

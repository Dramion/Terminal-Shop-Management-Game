"""Module containing functions."""
import sys
import os
import json
import random
from .classes import Item, Store, Customer #pylint: disable=relative-beyond-top-level

def start():
    """
    Function used to contain the user inputs for game setup.
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

def new_customer():
    """
    Function to create a new customer using the rand_name function and a random balance 
    between $3.50 and $9.00.
    """
    return Customer(rand_name(), random.randint(350, 900) / 100)

def rand_name():
    """
    Function that generates a random name from two lists contained in the names json file. 
    """
    with open('/workspaces/codecadproj/src/files/names.json', 'r', encoding='utf-8') as file:
        names_dict = json.load(file)
    return f'{names_dict["first names"][random.randint(0, len(names_dict["first names"])) - 1]} '\
        f'{names_dict["last names"][random.randint(0, len(names_dict["last names"])) - 1]}'

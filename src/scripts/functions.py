"""Module containing functions."""
import sys
import os
import random
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

    start_input()

    store = Store(
        input("What would you like the name of your store to be?\n").capitalize(), 30)
    for item in [sponge, soap, brush, milk]:
        store.inventory.update({item.name: item})

    return store

def start_input() -> None:
    """
    Function that will only accept a 'Y', "y", "N" or "n". Will loop until a valid input is 
    provided.
    """
    first_message = "For this game, type what is prompted and press enter to proceed. Every time "\
        "you purchase items marks the end of the turn. \nYou may only buy one type of item and up "\
        "to 10 of that item each turn. Are you ready to begin?\nPress Y/N: "
    invalid_input = "Did you mean to type Y/N? "
    start_in_txt = first_message
    valid_in = False
    while not valid_in:
        start_in = input(start_in_txt)
        if start_in == "Y" or start_in == "y":
            valid_in = True
        elif start_in == "N" or start_in == "n":
            sys.exit()
        else:
            start_in_txt = invalid_input

def next_turn(store = Store) -> None:
    """
    Function that starts the next turn. Currently adds a random number of customers between 0 and
    10 after emptying all customers from previous turn. TODO: Handle the customer purchases before
    removing them from the customers list.
    
    Args:
    -----
        - store (Store): Instance of the class Store, needed for accessing the store's customers.
    """
    store.customers = []
    for _ in range(random.randint(0, 10)):
        store.new_customer()

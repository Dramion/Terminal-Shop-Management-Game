"""
Module containing functions.

This work falls under the GNU General Public License v3.0
See https://github.com/Dramion/Codecademy-Terminal-Py-Game/blob/Testing/LICENSE
for more information.
"""
import random
import curses
import json
import os
from src.scripts.classes import Item, Store, SelScene

def menu_input(win:curses.window, sel_dict:dict, scene:SelScene, screen:curses.window) -> str:
    """
    Function that handles all input within menus.  Will loop until a valid input is provided.
    
    ### Args:
        - win (curses.window): Window that this function is called inside of.
        - sel_dict (dict): Dictionary containing all selection options.
            - Format: {"selections": {optName: {"action": func or bool, "input": [strings of
                possible inputs], "scene": func that reflects the selection inside the win}}}
        - screen (curses._CursesWindow, optional): The screen container.
    """
    cont = False
    # List of the name of all selections in the "selections" dict of sel_dict.
    sel_list = list(sel_dict["selections"])
    # List of all possible inputs.
    all_poss_in = ["\n", "KEY_UP", "KEY_DOWN"]
    # List of possible inputs introduced by the provided dict.
    poss_in = []
    # curr_sel will always start the func at the first key in the "selections" dict.
    curr_sel = sel_list[0]
    # Add all inputs from the each selection's "input" list to poss_in.
    for sel in sel_dict["selections"]:
        if "input" in sel_dict["selections"][sel]:
            for sel_input in sel_dict["selections"][sel]["input"]:
                poss_in.append(sel_input)
    def find_sel(up_down:str, curr_sel:str):
        """
        Updates the scene to display the newly selected option.

        ### Args:
            - up_down (str): Which key of "KEY_UP" and "KEY_DOWN" was pressed.
            - curr_sel (str): Which option from the menu is currently selected.

        Returns:
        -------
            - curr_sel: The option which is now selected after the up or down key was pressed.
        """
        if up_down == "KEY_DOWN" and sel_list.index(curr_sel) < len(sel_list)-1:
            curr_sel = sel_list[sel_list.index(curr_sel) + 1]
            scene.scene_builder(curr_sel)
        elif up_down == "KEY_DOWN" and sel_list.index(curr_sel) == len(sel_list)-1:
            curr_sel = sel_list[0]
            scene.scene_builder(curr_sel)
        elif up_down == "KEY_UP" and sel_list.index(curr_sel) > 0:
            curr_sel = sel_list[sel_list.index(curr_sel) - 1]
            scene.scene_builder(curr_sel)
        elif up_down == "KEY_UP" and sel_list.index(curr_sel) == 0:
            curr_sel = sel_list[len(sel_list)-1]
            scene.scene_builder(curr_sel)
        return curr_sel
    # While loop to test the key pressed for a valid input.
    while not cont:
        scr_input = screen.getkey()
        if scr_input in poss_in and sel_dict["arrow only"] is False:
            for selection in sel_dict["selections"]:
                if scr_input in sel_dict["selections"][selection]["input"]:
                    if isinstance(sel_dict["selections"][selection]["action"], bool):
                        cont = sel_dict["selections"][selection]["action"]
                    else:
                        sel_dict["selections"][selection]["action"]()
        elif scr_input == "KEY_UP" or scr_input == "KEY_DOWN":
            curr_sel = find_sel(scr_input, curr_sel)
        elif scr_input == "\n":
            if isinstance(sel_dict["selections"][curr_sel]["action"], bool):
                cont = sel_dict["selections"][curr_sel]["action"]
            elif isinstance(sel_dict["selections"][curr_sel]["action"], str):
                return sel_dict["selections"][curr_sel]["action"]
            else:
                if len(sel_dict["selections"][curr_sel]["args"]) > 0:
                    sel_dict["selections"][curr_sel]["action"](*sel_dict["selections"][curr_sel]
                        ["args"])
                else:
                    sel_dict["selections"][curr_sel]["action"]()
                cont = True
        elif scr_input not in all_poss_in:
            win.addstr(11, win.getmaxyx()[1] // 2 - 54 // 2,
                       "Please press Up/Down/Enter or a letter in Parentheses.",
                       curses.color_pair(1))
            win.refresh()

def next_turn(store:Store) -> None:
    """
    Function that starts the next turn. Clears the customers in the store after removing the items
    being bought by each customer from the store inventory and adding the item's price to the store
    balance. Creates a random number of customers between 0 and the total store stock up to 11. 
    
    Args:
    -----
        - store (Store): Instance of the class Store, needed for accessing the store's customers\
            and inventory.
    """
    custs = store.customers
    num = 0
    if store.total_quantity >= 11:
        num = 11
    elif store.total_quantity < 11:
        num = store.total_quantity
    for customer in custs:
        if store.inventory[custs[customer]["inv"]]["quantity"] > 0:
            store.inventory[custs[customer]["inv"]]["quantity"] -= 1
            store.balance += store.inventory[custs[customer]["inv"]]["sell price"]
    store.customers.clear()
    for _ in range(random.randint(0, num)):
        store.new_customer()

def live_getstr(y:int, x:int, n:int, win:curses.window, screen:curses.window) -> str:
    """
    An improved version of getstr() that updates the window with each key.

    ### Args:
        - y (int): Row of the input space.
        - x (int): Starting column of the input space.
        - n (int): Length of the input. x + n must be less than the lenght of win.
        - win (curses.window): Window containing the input space.

    Returns:
    -------
        - output (str): The result of the user's input after pressing enter.
    """
    input_done = False
    cursor_pos = x
    output = ""
    with open('src/files/lists.json', 'r', encoding='utf-8') as file:
        lists_dict = json.load(file)

    while not input_done:
        key = screen.getkey()
        if cursor_pos - x < n and not key in ["KEY_BACKSPACE", "\n"]:
            if (key in lists_dict["alphabet upper"] or
                  key in lists_dict["alphabet lower"] or
                  key == " "):
                output += key
                win.addstr(y, cursor_pos, key)
                win.refresh()
                cursor_pos += 1
        elif key == "\n":
            input_done = True
        elif key == "KEY_BACKSPACE" and not cursor_pos == x:
            output = output[:-1]
            cursor_pos -= 1
            win.addstr(y, cursor_pos, " ")
            win.refresh()
    return output

def save_load(sl:str, json_f="", store=None):
    """
    Used for saving/loading games.

    Args:
        - sl (str): Variable that contains whether "s"(save) or "l"(load) was passed.
        - json_f (str, optional): The full "name.json" str . Defaults to "".
        - store (Store, optional): Store object passed when attempting to save. Defaults to None.

    Returns:
        - load_store: Store returned when loading a file. No return when saving.
    """
    if not "saves" in os.listdir("/"):
        pass
    else:
        os.mkdir("saves")
    if sl == "s":
        w_dict = {store.name:{"bal":store.balance, "customers":store.customers,
                              "inv": store.inventory}}
        #if f'{store.name}.json' in os.listdir("src/files"):
        with open(f'saves/{store.name}.json', 'w', encoding='utf-8') as file:
            json.dump(w_dict, file, indent=4)
    elif sl == "l":
        with open(f'saves/{json_f}', 'r', encoding='utf-8') as file:
            load_dict = json.load(file)
        load_store = Store(json_f[:-5], load_dict[json_f[:-5]]["bal"])
        load_store.inventory = load_dict[json_f[:-5]]["inv"]
        load_store.customers = load_dict[json_f[:-5]]["customers"]
        return load_store

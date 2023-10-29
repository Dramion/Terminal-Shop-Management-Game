"""
Module containing curses window initializers.

This work falls under the GNU General Public License v3.0
See https://github.com/Dramion/Codecademy-Terminal-Py-Game/blob/Testing/LICENSE 
for more information.
"""
import curses
import sys
import os
from src.scripts.functions import next_turn, menu_input, live_getstr, save_load
from src.scripts.classes import Item, SelScene, Store

stdscr = curses.initscr()

player_store:Store = None

sponge = Item("Sponge", 350, 220, 0)
soap = Item("Soap", 438, 308, 2)
brush = Item("Brush", 620, 490, 0)
milk = Item("Milk", 810, 680, 0)
def screen_controller(screen=stdscr):
    """
    Initializes the main screen.

    ### Args:
        - screen (curses.window, optional): Screen object. Defaults to stdscr.
    """
    screen.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(0)
    screen.refresh()
    main_menu()


def start_menu(start_menu_win=curses.newwin(20, 82, 1, 3)):
    """
    Initializes a start menu with a disclaimer, not currently in use.
    """
    yn_dict = {"arrow only":False, "center":True,"selections":
        {"yes":{"text":"(Y)es", "action": True, "input":["Y", "y"]},
         "no":{"text":"(N)o", "action":sys.exit, "input":["N", "n"]}}}
    start_scene = SelScene(8, 1, yn_dict, start_menu_win)
    start_menu_win.addstr(1, 1,
        " For this game, press the key marked in parentheses to proceed. Every time you\n"\
        " purchase items marks the end of the turn. You may only buy one type of item and\n"\
        "                         up to 10 of that item each turn.")
    start_menu_win.addstr(6, start_menu_win.getmaxyx()[1] // 2 - 23 // 2, "Are you ready to begin?")
    start_scene.scene_builder("yes")
    start_menu_win.box()
    start_menu_win.refresh()
    menu_input(start_menu_win, yn_dict, start_scene, stdscr)
    start_menu_win.clear()
    start_menu_win.refresh()
    del start_menu_win

def main_menu(main_menu_win=curses.newwin(20, 82, 1, 3)):
    """
    Initializes the main menu, this can be returned to in order to save, load, create new, or exit\
        the game. Not currently able to be returned to.

    ### Args:
        - main_menu_win (curses.window, optional): Main menu window. Defaults to curses.newwin(10,\
            50, 1, 3).
    """
    main_menu_dict = {"arrow only":False, "center":True, "selections":
        {"new": {"text":"(N)ew", "action": "new", "args":[], "input":["N", "n"]},
         "load":{"text":"(L)oad", "action": "load", "args":[], "input": ["L", "l"]},
         "exit": {"text":"E(x)it", "action":sys.exit, "args":[], "input":["X", "x"]}}}
    main_menu_scene = SelScene(3, 1, main_menu_dict, main_menu_win)
    main_menu_win.addstr(1, main_menu_win.getmaxyx()[1] // 2 - 9 // 2, "Main Menu", curses.A_BOLD)
    main_menu_scene.scene_builder("new")
    main_menu_win.box()
    main_menu_win.refresh()
    main_in = menu_input(main_menu_win, main_menu_dict, main_menu_scene, stdscr)
    del main_menu_win
    if main_in == "load":
        load_menu()
    elif main_in == "new":
        new_game_menu()

def new_game_menu(new_game_win=curses.newwin(20, 82, 1, 3)):
    """
    Menu for creating a new shop, currently only used for creating a shop and immediately saving \
        it. All testing is being done using the load option in the Main Menu Window.

    ### Args:
        - game_menu_win (curses.window, optional): Game menu window. Defaults to curses.newwin(20,\
            82, 1, 3).
    """
    global player_store #pylint: disable=global-statement
    new_game_win.box()
    new_game_win.addstr(6, 82 // 2 - 29 // 2, "Please type your shop's name:")
    new_game_win.refresh()
    store_name = live_getstr(8, 82 // 2 - 10 // 2, 10, new_game_win, stdscr)
    player_store = Store(store_name.capitalize(), 30)
    for item in [sponge, soap, brush, milk]:
        player_store.inventory.update(item.dict)
    for _ in range(player_store.total_quantity()):
        player_store.new_customer()
    del new_game_win
    game_window()

def load_menu(load_menu_win=curses.newwin(20, 82, 1, 3)):
    """
    Pulls all files located in the "saves" directory. Then displays them in a selectable list for\
        the player to choose from using the arrow keys.

    ### Args:
        - load_menu_win (curses.window, optional): Load menu window. Defaults to curses.newwin(20,\
            82, 1, 3).
    """
    load_menu_win.box()
    load_menu_dict = {"selections":{},"x":5, "arrow only": True, "center": False}
    load_menu_scene = SelScene(2,0,load_menu_dict,load_menu_win)
    load_menu_win.addstr(1,1,"Saves: ")
    saves_list = os.listdir("saves")
    if len(saves_list) > 0:
        for save in saves_list:
            load_menu_dict["selections"].update({save[:-5]:{"text":save, "action":save}})
        load_menu_scene.scene_builder(saves_list[0][:-5])
        chosen_file = menu_input(load_menu_win,load_menu_dict,load_menu_scene,stdscr)
        del load_menu_win
        global player_store #pylint: disable=global-statement
        player_store = save_load("l", None, chosen_file)
        save_load("l", None, chosen_file)
        game_window()
    else:
        load_menu_win.addstr(2, 5, "Sorry, but you currently do not have any saves. "\
            "Press enter to return.")
        load_menu_win.refresh()
        cont = False
        while cont is False:
            if stdscr.getkey() == "\n":
                cont = True
        del load_menu_win
        main_menu()

def game_window(game_win=curses.newwin(20, 82, 1, 3)):
    """
    Window handling the actual gameplay.

    ### Args:
        - game_win (curses.window, optional): Game window. Defaults to curses.newwin(20, \
            82, 1, 3).
    """
    def inv_win_update():
        """
        Updates the inventory window to reflect any changes in store stock.
        """
        item_pos = 0
        column_2 = 0
        inv = player_store.inventory
        for item in player_store.inventory:
            item_str = f"{inv[item]['name']}(${inv[item]['sell price'] / 100}):"\
                       f"{inv[item]['quantity']}"
            if item_pos == 0:
                inv_win.addstr(1, len(inv_str) + 2, item_str)
                inv_win.addstr(1, len(inv_str) + 2 + item_str.find("$"),
                               f"${inv[item]['sell price'] / 100}", curses.color_pair(2))
                item_pos += 1
                column_2 = len(inv_str) + len(item_str) + 8
            elif item_pos == 1:
                inv_win.addstr(3, len(inv_str) + 2, item_str)
                inv_win.addstr(3, len(inv_str) + 2 + item_str.find("$"),
                               f"${inv[item]['sell price'] / 100}", curses.color_pair(2))
                item_pos += 1
            elif item_pos == 2:
                inv_win.addstr(1, column_2, item_str)
                inv_win.addstr(1, column_2 + item_str.find("$"),
                               f"${inv[item]['sell price'] / 100}", curses.color_pair(2))
                item_pos += 1
            elif item_pos == 3:
                inv_win.addstr(3, column_2, item_str)
                inv_win.addstr(3, column_2 + item_str.find("$"),
                               f"${inv[item]['sell price'] / 100}", curses.color_pair(2))
                item_pos += 1
        inv_win.refresh()

    def store_win_update():
        """
        Updates the store window with the player's new balance after the previous turn and any new
        customers.
        """
        cursor_y = 0
        custs = player_store.customers
        store_win.clear()
        for customer in player_store.customers:
            customer_str = f"{customer}(${custs[customer]['bal'] / 100}): "\
                f"{custs[customer]['inv']['name']}"
            if cursor_y < 12:
                store_win.addstr(store_win.getmaxyx()[0] // 2 - len(custs) // 2 + cursor_y,
                                 store_win.getmaxyx()[1] // 2 - len(customer_str) // 2,
                                 customer_str)
                cursor_y += 1
        store_win.addstr(1, 1, "Store Balance: ")
        store_win.addstr(1, 16, f"${player_store.balance / 100}", curses.color_pair(2))
        store_win.box()
        store_win.refresh()

    def store_win_purchase():
        """
        Handles the store purchases inside the store window.
        """
        def purchase_item():
            """
            Receives player's selection from a needlessly dynamic list of items available for 
            purchase.

            Returns:
            -------
                - dict: A dictionary of the item to purchase pulled from the player store's 
                inventory.
            """
            store_win.clear()
            store_win.box()
            inv = player_store.inventory
            purchase_dict = {"arrow only":False, "center":True, "selections":{}}
            sel_dict:dict = purchase_dict["selections"]
            for item in inv:
                sel_dict.update({item: {"text": item, "action": item, "args": [], "input": []}})
            purchase_scene = SelScene(4, 1, purchase_dict, store_win)
            purchase_scene.scene_builder(list(inv)[0])
            return player_store.inventory[menu_input(store_win, purchase_dict,
                                                       purchase_scene, stdscr)]

        def purchase_amount(item_to_purchase):
            """
            Takes a number between 0 and 99 from the player to determine how many of 
            item_to_purchase shall be purchased.

            ### Args:
                - item_to_purchase (dict): The dictionary of the item determined by purchase_item().

            Returns:
            -------
                - amount_purch (int): The number of the desired item to purchase as specified by the 
                player.
            """
            store_win.clear()
            store_win.addstr(1, 1, "Store Balance: ")
            store_win.addstr(6, store_win.getmaxyx()[1] // 2 - 19 // 2, "Amount to purchase:")
            store_win.addstr(1, 16, f"${player_store.balance / 100}", curses.color_pair(2))
            store_win.box()
            store_win.refresh()
            too_expensive = True
            while too_expensive is True:
                amount_purch = live_getstr(8, 30, 2, store_win, stdscr, True)
                if amount_purch.isnumeric():
                    if (int(amount_purch) * item_to_purchase["purchase price"] <=
                        player_store.balance):
                        too_expensive = False
                        confirmation_str = f"Confirm payment of $"\
                            f"{int(amount_purch) * item_to_purchase['purchase price'] / 100}"\
                            "? [Enter]"
                        store_win.addstr(10,
                                         store_win.getmaxyx()[1] // 2 - len(confirmation_str) // 2,
                                         confirmation_str, curses.color_pair(3))
                        store_win.refresh()
                        if stdscr.getkey() == "\n":
                            player_store.balance -= (int(amount_purch) *
                                                     item_to_purchase["purchase price"])
                            return int(amount_purch)

        purch_item = purchase_item()
        purch_amount = purchase_amount(purch_item)
        purch_item["quantity"] += purch_amount
        new_turn("next")

    def new_turn(start_next="start"):
        """
        The series of events that should take place at the start of a new turn.

        ### Args:
            - start_next (str, optional): _description_. Defaults to "start".
        """
        if start_next == "next":
            next_turn(player_store)
        inv_win.box()
        store_win.box()
        sel_win.box()
        inv_win.addstr(1, 1, inv_str)
        game_menu_dict = {"arrow only":False, "center":True, "selections":
            {"next": {"text":"(N)ext Turn", "action": store_win_purchase, "args":[],
                      "input":["N", "n"]},
            "skip": {"text":"S(k)ip Turn", "action": new_turn, "args":["next"],
                    "input": ["K", "k"]},
            "save": {"text": "(S)ave", "action": save_load, "args": ["s", new_turn, "",
                                                                     player_store],
                    "input": ["S", "s"]},
            "main": {"text":"Main Menu", "action": main_menu, "args":[], "input":[]}}}
        game_menu_scene = SelScene(2, 2, game_menu_dict, sel_win)
        game_menu_scene.scene_builder("next")
        inv_win_update()
        store_win_update()
        game_win.refresh()
        menu_input(sel_win, game_menu_dict, game_menu_scene, stdscr)

    inv_win = game_win.derwin(5, 82, 0, 0)
    store_win = game_win.derwin(15, 62, 5, 0)
    sel_win = game_win.derwin(15, 20, 5, 62)
    inv_str = f"{player_store.name} inventory:"
    new_turn()

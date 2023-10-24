"""Module containing curses window initializers."""
import curses
import sys
import os
from .functions import menu_input, live_getstr, save_load # pylint: disable=relative-beyond-top-level
from .classes import Item, SelScene, Store # pylint: disable=relative-beyond-top-level

stdscr = curses.initscr()
sponge = Item("Sponge", 3.50, 2.20, 0)
soap = Item("Soap", 4.38, 3.08, 0)
brush = Item("Brush", 6.20, 4.90, 0)
milk = Item("Milk", 8.10, 6.80, 0)
def screen_controller(screen=stdscr):
    """
    _summary_

    ### Args:
        screen (curses.window, optional): Screen object. Defaults to stdscr.
    """
    screen.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
    screen.refresh()
    main_in = main_menu()
    if main_in == "load":
        load_menu()
    elif main_in == "new":
        game_menu(main_in)


def start_menu(start_menu_win=curses.newwin(15, 82, 1, 3)):
    """
    Initiali
    
    Returns:
    -------
        - store (Store): An instance of the store class.
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

    """sponge = Item("Sponge", 3.50, 2.20, 0)
    soap = Item("Soap", 4.38, 3.08, 0)
    brush = Item("Brush", 6.20, 4.90, 0)
    milk = Item("Milk", 8.10, 6.80, 0)

    store = Store(store_name.capitalize(), 30)
    for item in [sponge, soap, brush, milk]:
        store.inventory.update({item.name: item})

    return store"""

def main_menu(menu_win=curses.newwin(15, 82, 1, 3)):
    """
    _summary_

    ### Args:
        - menu_win (curses.window, optional): _description_. Defaults to curses.newwin(10, 50, 1,\
            3).
    """
    main_menu_dict = {"arrow only":False, "center":True, "selections":
        {"new": {"text":"(N)ew", "action": "new", "args":[], "input":["N", "n"]},
         "load":{"text":"(L)oad", "action": "load", "args":[], "input": ["L", "l"]},
         "exit": {"text":"E(x)it", "action":sys.exit, "args":[], "input":["X", "x"]}}}
    main_menu_scene = SelScene(3, 1, main_menu_dict, menu_win)
    menu_win.addstr(1, menu_win.getmaxyx()[1] // 2 - 9 // 2, "Main Menu", curses.A_BOLD)
    main_menu_scene.scene_builder("new")
    menu_win.box()
    menu_win.refresh()
    func_out = menu_input(menu_win, main_menu_dict, main_menu_scene, stdscr)
    del menu_win
    return func_out
    #store_name = live_getstr(3, 14, 10, menu_win, stdscr)
    #store = Store(store_name.capitalize(), 30)
    #for item in [sponge, soap, brush, milk]:
        #store.inventory.update(item.dict)
    #store.new_customer()
    #save_load("s", store)

def game_menu(new_load="load", game_win=curses.newwin(15, 82, 1, 3)):
    game_win.box()
    if new_load == "new":
        game_win.addstr(6, 82 // 2 - 29 // 2, "Please type your shop's name:")
        game_win.refresh()
        shop_name = live_getstr(8, 82 // 2 - 10 // 2, 10, game_win, stdscr)

def load_menu(load_win=curses.newwin(15, 82, 1, 3)):
    load_win.box()
    load_menu_dict = {"selections":{},"x":5, "arrow only": True, "center": False}
    load_menu_scene = SelScene(2,0,load_menu_dict,load_win)
    load_win.addstr(1,1,"Saves: ")
    if len(os.listdir("saves")) > 0:
        for save in os.listdir("saves"):
            load_menu_dict["selections"].update({save[:-5]:{"text":save}})
        load_menu_scene.scene_builder(os.listdir("saves")[0])
        menu_input(load_win,load_menu_dict,load_menu_scene,stdscr)
    else:
        load_win.addstr(2, 5, "Sorry, but you currently do not have any saves.")
        load_win.refresh()

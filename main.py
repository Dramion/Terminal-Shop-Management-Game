"""Program initializer"""
from curses import wrapper
import src.scripts.functions as funcPy

if __name__ == "__main__":
    wrapper(funcPy.screen_controller)

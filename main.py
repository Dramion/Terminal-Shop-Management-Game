"""Program initializer"""
from curses import wrapper
from src.scripts.windows import screen_controller

if __name__ == "__main__":
    wrapper(screen_controller)

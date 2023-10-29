"""Program initializer

This work falls under the GNU General Public License v3.0
See https://github.com/Dramion/Codecademy-Terminal-Py-Game/blob/Testing/LICENSE 
for more information.
"""
from curses import wrapper
from src.scripts.windows import screen_controller

if __name__ == "__main__":
    wrapper(screen_controller)

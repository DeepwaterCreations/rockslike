"""This module is for the game's visual elements: Tiles"""
import curses

_max_color = 0
_registered_colors = {}

def get_color(foreground, background):
    """Initialize color pairs if necessary and return the curses color"""
    global _max_color
    # global _registered_colors
    if (foreground, background) in _registered_colors:
        c_id = _registered_colors[(foreground, background)]
    else:
        _max_color += 1
        c_id = _max_color
        curses.init_pair(c_id, foreground, background)
        _registered_colors[(foreground, background)] = c_id
    return curses.color_pair(c_id)


class Tile():
    """Holds char and color information for some game object's appearance"""

    def __init__(self, char, foreground=curses.COLOR_WHITE, background=curses.COLOR_BLACK):
        self.char = char
        self.color = get_color(foreground, background)

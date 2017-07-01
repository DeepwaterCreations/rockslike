"""This module is for the game's visual elements: Tiles"""
import curses

_max_color = 0
_registered_colors = {}

def get_color(foreground, background, bold):
    """Initialize color pairs if necessary and return the curses color"""
    global _max_color
    foreground = parse_color_name(foreground)
    background = parse_color_name(background)
    if (foreground, background) in _registered_colors:
        c_id = _registered_colors[(foreground, background)]
    else:
        _max_color += 1
        c_id = _max_color
        curses.init_pair(c_id, foreground, background)
        _registered_colors[(foreground, background)] = c_id
    color_pair = curses.color_pair(c_id)
    if bold:
        color_pair += curses.A_BOLD
    return color_pair

def parse_color_name(color_str):
    """Return a curses color matching the string, or raise an exception if the string has
    no match.
    """
    if color_str.upper() == "BLACK":
        return curses.COLOR_BLACK
    if color_str.upper() == "RED":
        return curses.COLOR_RED
    if color_str.upper() == "GREEN":
        return curses.COLOR_GREEN
    if color_str.upper() == "YELLOW":
        return curses.COLOR_YELLOW
    if color_str.upper() == "BLUE":
        return curses.COLOR_BLUE
    if color_str.upper() == "MAGENTA":
        return curses.COLOR_MAGENTA
    if color_str.upper() == "CYAN":
        return curses.COLOR_CYAN
    if color_str.upper() == "WHITE":
        return curses.COLOR_WHITE
    raise ValueError("Couldn't find color {0}".format(color_str))

class Tile():
    """Holds char and color information for some game object's appearance"""

    def __init__(self, char, foreground="WHITE", background="BLACK", bold=False):
        self.char = char
        self.color = get_color(foreground, background, bold)

"""A module for printing logging/debugging text to the screen in curses

Curses isn't very print-friendly, unfortunately.
"""

__dbg = {
        "debug_strings": [],
        "stdscr": None
        }

def init(stdscr):
    """Initialize the module"""
    __dbg["stdscr"] = stdscr

def add_debug_string(string):
    """Add a string to the list of debug strings that will be displayed"""
    __dbg["debug_strings"].append(string)

def flush_debug_text():
    """Display the queued debug text to the screen and clear the list"""
    y_offset = 0
    for s in __dbg["debug_strings"]:
        __dbg["stdscr"].addstr(y_offset, 1, s)
        y_offset += 1
    __dbg["debug_strings"] = []

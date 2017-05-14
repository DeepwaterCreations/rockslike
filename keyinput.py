"""A module for handling keyboard input"""
import events

def handle_key(key):
    if key in ["y", "7"]:
        events.trigger_event("player_move_nw")
    if key in ["KEY_UP", "k", "8"]:
        events.trigger_event("player_move_n")
    if key in ["u", "9"]:
        events.trigger_event("player_move_ne")
    if key in ["KEY_LEFT", "h", "4"]:
        events.trigger_event("player_move_w")
    if key in ["KEY_RIGHT", "l", "6"]:
        events.trigger_event("player_move_e")
    if key in ["b", "1"]:
        events.trigger_event("player_move_sw")
    if key in ["KEY_DOWN", "j", "2"]:
        events.trigger_event("player_move_s")
    if key in ["n", "3"]:
        events.trigger_event("player_move_se")

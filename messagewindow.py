"""A module for displaying in-game messages"""
import collections
import curses

import events
import debugoutput

class MessageWindow():
    """Displays messages in a curses window"""

    def __init__(self, window):
        self.window = window
        self._message_queue = collections.deque()
        self.more_messages_string = "==MORE=="

        events.listen_to_event("print_message", self.add_message)

    def add_message(self, text):
        """Add a message to the message queue"""
        self._message_queue.append(text)

    def display_messages(self):
        """Display all messages in the queue in FIFO order, pausing to wait for keystrokes
        after each one
        """
        #Can't use the 'for in' syntax, since we want to pop
        while len(self._message_queue) > 0:
            self.window.border()
            message = self._message_queue.popleft()
            self._display(message)
            self.window.getkey()
            self.window.clear()
        self.window.refresh()
    
    ## PRIVATE METHODS ##
    def _display(self, message):
        height, width = self.window.getmaxyx()
        #Account for border
        width -= 2
        height -= 2

        #Turn the message into an array of words, and reverse it so that
        #we can consume from the end
        message = message.split(' ')
        message.reverse()

        #Build a queue full of rows, where each row is a part of the message
        #that will fit horizontally in the window, and where the number of
        #rows is not greater than the window's height
        message_rows = collections.deque()
        while len(message_rows) < (height-1): #Leave space for a "==MORE==" message
            new_row = ""
            while len(message) > 0:
                #Put words into the current row's string
                #Break if putting another word in would overflow the width
                #Also break on a newline
                if len(new_row) + 1 + len(message[-1]) < width:
                    word = message.pop()
                    words = word.split('\n', 1)
                    new_row += " " + words[0]
                    if len(words) > 1:
                        for word in words[1:]:
                            message.append(word)
                        break
                elif new_row == "":
                    #Rather than choke forever on a string too long to print but too stubborn to die,
                    #if we haven't added any words at all this iteration, break the first word into 
                    #two words and try again.
                    stupid_long_word = message.pop()
                    first_part = stupid_long_word[:width-2] + '-'
                    second_part = stupid_long_word[width-2:]
                    message.append(second_part)
                    message.append(first_part)
                else:
                    break
            message_rows.append(new_row)

        #We should now have an array of strings, each of which represents a row of text
        #that will fit in the window. If there's any more of the message left, turn it into a new message
        #and push it back onto the top of the queue.
        if len(message) > 0:
            message.reverse()
            remaining_text = " ".join(message)
            self._message_queue.appendleft(remaining_text)

        #Put a "==MORE==" message at the bottom of the window if there are more messages
        if len(self._message_queue) > 0:
            message_rows.append(self.more_messages_string.center(width-1))

        #Print all the rows
        y = 1 #Start at 1 to make room for the border
        while len(message_rows) > 0:
            self.window.addstr(y, 1, message_rows.popleft())
            y += 1

"""
Helper functions for Sokoban game.
Provides utility functions for game logic.
"""

import sys

# Cross-platform single character input (no Enter required)
# Supports both WASD and arrow keys
if sys.platform == 'win32':
    import msvcrt
    
    def getch():
        """Get a single character from keyboard on Windows.
        Supports WASD and arrow keys.
        """
        key = msvcrt.getch()
        
        # Check for arrow keys (Windows sends \xe0 followed by direction)
        if key == b'\xe0':
            arrow = msvcrt.getch()
            if arrow == b'H':  # Up arrow
                return 'w'
            elif arrow == b'P':  # Down arrow
                return 's'
            elif arrow == b'K':  # Left arrow
                return 'a'
            elif arrow == b'M':  # Right arrow
                return 'd'
        
        # Regular key
        try:
            return key.decode('utf-8').lower()
        except (UnicodeDecodeError, AttributeError):
            return key.decode('latin-1').lower()
else:
    import termios
    import tty
    
    def getch():
        """Get a single character from keyboard on Unix/Mac.
        Supports WASD and arrow keys.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Check for arrow keys (Unix/Mac sends escape sequence)
            if ch == '\x1b':  # ESC character
                # Read the next two characters
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                
                # Arrow keys send: \x1b[A (up), \x1b[B (down), \x1b[C (right), \x1b[D (left)
                # Or: \x1bOA, \x1bOB, \x1bOC, \x1bOD (application mode)
                if ch2 == '[':
                    if ch3 == 'A':  # Up arrow
                        return 'w'
                    elif ch3 == 'B':  # Down arrow
                        return 's'
                    elif ch3 == 'C':  # Right arrow
                        return 'd'
                    elif ch3 == 'D':  # Left arrow
                        return 'a'
                elif ch2 == 'O':
                    if ch3 == 'A':  # Up arrow (application mode)
                        return 'w'
                    elif ch3 == 'B':  # Down arrow (application mode)
                        return 's'
                    elif ch3 == 'C':  # Right arrow (application mode)
                        return 'd'
                    elif ch3 == 'D':  # Left arrow (application mode)
                        return 'a'
                
                # If it's not an arrow key, return the ESC character
                return ch.lower()
            
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_player_position(board):
    """
    Find the player's current position on the board.

    Args:
        board: 2D list representing game state

    Returns:
        row, col: Player position (two values), or None if not found
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == '@' or board[row][col] == '+':
                return row, col
    return None


def is_win(board):
    """
    Check if all boxes are on target locations.

    Args:
        board: 2D list representing game state

    Returns:
        bool: True if level complete (no '$' symbols), False otherwise
    """
    for row in board:
        for cell in row:
            if cell == '$':  # Box not on target
                return False
    return True


def copy_board(board):
    """
    Create a deep copy of the board.

    Args:
        board: 2D list to copy

    Returns:
        2D list: Independent copy of the board
    """
    return [row[:] for row in board]


def count_boxes_on_targets(board):
    """
    Count how many boxes are currently on target locations.

    Args:
        board: 2D list representing game state

    Returns:
        int: Number of boxes on targets ('*' symbols)
    """
    count = 0
    for row in board:
        for cell in row:
            if cell == '*':
                count += 1
    return count


def count_total_targets(board):
    """
    Count total number of target locations in level.

    Args:
        board: 2D list representing game state

    Returns:
        int: Total targets ('.' and '*' symbols)
    """
    count = 0
    for row in board:
        for cell in row:
            if cell == '.' or cell == '*':
                count += 1
    return count


# BONUS #2: Level Select Mode - Input validation function
def validate_choice(prompt, min_choice, max_choice):
    """
    Validate user input for menu choices with error handling.
    Keeps asking until valid input is received.
    BONUS #2: Used for validating level number input in Level Select Mode
    
    Args:
        prompt: The message to display to the user
        min_choice: Minimum valid choice number
        max_choice: Maximum valid choice number
    
    Returns:
        int: The user's valid choice
    """
    while True:
        try:
            user_input = input(prompt)
            choice = int(user_input)
            if min_choice <= choice <= max_choice:
                return choice
            else:
                print(f"Please choose between {min_choice} and {max_choice}.")
                
        except ValueError:
            print("Please enter a valid number.")

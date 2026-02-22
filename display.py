"""
Display functions for Sokoban game.
Provides all rendering and display functionality.
"""

import os
import sys

# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Background colors
    BG_DARK_GRAY = '\033[100m'
    BG_BROWN = '\033[43m'


def get_display_char(cell):
    """
    Convert XSB format character to display character with color.
    
    Args:
        cell: Single character from XSB format ('#', ' ', '@', '$', '.', '*', '+')
        
    Returns:
        str: Colored Unicode character for display
    """
    # Check if terminal supports colors (basic check)
    supports_color = sys.stdout.isatty() and (sys.platform != 'win32' or os.getenv('TERM') != 'dumb')
    
    if not supports_color:
        # Fallback: Unicode symbols without colors
        mapping = {
            '#': '▓',
            ' ': ' ',
            '@': '☺',
            '$': '▦',
            '.': '○',
            '*': '▦',
            '+': '☺'
        }
        return mapping.get(cell, cell)
    
    # Color mapping with Unicode symbols
    if cell == '#':  # Wall
        return f"{Colors.GRAY}▓{Colors.RESET}"
    elif cell == ' ':  # Floor
        return ' '
    elif cell == '@':  # Player
        return f"{Colors.CYAN}{Colors.BOLD}☺{Colors.RESET}"
    elif cell == '$':  # Box
        return f"{Colors.YELLOW}▦{Colors.RESET}"
    elif cell == '.':  # Target
        return f"{Colors.RED}○{Colors.RESET}"
    elif cell == '*':  # Box on target
        return f"{Colors.GREEN}{Colors.BOLD}▦{Colors.RESET}"
    elif cell == '+':  # Player on target
        return f"{Colors.GREEN}{Colors.BOLD}☺{Colors.RESET}"
    else:
        return cell


def clear_screen():
    """
    Clear the terminal screen for clean display.
    Works on both Windows and Unix-based systems.
    """
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def print_board(board):
    """
    Display the game board with borders and formatting.
    Uses Unicode symbols and colors for better visualization.

    Args:
        board: 2D list of strings representing the game state
    """
    print("=" * (len(board[0]) * 2 + 2))
    for row in board:
        print("|", end="")
        for cell in row:
            display_char = get_display_char(cell)
            print(f" {display_char}", end="")
        print(" |")
    print("=" * (len(board[0]) * 2 + 2))


def print_level_header(level_number, moves):
    """
    Display level information at the top of the screen.

    Args:
        level_number: Current level (0-50, displayed as Level 0-50)
        moves: Number of moves taken
    """
    print(f"\n{'='*50}")
    print(f"Level {level_number} | Moves: {moves}")
    print(f"{'='*50}\n")


def print_win_message(level_number, moves):
    """
    Display victory message when level is completed.

    Args:
        level_number: Completed level number (0-50, displayed as Level 0-50)
        moves: Total moves taken
    """
    print("\n" + "="*50)
    print("🎉 LEVEL COMPLETE! 🎉".center(50))
    print("="*50)
    print(f"Level {level_number} completed in {moves} moves!")
    print("="*50 + "\n")


def print_controls():
    """
    Display game controls and instructions.
    """
    print("\nControls:")
    print("  ↑↓←→ or W/A/S/D - Move player")
    print("  R - Restart level")
    print("  Q - Quit game")
    print()


# BONUS #2: Level Select Mode - Menu display functions
def print_main_menu():
    """
    Display the main menu with game mode options.
    BONUS #2: Main menu for selecting game mode
    """
    clear_screen()
    print("="*50)
    print("SOKOBAN PUZZLE GAME".center(50))
    print("="*50)
    print("\nSelect a game mode:")
    print("  1. Progression Mode (Levels 0-4)")
    print("  2. Level Select Mode (Any level 0-50)")
    print("  Q. Quit")
    print("\n" + "="*50)


def print_level_select_prompt():
    """
    Display prompt for level selection.
    BONUS #2: Prompt for level selection in Level Select Mode
    """
    print("\n" + "="*50)
    print("LEVEL SELECT MODE".center(50))
    print("="*50)
    print("Choose any level from 0 to 50 to play.")


def print_level_complete_menu():
    """
    Display menu after level completion in Level Select mode.
    BONUS #2: Menu after level completion in Level Select Mode
    """
    print("\n" + "="*50)
    print("What would you like to do?")
    print("  M - Return to main menu")
    print("  N - Go to next level")
    print("="*50)


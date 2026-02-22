"""
Sokoban Puzzle Game - Week 17
A maze navigation game where you move through mazes to reach the target.
"""

from display import *
from helpers import *
from levels import *

# ============================================================================
# TODO: STEP #1: Implement get_direction_step() function
# ============================================================================
def get_direction_step(direction):
    """
    Convert direction character to vertical/horizontal step.
    Week 17 Student Implementation - STEP #1

    Args:
        direction: 'w', 'a', 's', or 'd'

    Returns:
        vertical_step, horizontal_step: Two values representing the direction step
    """
    # TODO: STEP #1: Implement get_direction_step() function
    # - Check if direction is 'w' (up) - return -1, 0
    # - Check if direction is 'a' (left) - return 0, -1
    # - Check if direction is 's' (down) - return 1, 0
    # - Check if direction is 'd' (right) - return 0, 1
    # - For any other direction, return 0, 0
    
    # Temporary: Return default values so game can run (player won't move until implemented)
    return 0, 0


# ============================================================================
# TODO: STEP #2: Implement is_valid_move() function
# ============================================================================
def is_valid_move(board, row, col):
    """
    Check if position is valid and not a wall.
    Week 17 Student Implementation - STEP #2

    Args:
        board: Game board
        row: Target row
        col: Target column

    Returns:
        bool: True if valid move, False otherwise
    """
    # TODO: STEP #2: Implement is_valid_move() function
    # - Check if row is within bounds (row >= 0 and row < len(board))
    # - Check if col is within bounds (col >= 0 and col < len(board[row]))
    # - Check if cell is not a wall (board[row][col] != '#')
    # - Return True if all checks pass, False otherwise
    
    # Temporary: Return False so player cannot move until function is implemented
    return False


# ============================================================================
# TODO: STEP #3: Implement move_player() function
# ============================================================================
def move_player(board, direction):
    """
    Move player in specified direction if valid.
    Week 17 Student Implementation - STEP #3

    Args:
        board: Game board
        direction: 'w', 'a', 's', or 'd'

    Returns:
        bool: True if moved, False if blocked
    """
    # TODO: STEP #3: Implement move_player() function
    # - Get player position using get_player_position(board)
    # - If player position is None, return False
    # - Get direction step using get_direction_step(direction)
    # - Calculate target position (player_row + vertical_step, player_col + horizontal_step)
    # - Check if move is valid using is_valid_move(board, target_row, target_col)
    # - If not valid, return False
    # - Get current cell value (board[player_row][player_col])
    # - Get target cell value (board[target_row][target_col])
    # - Update current cell: '@' -> ' ', '+' -> '.'
    # - Update target cell: ' ' -> '@', '.' -> '+'
    # - Return True if move was successful
    
    # Temporary: Return False so player cannot move until function is implemented
    return False


def play_single_level(level_number):
    """
    Play a single level of the maze game.
    
    Args:
        level_number: Level to play (0-4)
    
    Returns:
        bool: True if level was completed, False if player quit
    """
    # Load current level
    board = get_level(level_number)
    if board is None:
        print("Error loading level!")
        return False
    
    # Initialize level state
    moves = 0
    
    # Level loop - continues until level is won, restarted, or player quits
    while True:
        clear_screen()
        print_level_header(level_number, moves)
        print_board(board)
        print_controls()
        
        # Check win condition
        if is_win(board):
            print_win_message(level_number, moves)
            return True  # Level completed
        
        # Get user input
        print("Move: ↑↓←→ or W/A/S/D | R=restart | Q=quit")
        user_input = getch()
        
        # Handle special commands
        if user_input == 'q':
            # Confirm quit
            print("\nQuit game? (y/n): ", end='', flush=True)
            confirm = getch()
            print(confirm)
            if confirm == 'y':
                print("\nThanks for playing!")
                return False  # Player quit
            else:
                continue
        elif user_input == 'r':
            # Confirm restart
            print("\nRestart level? (y/n): ", end='', flush=True)
            confirm = getch()
            print(confirm)
            if confirm == 'y':
                # Restart level
                board = get_level(level_number)
                moves = 0
                continue
            else:
                continue
        elif user_input in ['w', 'a', 's', 'd']:
            # Attempt to move player
            if move_player(board, user_input):
                moves += 1
        else:
            # Invalid input - ignore and continue
            continue


def play_progression_mode():
    """
    Play progression mode: levels 0-4 in sequence.
    """
    current_level = 0
    progression_levels = 5  # Levels 0-4
    
    # Play through levels 0-4
    while current_level < progression_levels:
        completed = play_single_level(current_level)
        if not completed:
            # Player quit, return to menu
            return
        
        input("Press Enter to continue to next level...")
        current_level += 1
    
    # All progression levels completed
    clear_screen()
    print("="*50)
    print("🎉 CONGRATULATIONS! 🎉".center(50))
    print("="*50)
    print("You've completed all mazes (0-4)!")
    print("="*50)
    input("\nPress Enter to return to main menu...")


def main():
    """
    Main game loop for Week 17 maze navigation game.
    This game loop structure is provided to students with comments.
    """
    # Main menu loop - allows replaying the game
    while True:
        clear_screen()
        print("Welcome to Sokoban Maze Game - Week 17!")
        print("Navigate through the mazes to reach the target at the end.")
        print("\nPress Enter to start, or 'q' to quit: ", end='', flush=True)
        choice = input().strip().lower()
        
        if choice == 'q':
            print("\nThanks for playing!")
            break
        
        # Play through all mazes
        play_progression_mode()


if __name__ == "__main__":
    main()


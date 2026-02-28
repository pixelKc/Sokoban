"""
Sokoban Puzzle Game - Week 18
A warehouse puzzle game where you push boxes onto target locations.
"""

from display import *
from helpers import *
from levels import *

def get_direction_step(direction):
    """
    Convert direction character to vertical/horizontal step.
    This function is from Week 17 and is already implemented.

    Args:
        direction: 'w', 'a', 's', or 'd'

    Returns:
        vertical_step, horizontal_step: Two values representing the direction step
    """
    if direction == 'w':
        return -1, 0  # up
    elif direction == 'a':
        return 0, -1  # left
    elif direction == 's':
        return 1, 0   # down
    elif direction == 'd':
        return 0, 1   # right
    else:
        return 0, 0


def is_valid_move(board, row, column):
    """
    Check if position is valid and not a wall.
    This function is from Week 17 and is already implemented.

    Args:
        board: Game board
        row: Target row
        column: Target column

    Returns:
        bool: True if valid move, False otherwise
    """
    # Check if row is within bounds
    if row < 0 or row >= len(board):
        return False
    
    # Check if column is within bounds
    if column < 0 or column >= len(board[row]):
        return False
    
    # Check if cell is not a wall
    if board[row][column] == '#':
        return False
    
    return True


def move_player(board, direction):
    """
    Move player in specified direction if valid.
    This function is from Week 17 and is already implemented.

    Args:
        board: Game board
        direction: 'w', 'a', 's', or 'd'

    Returns:
        bool: True if moved, False if blocked
    """
    player_pos = get_player_position(board)
    if player_pos is None:
        return False
    
    player_row, player_column = player_pos
    
    # Get direction step
    vertical_step, horizontal_step = get_direction_step(direction)
    
    # Calculate target position
    target_row = player_row + vertical_step
    target_column = player_column + horizontal_step
    
    # Check if move is valid
    if not is_valid_move(board, target_row, target_column):
        return False
    
    # TODO: STEP #1, #2, #3: Box pushing will be implemented in Week 18
    # Check if there's a box (handled by push_box in Week 18)
    # For now, if there's a box, the player cannot move
    if detect_box(board, target_row, target_column):
        return push_box(board, direction)
    
    # Move player (no box in the way)
    current_cell = board[player_row][player_column]
    target_cell = board[target_row][target_column]
    
    # Update current cell
    if current_cell == '@':
        board[player_row][player_column] = ' '
    elif current_cell == '+':
        board[player_row][player_column] = '.'
    
    # Update target cell
    if target_cell == ' ':
        board[target_row][target_column] = '@'
    elif target_cell == '.':
        board[target_row][target_column] = '+'
    
    return True


# ============================================================================
# TODO: STEP #1: Implement detect_box() function
# ============================================================================
def detect_box(board, row, column):
    """
    Check if there's a box at the given position.
    Week 18 Student Implementation - STEP #1

    Args:
        board: Game board
        row: Target row
        column: Target column

    Returns:
        bool: True if box present ('$' or '*')
    """


    if not is_valid_move(board, row, column):
        return False
    return board[row][column] == '$' or board[row][column] == '*'


# ============================================================================
# TODO: STEP #2: Implement can_push_box() function
# ============================================================================
def can_push_box(board, box_row, box_column, direction):
    vertical_step, horizontal_step = get_direction_step(direction)

    box_target_row = box_row + vertical_step
    box_target_column = box_column + horizontal_step

    # Check bounds and walls first
    if not is_valid_move(board, box_target_row, box_target_column):
        return False

    box_target_cell = board[box_target_row][box_target_column]

    if box_target_cell == ' ' or box_target_cell == '.':
        return True
    return False


# ============================================================================
# TODO: STEP #3: Implement push_box() function
# ============================================================================
def push_box(board, direction):
    player_pos = get_player_position(board)
    if player_pos is None:
        return False
    
    player_row, player_column = player_pos
    vertical_step, horizontal_step = get_direction_step(direction)
    
    box_row = player_row + vertical_step
    box_column = player_column + horizontal_step
    
    if not detect_box(board, box_row, box_column):
        return False
    if not can_push_box(board, box_row, box_column, direction):
        return False
    
    box_target_row = box_row + vertical_step
    box_target_col = box_column + horizontal_step

    # Update box target cell
    if board[box_target_row][box_target_col] == ' ':
        board[box_target_row][box_target_col] = '$'
    elif board[box_target_row][box_target_col] == '.':
        board[box_target_row][box_target_col] = '*'

    # Update box's old cell (player moves here)
    if board[box_row][box_column] == '$':
        board[box_row][box_column] = '@'
    elif board[box_row][box_column] == '*':
        board[box_row][box_column] = '+'

    # Update player's old cell
    if board[player_row][player_column] == '@':
        board[player_row][player_column] = ' '
    elif board[player_row][player_column] == '+':
        board[player_row][player_column] = '.'

    return True



def play_single_level(level_number, return_to_menu_callback=None):
    """
    Play a single level of Sokoban.
    This is a helper function used by both progression and level select modes.
    
    Args:
        level_number: Level to play (0-50)
        return_to_menu_callback: Optional function to call if player quits (returns True if should return to menu)
    
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
    # TODO: BONUS #1: Implement undo system
    # BONUS #1: Undo system - Track move history, restore previous states
    undo_history = []  # List to store board states for undo
    max_undo = 10  # Maximum number of undo moves
    
    # Level loop - continues until level is won, restarted, or player quits
    while True:
        clear_screen()
        print_level_header(level_number, moves)
        print_board(board)
        print_controls()
        
        # Show progress
        boxes_on_targets = count_boxes_on_targets(board)
        total_targets = count_total_targets(board)
        if total_targets > 0:
            print(f"Progress: {boxes_on_targets}/{total_targets} boxes on targets")
        
        # Check win condition
        if is_win(board):
            print_win_message(level_number, moves)
            return True  # Level completed
        
        # Get user input
        print("Move: ↑↓←→ or W/A/S/D | R=restart | U=undo | Q=quit")
        user_input = getch()
        
        # Handle special commands
        if user_input == 'q':
            # Confirm quit
            print("\nQuit to menu? (y/n): ", end='', flush=True)
            confirm = getch()
            print(confirm)
            if confirm == 'y':
                if return_to_menu_callback:
                    return_to_menu_callback()
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
                undo_history = []
                continue
            else:
                continue
        elif user_input == 'u':
            # TODO: BONUS #1: Implement undo last move
            # BONUS #1: Undo last move
            # - Check if undo_history has any moves
            # - If yes, restore the previous board state using undo_history.pop()
            # - Decrement moves counter
            # - If no moves to undo, display message
            print("No moves to undo!")
            input("Press Enter to continue...")
            continue
        elif user_input in ['w', 'a', 's', 'd']:
            # TODO: BONUS #1: Save state for undo before making move
            # BONUS #1: Save state for undo before making move
            # - Check if undo_history is at max_undo limit
            # - If at limit, remove oldest state using undo_history.pop(0)
            # - Add current board state to undo_history using copy_board(board)
            
            # Attempt to move player
            if move_player(board, user_input):
                moves += 1
            else:
                # Move failed - undo state saving would be handled here if implemented
                pass
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
    print("🎉 PROGRESSION MODE COMPLETE! 🎉".center(50))
    print("="*50)
    print("You've completed all progression levels (0-4)!")
    print("="*50)
    input("\nPress Enter to return to main menu...")


# ============================================================================
# TODO: BONUS #2: Implement show_main_menu() function
# ============================================================================
def show_main_menu():
    """
    Display main menu and get user's choice.
    BONUS #2: Menu system for game mode selection
    
    Returns:
        str: User's choice ('1', '2', or 'q')
    """
    # TODO: BONUS #2: Implement show_main_menu() function
    # - Display the main menu using print_main_menu()
    # - Loop until valid input is received
    # - Get user input using input()
    # - Validate input (must be '1', '2', or 'q')
    # - Return the validated choice
    pass


# ============================================================================
# TODO: BONUS #2: Implement play_level_select_mode() function
# ============================================================================
def play_level_select_mode():
    """
    Play level select mode: choose any level 0-50.
    BONUS #2: Level Select Mode - Choose and play any level 0-50
    """
    # TODO: BONUS #2: Implement play_level_select_mode() function
    # - Set up a loop for level selection
    # - Display level select prompt using print_level_select_prompt()
    # - Get level number from user using validate_choice() (0-50)
    # - Play the selected level using play_single_level()
    # - After level completion, display menu using print_level_complete_menu()
    # - Get user choice (M for menu, N for next level)
    # - Handle returning to menu or going to next level
    pass


def main():
    """
    Main game loop with menu system.
    This game loop structure is provided to students with comments.
    """
    # TODO: BONUS #2: Implement main menu loop
    # BONUS #2: Main menu loop - Choose between Progression Mode and Level Select Mode
    # For now, just play progression mode directly
    # Once BONUS #2 is implemented, uncomment the menu loop below
    
    # Simplified version - just play progression mode
    play_progression_mode()
    
    # TODO: BONUS #2: Uncomment and implement the menu loop:
    # while True:
    #     choice = show_main_menu()
    #     
    #     if choice == '1':
    #         # Progression Mode
    #         play_progression_mode()
    #     elif choice == '2':
    #         # BONUS #2: Level Select Mode - Choose any level 0-50
    #         play_level_select_mode()
    #     elif choice == 'q':
    #         # Quit game
    #         clear_screen()
    #         print("="*50)
    #         print("Thanks for playing Sokoban!")
    #         print("="*50)
    #         break


if __name__ == "__main__":
    print("Welcome to Sokoban Puzzle Game!\n")
    print(f"Push all boxes onto the target locations {Colors.RED}○{Colors.RESET} to win each level.")
    input("\nPress Enter to start...")
    main()


"""
Level data for Sokoban game.
Loads levels from XSB format files in the levels/ directory.
"""

import os

def load_xsb_level(filename):
    """
    Load a Sokoban level from an XSB format file.
    
    XSB format uses:
    - '#' for walls
    - ' ' (space) for empty floor
    - '@' for player
    - '$' for box
    - '.' for target
    - '*' for box on target
    - '+' for player on target
    
    Args:
        filename: Path to the .xsb file
        
    Returns:
        2D list: Board layout for the level, or None if file not found
    """
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    levels_dir = os.path.join(current_dir, 'levels')
    filepath = os.path.join(levels_dir, filename)
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Strip trailing whitespace from each line (preserve leading spaces)
        # Remove empty lines
        rows = []
        for line in lines:
            stripped = line.rstrip()  # Remove trailing whitespace/newline
            if stripped:  # Only add non-empty lines
                rows.append(stripped)
        
        if not rows:
            return None
        
        # Find maximum width to normalize all rows
        max_width = max(len(row) for row in rows)
        
        # Pad shorter rows with trailing spaces to match max width
        normalized_rows = []
        for row in rows:
            padded_row = row + ' ' * (max_width - len(row))
            normalized_rows.append(padded_row)
        
        # Convert list of strings to 2D list (list of lists)
        # Each string becomes a list of characters
        return [list(row) for row in normalized_rows]
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error loading level file {filename}: {e}")
        return None


def get_level(level_number):
    """
    Get the board layout for a specific level.
    Loads from XSB format files (level000.xsb through level050.xsb).

    Args:
        level_number: Integer 0-50

    Returns:
        2D list: Board layout for the level, or None if invalid
    """
    if level_number < 0 or level_number > 50:
        return None
    
    # Format filename as level000.xsb, level001.xsb, etc.
    filename = f"level{level_number:03d}.xsb"
    return load_xsb_level(filename)


def get_total_levels():
    """
    Get the total number of available levels.

    Returns:
        int: Total number of levels (51)
    """
    return 51


import re
import sys

MARGIN = 1
BOARD_SIZE = 19

def get_sgf_bounds(sgf_content):
    # Extract all stone positions including those in multiple entries per property
    stone_positions = re.findall(r'\[([a-s]{2})\]', sgf_content)

    if not stone_positions:
        return None

    # Convert coordinates to numerical values
    x_coords = [ord(pos[0]) - ord('a') for pos in stone_positions]
    y_coords = [ord(pos[1]) - ord('a') for pos in stone_positions]

    # Find min and max for x and y coordinates with margins
    min_x = max(0, min(x_coords) - MARGIN)
    max_x = min(BOARD_SIZE - 1, max(x_coords) + MARGIN)
    min_y = max(0, min(y_coords) - MARGIN)
    max_y = min(BOARD_SIZE - 1, max(y_coords) + MARGIN)

    # Convert back to SGF coordinates
    min_coord = chr(min_x + ord('a')) + chr(min_y + ord('a'))
    max_coord = chr(max_x + ord('a')) + chr(max_y + ord('a'))

    return f'{min_coord}:{max_coord}'

def add_vw_property(sgf_content):
    # Remove existing VW properties
    sgf_content = re.sub(r'VW\[[a-s]{2}:[a-s]{2}\]', '', sgf_content)

    bounds = get_sgf_bounds(sgf_content)
    if bounds:
        # Insert the VW property after the board size property (SZ)
        sgf_content = re.sub(r'(SZ\[\d+\])', r'\1VW[' + bounds + ']', sgf_content, count=1)
    return sgf_content

if len(sys.argv) < 2:
    print("Usage: python3 sgf_add_vw.py <path/to/sgf/file>")
    sys.exit(1)

# Read the SGF file
sgf_file = sys.argv[1]
with open(sgf_file, 'r', encoding='utf-8') as f:
    sgf_content = f.read()

# Add the VW property
updated_sgf_content = add_vw_property(sgf_content)

# Write to file
with open(sgf_file, 'w', encoding='utf-8') as f:
    f.write(updated_sgf_content)

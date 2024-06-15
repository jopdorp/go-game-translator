import re

def get_sgf_bounds(sgf_content):
    # Extract all stone positions
    stone_positions = re.findall(r'[ABW]\[([a-s]{2})\]', sgf_content)

    if not stone_positions:
        return None

    # Convert coordinates to numerical values
    x_coords = [ord(pos[0]) - ord('a') for pos in stone_positions]
    y_coords = [ord(pos[1]) - ord('a') for pos in stone_positions]

    # Find min and max for x and y coordinates
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Convert back to SGF coordinates
    min_coord = chr(min_x + ord('a')) + chr(min_y + ord('a'))
    max_coord = chr(max_x + ord('a')) + chr(max_y + ord('a'))

    return f'{min_coord}:{max_coord}'

def add_vw_property(sgf_content):
    bounds = get_sgf_bounds(sgf_content)
    if bounds:
        # Insert the VW property after the board size property (SZ)
        sgf_content = re.sub(r'(SZ\[\d+\])', r'\1VW[' + bounds + ']', sgf_content, count=1)
    return sgf_content

# read sgf file from arg
import sys

if len(sys.argv) < 2:
    print("Usage: python3 sgf_add_vw.py <path/to/sgf/file>")
    sys.exit(1)


# Read the SGF file
with open(sys.argv[1], 'r') as f:
    sgf_content = f.read()

# Add the VW property
updated_sgf_content = add_vw_property(sgf_content)

# write to file
with open(sys.argv[1], 'w') as f:
    f.write(updated_sgf_content)

# Print the updated SGF content
print(updated_sgf_content)

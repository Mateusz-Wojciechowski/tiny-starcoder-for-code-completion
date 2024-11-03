# not used!!!!!!
from generate_structured_positions import load_code_lines, find_code_blocks, is_valid_middle
import random


def generate_structured_positions_full_context(file_list, num_positions=1):
    positions = []

    for file_path in file_list:
        code_lines = load_code_lines(file_path)

        blocks = find_code_blocks(code_lines)
        if not blocks:
            continue

        generated_positions = 0
        max_attempts = num_positions * 3

        while generated_positions < num_positions and max_attempts > 0:
            max_attempts -= 1

            block_type, start, end = random.choice(blocks)

            middle_size = random.randint(1, 3)
            middle_start = random.randint(start, max(start, end - middle_size + 1))
            middle_end = min(middle_start + middle_size - 1, end)

            prefix = "".join(code_lines[:middle_start])
            middle_lines = code_lines[middle_start:middle_end + 1]
            suffix = "".join(code_lines[middle_end + 1:])

            while not is_valid_middle(middle_lines) and middle_end < end:
                middle_end += 1
                middle_lines = code_lines[middle_start:middle_end + 1]

            middle = "".join(middle_lines)
            if is_valid_middle(middle_lines):
                positions.append({
                    'prefix': prefix,
                    'middle': middle,
                    'suffix': suffix
                })
                generated_positions += 1

    return positions
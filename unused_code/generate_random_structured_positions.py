import json
import random
import os
from generate_structured_positions import load_code_lines, is_valid_middle


# !!! I did not use this code in the final experiment but it was part of my attempts to extract structured_positions
# !!! Treat as a playground code

def create_completion_structure(file_path, positions):
    code_lines = load_code_lines(file_path)
    structure = []

    for pos in positions:
        prefix_lines = code_lines[max(0, pos["prefix_start_line"]): pos["middle_start_line"]]
        if pos["middle_start_char"] > 0:
            prefix_lines.append(code_lines[pos["middle_start_line"]][:pos["middle_start_char"]])
        prefix = "".join(prefix_lines)

        middle_lines = code_lines[pos["middle_start_line"]: pos["middle_end_line"] + 1]
        if middle_lines:
            middle_lines[0] = middle_lines[0][pos["middle_start_char"]:]
        middle = "".join(middle_lines)

        suffix_lines = code_lines[pos["middle_end_line"] + 1: pos["suffix_end_line"] + 1]
        suffix = "".join(suffix_lines)

        structure.append({
            "prefix": prefix,
            "middle": middle,
            "suffix": suffix
        })

    return structure


def generate_random_positions(file_list, num_positions=5, min_prefix_size_ratio=0.1, max_prefix_size_ratio=0.3,
                              min_suffix_size_ratio=0.1, max_suffix_size_ratio=0.3):
    all_positions = {}

    for file_path in file_list:
        code_lines = load_code_lines(file_path)
        total_lines = len(code_lines)
        random_positions = []

        for _ in range(num_positions):
            valid_position_found = False

            while not valid_position_found:
                use_full_context = random.random() < 0.7

                if use_full_context:
                    prefix_size = None
                    suffix_size = None
                else:
                    min_prefix_size = max(1, int(total_lines * min_prefix_size_ratio))
                    max_prefix_size = max(1, int(total_lines * max_prefix_size_ratio))
                    min_suffix_size = max(1, int(total_lines * min_suffix_size_ratio))
                    max_suffix_size = max(1, int(total_lines * max_suffix_size_ratio))

                    prefix_size = random.randint(min_prefix_size, max_prefix_size)
                    suffix_size = random.randint(min_suffix_size, max_suffix_size)

                middle_start_line = random.randint(prefix_size or 1, total_lines - (suffix_size or 1) - 2)
                middle_end_line = random.randint(middle_start_line,
                                                 min(total_lines - (suffix_size or 1) - 1, middle_start_line + 3))

                if is_valid_middle(code_lines):
                    start_from_middle = random.random() < 0.3
                    middle_line_content = code_lines[middle_start_line].rstrip()

                    if start_from_middle and middle_line_content:
                        middle_start_char = random.randint(0, len(middle_line_content) - 1)
                    else:
                        middle_start_char = 0

                    position = {
                        'prefix_start_line': 0 if use_full_context else max(0, middle_start_line - prefix_size),
                        'middle_start_line': middle_start_line,
                        'middle_start_char': middle_start_char,
                        'middle_end_line': middle_end_line,
                        'suffix_end_line': total_lines - 1 if use_full_context else min(total_lines - 1,
                                                                                        middle_end_line + suffix_size)
                    }

                    random_positions.append(position)
                    valid_position_found = True

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        all_positions[f"positions_{file_name}"] = random_positions

    return all_positions


if __name__ == '__main__':
    file_list = ["files_for_completion/one_liners.py", "files_for_completion/predicates.py",
                 "files_for_completion/LogJournal.py", "files_for_completion/functionalities.py",
                 "files_for_completion/QNet.py", "files_for_completion/AgentExperience.py"]

    with open('random_positions_data_new.json', 'w') as json_file:
        json.dump(generate_random_positions(file_list), json_file, indent=4)

    with open('random_positions_data_new.json', 'r') as data_file:
        positions = json.load(data_file)

    completion_structures = []
    for category in positions:
        completion_structures.extend(create_completion_structure(f'files_for_completion/{category.split("_", 1)[-1]}.py',
                                                       positions[f"{category}"]))

    with open('random_completions_new.json', 'w') as json_file:
        json.dump(completion_structures, json_file, indent=4)

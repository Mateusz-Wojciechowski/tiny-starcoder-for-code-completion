import random
import re
import json


def load_code_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File {file_path} doesn't exist.")
        return []
    except Exception as e:
        print(f"Error while loading file: {e}")
        return []


# uses regex to find blocks of various types in file's codelines
def find_code_blocks(code_lines):
    blocks = []

    for i, line in enumerate(code_lines):
        if re.match(r'^\s*def ', line):
            start = i
            for j in range(i + 1, len(code_lines)):
                if not code_lines[j].startswith(" "):
                    end = j - 1
                    blocks.append(('function', start, end))
                    break
            else:
                blocks.append(('function', start, len(code_lines) - 1))

        elif re.match(r'^\s*class ', line):
            start = i
            for j in range(i + 1, len(code_lines)):
                if not code_lines[j].startswith(" ") and code_lines[j].strip():
                    end = j - 1
                    blocks.append(('class', start, end))
                    break
            else:
                blocks.append(('class', start, len(code_lines) - 1))

        elif re.match(r'^\s*(if|elif|else|for|while)\b', line):
            start = i
            for j in range(i + 1, len(code_lines)):
                if not code_lines[j].startswith(" ") and code_lines[j].strip():
                    end = j - 1
                    blocks.append(('conditional', start, end))
                    break
            else:
                blocks.append(('conditional', start, len(code_lines) - 1))

    return blocks


# validates middle, checks if it contains at least one line that is not empty and is not a comment
def is_valid_middle(middle_lines):
    for line in middle_lines:
        if line.strip() and not line.strip().startswith("#"):
            return True
    return False


def generate_structured_positions(file_list, num_positions=4, min_prefix_size=1, max_prefix_size=3):
    positions = []

    for file_path in file_list:
        code_lines = load_code_lines(file_path)

        # finding blocks of code in the analysed file
        blocks = find_code_blocks(code_lines)

        if not blocks:
            print(f"Warning: No code blocks found in {file_path}. Skipping this file.")
            continue
        generated_positions = 0
        max_attempts = num_positions * 3

        while generated_positions < num_positions and max_attempts > 0:
            max_attempts -= 1

            block_type, start, end = random.choice(blocks)

            # the prefix is the first line of the block or longer
            prefix_size = random.randint(min_prefix_size, max_prefix_size)
            middle_size = random.randint(1, 3)
            middle_start = start + prefix_size
            middle_end = min(middle_start + middle_size - 1, end)

            prefix = "".join(code_lines[start:middle_start])
            middle_lines = code_lines[middle_start:middle_end + 1]
            # suffix is the remaining code in the block
            suffix = "".join(code_lines[middle_end + 1:end + 1])

            # checking whether middle is valid
            while not is_valid_middle(middle_lines) and middle_end < end:
                middle_end += 1
                middle_lines = code_lines[middle_start:middle_end + 1]
                suffix = "".join(code_lines[middle_end + 1:end + 1])

            middle = "".join(middle_lines)
            if is_valid_middle(middle_lines):
                positions.append({
                    'prefix': prefix,
                    'middle': middle,
                    'suffix': suffix
                })
                generated_positions += 1

    return positions


if __name__ == '__main__':
    file_list = ["files_for_completion/one_liners.py", "files_for_completion/predicates.py", "files_for_completion/LogJournal.py", "files_for_completion/functionalities.py", "files_for_completion/QNet.py", "files_for_completion/AgentExperience.py"]
    structured_positions = generate_structured_positions(file_list)


    with open("completion_data/structured_positions.json", "w") as json_file:
        json.dump(structured_positions, json_file, indent=4)


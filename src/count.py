import re
from collections import Counter 

def count_lines(old_data_file_path: str, new_data_file_path: str):

    with open(old_data_file_path, 'r') as file:
            # reads all lines and removes empty spaces and line breaks
            old_data_lines = [line.strip() for line in file.readlines() if line.strip()] 
            # Filers Special characters and keep only alphanumeric character
            old_data_filtered_lines = [re.sub(r'[^a-zA-Z0-9\s\\\/\.]', '', line) for line in old_data_lines]
            # Counts the occurences of every filtered line
            old_data_line_counts = Counter(old_data_filtered_lines)
            
            old_data_output_filename = "older_counted.txt"

            with open(old_data_output_filename, 'w') as output_file:
                for line, count in old_data_line_counts.items():
                    if line:  # Ensure the line is not empty
                        output_file.write(f"{line}: {count}\n")

    with open(new_data_file_path, 'r') as file:
        # reads all lines and removes empty spaces and line breaks
        new_data_lines = [line.strip() for line in file.readlines() if line.strip()] 
        # Filers Special characters and keep only alphanumeric character
        new_data_filtered_lines = [re.sub(r'[^a-zA-Z0-9\s\\\/\.]', '', line) for line in new_data_lines]
        # Counts the occurences of every filtered line
        new_data_line_counts = Counter(new_data_filtered_lines)
            
        new_data_output_filename = "newer_counted.txt"

        with open(new_data_output_filename, 'w') as output_file:
            for line, count in new_data_line_counts.items():
                if line:  # Ensure the line is not empty
                    output_file.write(f"{line}: {count}\n")

    file_names: list[str] = []    
    file_names.append(old_data_output_filename)
    file_names.append(new_data_output_filename)
    
    return file_names

import pandas as pd
import plotly.express as px
# needs to be downloaded

import sys
import os 
import shutil
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


def compare_data(file_names: list[str]):
    # Creates absolute paths for each file, for better functionality
    script_dir: str = os.path.dirname(os.path.abspath(__file__))

    older_data_counted_file_path: str = os.path.join(script_dir, file_names[0])
    newer_data_counted_file_path: str = os.path.join(script_dir, file_names[1])
    
    shutil.copyfile(newer_data_counted_file_path, "treemap_data.txt")

    treemap_data_file_path: str = os.path.join(script_dir, "treemap.txt")
    
    # Creates the lists so only the paths are compared
    with open(older_data_counted_file_path, 'r') as file:
        older_data_paths_as_list: list[str] = []
        for line in file: 
            path, _ = line.strip().split(": ")
            older_data_paths_as_list.append(path)

    with open(newer_data_counted_file_path, 'r') as file2:
        newer_data_paths_as_list: list[str] = []
        for line in file2.readlines():
            path, _ = line.strip().split(": ")
            newer_data_paths_as_list.append(path)
    
    # Actual Comparison
    with open(treemap_data_file_path, 'a+') as file3: 
        for line in older_data_paths_as_list:
            if line not in newer_data_paths_as_list:
                file3.write(f"\n{line}: 0")
    
    return treemap_data_file_path


def displaying_treemap(treemap_data_file_path: str):
    
    data: list = []
    # Data from the git log command after the set date (i.e 2024/01/01)
    # After running count_lines and compare_data (treemap_data.txt)
    with open(treemap_data_file_path, 'r') as file:
        for line in file:
            if line.strip():
                path, changes = line.strip().split(': ')
                changes = int(changes)  
                changes += 1 # Counting this as the initial commit 
                data.append({'File Path': path, 'Changes': changes})
            else:
                continue
    df = pd.DataFrame(data)

    df['Path Components'] = df['File Path'].apply(lambda x: x.split('/'))
    max_depth_of_dir: int = df['Path Components'].apply(len).max()
    for i in range(0,max_depth_of_dir):
        df[f'Level {i + 1}'] = df['Path Components'].apply(lambda x: x[i] if i < len(x) else None)
    #i == 0 --> Level 1; i == max_depth_of_dir == 4 --> Level 5 
    print(df)
    
    path = [px.Constant("all")] + [f'Level {i}' for i in range(1, max_depth_of_dir + 1)]
    fig = px.treemap(df, 
                    path=path, 
                    values='Changes', 
                    title='Treemap der Dateipfade basierend auf Änderungen')
    fig.update_traces(root_color="lightgrey")

    fig.show()

# Running the actual script
if __name__ == "__main__": 
    if len(sys.argv) != 3:
        print('Please provide 2 filenames as command line arguments.\n'
            'The file xontaining the older data must be named first\n'
            'Example: py createHotspots.py "old.txt" "new.txt"')
        sys.exit(1)

    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    older_data_file_path: str = os.path.join(script_dir, sys.argv[1])
    newer_data_file_path: str = os.path.join(script_dir, sys.argv[2])
    print("Argv:", sys.argv)

    file_names: list[str] = count_lines(older_data_file_path, newer_data_file_path)

    treemap_data_file_path: str = compare_data(file_names)

    displaying_treemap(treemap_data_file_path) 
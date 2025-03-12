import pandas as pd
import plotly.express as px
# needs to be downloaded

import sys
import os 
import shutil
import re
from collections import Counter 

def count_lines(older_data_file_path: str, newer_data_file_path: str):
    
    script_dir: str = os.path.dirname(os.path.abspath(__file__))

    with open(older_data_file_path, 'r') as file:
            # reads all lines and removes empty spaces and line breaks
            older_data_lines = [line.strip() for line in file.readlines() if line.strip()] 
            # Filers Special characters and keep only alphanumeric character
            older_data_filtered_lines = [re.sub(r'[^a-zA-Z0-9\s\\\/\.]', '', line) for line in older_data_lines]
            # Counts the occurences of every filtered line
            older_data_line_counts = Counter(older_data_filtered_lines)
            
            older_data_output_filename = os.path.join(script_dir, "older_counted.txt")

            with open(older_data_output_filename, 'w') as output_file:
                for line, count in older_data_line_counts.items():
                    if line:  # Ensure the line is not empty
                        output_file.write(f"{line}: {count}\n")

    with open(newer_data_file_path, 'r') as file:
        # reads all lines and removes empty spaces and line breaks
        newer_data_lines = [line.strip() for line in file.readlines() if line.strip()] 
        # Filers Special characters and keep only alphanumeric character
        newer_data_filtered_lines = [re.sub(r'[^a-zA-Z0-9\s\\\/\.]', '', line) for line in newer_data_lines]
        # Counts the occurences of every filtered line
        newer_data_line_counts = Counter(newer_data_filtered_lines)
            
        newer_data_output_filename = os.path.join(script_dir,"newer_counted.txt")

        with open(newer_data_output_filename, 'w') as output_file:
            for line, count in newer_data_line_counts.items():
                if line:  # Ensure the line is not empty
                    output_file.write(f"{line}: {count}\n")

    file_names: list[str] = []    
    file_names.append(older_data_output_filename)
    file_names.append(newer_data_output_filename)
    
    return file_names


def compare_data(file_names: list[str]):
    # Creates absolute paths for each file, for better functionality
    script_dir: str = os.path.dirname(os.path.abspath(__file__))

    older_data_counted_file_path: str = os.path.join(script_dir, file_names[0])
    newer_data_counted_file_path: str = os.path.join(script_dir, file_names[1])
    
    treemap_data_file_path: str = shutil.copyfile(newer_data_counted_file_path, "treemap_data.txt")

    # treemap_data_file_path: str = os.path.join(script_dir, "treemap.txt")
    
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

    df['Colors'] = df['Changes'].apply(lambda x: '#ADDDE6' if x == 1 else '#F3A880')
    
    print(df)
    
    path = [px.Constant("all")] + [f'Level {i}' for i in range(1, max_depth_of_dir + 1)]
    fig = px.treemap(df, 
                    path=path, 
                    values='Changes', 
                    title='Treemap der Dateipfade basierend auf Änderungen',
                    color='Colors',
                    color_discrete_sequence=['#ADDDE6', '#F3A880'])
    fig.update_traces(root_color="lightgrey")

    fig.show()

# Running the actual script
if __name__ == "__main__": 
    if len(sys.argv) != 1:
        print('Please provide one absolute filepath to the repository as command line argument.\n'
            'Example: py createHotspots.py "C:/path/to/repo"')
        sys.exit(1)
    
    print("Path to repo:\n", sys.argv)

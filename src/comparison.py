# John 3:16 
import os
import shutil

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




    
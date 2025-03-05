# John 3:16 
older_data_file_path: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Data\data_older_2024.txt"

newer_data_file_path: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Data\data_newer_2024.txt"

#Creating a copy of the newer data set is recommended
#Then use the path here
copy_of_newer_data_path: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Data\copy_data_newer_2024.txt"

with open(older_data_file_path, 'r') as file:
    older_data_paths_as_list: list[str] = []
    for line in file: 
        path, changes = line.strip().split(": ")
        older_data_paths_as_list.append(path)

with open(newer_data_file_path, 'r') as file2:
    newer_data_paths_as_list: list[str] = []
    for line in file2.readlines():
        path, changes = line.strip().split(": ")
        newer_data_paths_as_list.append(path)

#The "newer_data_file_path" can also be used, but keep in mind that the newer data set then will be modified.
#Data will not be truncated see:  'a+'
#This modified file then has to be used in treemap.py
with open(copy_of_newer_data_path, 'a+') as file3: 
    for line in older_data_paths_as_list:
        if line not in newer_data_paths_as_list:
            file3.write(f"\n{line}: 0")




    
# John 3:16 

#Data from the git log command before the set date (i.e 2024/01/01) 
#after running count.py
older_data_file_path: str = r""

#Data from the git log command after the set date (i.e 2024/01/01)
#after running count.py
newer_data_file_path: str = r""

#Creating a copy of the newer data set is recommended
#Then use the path here
copy_of_newer_data_path: str = r""


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




    
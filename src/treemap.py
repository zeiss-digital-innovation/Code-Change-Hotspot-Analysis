import pandas as pd
import plotly.express as px
# needs to be downloaded

import sys
import os 
import shutil
import re
from collections import Counter 





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



if len(sys.argv) != 3:
    print('Please provide 2 filenames as command line arguments.\n'
          'The file xontaining the older data must be named first\n'
          'Example: py createHotspots.py "old.txt" "new.txt"')
    sys.exit(1)

script_dir: str = os.path.dirname(os.path.abspath(__file__))
older_data_file_path: str = os.path.join(script_dir, sys.argv[1])
newer_data_file_path: str = os.path.join(script_dir, sys.argv[2])
print("Argv:", sys.argv)
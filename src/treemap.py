import pandas as pd
import plotly.express as px
# need to be downloaded

import sys
import os 


if len(sys.argv) != 3:
    print('Please provide 2 filenames as command line arguments.\n'
    'Example: py createHotspots.py "old.txt" "new.txt"')
    sys.exit(1)

script_dir: str = os.path.dirname(os.path.abspath(__file__))
first_file_path: str = os.path.join(script_dir, sys.argv[1])
second_file_path: str = os.path.join(script_dir, sys.argv[2])
print("Argv:", sys.argv)


data: list = []


##Data from the git log command after the set date (i.e 2024/01/01)
#After running count.py and comparison.py
with open(first_file_path, 'r') as file:
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
max_depth: int = df['Path Components'].apply(len).max()
for i in range(0,max_depth):
    df[f'Level {i + 1}'] = df['Path Components'].apply(lambda x: x[i] if i < len(x) else None)

print(df)
path = [px.Constant("all")] + [f'Level {i}' for i in range(1, max_depth + 1)]

fig = px.treemap(df, 
                 path=path, 
                 values='Changes', 
                 title='Treemap der Dateipfade basierend auf Änderungen')
fig.update_traces(root_color="lightgrey")


fig.show()
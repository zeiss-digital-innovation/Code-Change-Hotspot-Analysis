import pandas as pd
import plotly.express as px


data = []
##Data from the git log command after the set date (i.e 2024/01/01)
#After running count.py and comparison.py
file_path:str = r""
with open(file_path, 'r') as file:
    for line in file:
        if line.strip():
            path, changes = line.strip().split(': ')
            changes = int(changes)  
            changes += 1 # Counting this as the initial commit 
            data.append({'File Path': path, 'Changes': changes})
        else:
            continue


df = pd.DataFrame(data)
print(df)

fig = px.treemap(df, 
                 path=['File Path'], 
                 values='Changes', 
                 title='Treemap der Dateipfade basierend auf Änderungen')


fig.show()
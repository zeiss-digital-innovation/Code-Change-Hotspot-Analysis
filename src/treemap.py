import pandas as pd
import plotly.express as px


data = []
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
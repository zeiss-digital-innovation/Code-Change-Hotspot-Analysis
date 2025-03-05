import pandas as pd
import plotly.express as px


data = []
file_path:str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Data\copy_data_newer_2024.txt"
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
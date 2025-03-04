import pandas as pd
import plotly.express as px

# Schritt 1: Lese die Daten aus der Textdatei
data = []
file_path:str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Data\test_data_for_treemap.txt"
with open(file_path, 'r') as file:
    for line in file:
        path, changes = line.strip().split(': ')
        changes = int(changes)  
        changes += 1 # Counting this as the initial commit 
        data.append({'File Path': path, 'Changes': changes})

# Schritt 2: Erstelle ein DataFrame
df = pd.DataFrame(data)
print(df)
# Schritt 3: Erstelle die Treemap
fig = px.treemap(df, 
                 path=['File Path'], 
                 values='Changes', 
                 title='Treemap der Dateipfade basierend auf Änderungen')

# Schritt 4: Zeige die Treemap an
fig.show()
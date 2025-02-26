import pandas as pd
import plotly.express as px

# Schritt 1: Lese die Daten aus der Textdatei
data = []
file_path:str = "c:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Code-Change-Hotspot-Analysis\test_daten.txt"
with open(file_path, 'r') as file:
    for line in file:
        path, changes = line.strip().split(': ')
        data.append({'File Path': path, 'Changes': int(changes)})

# Schritt 2: Erstelle ein DataFrame
df = pd.DataFrame(data)

# Schritt 3: Erstelle die Treemap
fig = px.treemap(df, 
                 path=['File Path'], 
                 values='Changes', 
                 title='Treemap der Dateipfade basierend auf Änderungen')

# Schritt 4: Zeige die Treemap an
fig.show()
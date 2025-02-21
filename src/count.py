import re
from collections import Counter

# Pfad zur Textdatei
file_path = 'git-log.txt'  # Ändere dies auf den Pfad deiner Datei

def count_lines(file_path: str):
    with open(file_path, 'r') as file:
        # Lese alle Zeilen und entferne Leerzeichen und Zeilenumbrüche
        lines = [line.strip() for line in file.readlines() if line.strip()]  # Filtert Leerzeilen
        
    # Filtere Sonderzeichen und behalte nur alphanumerische Zeichen und Leerzeichen
    filtered_lines = [re.sub(r'[^a-zA-Z0-9\s\\\/\.]', '', line) for line in lines]

    # Zähle die Vorkommen jeder gefilterten Zeile
    line_counts = Counter(filtered_lines)
    
    # Ausgabe der Ergebnisse
    for line, count in line_counts.items():
        if line:  # Stelle sicher, dass die Zeile nicht leer ist
            print(f"{line}: {count}")

if __name__ == "__main__":
    count_lines(file_path)

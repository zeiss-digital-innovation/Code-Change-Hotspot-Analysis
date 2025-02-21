import matplotlib.pyplot as plt
import squarify
from collections import defaultdict

# Funktion zum Einlesen der Daten und Erstellen einer hierarchischen Struktur
def read_data(file_path):
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Überprüfen, ob die Zeile nicht leer ist
                try:
                    path, weight = line.split(': ')
                    parts = path.split('/')
                    weight = int(weight)
                    # Hierarchische Struktur aufbauen
                    hierarchy[parts[1]][parts[2]][parts[3]] += weight
                except ValueError:
                    print(f"Ungültige Zeile übersprungen: {line}")
    
    return hierarchy

# Funktion zum Erstellen der Treemap
def create_treemap(hierarchy):
    labels = []
    sizes = []
    
    # Durch die hierarchische Struktur iterieren
    for layer, tests in hierarchy.items():
        for category, items in tests.items():
            for test, weight in items.items():
                labels.append(f"{layer}/{category}/{test}")
                sizes.append(weight)

    # Treemap erstellen
    plt.figure(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, alpha=.8)
    plt.axis('off')  # Achsen ausblenden
    plt.title('Treemap der Tests nach Gewichtung', fontsize=16)
    plt.show()

# Hauptfunktion
def main():
    file_path = 'counted.txt'  # Pfad zur Datei mit den Daten
    hierarchy = read_data(file_path)
    create_treemap(hierarchy)

if __name__ == "__main__":
    main()
